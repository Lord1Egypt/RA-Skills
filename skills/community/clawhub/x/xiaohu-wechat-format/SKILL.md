---
name: xiaohu-wechat-format
description: "Format Markdown or rough notes into WeChat Official Account compatible inline-style HTML, preview 33 themes, upload images, generate optional covers, and push articles to WeChat draft box. Use when the user asks for WeChat/微信公众号 formatting, theme previews, Markdown-to-WeChat HTML, draft publishing, cover generation, or importing a WeChat article for republishing preview. External writes such as pushing drafts or enabling comment auto-replies require explicit user confirmation."
metadata:
  version: "1.0.0"
  category: publishing
  tags: [wechat, official-account, markdown, html, themes, draft]
---

# Xiaohu WeChat Format

Turn Markdown into WeChat Official Account-ready HTML. Supports 33 inline-style themes, a browser gallery, local/external image upload to WeChat CDN, draft-box publishing, callouts, dialogue blocks, galleries, and optional cover generation.

## Safety rules

- Formatting and local previews are safe.
- Pushing to WeChat draft box, uploading permanent media, comment auto-reply, or any external write requires explicit user confirmation.
- Never print `app_secret`, access tokens, or AI API keys.
- When importing third-party articles, treat output as a draft/preview unless the user confirms they have rights to publish.

## Quick commands

Use the skill directory as `{skill}`.

```bash
# Format one article locally
uv run --with markdown python {skill}/scripts/format.py \
  --input article.md --theme newspaper --no-open

# Open visual gallery for theme selection
uv run --with markdown python {skill}/scripts/format.py \
  --input article.md --gallery

# Publish to WeChat draft box from Markdown
uv run --with markdown --with requests --with pillow python {skill}/scripts/publish.py \
  --input article.md --theme newspaper --cover cover.jpg

# Publish an already formatted output directory
uv run --with markdown --with requests --with pillow python {skill}/scripts/publish.py \
  --dir /tmp/wechat-format/article --cover cover.jpg
```

## Configuration

1. Copy `config.example.json` to `config.json`.
2. Fill `wechat.app_id`, `wechat.app_secret`, and optional `wechat.author`.
3. Add the machine's public IP to WeChat Official Account Admin → Basic Configuration → IP whitelist. Error `40164` means the IP is not whitelisted.
4. Keep `config.json` private. It is ignored by git and must not be published.

## Recommended workflow

1. Read or create the Markdown article.
2. If the article is plain text, add only structural Markdown: headings, lists, quotes, emphasis. Do not rewrite meaning unless asked.
3. Format with one theme or gallery.
4. For draft publishing, ensure there is a cover image. WeChat requires one.
5. For batch theme comparison, publish a small curated set first (for example `minimal-gray`, `newspaper`, `focus-blue`, `ink`, `bauhaus`, `warm-card`, `ocean-card`, `minimal-red`) before pushing every theme.
6. Title draft previews with the theme id, e.g. `Article Title - preview - newspaper`.

## Important: WeChat article image imports

Images fetched from `mp.weixin.qq.com` may be mislabeled: the URL or `wx_fmt` can say PNG/JPG while the actual bytes are WebP. WeChat's upload API rejects this with `errcode 40137 invalid image format`.

Before publishing imported articles:

- Detect real file type from bytes, not filename.
- Convert WebP or unsupported images to real JPEG.
- Update Markdown/HTML image paths after conversion.
- Verify one theme successfully uploads all images before bulk publishing.

`publish.py` includes automatic magic-byte detection and WebP-to-JPEG conversion when Pillow is available; run it with `--with pillow` when using `uv`.

## Markdown extensions

```markdown
:::dialogue[Interview]
Alice: Hello
Bob: Hi
:::

:::gallery[Screenshots]
![](img1.jpg)
![](img2.jpg)
![](img3.jpg)
:::

> [!important] Key insight
> Highlighted text.

> [!tip] Tip
> Useful note.
```

## Available scripts

- `scripts/format.py` — Markdown → WeChat-compatible inline HTML + preview/gallery.
- `scripts/publish.py` — upload article images, upload cover, push to draft box.
- `scripts/generate.py` — optional cover-image generation using compatible image APIs.
- `scripts/comment_reply.py` — optional comment auto-reply; use only with explicit confirmation.

## Theme inventory

Run:

```bash
find {skill}/themes -maxdepth 1 -name '*.json' -printf '%f\n' | sed 's/\.json$//' | sort
```

Common starting themes: `newspaper`, `minimal-gray`, `focus-blue`, `ink`, `bauhaus`, `warm-card`, `ocean-card`, `wechat-native`.
