---
name: weixin-web-fetch
description: Fetch complete content from WeChat public account articles (mp.weixin.qq.com). Use when extracting content from WeChat official account links, especially when default web fetch gets incomplete content.
---

# WeChat Web Fetch Skill

## Features
- Specialized for WeChat public account articles (mp.weixin.qq.com)
- Simulates browser request with proper headers to bypass login restrictions for public articles
- Extracts clean content and converts to Markdown format
- Based on Readability for accurate content extraction

## Requirements
- Python 3.7+
- httpx
- readability-lxml

## Usage
```bash
{baseDir}/scripts/weixin_fetch.py <url>
```

## Output
Returns JSON with:
- `url`: Original URL
- `final_url`: Final URL after redirects
- `title`: Article title
- `author`: Article author (if found)
- `content`: Extracted content in Markdown
- `length`: Content length
- `truncated`: Whether content was truncated

## Examples
```bash
# Fetch a WeChat article
{baseDir}/scripts/weixin_fetch.py https://mp.weixin.qq.com/s/2o2s3owEDkZziyD0UCeq2w
```
