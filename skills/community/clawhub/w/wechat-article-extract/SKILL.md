---
name: wechat-article-extract
description: Extract public WeChat Official Account articles from mp.weixin.qq.com links or saved HTML into clean Markdown or structured JSON, including title, account name, publish time, article text, tables, image markers, and image URLs. Use when the user asks to read, scrape, parse, extract, archive, convert, summarize, or save WeChat/Weixin/微信公众号 public article content.
---

# WeChat Article Extract

Use this skill to extract a public WeChat Official Account article into portable Markdown or JSON. It is intentionally local and generic: it does not require the user's Feishu, knowledge-base profile, database, or API keys.

## Quick Start

Run the bundled script from the skill directory:

```bash
python3 scripts/extract_wechat_article.py "https://mp.weixin.qq.com/s/..." --format markdown --output article.md
python3 scripts/extract_wechat_article.py "https://mp.weixin.qq.com/s/..." --format json --output article.json
```

For an HTML file already saved from a browser:

```bash
python3 scripts/extract_wechat_article.py --html-file article.html --source-url "https://mp.weixin.qq.com/s/..." --format markdown
```

## Workflow

1. Confirm the input is a public `https://mp.weixin.qq.com/s/...` article URL or a saved HTML file. Private drafts, logged-in backend pages, and non-WeChat URLs are out of scope.
2. Extract with `scripts/extract_wechat_article.py`.
3. If network fetching fails because WeChat blocks the request, ask the user to save the article HTML from a browser and rerun with `--html-file`.
4. Use Markdown for human-readable archives and JSON for downstream import pipelines.
5. Keep copyright boundaries: summarize or transform extracted content when sharing externally; do not republish full articles unless the user has rights to do so.

## Outputs

Markdown output contains:

- article title, account name, publish time, source URL, and image count
- full text with blank-line paragraph separation
- tables converted to Markdown tables when possible
- inline image placeholders like `[[WECHAT_IMAGE_1]]`
- image URL list at the end

JSON output contains:

- `articleId`
- `title`
- `author`
- `publishTime`
- `sourceUrl`
- `content`
- `contentWithImageMarkers`
- `imageEntries`
- `imageUrls`
- `imageCount`
- `coverImageUrl`

## Notes

- The script uses only the Python standard library.
- It preserves image positions with markers but does not download images by default.
- Add `--download-images <dir>` when the user explicitly wants local image files.
- WeChat article pages change over time; if live extraction fails, saved HTML is the most reliable fallback.
