# Web to WeChat

抓取任意网页内容，AI 智能整理排版，自动生成封面图，一键发布到微信公众号草稿箱。

## Features

- **10+ site types** — WeChat articles, Toutiao, Zhihu, CSDN, Juejin, Medium, generic news/blog
- **AI-powered formatting** — Intelligent content cleanup, heading restructuring, style adaptation
- **Smart scraping** — Auto-detects site type and uses optimal selectors; WebFetch fallback for JS pages
- **Cover image generation** — AI-generated, auto-compressed to WeChat's 64KB limit
- **One-click publish** — Uploads directly to WeChat draft box with source attribution
- **Copyright-aware** — Preserves author credits, adds source links, supports faithful/summary/rewrite modes

## First-Time Setup

### 1. Install Dependencies

```bash
python -m pip install requests beautifulsoup4 html2text markdown Pillow
```

### 2. Install Companion Skills

```bash
clawhub install anything-to-wechat
clawhub install file-to-wechat
```

### 3. Configure WeChat Credentials

1. Log in to https://mp.weixin.qq.com/
2. Go to: 设置与开发 → 基本配置
3. Copy your **AppID** and **AppSecret**
4. Add your server IP to the **IP白名单**

Set environment variables (or the script will prompt you interactively):

**macOS / Linux:**
```bash
export WECHAT_APP_ID="your_appid"
export WECHAT_APP_SECRET="your_appsecret"
```

**Windows (PowerShell):**
```powershell
[Environment]::SetEnvironmentVariable("WECHAT_APP_ID", "your_appid", "User")
[Environment]::SetEnvironmentVariable("WECHAT_APP_SECRET", "your_appsecret", "User")
```

## How It Works

```
URL (any website)
    |
    v
scrape_web.py --> raw_article.md (title, author, content, images)
    |
    v
AI Reformatting --> article.md (clean Markdown, proper structure)
    |
    v
ImageGen --> wechat_cover.png
    |
    v
compress_image.py --> wechat_cover_compressed.jpg (<64KB)
    |
    v
md_to_wechat_html.py --> wechat_article.html (inline styles, WeChat-safe)
    |
    v
publish_to_wechat.py --> WeChat Draft Box
    |
    v
Review at mp.weixin.qq.com --> Publish
```

## Quick Start

Simply tell the agent:

```
帮我抓取 https://example.com/article 的内容，发到我的微信公众号
```

Or:

```
把这篇文章转载到我的公众号：https://mp.weixin.qq.com/s/xxxxx
```

## Content Styles

| Style | Description |
|---|---|
| **忠实转载** | Faithful reprint with clean formatting |
| **精华摘要** | Key highlights condensed version |
| **深度改写** | Deep rewrite in your own voice |

## Scripts

| Script | Description |
|---|---|
| `scripts/scrape_web.py` | Web scraping → clean Markdown (10+ site types) |
| `scripts/compress_image.py` | Image compression for WeChat cover (64KB target) |

## Supported Sites

| Site | Status |
|---|---|
| WeChat articles | Auto-detect selectors |
| Toutiao / 今日头条 | Auto-detect |
| Zhihu / 知乎 | Auto-detect |
| CSDN | Auto-detect |
| Juejin / 掘金 | Auto-detect |
| Medium | Auto-detect |
| Generic websites | Auto article detection |
| JS-rendered SPAs | WebFetch fallback |

## Configuration

| Variable | Required | Description |
|---|---|---|
| `WECHAT_APP_ID` | Yes | WeChat Official Account AppID (or prompted interactively) |
| `WECHAT_APP_SECRET` | Yes | WeChat Official Account AppSecret (or prompted interactively) |

## License

MIT
