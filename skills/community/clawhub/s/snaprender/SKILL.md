---
name: snaprender
description: "Screenshot any web page as an image (desktop or phone, cookie pop-ups blocked) or read it as markdown, with the SnapRender API. Use when the user wants to see, capture, compare or check how a website looks, or read a page."
homepage: https://snap-render.com/ai-agents
metadata: {"openclaw": {"emoji": "📸", "primaryEnv": "SNAPRENDER_API_KEY", "requires": {"bins": ["curl", "jq"], "env": ["SNAPRENDER_API_KEY"]}}}
---

# SnapRender: see any web page

Real Chrome screenshots of any URL, saved as an image file you can look at and send to the user. Cookie consent pop-ups and ads are blocked by default. It also reads pages as clean markdown.

## Setup (once)

1. Get a free key (200 captures a month, no card): https://snap-render.com/auth/signup
2. Put it in `~/.openclaw/openclaw.json`:
   ```json5
   { skills: { entries: { snaprender: { apiKey: "sk_live_..." } } } }
   ```
   OpenClaw then sets `$SNAPRENDER_API_KEY` for every run. If your agent runs commands in a sandbox, also set `SNAPRENDER_API_KEY` in the sandbox environment (skill keys are not passed into sandboxes).

## Capture a page

Use the `exec` tool with `curl`, not the `browser` tool: one request, no browser to drive, and the result is a ready image file.

Replace `TARGET_URL` and keep everything else as is:

```bash
mkdir -p snaprender && OUT="$PWD/snaprender/shot-$(date +%Y%m%d-%H%M%S)-$$.jpg"
code=$(jq -n --arg url 'TARGET_URL' \
  '{url: $url, format: "jpeg", quality: 80, block_ads: true, block_cookie_banners: true}' \
| curl -sS -X POST "https://app.snap-render.com/v1/screenshot" \
  -H "X-API-Key: $SNAPRENDER_API_KEY" -H "Content-Type: application/json" \
  -d @- -o "$OUT" -w '%{http_code}')
if [ "$code" = 200 ]; then echo "saved $OUT ($(wc -c < "$OUT" | tr -d " ") bytes)"; else echo "error $code: $(cat "$OUT")"; rm -f "$OUT"; fi
```

Then:
- **Send it to the user** with the `message` tool, giving the printed path as the media file. Never paste image data into the chat.
- **Look at it yourself** with `view_image` and the same path when the user asks what the page shows, whether it looks broken, or to compare pages.

Rules:
- Build the JSON with `jq --arg` as above. Never put user input straight into the shell string or the JSON.
- Use `$SNAPRENDER_API_KEY` exactly as written. Never print or echo the key.
- Each capture gets its own file (named by time), so comparisons never overwrite each other.

## Options

Add fields to the `jq` object, for example `{url: $url, device: "iphone_15_pro", dark_mode: true, ...}`.

| Field | Values | Default |
|---|---|---|
| `device` | `iphone_14`, `iphone_15_pro`, `pixel_7`, `ipad_pro`, `macbook_pro` | desktop 1280x800 |
| `full_page` | `true` captures the whole scrollable page | `false` |
| `lazy_load` | `true` with `full_page`: scrolls the page first so lazy-loaded images below the first screen appear (a few seconds slower) | `false` |
| `dark_mode` | `true` | `false` |
| `width`, `height` | 320-3840, 200-10000 | 1280, 800 |
| `format` | `jpeg`, `png`, `webp`, `pdf` (match the file extension) | `jpeg` |
| `quality` | 1-100 (jpeg, webp) | 80 here |
| `delay` | ms to wait after load, up to 10000 (slow or animated pages) | 0 |
| `hide_selectors` | CSS selectors to hide, comma separated | none |
| `click_selector` | CSS selector to click before the capture | none |
| `block_ads`, `block_cookie_banners` | `false` to keep them | `true` |
| `cache` | `true` reuses a recent identical capture, free of charge | `false` |

Common requests:
- "on my phone" or "mobile": `device: "iphone_15_pro"`
- "the whole page": `full_page: true` (add `lazy_load: true` if images further down come out blank)
- "desktop vs mobile": run the command twice, once with a `device`, and send both files
- "as a PDF": `format: "pdf"`, and name the file `.pdf`

## Read a page as markdown

For "what does this page say", summaries or quotes. Lighter on context than an image.

```bash
jq -n --arg url 'TARGET_URL' '{url: $url, type: "markdown", max_length: 20000}' \
| curl -sS -X POST "https://app.snap-render.com/v1/extract" \
  -H "X-API-Key: $SNAPRENDER_API_KEY" -H "Content-Type: application/json" -d @- \
| jq -r 'if .content then .content else . end'
```

`type` can also be `text`, `article` (title, author, text), `links` (every link on the page) or `metadata` (title, description, social tags). Add `selector: "main"` to read one part of the page.

## Watch a page for changes

SnapRender can capture a page on a schedule and compare each capture with the previous one, so nothing has to keep running on your side:

```bash
jq -n --arg url 'TARGET_URL' '{url: $url, interval: "daily", change_threshold: 0.5}' \
| curl -sS -X POST "https://app.snap-render.com/v1/schedules" \
  -H "X-API-Key: $SNAPRENDER_API_KEY" -H "Content-Type: application/json" -d @- | jq .
```

- `interval`: `hourly`, `daily` or `weekly` (the free plan has daily and weekly, for one page).
- `change_threshold`: percent of the page that must change to count as a change (0.5 is a good default).
- `notify_email: true` emails the account owner when the page changes (Business and Scale plans; on other plans leave it out and check the captures or use webhooks).
- Later, `GET /v1/schedules` lists them and `GET /v1/schedules/ID/captures` shows each capture with the percent changed.

## Credits left

```bash
curl -sS "https://app.snap-render.com/v1/usage" -H "X-API-Key: $SNAPRENDER_API_KEY" | jq '{plan, usage}'
```

## Errors and odd results

| What you see | Meaning | What to do |
|---|---|---|
| `error 401` | Key missing or wrong | Check `skills.entries.snaprender.apiKey`, or the sandbox environment |
| `error 429` | Monthly quota or per-minute limit reached | Wait a minute, or upgrade at https://snap-render.com/pricing |
| `error 400` | Bad URL or option | Read the message and fix that field |
| The image shows a "verify you are human" or security check page | The site's firewall (often Cloudflare) blocks automated visits | Tell the user. If it is their own site, they can let SnapRender in: https://snap-render.com/docs/allow-snaprender |
| Blank or half-loaded image | Slow page | Retry with `delay: 3000` |

Docs: https://snap-render.com/docs. Pricing: https://snap-render.com/pricing
