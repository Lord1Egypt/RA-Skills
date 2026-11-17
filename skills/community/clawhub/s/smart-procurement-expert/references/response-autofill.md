# 响应文件内容自动填充（深度节点 B 编排层）

## 一、为什么需要这一层

深度节点 B 的 `generate_bid_template.js` 只负责「按格式渲染」。真正的内容由用户/LLM 起草后注入。本参考定义一条**可复现、可审计**的内容填充流水线，把「招标解析 → 评分建模 → 章节初稿」串起来，避免每次手工拼装 config。

## 二、流水线（4 步）

```
① parse_bidding_docx.py   招标文件.docx  → parsed_config.json    （结构/格式/编号，已落地）
② 撰写 content.json        （每章起草正文 body + 图表占位 chart）  ← 本环节产出
③ autofill_prepare.py      parsed + content → bid_config.json     （注入 body/chart）
④ generate_bid_template.js bid_config.json → 投标文件.docx        （渲染章节初稿）
```

- ① 与 ④ 是工程脚本（scripts/）；
- ② 是**人/LLM 起草**环节，须基于对招标文件的实质理解与评分建模结果；
- ③ 是桥接脚本 `scripts/autofill_prepare.py`，把内容素材按章节标题关键词映射到结构骨架。

## 三、content.json 编写规范

匹配以「章节标题包含 match 关键词」为规则，关键词须与招标文件实际章节标题一致（建议取章节标题里的核心词，如「公司概况」「施工方案」「售后服务」）。

| 字段 | 类型 | 说明 |
|---|---|---|
| `project` | object | 可选；覆盖项目名称/编号/【正本】标记 |
| `chapters[].match` | string | 匹配锚点（章节标题子串，不区分大小写） |
| `chapters[].body` | string \| string[] \| {text,bold,size,font}[] | 章节初稿正文；多段用数组，留空行用 `""` |
| `chapters[].chart` | string \| {title,hint} | 图表占位说明，渲染为灰色提示块 |

> 每个 `match` 仅命中首个匹配章节；未命中章节在生成时保留占位，终端会打印「未填充清单」供查漏。

## 四、与评分建模的衔接

- 节点 2 评分建模识别的「客观分佐证点 / 主观分亮点」应直接转化为 ② 中对应章节的 `body` 要点；
- 价格分（深度节点 C）算出的报价策略结论，可写入「投标函 / 报价一览表」章节 `body`；
- ② 起草的正文须经节点 6 润色去模板化、节点 9 一致性审查后方可定稿。

## 五、安全边界

- `body` 内容由用户/LLM 提供，**引擎不生成、不臆造实质性承诺**；
- 涉及商务报价、实质性偏离、资质承诺的 `body` 为**需人工确认**项，定稿前须用户签字；
- 自动填充不改变招标文件原编号/格式（深度节点 B 的格式透传不受影响）。
