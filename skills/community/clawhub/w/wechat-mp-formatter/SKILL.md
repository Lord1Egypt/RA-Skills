---
name: wechat-mp-formatter
description: "公众号(WeChat Official Account)排版工具：将文章转换成可一键复制、直接粘贴进公众号编辑器并保留全部样式的 HTML。内置音乐卡片、歌词引用块、高亮块、金句块、互动引导等组件，默认暖色调配色，特别适合歌曲/音乐/怀旧/生活方式类内容；其他类型也可用，但配色与组件通常需微调。WeChat MP Formatter: turns articles into self-contained HTML that keeps all styling when pasted into the MP editor. Ships music cards, lyric quote blocks, highlight boxes, key-sentence blocks and interactive prompts with a warm-tone palette tuned for songs/music/nostalgia/lifestyle; other topics work too but may need palette/component tweaks."
agent_created: true
---

# WeChat MP Formatter（公众号排版器）

## Overview

Convert article content (title + body text + optional lyrics/quotes/highlights) into a self-contained HTML file with inline styles. The user opens the HTML in a browser, clicks a "copy" button, and pastes directly into the WeChat公众号 editor — all formatting (background colors, borders, font sizes) is preserved.

## When to Use

- User asks to format an article for WeChat公众号 / 公众号排版
- User wants to create styled content that can be copy-pasted into the公众号 editor
- User mentions "公众号文章" + "排版" / "格式" / "样式"
- User has article text and needs it turned into publishable公众号 format

## 适用场景 / Best For

- **强烈推荐（本 skill 的主打场景）**：歌曲分享、音乐人/专辑介绍、歌词赏析、怀旧 / 情感 / 生活方式类公众号文章。默认暖色调配色 + 音乐卡片 / 歌词引用块组件就是为这类内容调的。
- **可用但需调整**：通用文章、随笔、商业或科技类 —— 可保留高亮块、金句块、互动引导，但通常要换配色（见 Color Palette 的 Alternate palettes）并去掉"音乐卡片"这种强音乐语义的组件。
- **暂不适用**：依赖复杂多栏布局、数据图表，或强品牌 VI 统一规范的内容（公众号编辑器会过滤 flex / gradient / box-shadow，详见下方兼容性规则）。

> 说明：本 skill 当前实现以歌曲 / 音乐类排版为第一优先级。其他类型若要长期量产，建议后续补一套中性 / 冷色调配色与通用组件库（例如 1.1 版本规划）。

## Critical CSS Compatibility Rules（核心兼容性规则）

The WeChat公众号 editor **filters out certain CSS properties** when pasting. Follow these rules strictly:

### MUST DO
- Use `<section>` for ALL styled containers — NOT `<div>`. The editor strips `background-color` from `<div>` but preserves it on `<section>`.
- Use `<table>` for music cards or any multi-column layouts.
- Use `background-color` (not `background:` shorthand) for all background colors.
- Put ALL styles as inline `style="..."` attributes on each element.
- Use `border-radius`, `border`, `padding`, `margin`, `color`, `font-size`, `line-height`, `text-align` — all safe.

### MUST NOT DO
- Do NOT use `display:flex` — the editor removes it, layouts collapse.
- Do NOT use `linear-gradient` — the editor removes it, backgrounds turn transparent.
- Do NOT use `box-shadow` — the editor removes it.
- Do NOT use `<div>` for styled blocks (background-color will be stripped).
- Do NOT use external CSS classes for article content — only inline styles.
- Do NOT use `position`, `transform`, `animation` — filtered by the editor.

For the full compatibility reference, see `references/compatibility.md`.

## Formatting Components（排版组件库）

### 1. Music Card（音乐卡片）
Table-based layout with a circular disc icon + song info. Use `<table>` structure.

```html
<table style="width:100%;background-color:#faf6f0;border:1px solid #e8ddd0;border-radius:8px;margin-bottom:28px;border-collapse:collapse;">
  <tr>
    <td style="padding:12px 16px;width:52px;vertical-align:middle;">
      <section style="width:44px;height:44px;border-radius:50%;background-color:#8b4513;"></section>
    </td>
    <td style="padding:12px 16px;vertical-align:middle;">
      <p style="margin:0;font-size:15px;color:#8b4513;font-weight:600;">🎵 歌曲名</p>
      <p style="margin:4px 0 0;font-size:13px;color:#b08968;">歌手名 · 年份</p>
    </td>
  </tr>
</table>
```

### 2. Lyric Quote Block（歌词引用块）
Warm-toned background + left border + italic text. Use `<section>`.

```html
<section style="background-color:#faf6f0;border-left:3px solid #d4a574;padding:16px 20px;margin:20px 0;font-size:16px;line-height:1.9;color:#6b5544;font-style:italic;border-radius:0 6px 6px 0;">歌词内容</section>
```

### 3. Highlight Box（重点高亮块）
Bordered box for key insights. Use `<section>`.

```html
<section style="background-color:#faf6f0;border:1px solid #e8ddd0;border-radius:10px;padding:20px 22px;margin:28px 0 20px;">
  <p style="font-size:15px;line-height:1.9;color:#3f3f3f;margin:0;">内容</p>
</section>
```

### 4. Key Sentence Block（金句块）
Centered or left-aligned emphasis with distinct background. Use `<section>`.

```html
<section style="background-color:#f5f0e8;padding:14px 20px;margin:18px 0;border-radius:6px;font-size:16px;line-height:2.0;color:#4a3f35;">金句内容</section>
```

### 5. Interactive Prompt（互动引导框）
Dark background box at the end guiding comments/shares. Use `<section>`.

```html
<section style="background-color:#2c2520;border-radius:8px;padding:16px 20px;margin-top:16px;color:#d4a574;font-size:13px;line-height:1.8;">
  互动引导文字
</section>
```

### 6. Section Heading（小标题）
Left border accent + bold. Use `<h2>` with inline style.

```html
<h2 style="font-size:18px;font-weight:700;color:#2c2c2c;margin:36px 0 20px;padding-left:14px;border-left:4px solid #8b4513;line-height:1.5;">标题文字</h2>
```

### 7. Body Paragraph（正文段落）
Standard paragraph style. Use `<p>` with inline style.

```html
<p style="font-size:16px;line-height:2.0;color:#3f3f3f;margin:0 0 18px;text-align:justify;letter-spacing:0.3px;">正文内容</p>
```

### 8. Inline Emphasis（行内强调）
Colored bold text within paragraphs. Use `<span>`.

```html
<span style="color:#8b4513;font-weight:600;">强调文字</span>
```

## Color Palette（配色方案）

Default warm-tone palette (suitable for nostalgia/music/lifestyle content):

| Role | Color | Usage |
|------|-------|-------|
| Primary | `#8b4513` | Headings, accents, inline emphasis |
| Secondary | `#d4a574` | Left borders, decorative elements |
| Quote BG | `#faf6f0` | Lyric blocks, highlight boxes, music cards |
| Highlight BG | `#f5f0e8` | Key sentence blocks |
| Dark BG | `#2c2520` | Interactive prompts, series navigation |
| Dark text | `#d4a574` | Text on dark backgrounds |
| Body text | `#3f3f3f` | Paragraphs |
| Muted text | `#6b5544` | Lyric text |
| Border | `#e8ddd0` | Card borders |

Alternate palettes: change `#8b4513` (primary) and `#d4a574` (secondary) to match the article tone. Keep the BG colors neutral.

## Workflow

### Step 1: Receive Article Content
Get the article title, body text, and any special elements (lyrics, quotes, key sentences, music info) from the user.

### Step 2: Choose Components
Select which formatting components to use based on content type:
- Music/literature articles: Music Card + Lyric Quote + Highlight + Interactive Prompt
- General articles: Highlight + Key Sentence + Interactive Prompt
- Series articles: add Series Navigation at the bottom

### Step 3: Build HTML
Use `assets/template.html` as the base template. Fill in:
1. Article title in the `<h1>` and `<title>` tags
2. Article body using the component styles above
3. If multiple articles: duplicate the content section, add nav tabs

### Step 4: Copy Function
The template includes a `copyArticle(id, btn)` function using `document.execCommand('copy')`. This works in `file://` context (no HTTPS needed). Do NOT use `ClipboardItem` API — it requires a secure context.

### Step 5: Output
Save the HTML file to the user's working directory. Tell the user to:
1. Open the HTML file in a browser
2. Click the "复制全文" button
3. Paste (Ctrl+V) into the WeChat公众号 editor

## Template Usage

The base template is at `assets/template.html`. It contains:
- Complete `<style>` block for page chrome (nav bar, buttons) — these use CSS classes (safe, not copied)
- Copy function (`execCommand`-based, works on `file://`)
- Example article structure with all components
- Multiple article support with tab navigation

To use: read the template, replace the example content with the actual article, save as a new HTML file.

## Typography Rules

- Body font-size: **16px** (17px for elderly audiences)
- Body line-height: **2.0** (generous spacing for readability)
- Heading font-size: **18px**
- Lyric font-size: **16px**, line-height **1.9**
- Interactive prompt font-size: **13px**
- Use `letter-spacing:0.3px` on body paragraphs for slight breathing room
- Keep paragraphs short: **3-5 lines max** per paragraph for mobile reading

## Common Mistakes to Avoid

1. Using `<div>` instead of `<section>` → background colors will be stripped after pasting
2. Using `background:` instead of `background-color:` → less reliable
3. Using flexbox for layouts → will collapse after pasting
4. Using `ClipboardItem` in the copy function → fails on `file://` protocol
5. Making paragraphs too long → mobile readers (especially elderly) won't finish
6. Forgetting `border-collapse:collapse` on tables → gaps in music cards
