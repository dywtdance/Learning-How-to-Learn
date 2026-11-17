# CBT 技能与 MCP 核查

核查日期：2026-11-07。用户希望长期对话有稳定、可复用的方法，而非临时查书。此次只使用通用搜索词，没有将个人记录或书籍上传到候选服务。

## 结论与当前状态

找到了现成候选，但目前不建议原样安装。较可借鉴的是 Cognitive Toolkit 的逐步思维记录流程；它的默认保存、健康数据使用和隐藏分类方式需要调整。没有发现足以据此宣称这些 AI 工具经过临床有效性验证的证据；这与 CBT 方法本身的研究证据是两回事。

本次状态：完成候选筛选及关键源码／说明文件核查；未安装、未连接第三方心理服务，未改全局 MCP 配置，未用个人对话测试外部服务。没有新技能在后台监测对话。

更符合当前项目的落地方案是：项目内的中文 CBT 自助支持技能，结合可核查的书籍笔记和必要摘要。技能负责固定流程，资料负责概念与证据，个人记录负责延续背景；仍须逐次核对，不保证自动理解正确。此方案尚未创建或安装。

## 候选对比

| 候选 | 已核查到的实际内容 | 与当前需求的差距 | 建议 |
|---|---|---|---|
| [Claude Cognitive Toolkit](https://github.com/glebis/claude-cognitive-toolkit) | 技能入口、逐步思维记录参考文件；含情境、自动想法、情绪、证据与替代观点等环节 | 默认保存完整会话；健康数据在可用时可能被读取；参考文件要求内部分类、不向用户宣布分类。我们需要透明解释、仅存必要摘要 | 可作结构参考，原样不安装；没有完成所有依赖文件和运行兼容性检查 |
| [Open Medica CBT Tools](https://github.com/Open-Medica/open-medical-skills/tree/main/skills/cognitive-behavioral-therapy-tools) | 读取技能入口、说明与 Python 源码，提供记录结构、活动计划和词汇解释 | `identify_distortions` 使用英文关键词匹配，例如出现 `always` 就可能分类；不具备中文语境理解，不等于心理评估。没有运行代码 | 可参考表格结构，不用其自动分类判断用户 |
| [therapy-mode](https://github.com/sundial-org/awesome-openclaw-skills/blob/main/skills/therapy-mode/SKILL.md) | 涵盖 CBT、ACT、DBT、MI、对话记录和会话总结 | 文档含临床印象、预后和依恋模式推断要求；混合范围过宽，且逐轮记录方式不符合本项目精简摘要约定 | 不原样安装，不将其作为心理学家替身 |
| [sundai-club/cbt-mcp](https://github.com/sundai-club/cbt-mcp) | README 明确面向 AI agent 自身的卡顿、思考与任务表现 | 同名 CBT，但主要服务对象不是寻求心理支持的人 | 排除，目标不符 |
| [CBT Cards](https://cbt-cards-move.vedokrok.com/agents/) | 发布者提供只读练习资料、来源和审核状态；明确定位为一般自我反思 | 当前英文为主；发布者所称审核不等于独立临床验证。只读资料不能承担长期对话理解 | 可作为补充练习来源；未完成安装包审计，不安装 |

## 关键证据

- Toolkit [技能入口](https://raw.githubusercontent.com/glebis/claude-cognitive-toolkit/main/SKILL.md)：保存位置、完整对话记录及可选健康数据规则。
- Toolkit [思维记录文件](https://github.com/glebis/claude-cognitive-toolkit/blob/main/references/thought-record.md)：逐步流程以及内部认知偏差分类要求。
- Open Medica [实现代码](https://raw.githubusercontent.com/Open-Medica/open-medical-skills/main/skills/cognitive-behavioral-therapy-tools/script.py)：`identify_distortions` 的英文关键词匹配；这是一项源码审查发现，没有把演示当作实测。
- therapy-mode [原始技能文件](https://raw.githubusercontent.com/sundial-org/awesome-openclaw-skills/main/skills/therapy-mode/SKILL.md)：会话总结与临床式推断要求。
- [OpenAI 官方技能说明](https://developers.openai.com/plugins/concepts/skills)：技能用于提供可复用流程，MCP 提供信息或动作能力。安装技能本身不等于获得临床资质，也不代表模型完成了专门训练。


## 若后续落地，应满足的具体要求

1. 中文交互，一次聚焦一个问题；解释用户想理解的机制，不机械重复提问或强行填写表格。
2. 对自动想法、情绪、行为、身体反应及现实处境分别核对；没有明确想法时保留未知，不逼迫用户编造。
3. 模式解释标注依据、信心与其他可能性，向用户展示并允许纠正；不做隐藏的人格分类。
4. 建议前先说明所检验的假设；实践由用户接受后才记为约定，反馈不以情绪立刻下降或任务完成率作为唯一成功标准。
5. 只在本项目保存必要摘要；不自动保存逐字稿、读取健康账户、接入消息平台或外传记录。
6. 图示使用 Excalidraw，保留可编辑版本；书内术语必须能追溯到原文。
7. 用虚构案例检查误判、中文语境、用户不同意解释、单纯疲劳、真实环境障碍等情况；通过流程检查也不能宣称临床有效。


## 搜索范围与限制

本次搜索了当前插件目录、公开技能和 GitHub 项目。插件目录没有返回相关心理支持插件，结果不是完整目录；仍可在 [插件目录](https://chatgpt.com/plugins) 查看更多候选。技能安装器的官方目录查询遇到本机证书验证错误，GitHub CLI 未登录；随后用公共网页与只读公开 API 查阅候选，没有关闭证书验证或更改登录。

此报告不是安全认证。未完成供应链审计、实际安装验证、对话效果评估或临床验证。不能把项目自称“evidence-based”解释为其 AI 实现已获验证。
