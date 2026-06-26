# Weixin Article Reader

`weixin-article-reader` is an OpenClaw skill for extracting content from public Weixin official account article pages on `mp.weixin.qq.com`.

## What It Does

- Extracts article title
- Extracts author / account name when available
- Extracts publish date when available
- Extracts main article body text
- Returns structured JSON

## Input

A public Weixin article URL such as:

```text
https://mp.weixin.qq.com/s/xxxxxxxxxxxxxxxxxxxx
```

## Output

The bundled script prints JSON like:

```json
{
  "ok": true,
  "source_url": "https://mp.weixin.qq.com/s/...",
  "title": "Article title",
  "author": "Account name",
  "publish_date": "2026-03-29",
  "content": "Full article body text..."
}
```

## Run

From the skill directory:

```bash
python3 scripts/extract_wechat_article.py "https://mp.weixin.qq.com/s/xxxxxxxxxxxxxxxxxxxx"
```

## Constraints

- Standard library only, no third-party Python dependencies
- Supports `mp.weixin.qq.com` article pages only
- Some pages may not expose a publish date
- Some pages may block extraction or use a page structure that yields partial or empty content

## License

MIT-0
