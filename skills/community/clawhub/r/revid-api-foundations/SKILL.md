---
name: revid-api-foundations
description: Foundation knowledge for every Revid skill — auth, the single render endpoint, the workflow discriminator, polling, webhooks, and the response envelope. Load this once at session start; specific skills build on it.
metadata: {"openclaw":{"requires":{"config":["REVID_API_KEY"]}}}
---

# Revid API foundations

Everything every other skill in this library depends on. **Read this once.**

## When to use

Always — but transparently. Other skills assume the agent already knows:

- how to authenticate
- which endpoint to hit
- how to wait for the result
- the response envelope shape

## The shape of every Revid call

```
POST https://www.revid.ai/api/public/v3/render
Header:  key: $REVID_API_KEY
Body:    { "workflow": "<one-of-9>", "source": { … }, … }
   ↓
{ "success": 1, "pid": "p_…" }
   ↓
GET https://www.revid.ai/api/public/v3/status?pid=p_…
   ↓ (poll every 5–8 s)
{ "status": "ready", "videoUrl": "https://cdn.revid.ai/v/…mp4", … }
```

That's the entire contract. Skills only differ in the body of `POST /render`.

## Auth

```
key: $REVID_API_KEY
```

The header is literally named `key` (not `Authorization`). If unset, fail with a
clear message instead of calling the API.

## The 9 workflows

| Workflow | Use when input is… |
|---|---|
| `script-to-video` | Already-written script (text). |
| `prompt-to-video` | A one-liner idea — the API writes the script. |
| `article-to-video` | Any URL with text content (blog/product/news). |
| `avatar-to-video` | A script + an avatar image (talking-head). |
| `ad-generator` | A product description — AI writes ad hooks. |
| `music-to-video` | A music URL + visuals. |
| `motion-transfer` | A reference image animated with motion from a clip. |
| `caption-video` | An existing video that needs captions. |
| `static-background-video` | A voiceover over a fixed background. |

Pick the workflow that matches the *input shape*, not the *output you want*.
The same `script-to-video` workflow can produce a Reel, a YouTube short, or a
LinkedIn square — that's just `aspectRatio`.

## Source mapping

Each workflow expects one of these `source.*` fields:

| Workflow | Field |
|---|---|
| `script-to-video` | `source.text` |
| `prompt-to-video` | `source.prompt` (+ optional `source.stylePrompt`, `durationSeconds`) |
| `article-to-video` | `source.url` (+ optional `source.scrapingPrompt`) |
| `ad-generator` | `source.prompt` (the product description) |
| `avatar-to-video` | `source.text` (script) + top-level `avatar.url` |
| `music-to-video` / `caption-video` / `motion-transfer` | `source.url` |
| `static-background-video` | `source.text` + `media.backgroundVideo` |

If you put text in the wrong field, the call fails 422 with a schema error.

## Common knobs every skill should set

1. `aspectRatio` — pick from the consumer surface:
   - Reels / TikTok / Shorts → `9:16`
   - LinkedIn / Instagram feed → `1:1`
   - YouTube long-form → `16:9`

2. `voice.enabled` — `true` for narrated content; `false` for music-only or
   caption-only outputs.

3. `captions.enabled` — keep `true` by default. Most short-form watches happen
   on mute.

4. `music.enabled` — `true` for promo / ad / story content; `false` for
   talking-head where the avatar voice should breathe.

5. `render.resolution` — `1080p` is the right default. Use `720p` for cheap
   previews; `4k` only when downstream needs it.

6. `media.quality` / `media.videoModel` — start at `pro`. Bump to `ultra` /
   `veo3` / `sora2` only when the cost is justified. Mirror the `/render` body
   to `POST /api/public/v3/calculate-credits` first to get a price estimate
   without spending.

7. `webhookUrl` — pass it whenever the caller can receive webhooks. Saves polling
   entirely.

## Reading the response

Success:
```json
{ "success": 1, "pid": "p_…", "workflow": "…", "endpoint": "…", "docs": {…} }
```

Failure:
```json
{ "success": 0, "error": "human-readable string" }
```

Skills should always check `success === 1` and fail loudly otherwise.

## Polling

After `POST /render`, poll until `status === "ready"`:

```bash
PID="<pid-from-render>"
while :; do
  R=$(curl -fsSL "https://www.revid.ai/api/public/v3/status?pid=$PID" \
        -H "key: $REVID_API_KEY")
  S=$(echo "$R" | jq -r .status)
  case "$S" in
    ready)  echo "$R" | jq .; break ;;
    failed) echo "FAILED: $R"; exit 1 ;;
    *)      sleep 5 ;;
  esac
done
```

Recommended cadence: poll every 5 s; back off to 8 s once `progress > 30`.
In production prefer setting `webhookUrl` in the request body and skip polling
entirely.

## Failure modes

The two most common errors every skill must handle:

- **`scrape failed` / `403` from source URL** — the page is JS-only or blocks
  bots. Either pre-scrape it yourself and switch to `script-to-video`, or pass
  `source.scrapingPrompt` with the manual title + body.
- **`insufficient_credits`** — drop `media.quality` / `videoModel` / `resolution`
  and retry, or top up with `POST /api/public/v3/buy-credit-pack`.

## See also

- Full Revid Public API v3 spec: <https://documenter.getpostman.com/view/36975521/2sBXcGEfaB>
- The other Revid skills in this catalog apply this foundation to specific
  content types (article, product page, blog, tweet, PDF, etc.).
