---
name: wechat-article-download-api
description: Fetch and export WeChat public article content through down.mptext.top API. Use when testing this API, downloading a WeChat article, validating html/markdown/text/json output differences, or batch-saving article content to local files.
---

# WeChat Article Download API

## Overview

Use this skill to call `https://down.mptext.top/api/public/v1/download` without API key, fetch a WeChat article by URL, and save outputs as `html`, `markdown`, `text`, or `json`.

## Workflow

1. Confirm target article URL.
2. Pick output format(s): `html`, `markdown`, `text`, `json`.
3. Run `scripts/fetch_wechat_article.py` to request API and save files.
4. Check returned status, content type, and local file size.

## Quick Commands

Fetch all 4 formats to current directory:

```bash
python scripts/fetch_wechat_article.py \
  --url "https://mp.weixin.qq.com/s/W-8MSBo5FwDY8OmCUN0cSw" \
  --formats html markdown text json
```

Set output directory and basename:

```bash
python scripts/fetch_wechat_article.py \
  --url "https://mp.weixin.qq.com/s/xxx" \
  --formats json \
  --outdir "d:/wechattxt/output" \
  --basename "wx_article"
```

## Output Naming

Save files as `{basename}.{ext}`:
- `html -> .html`
- `markdown -> .md`
- `text -> .txt`
- `json -> .json`

Print one summary line per format:
- HTTP status code
- response `Content-Type`
- output file path
- byte size

## Error Handling

Treat non-200 status as failure.
Keep processing remaining formats unless `--fail-fast` is set.
Raise process exit code `1` if any format fails.

## Resources

- API details: `references/api.md`
- Runner script: `scripts/fetch_wechat_article.py`
