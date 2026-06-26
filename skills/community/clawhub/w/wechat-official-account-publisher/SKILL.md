---
name: wechat-publisher
description: Publish articles to WeChat Official Account (微信公众号) draft box via API. Use when the user wants to upload a Markdown article (with optional local images) to their WeChat 公众号 草稿箱. Handles token management, image uploading to WeChat CDN, Markdown-to-HTML conversion, and draft creation. Does NOT generate images — images must be provided as local files.
---

# WeChat Publisher Skill

Publish Markdown articles to WeChat Official Account draft box.

## Prerequisites

1. Create `config.json` in the skill root (copy from `config.example.json`), **or** set env vars `WX_APPID` / `WX_APPSECRET` (recommended for secrets).
2. Python 3 available (`python3`)
3. All scripts are in `scripts/` relative to this SKILL.md

For full API details, read `references/wechat_api.md`.

## Workflow

### Step 1 — Gather inputs

Ask the user (or infer from context):
- **Article**: path to `.md` file
- **Cover image** (required): local image file for the article thumbnail (jpg/png, ≤1MB)
- **Body images** (optional): local image files referenced in the article
- **Title**: article title (use H1 from markdown if not specified)
- **Author** (optional)
- **Digest/summary** (optional, ≤120 chars)

### Step 2 — Upload cover image → get thumb_media_id

```bash
THUMB_ID=$(python3 scripts/upload_thumb.py cover.jpg)
```

### Step 3 — Upload body images → build image map

For each body image referenced in the article:
```bash
WX_URL=$(python3 scripts/upload_img.py images/fig1.png)
```

Build a JSON map of local filenames to WeChat CDN URLs:
```json
{"fig1.png": "http://mmbiz.qpic.cn/...", "fig2.jpg": "http://..."}
```

Save as `/tmp/image_map.json`.

Skip this step if the article has no inline images.

### Step 4 — Convert Markdown to HTML

```bash
# Without images:
python3 scripts/md_to_html.py article.md > /tmp/article.html

# With image map:
python3 scripts/md_to_html.py article.md --image-map /tmp/image_map.json > /tmp/article.html
```

### Step 5 — Upload draft

```bash
python3 scripts/upload_draft.py \
  --title "文章标题" \
  --html /tmp/article.html \
  --thumb-media-id "$THUMB_ID" \
  --author "作者名" \
  --digest "文章摘要"
```

Output: `media_id` of the created draft.

The draft appears in the WeChat MP backend at: https://mp.weixin.qq.com → 草稿箱

### Step 6 — Confirm

Tell the user:
- ✅ Draft uploaded successfully
- Draft media_id: `XXX`
- View in WeChat MP backend: https://mp.weixin.qq.com (草稿箱)

---

## Error Handling

| Error | Fix |
|-------|-----|
| `errcode: 40001` | Token expired → delete `.token_cache.json` and retry |
| `errcode: 48001` | Account lacks API permission (check subscription vs service account) |
| `errcode: 40007` | Invalid thumb_media_id → re-upload cover image |
| Cover upload fails | Image must be jpg/png, ≤1MB |

## Notes

- Access tokens are cached in `.token_cache.json` (auto-refreshed when expired)
- WeChat only accepts images hosted on WeChat CDN — always upload images first
- The draft is saved but NOT published; user must publish manually from MP backend or via `/cgi-bin/freepublish/submit`
- Subscription accounts (订阅号) may have limited publishing frequency (once per day/week)
