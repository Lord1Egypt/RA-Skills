---
name: web-fetcher
description: "Smart web content fetcher - articles and videos from WeChat, Feishu, Bilibili, Zhihu, Toutiao, YouTube, etc. Triggers: '抓取文章', '下载网页', '保存文章', 'fetch URL', '下载视频', '抓取飞书文档', '抓取微信文章', '把这个链接内容保存下来', '下载B站视频', 'download video', 'scrape article'."
version: 0.1.1
license: Complete terms in LICENSE
---

# Web Fetcher

Smart web content fetcher for Claude Code. Automatically detects platform and uses the best strategy to fetch articles or download videos.

## Quick Start

```bash
# Fetch an article
python3 {SKILL_DIR}/fetcher.py "URL" -o ~/docs/

# Download a video
python3 {SKILL_DIR}/fetcher.py "https://b23.tv/xxx" -o ~/videos/

# Batch fetch from file
python3 {SKILL_DIR}/fetcher.py --urls-file urls.txt -o ~/docs/
```

## Install Dependencies

Install only what you need — dependencies are checked at runtime:

| Dependency | Purpose | Install |
|-----------|---------|---------|
| scrapling | Article fetching (HTTP + browser) | `pip install scrapling` |
| yt-dlp | Video download | `pip install yt-dlp` |
| camoufox | Anti-detection browser (Xiaohongshu, Weibo) | `pip install camoufox && python3 -m camoufox fetch` |
| html2text | HTML to Markdown conversion | `pip install html2text` |

## Smart Routing

The fetcher automatically detects the platform from the URL:

| Platform | Method | Notes |
|----------|--------|-------|
| mp.weixin.qq.com | scrapling | Extracts `data-src` images, handles SVG placeholders |
| *.feishu.cn | Virtual scroll | Collects all blocks via scrolling, downloads images with cookies |
| zhuanlan.zhihu.com | scrapling | `.Post-RichText` selector |
| www.zhihu.com | scrapling | `.RichContent` selector |
| www.toutiao.com | scrapling | Handles `toutiaoimg.com` base64 placeholders |
| www.xiaohongshu.com | camoufox | Anti-bot protection requires stealth browser |
| www.weibo.com | camoufox | Anti-bot protection requires stealth browser |
| bilibili.com / b23.tv | yt-dlp | Video download, supports quality selection |
| youtube.com / youtu.be | yt-dlp | Video download |
| douyin.com | yt-dlp | Video download |
| Unknown URLs | scrapling | Generic fetch with fallback tiers |

## CLI Reference

```
python3 {SKILL_DIR}/fetcher.py [URL] [OPTIONS]

Arguments:
  url                    URL to fetch

Options:
  -o, --output DIR       Output directory (default: current)
  -q, --quality N        Video quality, e.g. 1080, 720 (default: 1080)
  --method METHOD        Force method: scrapling, camoufox, ytdlp, feishu
  --selector CSS         Force CSS selector for content extraction
  --urls-file FILE       File with URLs (one per line, # for comments)
  --audio-only           Extract audio only (video downloads)
  --no-images            Skip image download (articles)
  --cookies-browser NAME Browser for cookies (e.g., chrome, firefox)
```

## Platform Notes

### WeChat (mp.weixin.qq.com)
- Images use `data-src` attribute with `mmbiz.qpic.cn` URLs
- Visible `<img>` tags contain SVG placeholders (lazy loading)
- Image download requires `Referer: https://mp.weixin.qq.com/` header
- Scrapling GET usually works; no browser needed

### Feishu (*.feishu.cn)
- Uses virtual scroll — content blocks are rendered on-demand
- The fetcher scrolls through the entire document, collecting `[data-block-id]` elements
- Images require authenticated fetch (cookies), downloaded via browser's fetch API
- May show "Unable to print" artifacts which are auto-cleaned

### Bilibili
- Short links (b23.tv) are auto-resolved
- For premium/member content, use `--cookies-browser chrome`
- Default quality is 1080p, adjustable with `-q`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `scrapling not found` | `pip install scrapling` |
| `yt-dlp not found` | `pip install yt-dlp` |
| Article content too short | Try `--method camoufox` for JS-heavy pages |
| Feishu returns login page | The doc may require authentication |
| Bilibili 403 | Use `--cookies-browser chrome` |
| Image download fails | Check network; WeChat images need Referer header (auto-handled) |

## Manual Usage

When the CLI doesn't fit your needs, use the modules directly:

```python
from lib.router import route, check_dependency
from lib.article import fetch_article
from lib.video import fetch_video
from lib.feishu import fetch_feishu

# Route a URL
r = route("https://mp.weixin.qq.com/s/xxx")
# {'type': 'article', 'method': 'scrapling', 'selector': '#js_content', 'post': 'wx_images'}

# Fetch article
fetch_article(url, output_dir="/tmp/out", route_config=r)

# Download video
fetch_video(url, output_dir="/tmp/out", quality="720")

# Fetch Feishu doc
fetch_feishu(url, output_dir="/tmp/out")
```
