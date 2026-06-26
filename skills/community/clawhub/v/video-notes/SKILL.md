---
name: video-notes
slug: video-notes
version: 1.1.0
author: 2992638402-art
description: 把 YouTube / 哔哩哔哩视频变成一份精美的结构化笔记。自动提取字幕、识别关键时刻并截图、生成核心论点总结和 SVG 图表，输出带侧边导航和全文搜索的单文件 HTML 文档。适用于技术演讲、公开课、播客、产品发布会等场景。This skill should be used when a user provides a YouTube or Bilibili URL and asks to take notes, summarize a video, or create a study document from video content.
---

# Video Notes Skill

Convert any YouTube / Bilibili video into a polished, self-contained HTML notes document with:
- **Executive summary** (~300 words) capturing the core arguments
- AI-generated structured notes with SVG diagrams
- **Keyframe gallery** — screenshots auto-captured at key moments, each linking back to the video
- Fixed sidebar navigation with scroll-spy
- Searchable raw subtitle panel (click any line → jump to that timestamp)

## Workflow

### Step 1: Extract Subtitles

```bash
python3 ~/.claude/skills/video-notes/scripts/extract_subtitles.py <url> --output /tmp/subs.json
```

**语言参数：**
- YouTube 英文视频（默认）：不加 `--lang`
- YouTube / B站 中文视频：`--lang zh` 或 `--lang zh-Hans`

**YouTube 认证问题（常见！）：**

若直接运行报错 `Sign in to confirm you're not a bot` 或 `No subtitles found`，需要传入浏览器 cookies：

```bash
# 使用 Chrome cookies（推荐）
python3 ~/.claude/skills/video-notes/scripts/extract_subtitles.py <url> \
  --output /tmp/subs.json \
  --cookies-from-browser chrome

# 或使用已导出的 cookies 文件
python3 ~/.claude/skills/video-notes/scripts/extract_subtitles.py <url> \
  --output /tmp/subs.json \
  --cookies /tmp/yt-cookies.txt
```

**脚本内置降级策略（自动执行，无需手动干预）：**

1. **快速路径**：`--skip-download` 直接获取字幕（速度最快）
2. **降级路径**：若快速路径失败，自动导出 cookies 后用 `-f sb3`（storyboard 格式，YouTube 始终可用）触发字幕下载，解析 VTT 格式
3. **格式兼容**：优先 VTT（支持内联时间标签），失败则回退 SRT

**哔哩哔哩支持：**

B站视频直接传 URL，yt-dlp 原生支持：

```bash
# B站视频（中文字幕）
python3 ~/.claude/skills/video-notes/scripts/extract_subtitles.py \
  "https://www.bilibili.com/video/BVxxxxxxxx" \
  --lang zh --output /tmp/subs.json

# 需要登录的 B站视频（会员内容等）
python3 ~/.claude/skills/video-notes/scripts/extract_subtitles.py \
  "https://www.bilibili.com/video/BVxxxxxxxx" \
  --lang zh --cookies-from-browser chrome --output /tmp/subs.json
```

> **注意**：B站部分视频有人工上传字幕（非 AI 生成），脚本已同时尝试 `--write-subs` 和 `--write-auto-subs`，两种都能获取。没有任何字幕的视频（纯口播无字幕）会返回错误，此时需告知用户。

Output: `[{"t": "mm:ss", "s": 123.4, "text": "..."}]`

### Step 2: Capture Keyframes (requires ffmpeg)

Run the keyframe script. It scores subtitles using heuristics, selects the most important moments (spaced ≥60s apart), downloads only those short video sections, and extracts frames:

```bash
python3 ~/.claude/skills/video-notes/scripts/capture_keyframes.py \
  <youtube_url> /tmp/subs.json \
  --max-frames 8 \
  --output-json /tmp/keyframes.json
```

Output: `[{"t": "mm:ss", "s": 123.4, "text": "...", "score": 0.5, "image_b64": "..."}]`

- If ffmpeg is not installed, skip this step and set `{{KEYFRAMES_JSON}}` to `[]` in the template — the gallery section will auto-hide.
- Default `--max-frames` is 8; reduce for faster generation or increase for longer videos.

### Step 3: Read and Understand the Content

Read the subtitle text to understand:
- The video's main topic and overall structure
- Key concepts, arguments, frameworks, and terminology
- Any notable quotes or memorable lines
- Natural section boundaries (topic shifts)

### Step 4: Generate HTML Notes

Use `assets/note-template.html` as the foundation. Fill in each placeholder:

| Placeholder | Content |
|---|---|
| `{{TITLE}}` | Page `<title>` tag |
| `{{SIDEBAR_NAV}}` | `.sb-logo` block + `.nav-a` links for each section |
| `{{SUMMARY}}` | Executive summary HTML (see below) |
| `{{MAIN_CONTENT}}` | Hero block + all note sections |
| `{{SUBTITLE_SEC_NUM}}` | Section number for the subtitle panel (e.g. `6`) |
| `{{VIDEO_URL}}` | Full YouTube URL |
| `{{VIDEO_ID}}` | YouTube video ID (e.g. `dQw4w9WgXcQ`) |
| `{{SUBTITLE_JSON}}` | Full JSON array from Step 1 |
| `{{KEYFRAMES_JSON}}` | Full JSON array from Step 2 (or `[]` if skipped) |
| `{{SECTION_IDS}}` | JS array: `['hero','summary','s1','s2','keyframes','subtitles']` |

#### Executive Summary (`{{SUMMARY}}`)

Write ~300 words of HTML paragraphs inside `<p>` tags. Structure:
1. **One-sentence core thesis** — what is the speaker's central claim?
2. **Main argument 1** — first major thread (2–3 sentences)
3. **Main argument 2** — second major thread
4. **Main argument 3** — third major thread (if applicable)
5. **Closing** — key prediction, implication, or call to action

Use `<strong style="color:var(--text)">` for emphasis. Keep line-height loose (`line-height:2`).

#### Hero Section

Always include a hero section (`id="hero"`) with:
- `.hero-badge`: speaker name + event/source
- `<h1>`: video title (concise, impactful)
- `.hero-sub`: speaker · role · note type
- `.chips`: 3–5 topic tags
- `.hero-quote`: the single most memorable quote

#### Note Sections

For each major topic area, create `<div class="sec" id="sN">` with:
- `.sec-hd` header (numbered `.sec-n` + `.sec-title`)
- Content using: `.card`, `.g2`/`.g3` grids, `.diag` SVG diagrams, `.tl` timelines, `.ql` quotes

#### SVG Diagrams (`.diag` blocks)

Generate SVGs for comparisons, progressions, and architectures:

```
Background: rgba(R,G,B,.4) fill + rgba(R,G,B,.3) stroke
Labels: fill="#fff" font-weight="700"; sublabels: fill="#aaa" font-size="9-10"
Arrows: › in <text>, colored to match the row
Connectors: stroke="rgba(255,255,255,.12)" stroke-dasharray="3,3"
```

Color palette:
- Blue flow: `#5b8dee` → `#9b7cf4` | Green flow: `#3ecf8e` → `#5b8dee`
- Old/danger: `rgba(244,63,94,.4)` | Mid: `rgba(240,169,70,.4)` | New: `rgba(62,207,142,.4)`

#### Sidebar Navigation

```html
<div class="sb-logo">
  <div class="sb-logo-icon">🎬</div>
  <h2>{{Short Title}}</h2>
  <p>{{Speaker}} · {{Source}}</p>
</div>
<a class="nav-a active" href="#hero"><span class="nav-icon">🏠</span>概览</a>
<a class="nav-a" href="#summary"><span class="nav-icon">✦</span>核心总结</a>
<!-- one .nav-a per note section -->
<div class="nav-sep"></div>
<a class="nav-a" href="#keyframes"><span class="nav-icon">🎬</span>关键画面</a>
<a class="nav-a" href="#subtitles"><span class="nav-icon">📄</span>原始字幕</a>
```

### Step 5: Save and Open

```bash
open /tmp/<video-id>-notes.html   # macOS
```

Tell the user: save path, subtitle entry count, keyframe count, sections covered.

## Quality Guidelines

- **Summary is mandatory** — always write the executive summary; it's the first thing readers see.
- **Keyframes add context** — when ffmpeg is available, always capture frames; they anchor abstract concepts to real visuals.
- **Depth over breadth** — 4–7 well-developed sections beat 12 shallow ones.
- **Diagrams are mandatory** when content has comparisons, progressions, or architectures.
- **Language matching (MANDATORY)** — The notes UI language MUST match the user's request language, regardless of the video's language. If the user writes in Chinese, ALL generated text (summary, section titles, card content, quotes, sidebar nav, hero text, diagram labels, takeaways) MUST be in Chinese. English video + Chinese request = Chinese notes. Never default to English just because the video is in English.
