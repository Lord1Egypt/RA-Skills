---
name: wechat-sticker-publisher
description: Publish WeChat Official Account image-first sticker posts (图片消息 / 发贴图) into the draft box via the official API. Use when the user wants to create公众号“发贴图”草稿、图片消息草稿、image-first posts, poster-style posts, or a visual post that is primarily images with short supporting text instead of a long article. This skill uploads permanent image materials and creates `newspic` drafts only; final publication remains manual in the WeChat backend.
metadata:
  openclaw:
    emoji: "🖼️"
    category: publishing
  clawdbot:
    emoji: "🖼️"
    requires:
      bins: []
      env.optional: ["WECHAT_APP_ID", "WECHAT_APP_SECRET"]
---

# WeChat Sticker Publisher

Create **draft-only** WeChat Official Account sticker/image-message posts using the official API.

## Workflow

1. Use `scripts/publish_sticker.py`.
2. Provide one or more **absolute image paths**.
3. Provide a title and short text.
4. The script uploads permanent image materials.
5. The script creates a `newspic` draft in the WeChat draft box.
6. Do **not** auto-publish; final publish is manual in the WeChat backend.

## Rules

- Keep this skill limited to **draft creation**.
- Do not modify the existing daily article publishing workflow unless explicitly requested.
- Require absolute local image paths.
- Support up to 20 images; the first image becomes the cover image.
- Send JSON request bodies explicitly as **UTF-8** (`application/json; charset=utf-8`).
  - This is important: using a different request-body path can lead to garbled Chinese text.

## Credentials

The script reads credentials from environment variables:
- `WECHAT_APP_ID`
- `WECHAT_APP_SECRET`

It can also load a local `wechat.env` file placed in the skill root.
Use `wechat.env.example` as the starting template.

If packaging/publishing this skill publicly, do **not** include any real secrets or local credential files.

## Primary command

```bash
python3 scripts/publish_sticker.py \
  --image /abs/path/to/image.jpg \
  --title "标题 / Title" \
  --text "配文 / Caption"
```

## Multi-image example

```bash
python3 scripts/publish_sticker.py \
  --image /abs/1.jpg \
  --image /abs/2.jpg \
  --title "多图贴图测试" \
  --text "这是一个多图图片消息草稿。"
```

## Outputs

Each run writes a JSON record to `outputs/` containing:
- uploaded image material responses
- draft request body
- draft creation response

Use those files for debugging and verification.

## Files

- `scripts/publish_sticker.py` — main deterministic implementation
- `references/api-notes.md` — concise implementation notes and known behavior
- `README.md` — bilingual human-facing overview for repository/ClawHub readers
- `LICENSE` — MIT license

## When to read references

Read `references/api-notes.md` if you need:
- the exact API mapping (`add_material` + `draft/add`)
- encoding gotchas
- the distinction between `news` and `newspic`
