---
name: weixin-article-reader
description: Extract the title, author, publish date, and full body text from Weixin official account article links on mp.weixin.qq.com. Use this skill when a user wants the full article text or needs the content extracted before summarization.
license: MIT-0
---

# Weixin Article Reader

Use this skill when the user provides a `mp.weixin.qq.com` article URL and wants the raw article text, or when article content must be extracted before summarization.

## Usage

Prefer the bundled script:

```bash
python3 scripts/extract_wechat_article.py "https://mp.weixin.qq.com/s/xxxx"
```

If the current working directory is not the skill root, first locate the installed `weixin-article-reader` skill directory and run `scripts/extract_wechat_article.py` from there.

The script returns JSON with:
- `title`
- `author`
- `publish_date`
- `content`
- `source_url`

## Workflow

1. Detect a `mp.weixin.qq.com` article URL.
2. Run the bundled extraction script.
3. If the user wants the full article, return title, author, publish date, and body text.
4. If the user wants a summary, first confirm the extracted `content` is non-empty, then summarize it.

## Response Guidance

- For full-text requests, return the title, author, publish date, and then the article body.
- For summaries, summarize the extracted `content` and include the title plus source URL.
- If `publish_date` is empty, do not invent a date. State that the page did not expose a publish date in a reliably parsed form.

## Notes

- Do not use `pip install`.
- Do not require `beautifulsoup4` or `requests`.
- Prefer the bundled script instead of relying on unavailable generic web-extraction helpers.
- If the script returns empty content, explain that the article may use a special page structure or access restriction.
- This skill only applies to `mp.weixin.qq.com` article pages. If the URL is from another domain, say the skill does not apply.
