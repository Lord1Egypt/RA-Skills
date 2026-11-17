# IM attachments and `resolve-input`

How to turn chat media into a **local path** or URL for `vmake_ai.py run-task --input …`.

## Attachment reuse and authorization boundary

- An image or video already attached to the conversation is the current input. Keep and reuse its attachment reference, URL, file ID, or resolved local path; do not ask the user to upload it again or repeat its media type when those details are available.
- Resolving an existing attachment to a local path is preparation. The external Vmake upload, quota consumption, and task submission begin with the authorized `run-task` flow.
- Once the user authorizes uploading the current media and using the Vmake account quota, continue automatically through `resolve-input` when needed and then `run-task` or `spawn-run-task`. Do not request a second authorization at the worker boundary.
- If the host cannot access the attachment bytes or reference, explain that specific limitation and ask for a new direct upload. Do not describe a received chat attachment as missing merely because it has not yet been sent to Vmake.

## Platform cheat sheet

| Platform | Typical source | Easiest path |
|----------|----------------|--------------|
| **Discord** | `attachments[0].url` | Often a public URL → pass directly to `--input`, or `resolve-input --url` |
| **Generic URL** | User paste | `--input "<url>"` or `resolve-input --url` |
| **Local file** | Host downloaded attachment | `--input /path/to/file` or `resolve-input --file` (copies to a unique name under `--output-dir`) |
| **Telegram** | `message.photo[-1].file_id` or video `file_id` | `resolve-input --telegram-file-id "…"` (**requires `TELEGRAM_BOT_TOKEN`**) |
| **Feishu** | `image_key` + `message_id` in content | `resolve-input --feishu-image-key … --feishu-message-id …` (**requires `FEISHU_APP_TOKEN`**) |

## Feishu: video file vs preview `image_key`

Video cards often include **two** resources: a **preview/cover** (reachable via `image_key`) and the **real video** (separate URL or file id in your host’s message model). For **video** tasks (`videoscreenclear`, `hdvideoallinone`), resolve and pass **only the video** as `--input`.

**Do not** also run an **image** task on the preview (`eraser_watermark` or `image_restoration`) unless the user explicitly wants that still frame processed—otherwise you pay for **two** Vmake jobs (image + video) for a single “fix this video” request (watermark removal or quality restoration).

After a video task completes, [feishu-send-video.md](feishu-send-video.md) may **upload a cover to Feishu** for native video messages; that uses Feishu’s image upload API, **not** Vmake `image_restoration` or `eraser_watermark`.

## `resolve-input` CLI

Writes a file under **`--output-dir`** (default `/tmp`) and prints JSON: `path`, `filename`, `bytes`.

```bash
# Local path (e.g. host saved an attachment)
python3 {baseDir}/scripts/vmake_ai.py resolve-input \
  --file /tmp/user_upload.jpg \
  --output-dir /tmp

# Public URL (download first — useful if Vmake cannot fetch the URL)
python3 {baseDir}/scripts/vmake_ai.py resolve-input \
  --url "https://cdn.example.com/clip.mp4" \
  --output-dir /tmp
```

**Telegram** — token **only** via environment (never CLI):

```bash
TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" python3 {baseDir}/scripts/vmake_ai.py resolve-input \
  --telegram-file-id "AgACAgIAAxk..." \
  --output-dir /tmp
```

**Feishu** — tenant token from your Feishu app (same as other IM resource downloads):

```bash
FEISHU_APP_TOKEN="$FEISHU_APP_TOKEN" python3 {baseDir}/scripts/vmake_ai.py resolve-input \
  --feishu-message-id "om_xxx" \
  --feishu-image-key "img_v3_xxx" \
  --output-dir /tmp
```

Optional: **`--feishu-app-token`** instead of env.

## Limits

Max download/copy size: **100 MB** (same guard as similar skills). For larger assets, use a direct URL if Vmake can fetch it, or another upload path your tenant supports.

## Then run Vmake

Use the printed **`path`** as **`--input`**:

```bash
python3 {baseDir}/scripts/vmake_ai.py run-task \
  --task eraser_watermark \
  --input "/tmp/vmake_in_xxxxxxxxxx_user_upload.jpg"
```

Replace `{baseDir}` with the skill root (the parent of `scripts/`).
