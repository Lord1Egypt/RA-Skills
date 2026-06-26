---
name: wechat-article-preset-preview
version: 1.0.0
description: 公众号文章预设主题排版--Markdown 一键渲染主题并生成复制页预览链接（不含 AI 结构化预览）
trigger: "预设主题排版|公众号主题排版|主题排版|preset排版|主题预览|wechat-copy.js"
tools: [filesystem, http, shell]
author: wework
---


# 公众号文章预设主题排版

当用户需要对文章做**预设主题排版**并生成**可复制到公众号的预览链接**时：输入是用户的 Markdown 文件，本技能只产出 **预设主题渲染版** 的预览链接（不做 AI 结构化预览）。

## When to Use

- 用户明确要「**预设主题/主题排版/preset**」并希望直接得到**复制页预览链接**。
- 用户提供一篇 Markdown（如 `article.md`），希望用主题/版式快速美化并复制到公众号后台。
- 若用户希望「AI 自由排版/结构化改写 HTML/自定义卡片样式」等，请使用**AI 生成预览**对应技能；本技能不处理该链路。

## 输入与输出

- **输入**：用户的 **Markdown 文件**（如 `article.md` 或用户指定的 .md 路径）。
- **输出**（两种等价形态，至少满足其一）：
  - **链接形态**：一条**文章预览链接**（`https://edit.shiker.tech/copy.html?id=xxx`），即预设主题渲染版。
  - **完整产物形态**：在返回上述预览链接的同时，一并给出本技能约定的**全部技能产物**（预设主题 HTML、含预览地址的 txt），可为：
    - 直接给出这两个文件的**内容**；
    - 或明确给出这两个文件在本地/远端的**路径**（脚本已按约定写入，详见下文「技能产物（必交）」）。

## 技能产物（必交，防止 AI 执行时偷懒）

执行本技能时**必须**在用户 Markdown 同目录（或约定工作目录）产出以下文件，缺一不可：


| 产物             | 说明                                         | 约定路径/文件名                 |
| -------------- | ------------------------------------------ | ------------------------ |
| **预设主题 HTML**  | 使用主题/版式（或 preset）将 Markdown 渲染为公众号可复制 HTML | `article.preset.html`    |
| **含预览地址的 txt** | 包含预设主题版的预览链接，以脚本输出为准，便于用户直接打开              | `wechat-preview-url.txt` |


- 不得仅口头返回链接而不写入 txt；不得跳过预设主题 HTML 的落盘，否则视为未完成技能。
- 预览链接以**脚本标准输出**或上述 txt 文件内容为准，勿以 AI 转述为准（长 id 易抄错）。

## 1. 整体流程（Md → 预设主题预览链接）

1. **读取用户的 Markdown 文件**（用户提供的 .md 路径）。
2. **生成预设主题 HTML**：使用预设（`--preset`）或主题/版式（`--theme` + `--layout`）对 Markdown 做主题渲染，得到 `article.preset.html`。
3. **请求复制页**：将渲染后的 HTML POST 到 `edit.shiker.tech/api/copy`，得到一条预览链接。
4. **将链接交给用户**：以脚本标准输出或同目录写入的 `wechat-preview-url.txt` 为准（勿让 AI 自行"转述"链接，否则长 id 易漏数字导致链接错误）；用户浏览器打开 → 点击「复制到剪贴板」→ 粘贴到公众号后台。
5. **必交产物**：同目录须存在 **预设主题 HTML**（`article.preset.html`）与 **含预览地址的 txt**（`wechat-preview-url.txt`），详见上文「技能产物（必交）」表。

## 2. 脚本入口

- `**wechat-copy.js`（推荐）**：输入一个 `.md`，生成预设主题 HTML + 单条预览链接，并在 md 同目录写入 `article.preset.html` 与 `wechat-preview-url.txt`。
- `wechat-html.js`：仅从 Markdown 生成预设主题 HTML（不请求预览链接）。

## 3. 文章类型与推荐预设（便于选主题）

本技能仅做**预设主题渲染（PRESET）**，不区分“格式一/格式二”。你只需要按文章气质选择 `--preset`（或 `--theme` + `--layout`）即可。

| 文章类型/气质 | 推荐选择 | 说明 |
|---|---|---|
| 资讯密集（早报/周报/速读） | 优先用 `--preset <预设名>` | 更强调层级与可扫读性。 |
| 深度长文（复盘/观点/教程） | 优先用 `--preset <预设名>` | 更强调段落节奏与引用块。 |
| 通知/公告（偏正式） | 用 `--theme <themeId> --layout <layoutId>` 微调 | 方便固定到一套“公司风格”组合。 |
| 追求稳定一致（团队长期复用） | 固定一个 `--preset` 或固定 `--theme/--layout` | 所有人使用同一组合，输出风格一致。 |

查看可用预设/主题/版式：
- `node wechat-html.js --list-presets`
- `node wechat-html.js --list-themes`
- `node wechat-html.js --list-layouts`


## 4. API 说明（edit.shiker.tech）

- **接口**：`POST https://edit.shiker.tech/api/copy`
- **请求体**：`Content-Type: application/json`，`{ "html": "完整 HTML 字符串" }`
- **响应**：`{ success: true, data: { id, url } }`；`url` 即为预览页地址。

## 5. 注意点

- 图片：内容中的图片需为可公网访问的 URL，否则公众号内无法显示。
- 公众号粘贴时，仅**引用（blockquote）和表格**会保留背景色与边框；脚本已按此规则将需强调的块转为 blockquote。
- **预览链接勿以 AI 转述为准**：长 id 容易被 AI 抄错或漏数字，导致链接失效。请以**脚本标准输出**或**同目录下生成的 `wechat-preview-url.txt`** 中的链接为准；若 AI 提供了链接，请与上述文件内容核对。

---

## 简要流程小结

1. 执行 `**node wechat-copy.js <input.md>**`（可选加 `--preset` 或 `--theme/--layout`）。
2. 得到一条预览链接（标准输出），并在同目录写入 `article.preset.html` 与 `wechat-preview-url.txt`。
3. 打开链接复制后粘贴到公众号。

