---
name: xhs-post-factory
description: 小红书多输入内容生成技能。用于将 pdf/md/txt/json 等文件转为结构化的小红书博文。默认生成论文解读（paper-interpretation）类型，输出 xhs-post.md 与 xhs-post.json 到输入文件所在目录，并保留可扩展模板机制以支持后续更多博文类型。
---

# XHS Post Factory

将指定文件内容转成可直接发布的小红书文案（v1 默认: 论文解读）。

## v1 Scope

- 只做文案生成，不做图片渲染与平台发布。
- 默认模板: `paper-interpretation`。
- 默认语言: 中文为主，夹少量英文术语。

## Input Contract

支持输入类型:

- `pdf`
- `md`
- `txt`
- `json`

输入处理规则:

1. `pdf`
   - 优先使用同目录下已经生成的paper-card产物：`paper-card.md` + `paper-card.json`
   - 优先复用同目录下 `paper-parse` 产物: `*_content.md` + `*_parsed.json`。
   - 如果没有可复用产物，先提取可读文本，再继续生成。
2. `md` / `txt`
   - 直接作为正文语料。
3. `json`
   - 优先读取结构化字段: 标题/摘要/方法/实验/结论。
   - 字段缺失时，回退到全文字段（如 `content` / `text`）。

当输入信息不足时，明确写出“原文未明确给出”，禁止臆测补全。

## Output Contract

始终保存到输入源所在目录（多输入时保存到主输入文件目录）:

- `xhs-post.md`
- `xhs-post.json`

`xhs-post.json` 顶层字段至少包含:

- `post_type` (`paper-interpretation`)
- `title_candidates` (3-5)
- `final_title`
- `body_sections`
- `emoji_density_level` (`low`/`medium`/`high`)
- `hashtags` (5-10)
- `evidence_notes`

## Template Routing

模板目录: `templates/`

路由规则:

1. 用户明确指定 `post_type` 时，优先使用指定模板。
2. 用户未指定时，按意图关键词匹配模板。
3. v1 默认路由到 `paper-interpretation`。
4. 模板文件不存在时，报错并提示可用模板列表。

新增模板规范:

1. 新增 `templates/<post-type>.md`。
2. 在本文件的“Template Routing”中登记触发关键词与输出要求。
3. 复用 `references/style-guide.md` 的通用风格规则。

## Paper-Interpretation Template (v1)

按固定骨架生成，段落顺序不可变:

1. 研究问题（这篇论文试图解决什么）
2. 核心思路（作者怎么做）
3. 方法亮点（2-4 条）
4. 实验结果（关键指标与结论）
5. 局限性（至少 1 条）
6. 一句话总结
7. 互动问题（引导评论）
8. 标签（5-10 个）

可调参数:

- `length`: `short` / `medium` / `long`
- `emoji_density`: `low` / `medium` / `high`

默认参数:

- `length=medium`
- `emoji_density=medium`

## Reliability Rules

1. 不虚构事实、数字、基线、数据集。
2. 任何数值或结论都必须来自输入文件；否则删除或标注“原文未明确给出”。
3. 明确区分“作者结论”和“解读者判断”。
4. 对证据弱的结论，用保守措辞（如“可能”“倾向于”）。
5. 每个核心段落在 `evidence_notes` 里提供来源依据（原段落、字段或缺失说明）。

输出前自检:

- 结构完整（7 个固定段落 + 标签）
- 语气符合小红书但不过度夸张
- Emoji 密度符合参数
- 标签数量 5-10 且与主题相关
- `xhs-post.md` 与 `xhs-post.json` 内容一致

## Writing Style (from existing redbook experience)

- 标题不冗长，强调读者收益与问题意识。
- 正文短段落、清晰换行、信息块可快速扫描。
- Emoji 优先放在小标题（章节标题）中；正文中也可视情况添加emoji增强活人感
- 结尾使用可检索标签，但避免堆砌无关热词。
- 保持“可读性优先 + 信息可信”。

## Failure Handling

遇到以下情况必须显式报错或降级说明:

- 文件不存在或格式无法读取
- 关键内容缺失导致无法形成论文解读骨架
- 模板不存在或模板未注册

若可降级生成，正文必须包含“信息不足”提示，并在 `evidence_notes` 说明缺口。
