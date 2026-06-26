---
name: wechat-article-reader
description: Extract full text from WeChat Official Account (微信公众号) article URLs. Use when a user shares an mp.weixin.qq.com link and asks to read, summarize, analyze, or save the article. Handles WeChat's JS-rendered content and anti-bot detection via headless Chromium. Falls back to mirror-site search when headless browser is unavailable.
metadata:
  openclaw:
    requires:
      bins: [python3]
    install:
      - id: playwright
        kind: pip
        package: playwright
        label: Install Playwright (pip)
---

# WeChat Article Reader

Extract full article content from `mp.weixin.qq.com` URLs.

## When to Use

- User shares a WeChat article link (`mp.weixin.qq.com/s/xxx`)
- Need to read/summarize/analyze/archive a WeChat article
- ContentPipe Scout node receives a WeChat URL for reference

## Quick Start

```bash
# First-time setup (installs headless Chromium ~200MB)
python3 SKILL_DIR/scripts/setup.py

# Extract article
python3 SKILL_DIR/scripts/fetch_article.py "https://mp.weixin.qq.com/s/xxx"

# Output: JSON with title, author, publish_time, content, word_count
```

## How It Works

WeChat articles are JS-rendered — HTTP requests only get an empty shell. This skill uses Playwright headless Chromium to:

1. Launch headless browser with anti-detection flags
2. Navigate to the WeChat URL, wait for `networkidle`
3. Wait for `#js_content` (article body container)
4. Extract title (`h1#activity-name`), author, time, body text
5. Clean HTML → plain text (strip scripts/styles, compress whitespace)
6. Return structured JSON

### Fallback: Mirror Search

If Playwright is unavailable, the skill searches Chinese content aggregators (53ai.com, 36kr.com, juejin.cn, woshipm.com) for mirror copies of the article.

## Python API

```python
from fetch_article import fetch_wechat_article

result = fetch_wechat_article("https://mp.weixin.qq.com/s/xxx")
# result = {
#   "success": True,
#   "title": "文章标题",
#   "author": "作者名",
#   "publish_time": "2026-03-10",
#   "content": "正文全文...",
#   "word_count": 2500,
#   "source": "playwright",  # or "mirror"
#   "url": "https://mp.weixin.qq.com/s/xxx"
# }
```

## Limitations

- Requires one-time Chromium install (`python3 scripts/setup.py`)
- First fetch takes ~5-10s (browser startup); subsequent fetches ~3-5s (browser reuse)
- Cannot bypass WeChat login walls (paid content, follower-only articles)
- Mirror fallback only works for popular/widely-shared articles
