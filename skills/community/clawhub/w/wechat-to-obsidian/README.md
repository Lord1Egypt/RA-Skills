# wechat-to-obsidian｜微信公众号剪藏到 Obsidian

> **中文为主 / English below each section**
>
> 把微信公众号文章一键剪藏到 Obsidian：保留正文、图片顺序、标题层级，图片自动下载到 `attachments/`，并使用 Obsidian 原生嵌入语法。
>
> Clip WeChat public-account articles into Obsidian: preserve text, image order, Markdown heading hierarchy, download images into `attachments/`, and use native Obsidian embeds.

---

## 这是什么？｜What is this?

`wechat-to-obsidian` 是一个 OpenClaw / Agent Skill，用于把微信公众号文章稳定转换成 Obsidian Markdown 笔记。

`wechat-to-obsidian` is an OpenClaw / Agent Skill that converts WeChat public-account articles into Obsidian-friendly Markdown notes.

它解决三个常见坑：

It solves three common pain points:

1. 微信文章不能直接 `curl` 抓取，容易被反爬拦截。  
   WeChat pages are hard to fetch with plain `curl` because of anti-bot behavior.
2. 图片是懒加载，而且下载时需要正确 `Referer`。  
   Images are lazy-loaded and often require the correct `Referer` header.
3. 原文视觉标题经常不是 `<h2>`，而是带样式的 `<p>` / `<section>`，普通 `innerText` 会丢失 Markdown 层级。  
   Visual headings are often styled `<p>` / `<section>` nodes instead of real `<h2>` tags, so naive `innerText` extraction loses Markdown structure.

---

## 功能特点｜Features

| 功能 | 中文说明 | English |
|---|---|---|
| 🌐 真实浏览器提取 | 使用 `agent-browser` 打开页面，绕过普通抓取限制 | Uses `agent-browser` to load the real page |
| 🖼 图片完整保存 | 滚动触发懒加载，下载正文图片到 `attachments/` | Scrolls to trigger lazy loading and downloads article images |
| 📐 图文顺序保留 | 单次 DOM 顺序遍历，文字和图片不会错位 | Preserves text/image order with one DOM-order pass |
| 🧱 标题层级保留 | 识别 `h1-h6` 与微信常见视觉标题，输出 `##` / `###` | Preserves heading hierarchy from native and styled headings |
| ✋ 写入前确认 | 先建议保存目录，等待用户确认后才写入 | Suggests a path first and waits for confirmation |
| 📝 Obsidian 友好 | 使用 `![[filename]]` 图片嵌入语法 | Uses Obsidian-native image embed syntax |

---

## 安装｜Installation

### 通过 ClawHub 安装（推荐）｜Install via ClawHub (recommended)

在 OpenClaw / Agent 对话里输入：

In your OpenClaw / Agent chat, run:

```text
/install wechat-to-obsidian
```

或访问：

Or visit:

<https://clawhub.ai/dw1161/wechat-to-obsidian>

### 手动安装｜Manual install

```bash
git clone https://github.com/dw1161/wechat-to-obsidian ~/.openclaw/workspace/skills/wechat-to-obsidian
```

---

## 依赖｜Requirements

- [OpenClaw](https://openclaw.ai)
- `agent-browser` ≥ 0.17
- `curl`（macOS/Linux 通常自带）

```bash
npm install -g agent-browser
agent-browser install
```

---

## 使用方式｜Usage

把微信公众号链接发给你的 Agent，并说明要保存到哪里：

Send a WeChat article URL to your Agent and tell it where to save the note:

```text
https://mp.weixin.qq.com/s/xxxxx 帮我存到 Obsidian 的这个路径下：10 Projects/AI/ClaudeCode
```

Agent 会：

The Agent will:

1. 用 `agent-browser` 打开文章。  
   Open the article with `agent-browser`.
2. 滚动页面，触发懒加载图片。  
   Scroll through the page to trigger lazy-loaded images.
3. 按 DOM 顺序提取正文、标题、图片。  
   Extract text, headings, and images in DOM order.
4. 识别标题层级，输出 Markdown `##` / `###`。  
   Detect heading hierarchy and emit Markdown `##` / `###`.
5. 下载图片到笔记同级 `attachments/`。  
   Download images into a sibling `attachments/` folder.
6. 写入 Markdown 笔记，并汇报保存路径和图片数量。  
   Write the Markdown note and report the path and image count.

---

## Markdown 标题保留｜Markdown heading preservation

微信编辑器常把标题做成“加粗 + 20px 字号 + 背景色”的普通段落，而不是标准 HTML heading。

WeChat often represents headings as styled paragraphs instead of semantic HTML headings.

本 Skill 会做保守识别：

This skill uses conservative detection rules:

- 原生 `h1-h6` → `#` 到 `######`
- `一. / 一、 / 二.` 这类章节标题 → `##`
- `1. Mac / 2. Windows` 这类数字小标题 → `###`
- 短文本 + 加粗 + 较大字号 → `###`

Examples:

```markdown
## 一. Claude Code 安装

### 1. Mac

### 2. Windows
```

---

## 工作流程｜Workflow

```text
发送链接 / Send URL
  → 浏览器打开 / Open in browser
  → 滚动触发懒加载 / Scroll for lazy loading
  → DOM 顺序提取 / Extract in DOM order
  → 标题层级识别 / Detect headings
  → 确认保存路径 / Confirm save path
  → 下载图片 / Download images
  → 写入 Markdown / Write Markdown
  → 汇报结果 / Report result
```

---

## 常见问题｜FAQ

| 问题 | 中文说明 | English |
|---|---|---|
| 图片下载 403 | Skill 会携带 `Referer: https://mp.weixin.qq.com/` | The skill sends the proper WeChat `Referer` |
| 图片显示为空 | 需要先滚动全页触发懒加载 | Scroll first to trigger lazy loading |
| 图片顺序错乱 | 使用 DOM 单次遍历避免错位 | One DOM-order pass prevents reordering |
| 标题变普通文字 | 已支持视觉标题识别并输出 Markdown heading | Styled headings are converted into Markdown headings |
| zsh `bad substitution` | 下载脚本避免使用 zsh 不支持的关联数组 | Avoid zsh-incompatible associative arrays |

---

## 安全与隐私｜Security & privacy

- 不内置任何账号、Cookie、Token 或私人路径。  
  No bundled accounts, cookies, tokens, or private paths.
- 图片下载仅使用文章中的公开资源 URL。  
  Image downloads use public resource URLs from the article.
- 写入位置由用户确认。  
  The save location is confirmed by the user.

---

## License

MIT

---

> 基于 [OpenClaw](https://openclaw.ai) Agent Skill 框架构建。  
> Built with the [OpenClaw](https://openclaw.ai) Agent Skill framework.
