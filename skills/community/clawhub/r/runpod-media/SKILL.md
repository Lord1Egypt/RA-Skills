---
name: runpod-media
description: Generate images from text, edit images with text instructions, animate images to video, and generate video from text — all via RunPod public AI endpoints. Use when the user asks to generate/create/make an image or video, edit a photo, animate an image, or produce AI media. Requires a RunPod API key.
---

# RunPod Media Skill

Generate AI images and videos using RunPod public endpoints. All output is saved to `~/runpod-media/`.

## API Keys

One key required — add to `~/.openclaw/secrets.json`:

| Key path | Purpose | Get it from |
|----------|---------|-------------|
| `/runpod/apiKey` | Call RunPod endpoints | [runpod.io/console/user/settings](https://www.runpod.io/console/user/settings) |

Local images are uploaded to **Cloudflare R2** as presigned URLs (1 min expiry) before being sent to RunPod endpoints. R2 credentials are read from `/cloudflare/r2` in secrets.json — already configured ✅

> imgbb is no longer used. R2 presigned URLs replace it for all local file uploads.

**R2 cleanup:** Objects in `uploads/` are auto-deleted after **1 day** via a lifecycle rule on the `openclaw` bucket. Presigned URLs expire after 1 min (no access), objects are cleaned up within 24h.

Keys are resolved in this order:
1. **OpenClaw secrets.json** — `~/.openclaw/secrets.json` ✅ (already configured)
2. **Env vars** — `RUNPOD_API_KEY`

## How Users Ask (Natural Language Examples)

The user will never type CLI commands — translate their natural requests into the right script call.

**Generate an image:**
- "Generate an image of a samurai cat in neon Tokyo" → `generate_image --prompt "..."`
- "Make me a 16:9 image of a stormy ocean at sunset" → `generate_image --prompt "..." --aspect-ratio 16:9`
- "Create an image using Nano Banana — a futuristic city" → `call_endpoint --endpoint google-nano-banana-2-edit --prompt "..."`

**Edit an image:**
- "Edit this image — add snow falling" → `edit_image --images <file> --prompt "add snow falling"`
- "Use Qwen to edit this photo, make it look like a painting" → `call_endpoint --endpoint qwen-image-edit --image <file> --prompt "make it look like a painting"`

**Animate to video:**
- "Animate this image — slow camera pan" → `image_to_video --image <file> --prompt "slow camera pan"`
- "Make a video from this with Kling" → `image_to_video --image <file> --model kling --prompt "..."`
- "Turn this into a 10 second clip with Sora 2" → `call_endpoint --endpoint sora-2-pro-i2v --image <file> --prompt "..." --duration 10`

**Text to video:**
- "Generate a video of a wolf howling at the moon" → `text_to_video --prompt "..."`

**List available models:**
- "What image/video models do you have?"
- "List the available endpoints"
- "Show me what RunPod models are available"
→ Run `list_endpoints` and summarize the output in plain language for the user

**Add a new endpoint:**
- "Add this RunPod endpoint: https://console.runpod.io/hub/playground/voice/kokoro-tts"
- "Probe and add these endpoints: kokoro-tts, flux-kontext-pro"
→ Run `discover_endpoints add --candidates "<url-or-id>"`

---

## Capabilities & Cost

| Task | Command | Cost | Time |
|------|---------|------|------|
| Text → Image | `generate_image` | ~$0.005/image | 3–8s |
| Edit image(s) | `edit_image` | ~$0.005/image | 5–15s |
| Image → Video | `image_to_video` | $0.03–$0.90/clip | 30–120s |
| Text → Video | `text_to_video` | $0.04–$1.22/clip | 30–120s |
| **Any endpoint** | `call_endpoint` | varies | varies |

The built-in commands use default endpoints. For **more models** (Nano Banana Pro, FLUX, Sora 2, Kling, TTS, etc.) use `call_endpoint` with any RunPod public endpoint ID.

## Endpoint Registry

All known public endpoints are in `scripts/endpoints.json`. List them:

```bash
$SKILL_DIR/run.sh list_endpoints
```

### Call Any Endpoint

```bash
$SKILL_DIR/run.sh call_endpoint \
  --endpoint <ENDPOINT_ID> \
  [--prompt "TEXT"] \
  [--image PATH_OR_URL] \
  [--audio PATH_OR_URL] \
  [--duration 5] \
  [--aspect-ratio 16:9] \
  [--input '{"key": "value"}']   # full JSON override
```

**Examples:**

```bash
# Nano Banana Pro image generation
$SKILL_DIR/run.sh call_endpoint --endpoint nano-banana-pro --prompt "a golden retriever in space"

# Nano Banana Pro image editing
$SKILL_DIR/run.sh call_endpoint --endpoint nano-banana-pro --prompt "make it nighttime" --image photo.jpg

# Sora 2 Pro video from image
$SKILL_DIR/run.sh call_endpoint --endpoint sora-2-pro-i2v --image photo.jpg --prompt "camera slowly pulls back" --duration 5

# Kokoro TTS
$SKILL_DIR/run.sh call_endpoint --endpoint kokoro-tts --text "Hello world"

# FLUX Schnell
$SKILL_DIR/run.sh call_endpoint --endpoint flux-schnell --prompt "cyberpunk city" --input '{"width":1024,"height":1024}'
```

### Adding New Endpoints

When the user asks to use an endpoint not in the registry, or the `runpod` skill reveals a new one:
1. Call it directly with `--endpoint <id>` — no registry entry needed
2. Optionally add it to `scripts/endpoints.json` for future sessions

**With `runpod` skill:** Use the `runpod` skill to browse/discover endpoint IDs on the RunPod hub, then pass that ID to `call_endpoint` here.



### Generate Image

```bash
$SKILL_DIR/run.sh generate_image \
  --prompt "PROMPT" \
  [--aspect-ratio 1:1|16:9|9:16|4:3|3:4] \
  [--seed 42]
```

### Edit Image

```bash
$SKILL_DIR/run.sh edit_image \
  --images PATH_OR_URL [PATH_OR_URL ...] \
  --prompt "EDIT INSTRUCTION" \
  [--aspect-ratio 1:1] \
  [--seed 42]
```

- Accepts 1–5 images (local paths or URLs)
- Local files are auto-uploaded via imgbb (requires `/imgbb/apiKey` in secrets.json)

### Animate Image → Video

```bash
$SKILL_DIR/run.sh image_to_video \
  --image PATH_OR_URL \
  --prompt "MOTION DESCRIPTION" \
  [--model wan25|kling|seedance] \
  [--duration 5|10] \
  [--negative-prompt "TEXT"]
```

**Models:**
- `wan25` (default) — WAN 2.5, ~$0.026/5s
- `kling` — Kling v2.1 Pro, $0.45/5s (highest quality)
- `seedance` — Seedance 1.0 Pro, ~$0.12/5s

### Generate Video from Text

```bash
$SKILL_DIR/run.sh text_to_video \
  --prompt "VIDEO DESCRIPTION" \
  [--model wan26|seedance] \
  [--duration 5|10|15] \
  [--size 1920x1080] \
  [--negative-prompt "TEXT"]
```

**Models:**
- `wan26` (default) — WAN 2.6, ~$0.04/5s
- `seedance` — Seedance 1.0 Pro, ~$0.12/5s

## Defaults

- **Delete after send** — always delete the local file after successful delivery. Only keep if the user explicitly asks ("keep it", "save it", "--keep").
- **Captions** — keep them short and natural. Do NOT include render time or cost unless the user asks. Example: `🦊 Fox under the aurora` not `🦊 Fox — 105s render (~$0.026)`.

## Delivering Media to the User

After generating an image or video, **always deliver it** to the user via their active channel.

### The Problem
The `message` tool with a local `media` path may fail in sandboxed agent modes due to SecretRef resolution not being available for media sends. This is a known OpenClaw limitation.

### The Solution: Use curl + Telegram Bot API directly

Read the bot token from secrets and send via curl — this always works regardless of sandbox mode:

```bash
TOKEN=$(cat ~/.openclaw/secrets.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('telegram',{}).get('botToken',''))")

# Send photo
curl -s \
  -F "chat_id=CHAT_ID" \
  -F "photo=@$HOME/.openclaw/workspace/runpod-media/OUTPUT_FILE.jpg" \
  -F "caption=YOUR CAPTION" \
  "https://api.telegram.org/bot${TOKEN}/sendPhoto"

# Send video (.mp4)
curl -s \
  -F "chat_id=CHAT_ID" \
  -F "video=@$HOME/.openclaw/workspace/runpod-media/OUTPUT_FILE.mp4" \
  -F "caption=YOUR CAPTION" \
  "https://api.telegram.org/bot${TOKEN}/sendVideo"
```

**Where to find CHAT_ID:** Use the `chat_id` from the inbound message metadata (e.g. `telegram:1231438498` → use `1231438498`).

### Delivery Checklist
1. ✅ Generate the file (note the saved path from script output)
2. ✅ Send via `message` tool with a short, natural caption (no cost/time unless asked)
3. ✅ **Delete the local file** after successful send: `rm <path>`
4. ⏭️ Skip deletion only if user said "keep it" / "save it" / passed `--keep`

### Why not `message` tool?
Try it first — if it works, great. If it returns a SecretRef error, fall back to the curl method above.

## Notes

- Video generation takes **30–120 seconds** — inform the user to wait
- Output files saved to `~/.openclaw/workspace/runpod-media/` — accessible in **both sandboxed and elevated** agent modes
- Shared utilities in `scripts/_utils.py` — do not call directly
