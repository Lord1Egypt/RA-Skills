---
name: web-to-wechat
description: "抓取任意网页内容，AI 智能整理格式，自动生成封面图和配图，发布到微信公众号草稿箱。支持微信公众号文章、新闻网站、技术博客、知乎、CSDN 等。Use when the user wants to scrape a web page and publish it to WeChat."
version: 1.0.0
prerequisites:
  - anything-to-wechat
  - file-to-wechat
tags:
  - wechat
  - web-scraping
  - article
  - publishing
  - chinese
  - 公众号
  - 网页抓取
triggers:
  - "抓取.*网页.*发.*微信"
  - "把.*链接.*发到.*公众号"
  - "抓.*文章.*发微信"
  - "网页.*转.*公众号"
  - "scrape.*web.*wechat"
  - "web to wechat"
  - "抓取网页发布"
  - "转载.*到.*微信"
  - "把这篇文章发到公众号"
---

# Web to WeChat

抓取**任意网页链接**的内容，AI 智能整理排版，自动生成封面图，发布到微信公众号草稿箱。

## User-Facing Promise

Accept requests like:

- "帮我抓取这个链接的内容，发到微信公众号"
- "把这篇文章转载到我的公众号"
- "抓取 https://xxx.com/article 发布到微信"
- "把这个网页内容整理成公众号文章"
- "帮我收藏这篇文章到我的公众号"

**Return a published draft in the WeChat draft box, not a proposal.**

## First-Time Setup

### 1. Install Python Dependencies

```bash
python -m pip install requests beautifulsoup4 html2text markdown Pillow
```

### 2. Install Companion Skills

This skill depends on two companion skills from ClawHub:

```
clawhub install anything-to-wechat
clawhub install file-to-wechat
```

- **anything-to-wechat** — provides `publish_to_wechat.py` (WeChat API publishing)
- **file-to-wechat** — provides `md_to_wechat_html.py` (Markdown → WeChat HTML)

### 3. Configure WeChat Credentials

You need a **WeChat Official Account** (服务号 or 订阅号 with API access).

**Get your credentials:**

1. Log in to https://mp.weixin.qq.com/
2. Go to: 设置与开发 → 基本配置
3. Copy your **AppID** and reset/view **AppSecret**
4. Add your server's public IP to the **IP白名单**

**Set environment variables (recommended):**

On **macOS / Linux**:
```bash
export WECHAT_APP_ID="your_appid_here"
export WECHAT_APP_SECRET="your_appsecret_here"
```

On **Windows** (PowerShell):
```powershell
[Environment]::SetEnvironmentVariable("WECHAT_APP_ID", "your_appid_here", "User")
[Environment]::SetEnvironmentVariable("WECHAT_APP_SECRET", "your_appsecret_here", "User")
```

**No environment variables?** The publish script will prompt you interactively on first run.

## Prerequisites

| Dependency | Required | Purpose |
|---|---|---|
| `requests` (pip) | Yes | HTTP fetching |
| `beautifulsoup4` (pip) | Yes | HTML parsing |
| `html2text` (pip) | Yes | HTML → Markdown conversion |
| `markdown` (pip) | Yes | Markdown → HTML (via md_to_wechat_html.py) |
| `Pillow` (pip) | Yes | Image compression |
| **anything-to-wechat** skill | Yes | WeChat API publishing |
| **file-to-wechat** skill | Yes | Markdown → WeChat HTML conversion |

## Workflow

### Phase 1: Collect Input

If the user has NOT provided a URL, ask using AskUserQuestion:

```
Question: "请提供你想抓取并发布到微信公众号的网页链接"
Options:
  - "粘贴 URL"
  - "搜索关键词后选择文章"
```

If the user already provided a URL, **skip and proceed**.

### Phase 2: Scrape Web Content

**IMPORTANT: Always use UTF-8 encoding on Windows.**

**Primary: Use scrape_web.py script (structured extraction)**

```bash
python "<skill_dir>/scripts/scrape_web.py" \
  --url "<url>" \
  --output "<workspace>/raw_article.md" \
  --json
```

The `--json` flag outputs structured data including title, author, date, cover URL, and Markdown content.

**Fallback: Use WebFetch tool (for JS-rendered pages)**

If scrape_web.py fails (e.g., the page requires JavaScript rendering), use the built-in `WebFetch` tool:

```
WebFetch(url="<url>", prompt="Extract the full article content including: title, author, publish date, and the complete article text. Return in a structured format.")
```

Then manually compose the Markdown from the WebFetch output.

**After scraping:** Read the output. Inspect the content structure and quality. Proceed to Phase 3.

### Phase 3: AI Content Reformatting

**This is the key quality step.** The agent should:

1. **Read** the scraped Markdown content
2. **Rewrite/reformat** the content for WeChat publishing:
   - Ensure clean heading hierarchy (H1 → H2 → H3)
   - Fix broken formatting (tables, lists, code blocks)
   - Remove navigation artifacts, ads, social media buttons
   - Ensure paragraphs flow naturally
   - Add section breaks where appropriate
   - Keep the original meaning and facts intact
3. **Output** a clean, well-structured Markdown file

**Style options** (ask user or auto-detect):

| Style | When to use |
|---|---|
| **忠实转载** (faithful reprint) | User wants exact copy, just clean formatting |
| **精华摘要** (key highlights) | Long article → condensed version with key points |
| **深度改写** (deep rewrite) | Rewrite in user's own voice/style |

**Save the reformatted Markdown:**

Write the reformatted content to `<workspace>/article.md` using the Write tool.

### Phase 4: Generate Cover Image

Use the `ImageGen` tool with a prompt derived from the article's topic and content.

- Save as `wechat_cover.png` in the workspace.
- **Size: `1024x768`** (WeChat cover ratio 4:3).
- Make it visually compelling and relevant to the article topic.

### Phase 5: Compress Cover Image

WeChat requires cover images (thumb_media_id) to be **under 64KB**.

```bash
python "<skill_dir>/scripts/compress_image.py" \
  --input "<workspace>/wechat_cover.png" \
  --output "<workspace>/wechat_cover_compressed.jpg" \
  --max-size 64
```

If the original cover is already under 64KB (rare for PNG), this step can be skipped. But always run it to be safe — it won't enlarge files.

**Fallback:** If compress_image.py fails to reach 64KB, use ImageGen to regenerate a simpler cover image (fewer details, simpler composition) and try again.

### Phase 6: Convert to WeChat HTML

Use `md_to_wechat_html.py` from the **file-to-wechat** skill:

```bash
python "<file-to-wechat_skill_dir>/scripts/md_to_wechat_html.py" \
  --input "<workspace>/article.md" \
  --output "<workspace>/wechat_article.html" \
  --title "<article_title>"
```

This generates WeChat-compatible inline-style HTML with Clockless design tokens.

### Phase 7: Publish to WeChat Draft Box

**On Windows, use Python subprocess to pass environment variables:**

```python
python -c "
import os, subprocess, sys
os.environ['WECHAT_APP_ID'] = '<app_id>'
os.environ['WECHAT_APP_SECRET'] = '<app_secret>'
result = subprocess.run([
    sys.executable,
    r'<anything-to-wechat_skill_dir>/scripts/publish_to_wechat.py',
    '--file', r'<workspace>/wechat_article.html',
    '--title', '<article_title>',
    '--cover', r'<workspace>/wechat_cover_compressed.jpg',
    '--digest', '<article_summary_under_120_chars>',
    '--source-url', '<original_url>'
], capture_output=True, text=True, encoding='utf-8')
print(result.stdout)
print(result.stderr)
"
```

**Or with environment variables already set:**

```bash
python "<anything-to-wechat_skill_dir>/scripts/publish_to_wechat.py" \
  --file "<workspace>/wechat_article.html" \
  --title "<article_title>" \
  --cover "<workspace>/wechat_cover_compressed.jpg" \
  --digest "<article_summary_under_120_chars>" \
  --source-url "<original_url>"
```

**Credentials:** The script reads from `WECHAT_APP_ID` / `WECHAT_APP_SECRET` env vars. If not set, it prompts interactively.

### Phase 8: Confirm & Handoff

Report success with Media ID and link to `https://mp.weixin.qq.com/`.

Tell the user: "文章已发送到你的微信公众号草稿箱，请登录微信公众平台审核后一键发布。"

Include:
- Original source URL
- Article title
- Content summary
- Media ID

## Site Compatibility

| Site | Scraping Method | Notes |
|---|---|---|
| WeChat articles (mp.weixin.qq.com) | scrape_web.py | Anti-scraping: may need WebFetch fallback |
| Toutiao / 今日头条 | scrape_web.py | JS-heavy, may need WebFetch |
| Zhihu / 知乎 | scrape_web.py | Login wall for some content |
| CSDN | scrape_web.py | Works well |
| Juejin / 掘金 | scrape_web.py | Works well |
| Medium | scrape_web.py | Works well |
| News sites (generic) | scrape_web.py | Auto-detects article content |
| JS-rendered SPAs | WebFetch | Use browser rendering fallback |

## Error Handling

| Error | Action |
|---|---|
| Page returns 403/404 | Try WebFetch; if blocked, inform user |
| Content too short (<200 chars) | Page may be JS-rendered, try WebFetch |
| Chinese characters garbled | scrape_web.py auto-detects encoding |
| Cover image > 64KB | Run compress_image.py; regenerate if needed |
| Images not loading in WeChat | publish_to_wechat.py auto-uploads to WeChat CDN |
| WeChat credentials missing | Script prompts interactively |
| IP not in whitelist | Show IP from error, guide user to mp.weixin.qq.com |
| WebFetch returns empty | Page has strong anti-scraping, inform user |
| Content copyrighted | Add disclaimer, keep source attribution |

## Copyright & Attribution

**IMPORTANT:** When republishing web content:

1. Always include the original source URL in the article metadata
2. Preserve the original author's name when available
3. Add a disclaimer line at the end: "本文内容来源于[原作者名称]，原文发布于[来源网站]。如有侵权请联系删除。"
4. Use `--source-url` when publishing to add a "Read More" link
5. Consider using "精华摘要" or "深度改写" style instead of exact copy to avoid copyright issues

## Script Reference

| Script | Purpose |
|---|---|
| `scripts/scrape_web.py` | Web scraping → clean Markdown (supports 10+ site types) |
| `scripts/compress_image.py` | Image compression (target 64KB for WeChat cover) |
| `file-to-wechat/scripts/md_to_wechat_html.py` | Markdown → WeChat inline HTML |
| `anything-to-wechat/scripts/publish_to_wechat.py` | WeChat draft box publishing |

## Configuration

| Variable | Required | Description |
|---|---|---|
| `WECHAT_APP_ID` | Yes | WeChat Official Account AppID (or prompted interactively) |
| `WECHAT_APP_SECRET` | Yes | WeChat Official Account AppSecret (or prompted interactively) |
