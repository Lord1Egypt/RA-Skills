---
name: revid-pdf-to-video
description: Turn a PDF (whitepaper, ebook chapter, slide deck export, research paper) into a short summary video. Use when the source is a PDF URL or a PDF the agent can upload to public storage first.
metadata: {"openclaw":{"requires":{"config":["REVID_API_KEY"]}}}
---

# PDF → summary video

Take a PDF URL and produce a short summary video. Internally this routes
through `article-to-video` once the PDF text has been extracted by Revid's
scraper.

## When to use this skill

- Source is a public PDF URL (whitepaper, paper, ebook, slide export).
- Goal is a 30–90 s summary, not a full reading.
- For HTML articles use [`revid-article-to-short`](../revid-article-to-short/SKILL.md).
- For local PDFs the agent must first upload to public storage (S3, Supabase
  Storage, etc.) so Revid can fetch it.

## Inputs

| Field | Required | Notes |
|---|---|---|
| `url` | yes | Public PDF URL (must be reachable, no auth) |
| `aspectRatio` | no | Default `9:16` |
| `targetDuration` | no | Default 60 (s); raise to 90 s for dense papers |

## Step-by-step

1. Confirm the URL ends in `.pdf` or returns `Content-Type: application/pdf`.
2. Set `source.scrapingPrompt` to bias the summary toward what the user cares
   about ("Focus on the methodology section", "Focus on the executive summary",
   "Pull the 3 biggest takeaways").
3. POST `/render` with the payload below.
4. Poll `/status`.

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
    "url": "{PDF_URL}",
    "scrapingPrompt": "Extract the executive summary and the 3 biggest takeaways. Skip references and appendices."
  },
  "aspectRatio": "9:16",
  "voice":    { "enabled": true, "stability": 0.65, "speed": 0.95, "language": "en-US" },
  "captions": { "enabled": true, "position": "middle", "autoCrop": true },
  "music":    { "enabled": true, "syncWith": "beats" },
  "media": {
    "type": "stock-video",
    "density": "medium",
    "animation": "soft",
    "quality": "pro",
    "imageModel": "good",
    "videoModel": "pro"
  },
  "options": {
    "targetDuration": 60,
    "summarizationPreference": "summarize",
    "soundEffects": true,
    "hasToGenerateCover": true,
    "coverTextType": "title"
  },
  "render": { "resolution": "1080p", "frameRate": 30 }
}
```

## Examples

- [`examples/whitepaper.json`](examples/whitepaper.json)
- [`examples/run.sh`](examples/run.sh)

## Failure modes

| Symptom | Fix |
|---|---|
| `scrape failed` | PDF behind auth or login wall. Re-host the PDF on public storage. |
| Summary skips the section the user cares about | Tighten `scrapingPrompt` (be specific: section names, page ranges). |
| Visuals are abstract / off-topic | PDFs rarely have crawlable hero images. Pre-render a few key figures as images and pass them in `media.provided`. |
| Voice rushes through technical terms | Lower `voice.speed` to `0.9`. |

## See also

- [`revid-article-to-short`](../revid-article-to-short/SKILL.md) for HTML.
- [`revid-script-with-custom-media`](../revid-script-with-custom-media/SKILL.md)
  for full visual control.
