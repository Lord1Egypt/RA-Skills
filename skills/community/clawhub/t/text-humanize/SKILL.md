---
name: text-humanize
description: >
  Edit English and Chinese text for clarity and style: improve concision, structure, tone,
  rhythm, rhetoric, and typography while preserving meaning, facts, quotations, citations,
  and necessary authorship or AI-use disclosures. Adapt to comments, articles, and literary
  prose. Offers diagnosis or diagnosis with a comparison rewrite. Use for 润色、优化表达、
  删冗余、调整语气、体裁适配、修辞分析、排版, or requests described as humanize / 去AI味
  when the goal is ordinary editing. Does not infer human/AI origin or aim to evade review,
  detection, or required disclosure.
---

- **Version**: 1.7.0
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/better-office-work-flow/tree/main/skills/text-humanize

# Text Humanize — 中英文清晰表达与风格润色

Improve readability and fit the author's purpose. 保留原意、事实、证据强度、立场和作者声音，修改真正妨碍阅读的地方。自然表达可以正式、完整、准确，也可以简短、口语化。

## 编辑边界

- 正常的 AI 草稿可以润色；保留原有及必要的作者、AI 辅助使用披露、引用和链接，不因追求文风删除或淡化。
- 不判断文本由人还是 AI 撰写，不输出来源概率、AI 分数、Looks human、High risk of flagging 或过审保证。
- 用户要求绕过检测、规避审核、隐瞒必要披露或伪装真人时，简短说明不能以此为目标，转为提供清晰度、冗余、结构和语气方面的正常编辑帮助。
- 不故意制造错字、语法错误、假犹豫、自我打断或所谓「人类指纹」。不强迫作者站队，也不把有依据的平衡观点改成偏激判断。
- 不添加作者没有提供的身份、资历、亲历、记忆、场景、对话或来源。创作性扩写须符合用户明确的虚构写作意图；新增示例明确标为虚构，不混进非虚构正文。
- 数字、人名、精确日期、因果关系、引语及出处保持准确。存疑处在编辑说明中标「待核实」；不得擅自把日期改模糊、把数字改成「据说」，或编造「记不清在哪篇报道里」等出处。发现可能的事实冲突，指出并请作者核实，证据不足不静默纠正。
- 标题、列表、平衡论证、正确语法、规范标点和破折号都是允许的表达。是否调整取决于阅读效果和用户要求。

## 先确定语言、体裁和目标

1. 用户指定语言和风格时以其要求为准。未指定时保留原语言，混合内容按段编辑，保留术语和英文片段。
2. 自动语言口径：在可分析的自然语言中计 CJK（U+4E00–U+9FFF、U+3400–U+4DBF、U+F900–U+FAFF）与 Latin（A–Z/a–z）；CJK / (CJK + Latin) **>50%** 才进入中文模式，等于 50% 归英文模式；无字母时不作语言推断。脚本排除代码、URL、Markdown 引用区域及可识别的成对行内引语，结果只是路由提示。
3. 判断体裁：短文本以信息集中为目标；长文保持论述层次、标题和必要证据；文学以意象、叙事和声音为目标。字数和发布平台不决定固定段数或句式。拿不准时保留现有结构，做最小必要编辑。
4. 社交评论可更简洁，技术文档可用步骤和列表，署名文章可完整论证，诗歌可保留换行。未指定平台时依据文本用途，不默认某个平台的审查偏好。涉及当前平台规则时另行核实，不把文风建议当平台要求。

## 两种工作模式

### A · 诊断（check / audit / 检查 / 看看）

1. 加载 [中文风格参考](references/style-patterns-cn.md) 或 [English style patterns](references/style-patterns-en.md)。抒情或文学文本另读 [修辞参考](references/rhetoric-cn.md) 与 [同位语例句](references/lyrical-appositive.md)。
2. 指出具体片段、影响（冗余、歧义、跳跃、语气失配等）和可选改法。没有明显问题就直说，不凑问题数。
3. 如使用脚本，先记录基线。统计只支持人工判断，不代表质量结论，更不能推断作者来源。
4. 只诊断时不擅自改正文；报告以阅读问题和修改优先级为主，不给来源评分。

### B · 诊断 + 对照改写（rewrite / humanize / 优化 / 润色 / 改一下）

1. 按模式 A 诊断，确定需要保留的事实、引语、披露和语气。
2. 按体裁修改：删重复、澄清指代、整理顺序、调整句子负担和段落。短文无须强压成两段；长文无须去标题；文学无须补亲历。作者偏好口语化节奏的署名长文（如公众号正文），可建议拆除「01/02/03」「首先其次最后」式编号小标题骨架，改为概括性标题或自然过渡——这是文风选择，按作者目标执行，不是纠错。用户选定「格式统一」润色时，执行 [SS-CN7 体例统一清单](references/style-patterns-cn.md)：主流人物译名、中文间隔号「·」、全角引号及配对核对、冗余空格清理、书名号并列不加顿号，并在改动说明中逐条报告。
3. 给出对照或改稿 + 简短改动说明。长文可交付文件，将正文与编辑说明分开，不能让说明混入待发布正文。事实疑点单列，不虚构解决方案。
4. 核对披露、引用、链接、数字和日期是否保留，检查改稿有无新增事实或立场变化。
5. 若基线使用脚本，对改稿用同参数复测并报告实际结果；没有执行工具时明确未运行，不宣称通过。只对用户显式选定的格式约束修复失败项；风格统计不阻塞交付。
6. 复测数字直接写进回复（如「复测：半角引号 0 / 破折号 0」）供作者核对。改写涉及引号替换时，残留量常与原文同量级，肉眼不可辨，须按脚本计数逐处核对，不凭印象。用户选定的格式约束未归零时，优先修到位再交付；这只是排版验收习惯，不改变第 5 步的边界。

## 依赖

普通编辑无需额外依赖；运行统计脚本需要 Python 3，仅使用标准库，无需安装第三方包。

## 统计与格式检查

[scripts/preflight-check.py](scripts/preflight-check.py) 仅用 Python 标准库，读取文件、不改文件。保留 CLI、JSON、体裁路由及改前改后统计。它不做模型来源判定、事实核查或平台审核预测。

```bash
python3 scripts/preflight-check.py original.md --tier long --json
python3 scripts/preflight-check.py revised.md --tier long --json
python3 scripts/preflight-check.py revised.md --cut '## 本轮改动'
# 仅在用户明确要求这些格式约束时选定检查项
python3 scripts/preflight-check.py revised.md --lang zh --strict --check quotes --check spacing
```

- 默认只有 INFO / WARN；引号、编号和破折号是可选排版建议，短文本同样允许使用。
- `--check` 可选 `quotes`（未保护区域的中文引号体例）、`punctuation`（中文逗号/句点/省略号体例）、`spacing`（中文标点周边空格）、`dashes`（中文破折号形态）、`numbered-headings`（禁编号行的显式要求，粗计含标题与列表）。`--strict` 仅把所选格式约束的超限项升为 FAIL；未选任何项时不会因文风产生非零退出码。
- 中文专属检查只在中文模式生效，英文不强制中文标点；`--lang zh|en` 可显式覆盖。代码、URL、引用及可识别的英文片段不参与中文标点约束。不能可靠识别的嵌套引用和混合句式须人工核对。
- 引号数量只能说明使用情况；`baseline_note()` 提醒对照原文件，不能断定发生了转录污染，不能据此自动替换。
- 段落按空行解析，软换行不会变成新段或新句；标题、列表、引用和表格不计正文段落。诗歌的有意分行由作者判断，不以该统计约束。
- R 类结构和词库、SS-CN8 节奏词频、句长与段尾比例全部只报统计，没有质量阈值，不影响 `--strict` 退出码。SS-CN8 保留代码名用于历史兼容，现指「节奏观察」。具体计数口径见参考及 README。
- 退出码 `0` 表示无选定格式失败，`1` 表示有选定格式失败，`2` 表示参数或文件读取错误；`0` 不代表文稿质量或审核通过。

## 边界情况

- 极短文本：上下文不足时只提有依据的编辑意见，不推测来源。
- 英文或混合稿：保留引号内的英文、缩写的 apostrophes、URL 和代码语法，不机械替换全部标点。
- 引用和转述：默认不改引语；需编辑转述时保留出处并区分转述与原话。排版体例调整也应确认不会改变引文含义。
- 无真实细节的抒情：可以删掉空泛修饰，或在说明中请求作者补真实材料；不把新编的纸箱、凉水等细节写成作者经历。
- 用户使用「去AI味」等旧称：按本版本的普通润色目标处理；若同时明确要求规避检测，应用上面的编辑边界。

历史版本仅供变更追溯，旧版目标和写作规则已废弃，不作为当前指令。验收方法见 [tests/README.md](tests/README.md)。
