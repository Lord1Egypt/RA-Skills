---
name: revid-product-description-to-ad
description: Turn a product description (free-form text — no URL needed) into a punchy 15–30 second AI-generated ad with hooks, CTA, and visuals. Use when the user pastes copy or specs but doesn't have a live page to scrape.
metadata: {"openclaw":{"requires":{"config":["REVID_API_KEY"]}}}
---

# Product description → AI ad

Take a paragraph (or bullet list) describing a product and produce a polished
short-form ad. The `ad-generator` workflow writes the hook + body + CTA itself
based on the description.

## When to use this skill

- The user pastes a product description, spec sheet, or feature list — *not* a
  URL.
- They want hook → benefit → CTA structure (a *commercial*).
- They have no avatar / talking-head requirement (use
  [`revid-blog-to-avatar-video`](../revid-blog-to-avatar-video/SKILL.md)
  for that).
- For a live URL, use
  [`revid-shopify-product-promo`](../revid-shopify-product-promo/SKILL.md).

## Inputs

| Field | Required | Notes |
|---|---|---|
| `prompt` | yes | The product description (the AI uses it as the brief) |
| `stylePrompt` | no | Optional brand voice notes (e.g. *"Apple-like, calm, premium"*) |
| `aspectRatio` | no | Default `9:16` |
| `targetDuration` | no | Default 22 (s) |
| `mediaItems` | no | If you have product images, pass them in `media.provided` |

## Step-by-step

1. Validate `prompt` has at least ~30 words (otherwise the ad is too thin).
2. Build the payload below; if product images were provided, slot them into
   `media.provided` and set `media.useOnlyProvided: false` (mix with stock).
3. POST `/render`.
4. Poll `/status`.
5. Return `videoUrl`.

## API call template

```http
POST /api/public/v3/render
Host: www.revid.ai
Content-Type: application/json
key: $REVID_API_KEY
```

```json
{
  "workflow": "ad-generator",
  "source": {
    "prompt":      "{PRODUCT_DESCRIPTION}",
    "stylePrompt": "{OPTIONAL_BRAND_VOICE_NOTES}",
    "durationSeconds": 22
  },
  "aspectRatio": "9:16",
  "voice":    { "enabled": true, "stability": 0.55, "speed": 1.05, "language": "en-US" },
  "captions": { "enabled": true, "position": "middle", "autoCrop": true },
  "music":    { "enabled": true, "syncWith": "beats", "trackName": "ad-energetic" },
  "media": {
    "type": "stock-video",
    "density": "high",
    "animation": "dynamic",
    "quality": "ultra",
    "imageModel": "ultra",
    "videoModel": "ultra",
    "turnImagesIntoVideos": true,
    "applyStyleTransfer": false,
    "provided": []
  },
  "options": {
    "targetDuration": 22,
    "promptTargetDuration": 22,
    "summarizationPreference": "summarizeIfLong",
    "soundEffects": true,
    "addStickers": true,
    "hasToGenerateCover": true,
    "coverTextType": "hook"
  },
  "render": { "resolution": "1080p", "frameRate": 30 }
}
```

`ad-generator` defaults to higher visual quality than article-to-video because
ads compete on the first second. If credits are tight drop `quality` to `pro`.

## Examples

- [`examples/aeropods-ad.json`](examples/aeropods-ad.json) — payload with brand
  notes.
- [`examples/run.sh`](examples/run.sh) — accepts description as a file or
  positional arg.

## Failure modes

| Symptom | Fix |
|---|---|
| Hook is generic | Make `prompt` specific. `"Wireless earbuds"` → meh. `"Wireless earbuds with adaptive ANC and 38h battery for $179"` → strong. |
| Ad reads like a feature list, not a hook | Add `stylePrompt: "Lead with a question or emotional hook. Save specs for the middle. End with the price + a single CTA."` |
| Visuals don't match the product | Pass real product images via `media.provided: [{ url, type: "image" }]`. The AI will weave them in. |
| Voice rushes | Lower `voice.speed` to `0.95`. |
| Too many on-screen stickers | `options.addStickers: false`. |

## See also

- [`revid-shopify-product-promo`](../revid-shopify-product-promo/SKILL.md) — same
  goal but starts from a URL.
- [`revid-script-with-custom-media`](../revid-script-with-custom-media/SKILL.md)
  — full creative control.
