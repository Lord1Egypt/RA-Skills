---
name: x-article-reader
description: Read X (Twitter) Articles aloud using macOS text-to-speech. Accepts an X Article URL and reads the content out loud. Automatically detects Chinese vs English and picks the appropriate voice. Use when user says "读出来", "朗读", "read aloud", "read this X article", or provides an x.com/articles URL and wants it spoken.
homepage: https://github.com/ewangchong/x-article-reader
---

# X Article Reader

Read X (Twitter) Articles aloud using macOS `say` command. Automatically detects language and selects the right voice.

## What This Skill Does

- Opens the X article URL in a **local headless browser** (patchright/Chromium — runs 100% locally)
- Extracts the article title and body text
- Reads it aloud via macOS built-in `say` command (no external TTS API)

## What Gets Installed

| Component | Size | Where |
|-----------|------|--------|
| `patchright` (Python pkg) | ~5MB | your Python env |
| Chromium browser | ~170MB | `~/.cache/ms-playwright/` |

All processing is local. No data is sent to any third-party service.

## Prerequisites

```bash
# macOS only (uses built-in say command)
pip install patchright
python3 -m patchright install chromium
```

## First-Time Setup (One-Time Login)

The skill stores its own browser profile at:
```
<skill_dir>/data/browser_state/
```

This is **completely isolated** — it does not read or write credentials from any other skill or app.

```bash
cd <skill_dir>/scripts
python3 auth_setup.py
```

A browser window opens → log in to X → session saved automatically (~7 days).

## Usage

```bash
cd <skill_dir>/scripts
python3 read_article.py "https://x.com/user/articles/123"
```

### Options

```bash
# Force a voice
python3 read_article.py "<url>" --voice Tingting

# Save audio file instead of playing
python3 read_article.py "<url>" --output ~/Desktop/article.aiff

# Show browser (debug)
python3 read_article.py "<url>" --show-browser
```

## Voices

| Language (auto-detected) | Voice |
|--------------------------|-------|
| 中文 (>15% Chinese chars) | Tingting |
| English | Samantha |

## Source Code

https://github.com/ewangchong/x-article-reader

## Trigger Examples

- "帮我读一下这篇X文章：https://x.com/xxx/articles/yyy"
- "Read this X article aloud: https://x.com/xxx/articles/yyy"
- "朗读 https://x.com/xxx/articles/yyy"
