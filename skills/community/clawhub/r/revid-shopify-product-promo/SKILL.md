---
name: revid-shopify-product-promo
description: Turn a Shopify (or any e-commerce) product page URL into a 30–45 second 9:16 promo video ready for TikTok / Reels / Shorts. Use when the user shares a product link and wants a short ad/promo, not a long-form review.
metadata: {"openclaw":{"requires":{"config":["REVID_API_KEY"]}}}
---

# Shopify product → promo video

Take a product page URL and produce a vertical promo video that pulls the
product image(s), name, key features, and price.

## When to use this skill

- Input is a single product page URL from Shopify, WooCommerce, BigCommerce, or
  any storefront with crawlable HTML (most stores).
- Output goal is a **promo / ad / launch teaser**, 30–45 s, vertical (9:16).
- The user wants Revid to extract the product details automatically. If they
  hand you a script instead, use [`revid-script-to-video`](../revid-script-to-video/SKILL.md).
- For a generic ad written from a product description (no live URL), use
  [`revid-product-description-to-ad`](../revid-product-description-to-ad/SKILL.md).

## Inputs

| Field | Required | Notes |
|---|---|---|
| `url` | yes | Public product page URL |
| `aspectRatio` | no | Defaults to `9:16` |
| `targetDuration` | no | Defaults to 35 (s) |
| `voiceId` | no | Default voice if omitted |
| `webhookUrl` | no | Skip polling if you can receive webhooks |

## Step-by-step

1. **Validate the URL** — must start with `http(s)://`. Reject obvious
   non-product paths (`/cart`, `/blog`, `/collections/all`).
2. **Optional pre-flight** — fetch the URL once with `HEAD` to confirm it
   returns 200. If 4xx, ask the user to confirm the link.
3. **Build the payload** (see template). Defaults are tuned for product promo:
   high `density`, dynamic animation, captions ON, music ON.
4. **POST `/api/public/v3/render`** — capture the returned `pid`.
5. **Poll `/status?pid=…`** with the canonical loop (see Polling section
   below) or wait for the webhook.
6. **Return** `{ pid, status, videoUrl, thumbnailUrl, durationSeconds, creditsUsed }`.

## API call template

```http
POST /api/public/v3/render
Host: www.revid.ai
Content-Type: application/json
key: $REVID_API_KEY
```

```json
{
  "workflow": "article-to-video",
  "source": {
    "url": "{PRODUCT_URL}",
    "scrapingPrompt": "Extract the product name, hero image, 3 key features, and price. Ignore reviews, related products, footer, and navigation."
  },
  "aspectRatio": "9:16",
  "voice":    { "enabled": true, "stability": 0.55, "speed": 1.05, "language": "en-US" },
  "captions": { "enabled": true, "position": "middle", "autoCrop": true },
  "music":    { "enabled": true, "syncWith": "beats", "trackName": "uplifting-pop" },
  "media": {
    "type": "stock-video",
    "density": "high",
    "animation": "dynamic",
    "quality": "pro",
    "imageModel": "good",
    "videoModel": "pro",
    "turnImagesIntoVideos": true,
    "applyStyleTransfer": false
  },
  "options": {
    "targetDuration": 35,
    "summarizationPreference": "summarize",
    "hasToGenerateCover": true,
    "coverTextType": "product-name",
    "soundEffects": true,
    "addStickers": false
  },
  "render": { "resolution": "1080p", "frameRate": 30 }
}
```

`scrapingPrompt` is the most important knob — it stops Revid from picking up
header/footer junk. Customize it per storefront if you find a recurring noise
pattern.

## Examples

- [`examples/shopify-aeropods.json`](examples/shopify-aeropods.json) — payload.
- [`examples/run.sh`](examples/run.sh) — end-to-end curl.

### Quick test

```bash
URL="https://your-shop.myshopify.com/products/your-product"

curl -s https://www.revid.ai/api/public/v3/render \
  -H "Content-Type: application/json" \
  -H "key: $REVID_API_KEY" \
  -d "$(jq --arg url "$URL" '.source.url=$url' \
        examples/shopify-aeropods.json)"
```

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

In production prefer setting `webhookUrl` in the request body and skip polling.

## Failure modes

| Symptom | Fix |
|---|---|
| `scrape failed` / 403 from the URL | Storefront blocks bots. Open the page in a real browser, copy the title + 3 bullet features + price into a script, and switch to [`revid-script-to-video`](../revid-script-to-video/SKILL.md). |
| Video shows wrong product image | Storefront serves SSR via JS only. Pass `media.useOnlyProvided: true` and `media.provided: [{ url: "<hero-image-url>", type: "image" }]` to force the right asset. |
| Voice sounds robotic | Increase `voice.stability` to `0.7` and pick a specific `voice.voiceId`. Default voice varies. |
| Duration overshoots target | Set `options.summarizationPreference: "summarize"` (already in the template) and lower `targetDuration`. |
| Captions cover product | `captions.position: "top"` (or `"bottom"`). |

## See also

- [`revid-product-description-to-ad`](../revid-product-description-to-ad/SKILL.md)
  if you don't have a live URL.
- [`revid-script-with-custom-media`](../revid-script-with-custom-media/SKILL.md)
  if you want to control every visual.
- [`revid-api-foundations`](../revid-api-foundations/SKILL.md) for the contract.
