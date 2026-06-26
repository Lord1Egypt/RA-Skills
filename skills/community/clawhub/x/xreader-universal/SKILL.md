---
name: x-reader
description: "Universal content reader for WeChat/Bilibili/Twitter/YouTube/Xiaohongshu. Use when you need to fetch full article content from platforms that block simple HTTP fetching, especially WeChat public accounts. Supports: WeChat, Bilibili, X/Twitter, YouTube, Xiaohongshu, RSS, any web page."
---

# x-reader

Universal content reader — fetch and digest content from 7+ platforms.

## Installation

```bash
# Python venv: ~/.openclaw/venv-xreader
# CLI path: ~/.openclaw/venv-xreader/bin/x-reader
```

## Environment Setup

Obsidian vault path is configured via environment variable:
```
OBSIDIAN_VAULT=~/Library/Mobile Documents/com~apple~CloudDocs/MyVault
```

## Usage

```bash
# Basic fetch
x-reader <url>

# Multiple URLs
x-reader <url1> <url2>

# Login to platform (saves session for browser fallback)
x-reader login xhs

# Show inbox
x-reader list

# Clear inbox
x-reader clear
```

## Supported Platforms

| Platform | Text Fetch | Video Transcript |
|----------|-----------|-----------------|
| WeChat (微信公众号) | Jina → Playwright fallback | — |
| Bilibili (B站) | API | via skill |
| X / Twitter | Jina → Playwright | — |
| YouTube | Jina + yt-dlp subtitles | Groq Whisper |
| Xiaohongshu (小红书) | Jina → Playwright + session | — |
| Telegram | Telethon | — |
| RSS | feedparser | — |
| Any web page | Jina | — |

## For WeChat Articles

WeChat public accounts require Playwright browser fallback. Run once:
```bash
x-reader login xhs  # creates browser session
```

Then fetch WeChat articles normally:
```bash
x-reader https://mp.weixin.qq.com/s/abc123
```

## As Python Library

```python
import asyncio
from x_reader.reader import UniversalReader

async def main():
    reader = UniversalReader()
    content = await reader.read("https://mp.weixin.qq.com/s/abc123")
    print(content.title)
    print(content.content[:200])

asyncio.run(main())
```

## CLI Path

`~/.openclaw/venv-xreader/bin/python` — Python with x-reader installed
`~/.openclaw/venv-xreader/bin/x-reader` — x-reader CLI
