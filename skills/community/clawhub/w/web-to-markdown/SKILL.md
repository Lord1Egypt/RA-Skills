---
name: web-to-markdown
description: |
  网页内容抓取与图片提取技能。支持：(1) 将网页转换为 Markdown 格式阅读 (2) 从任意网站提取图片 URL (3) 批量下载网页图片。当需要抓取网页内容、读取文章、提取或下载网站图片时使用此技能。支持 markdown.new、defuddle.md、r.jina.ai 等转换服务，自动降级确保成功。
  Web scraping and image extraction skill. Supports: (1) Converting web pages to Markdown for reading (2) Extracting image URLs from any website (3) Batch downloading images. Use this skill when you need to scrape web content, read articles, or extract/download images from websites. Supports markdown.new, defuddle.md, r.jina.ai conversion services with automatic fallback.
---

# Web to Markdown

## 概述 / Overview

通用网页抓取工具，支持：
A general-purpose web scraping tool that supports:

- 将网页内容转换为干净的 Markdown / Converting web content to clean Markdown
- 从任意网站提取图片 URL / Extracting image URLs from any website
- 批量下载网页图片 / Batch downloading images from web pages

适用于内容阅读、图片收集、资料整理等场景。
Suitable for content reading, image collection, and data organization.

## 功能模块 / Features

### 1. 网页转 Markdown / Web to Markdown

将网页 URL 转换为干净的 Markdown 文本，移除广告、导航栏等无关内容。
Converts a web page URL into clean Markdown text, removing ads, navigation bars, and other irrelevant content.

**URL 前缀服务 / URL Prefix Services：**

| 服务 Service | 前缀 Prefix | 特点 Notes |
|------|------|------|
| markdown.new | `https://markdown.new/` | 首选，速度快 / Preferred, fast |
| defuddle | `https://defuddle.md/` | 备选 / Fallback |
| r.jina.ai | `https://r.jina.ai/` | 适合动态内容 / Good for dynamic content |

**使用 / Usage：**
```bash
curl -s "https://markdown.new/https://example.com/article"
curl -s "https://r.jina.ai/https://example.com/article"
```

### 2. 提取网页图片 / Extract Images from Web Pages

从任意网页提取所有图片 URL。
Extracts all image URLs from any web page.

**通用提取 / General Extraction：**
```bash
# 提取所有图片 URL / Extract all image URLs
curl -s "https://r.jina.ai/<url>" | grep -oE 'https://[^)\s"]+\.(jpg|jpeg|png|gif|webp|avif)'
```

**使用脚本 / Using the Script：**
```bash
python scripts/extract_images.py <url> [--output urls.txt]
```

### 3. 批量下载图片 / Batch Download Images

从网页提取图片并批量下载到本地。
Extracts images from web pages and downloads them in batch to local storage.

**使用脚本 / Using the Script：**
```bash
python scripts/download_images.py <url> [--output <dir>] [--limit <n>] [--min-size <bytes>]
```

**参数 / Parameters：**
- `url`: 网页 URL / Web page URL
- `--output`: 输出目录（默认 `~/.openclaw/images`）/ Output directory (default: `~/.openclaw/images`)
- `--limit`: 最大下载数（默认 50）/ Max downloads (default: 50)
- `--min-size`: 最小文件大小，过滤小图标（默认 10KB）/ Min file size to filter out small icons (default: 10KB)
- `--ext`: 只下载指定格式（jpg/png/gif/webp）/ Only download specific formats (jpg/png/gif/webp)

**示例 / Examples：**
```bash
# 下载网页中的所有大图 / Download all large images from a page
python scripts/download_images.py "https://example.com/gallery" --output ~/Downloads/images

# 只下载 PNG，最多 20 张 / Download only PNGs, max 20
python scripts/download_images.py "https://example.com" --ext png --limit 20

# Pinterest（自动转换原始尺寸）/ Pinterest (auto-converts to original size)
python scripts/download_images.py "https://www.pinterest.com/search/pins/?q=architecture"
```

## 工作流程 / Workflow

### 网页内容抓取 / Web Content Scraping

1. 首选 `markdown.new/` / Prefer `markdown.new/`
2. 失败则尝试 `defuddle.md/` / Fall back to `defuddle.md/`
3. 再失败尝试 `r.jina.ai/` / Then try `r.jina.ai/`
4. 最终使用本地 Scrapling 脚本 / Finally use local Scrapling script

### 图片提取下载 / Image Extraction & Download

1. 使用 `r.jina.ai` 获取网页内容 / Use `r.jina.ai` to fetch page content
2. 正则提取所有图片 URL / Extract all image URLs via regex
3. 过滤小图片（图标、表情等）/ Filter out small images (icons, emojis, etc.)
4. 智能命名并下载保存 / Smart naming and download

## 特殊网站支持 / Special Website Support

### Pinterest

自动识别 Pinterest URL，将缩略图转换为原始尺寸：
Automatically detects Pinterest URLs and converts thumbnails to original size:
- `236x` → `originals`
- `564x` → `originals`

### 其他常见网站 / Other Common Websites

脚本会自动处理各种网站的图片 URL 格式，包括：
The scripts automatically handle various image URL formats, including:
- CDN 链接 / CDN links
- 带参数的 URL / URLs with query parameters
- 懒加载图片 / Lazy-loaded images

## 脚本说明 / Script Reference

### scripts/scrape.py

本地网页抓取脚本，作为在线服务的降级方案。
Local web scraping script, used as a fallback for online services.

```bash
python scripts/scrape.py <url>
```

### scripts/extract_images.py

提取网页中的图片 URL，输出为列表。
Extracts image URLs from a web page and outputs them as a list.

```bash
python scripts/extract_images.py <url> [--output urls.txt]
```

### scripts/download_images.py

批量下载网页图片。
Batch downloads images from a web page.

```bash
python scripts/download_images.py <url> [options]
```

## 依赖 / Dependencies

`extract_images.py` 和 `download_images.py` 仅使用 Python 标准库，无需额外安装。
`extract_images.py` and `download_images.py` only use the Python standard library — no extra installation needed.

`scrape.py` 需要安装 `scrapling`（本地抓取降级方案）：
`scrape.py` requires `scrapling` (local scraping fallback):

```bash
pip install scrapling
```

## 注意事项 / Notes

- 遵守网站的 robots.txt 和使用条款 / Respect the website's robots.txt and terms of use
- 大量下载前考虑网站服务器压力 / Consider server load before mass downloading
- 部分网站有防盗链，可能无法直接下载 / Some sites have hotlink protection and may block direct downloads
- 动态加载的图片可能需要使用 `r.jina.ai` / Dynamically loaded images may require `r.jina.ai`
