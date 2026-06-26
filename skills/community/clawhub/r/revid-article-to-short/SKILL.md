---
name: revid-article-to-short
description: Turn any news article or long-form post URL into a 30–60 second 9:16 short with stock visuals, narration, and captions. Use when the user shares a link and wants an edited summary, not a talking-head.
metadata: {"openclaw":{"requires":{"config":["REVID_API_KEY"]}}}
---

# Article / news → short

Take any URL with a substantial article body and produce a vertical short with
voiceover + auto-cut stock b-roll + captions.

## When to use this skill

- Source is a news article, long-form blog, press release, or essay.
- Output goal: an **edited summary**, voiceover + visuals, 30–60 s.
- The user does NOT want a talking-head (use
  [`revid-blog-to-avatar-video`](../revid-blog-to-avatar-video/SKILL.md) for that).
- For e-commerce product pages prefer
  [`revid-shopify-product-promo`](../revid-shopify-product-promo/SKILL.md) — same
  workflow but tuned defaults.

## Inputs

| Field | Required | Notes |
|---|---|---|
| `url` | yes | Article URL |
| `aspectRatio` | no | Default `9:16` |
| `targetDuration` | no | Default 45 s |
| `language` | no | Auto-detected; override for non-English |

## Step-by-step

1. Validate the URL.
2. POST the payload below.
3. Poll `/status` (canonical loop in the Polling section below).
4. Return `videoUrl`.

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
    "url": "{ARTICLE_URL}",
    "scrapingPrompt": "Summarize the article body. Skip ads, related links, navigation, and footer."
  },
  "aspectRatio": "9:16",
  "voice":    { "enabled": true, "stability": 0.6, "speed": 1.0, "language": "en-US" },
  "captions": { "enabled": true, "position": "middle", "autoCrop": true },
  "music":    { "enabled": true, "syncWith": "beats" },
  "media": {
    "type": "stock-video",
    "density": "medium",
    "animation": "soft",
    "quality": "pro",
    "videoModel": "pro",
    "imageModel": "good"
  },
  "options": {
    "targetDuration": 45,
    "summarizationPreference": "summarize",
    "soundEffects": true,
    "hasToGenerateCover": true,
    "coverTextType": "headline"
  },
  "render": { "resolution": "1080p", "frameRate": 30 }
}
```

## Examples

- [`examples/article-techreview.json`](examples/article-techreview.json)
- [`examples/run.sh`](examples/run.sh)

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
| `scrape failed` | Pre-fetch the article body server-side and switch to [`revid-script-to-video`](../revid-script-to-video/SKILL.md) with the body in `source.text`. |
| Off-topic stock visuals | Pass a tighter `scrapingPrompt` (e.g. *"Focus on the financial markets angle, not the company history"*) and lower `media.density: "low"`. |
| Wrong language detected | Set `voice.language` and `options.language` explicitly. |
| Captions clip subjects | `captions.position: "top"`. |

## See also

- [`revid-shopify-product-promo`](../revid-shopify-product-promo/SKILL.md)
- [`revid-news-to-daily-short`](../revid-news-to-daily-short/SKILL.md) for
  *generating* news from a topic vs summarizing a known URL.
- [`revid-pdf-to-video`](../revid-pdf-to-video/SKILL.md) for PDFs instead of HTML.
