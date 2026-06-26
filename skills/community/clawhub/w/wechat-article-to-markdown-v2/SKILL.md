---
name: wechat-article-to-markdown
description: This skill converts WeChat Official Account (微信公众号) article pages into high-quality, clean Markdown format. It should be used when the user provides a WeChat article URL (mp.weixin.qq.com) and wants to convert, extract, save, or archive the article content as Markdown. Trigger phrases include "convert WeChat article", "微信文章转Markdown", "save this WeChat article", "extract article content", "抓取微信文章", "文章转MD", or when a mp.weixin.qq.com URL is provided.
version: "1.1.0"
---

## Changelog

### v1.1.0 (2026-04-11)

**修复：**
- `fetch_with_playwright` 改用移动端 Chromium（`is_mobile=True` + iPhone UA + 393×852 viewport），临时分享链接（tempkey）可正常渲染
- 新增懒加载图片处理：滚动触发 `data-src` 图片加载
- 新增「页面不存在」错误检测

**对比（v1.0 → v1.1）：**
| 项目 | 旧版 | 新版 |
|------|------|------|
| User Agent | 桌面 Chrome | iPhone Safari |
| Viewport | 1280×900 | 393×852 |
| 临时链接 | ❌ 无法渲染 | ✅ 正常 |
| 懒加载图片 | ❌ | ✅ 滚动触发 |

---

# WeChat Article to Markdown

## Overview

Convert WeChat Official Account articles (`mp.weixin.qq.com`) into clean, high-quality Markdown. The skill uses a Python script optimized for WeChat's unique DOM structure, featuring deep noise removal, smart code block detection, rich text preservation, and intelligent paragraph formatting.

## Workflow

### Decision Tree

```
User provides WeChat article URL?
├── Yes → Go to Step 1: Install Dependencies & Run Script
├── User wants to convert HTML directly?
│   └── Use Step 2: In-Line Conversion (for fetched HTML)
└── User asks about multiple URLs?
    └── Use batch mode with -f flag
```

### Step 1: Install Dependencies & Convert

1. Ensure Python dependencies are available. Install if missing:
   ```bash
   pip install requests beautifulsoup4 markdownify
   ```

2. Run the conversion script:
   ```bash
   python scripts/wechat_to_md.py "<WECHAT_URL>" -o "<OUTPUT_DIR>"
   ```

   **Options:**
   - `--no-images` — Skip image downloading, keep remote URLs
   - `--no-frontmatter` — Omit YAML frontmatter
   - Multiple URLs: `python scripts/wechat_to_md.py url1 url2 url3`

3. The output structure:
   ```
   <OUTPUT_DIR>/
   └── <Article_Title>/
       ├── <Article_Title>.md
       └── images/
           ├── img_000.png
           └── img_001.jpg
   ```

### Step 2: In-Line Conversion (for Pre-Fetched HTML)

If the HTML has already been fetched (e.g., via `web_fetch`), use the script's `convert_simple()` function programmatically:

```python
import sys
sys.path.insert(0, "<SKILL_DIR>/scripts")
from wechat_to_md import convert_simple

# 基础用法：仅转换，不下载图片
result = convert_simple("https://mp.weixin.qq.com/s/xxxxx")
markdown = result["markdown"]       # Full Markdown string
metadata = result["metadata"]       # {title, author, date, url, ...}
code_blocks = result["code_blocks"] # [{lang, code}, ...]
image_urls = result["image_urls"]   # 原始图片 URL 列表

# 高级用法：同时下载图片到本地
result = convert_simple(
    "https://mp.weixin.qq.com/s/xxxxx",
    download_imgs=True,              # 启用图片下载
    output_dir="./my_article"        # 指定输出目录（可选）
)
markdown = result["markdown"]        # 图片链接已替换为本地路径
image_mapping = result["image_mapping"]  # URL -> 本地路径映射
output_dir = result["output_dir"]    # 实际输出目录
```

Return the Markdown content directly to the user or write it to a file.

### Step 3: Present Results

- Display the generated Markdown file path to the user.
- If the user wants to review the content, read the `.md` file and present a summary.
- For batch conversions, report success/failure count.

## Core Capabilities

### 1. Deep Noise Removal (WeChat-Specific)

The script removes 30+ WeChat-specific noise elements including:
- Ad banners and promotional content (`.mp_profile_iframe`, `#ad_content`)
- QR codes and reward/tip areas (`.reward_area`, `.qr_code_pc`)
- Comment sections (`#comment_container`, `#js_cmt_area`)
- Audio/video players (`mpvoice`, `mpvideo`)
- Related article recommendations (`#relation_article`)
- Tool bars, footers, copyright areas, tag sections
- Hidden elements (`display:none`, `visibility:hidden`)
- Empty `<span>` placeholders

### 2. Smart Code Block Detection

Handles all 3 WeChat code block formats:
- `pre.code-snippet` with `data-lang` attribute
- `.code-snippet__fix` container with nested `pre[data-lang]`
- Generic `pre[data-lang]`

Features:
- Auto-detects programming language from `data-lang`, CSS class, and code content
- Removes line numbers (`.code-snippet__line-index`)
- Filters CSS counter leaks (`counter(line)` garbage text)
- Uses placeholder strategy: extract code blocks before conversion, restore after
- Supports 25+ languages: Python, JavaScript, TypeScript, Go, Rust, Java, C, C++, SQL, HTML, CSS, JSON, YAML, Shell, Dockerfile, etc.

### 3. Rich Text Preservation

- **Bold/Italic**: Normalizes `<b>` → `<strong>`, `<i>` → `<em>`, handles inline `font-weight: bold`
- **Lists**: Converts WeChat marker-based lists (`•`, `·`, `1.`, `(1)`) to proper Markdown lists
- **Blockquotes**: Detects left-border styled sections as blockquotes
- **Tables**: Preserves table structure
- **Links**: Preserves article links
- **Headings**: Detects font-size based headings (≥22px → H2, ≥19px → H3)

### 4. Intelligent Paragraph Formatting

- Fixes lazy-loaded images (`data-src` → `src`)
- Cleans HTML entity residuals (`&nbsp;` → space, zero-width spaces removed)
- Collapses excessive blank lines (max 2 consecutive)
- Trims trailing whitespace per line
- Proper spacing around code blocks
- Full-width spaces → half-width spaces

### 5. Metadata Extraction

Generates YAML frontmatter:
```yaml
---
title: "Article Title"
author: "Account Name"
date: "2026-04-08"
source: "https://mp.weixin.qq.com/s/xxxxx"
description: "Article description if available"
---
```

### 6. Image Handling

- **自动下载**：下载所有文章图片到 `images/` 子目录
- **并发下载**：默认 5 个并发线程，支持重试机制（默认重试 2 次）
- **格式检测**：从 URL 和 Content-Type 自动检测图片格式
- **链接替换**：自动将 Markdown 中的远程 URL 替换为本地相对路径 (`images/img_000.png`)
- **URL 变体处理**：智能处理微信图片 URL 的不同查询参数变体
- **失败回退**：下载失败时保留原始远程 URL
- **文件验证**：验证下载文件大小（过滤小于 100 字节的损坏文件）

图片下载增强功能：
```python
# 下载图片并获取映射关系
from wechat_to_md import download_images, replace_image_urls

# 下载图片
url_to_local = download_images(
    img_urls=["https://mmbiz.qpic.cn/..."],
    output_dir=Path("./output"),
    concurrency=5,    # 并发数
    timeout=30,       # 超时时间（秒）
    retries=2         # 重试次数
)

# 替换 Markdown 中的图片链接
md = replace_image_urls(markdown, url_to_local)
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `NetworkError` | HTTP failure, timeout, 404 | Retries 3x with exponential backoff |
| `CaptchaError` | Captcha page detected | Inform user to wait and retry |
| `ParseError` | Content element not found | Check URL validity, may be restricted article |
| Missing dependencies | `pip install` not run | Install: `pip install requests beautifulsoup4 markdownify` |

## Important Notes

- Only supports `mp.weixin.qq.com` domain articles
- Some code blocks are rendered as images/SVG — their source code cannot be extracted
- Captcha pages may appear under high-frequency access; wait and retry
- Public articles only — login-gated articles cannot be fetched
- Respect original author copyright; for personal study/archiving use only

## References

For detailed WeChat article DOM structure, selectors, and element handling, refer to:
- `references/wechat-dom-reference.md` — Complete WeChat DOM structure documentation
