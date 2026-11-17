"""Build local, traceable text indexes; extraction is not a claim of reading."""
from pathlib import Path
import hashlib
import json
import posixpath
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '阅读' / '文本索引'


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
        if tag in ('p', 'div', 'br', 'li', 'h1', 'h2', 'h3'):
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)
        if tag in ('p', 'div', 'li', 'h1', 'h2', 'h3'):
            self.parts.append('\n')

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def html_text(raw):
    parser = TextParser()
    parser.feed(raw.decode('utf-8-sig', errors='replace'))
    return re.sub(r'\n\s*\n+', '\n', ''.join(parser.parts)).strip()


def extract(path):
    sections, toc = [], []
    if path.suffix.lower() == '.pdf':
        reader = PdfReader(path)
        for number, page in enumerate(reader.pages, 1):
            sections.append((f'PDF 文件页 {number}', page.extract_text() or ''))
    else:
        with zipfile.ZipFile(path) as archive:
            container = ET.fromstring(archive.read('META-INF/container.xml'))
            opf = next(e.attrib['full-path'] for e in container.iter() if e.tag.endswith('rootfile'))
            package = ET.fromstring(archive.read(opf))
            folder = posixpath.dirname(opf)
            manifest = {e.attrib['id']: e.attrib for e in package.iter() if e.tag.endswith('}item')}
            def member(href):
                from urllib.parse import unquote
                return posixpath.normpath(posixpath.join(folder, unquote(href.split('#')[0])))
            for item in manifest.values():
                if item.get('media-type') == 'application/x-dtbncx+xml':
                    ncx = ET.fromstring(archive.read(member(item['href'])))
                    toc = [e.text for e in ncx.iter() if e.tag.endswith('}text') and e.text]
            spine = [e.attrib['idref'] for e in package.iter() if e.tag.endswith('}itemref')]
            for number, item_id in enumerate(spine, 1):
                href = member(manifest[item_id]['href'])
                sections.append((f'EPUB spine {number} | {href}', html_text(archive.read(href))))
    body = '\n\n'.join(f'## {label}\n{text}' for label, text in sections)
    target = OUT / (path.stem + '.txt')
    target.write_text(body, encoding='utf-8')
    return {'source': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'index': target.name, 'sections': len(sections),
            'empty_sections': [label for label, text in sections if len(text.strip()) < 30],
            'characters': sum(len(text) for _, text in sections), 'toc': toc}


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    OUT.mkdir(parents=True, exist_ok=True)
    result = []
    for source in sorted((ROOT / '资料').iterdir()):
        if source.suffix.lower() not in ('.epub', '.pdf'):
            continue
        row = extract(source)
        result.append(row)
        print(json.dumps({k: v for k, v in row.items() if k not in ('toc', 'sha256')}, ensure_ascii=False), flush=True)
    (OUT / 'manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
