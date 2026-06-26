---
name: revid-script-with-custom-media
description: Render a video from a script using only the media assets the caller provides (no stock visuals). Use for branded content where every frame must be on-brand — product clips, brand b-roll, hand-shot footage.
metadata: {"openclaw":{"requires":{"config":["REVID_API_KEY"]}}}
---

# Script + your own media → branded video

For when the user has the script *and* the visuals. Revid only handles voice +
captions + assembly. No stock content is mixed in.

## When to use this skill

- The user has both a script and a set of clips/images they want used.
- Brand fidelity matters more than visual variety.
- For mixed (your media + stock to fill gaps), drop `media.useOnlyProvided` and
  use [`revid-script-to-video`](../revid-script-to-video/SKILL.md) with `media.provided`.

## Inputs

| Field | Required | Notes |
|---|---|---|
| `text` | yes | The script |
| `media.provided[]` | yes | At least 3 items recommended; URLs must be public |
| `aspectRatio` | no | Default `9:16` |
| `voiceId` | no | Default voice if omitted |

`MediaItem` shape:

```json
{ "url": "https://…", "type": "image" | "video" | "audio", "title": "optional", "noReencode": false }
```

Use `type: "image"` for stills (Revid will optionally pan/zoom them via
`media.turnImagesIntoVideos`). Use `type: "video"` for clips. Keep clip
duration roughly comparable to the script length.

## Step-by-step

1. Validate every `media.provided[].url` returns 200 and a video/image
   content-type.
2. Confirm enough assets for the script: rough rule = 1 asset per 8–10 s of
   script, minimum 3.
3. POST `/render` with `media.useOnlyProvided: true`.
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
  "workflow": "script-to-video",
  "source": {
    "text": "{SCRIPT}"
  },
  "aspectRatio": "9:16",
  "voice":    { "enabled": true, "voiceId": "aria-en-us", "stability": 0.6, "speed": 1.0 },
  "captions": { "enabled": true, "position": "middle", "autoCrop": true },
  "music":    { "enabled": true, "syncWith": "beats" },
  "media": {
    "type": "custom",
    "useOnlyProvided": true,
    "turnImagesIntoVideos": true,
    "mergeVideos": false,
    "animation": "soft",
    "provided": [
      { "url": "https://cdn.example.com/clip-1.mp4", "type": "video" },
      { "url": "https://cdn.example.com/clip-2.mp4", "type": "video" },
      { "url": "https://cdn.example.com/hero.jpg",   "type": "image" }
    ]
  },
  "options": {
    "summarizationPreference": "no-summarization",
    "useOnlyProvidedMedia": true,
    "soundEffects": false,
    "hasToGenerateCover": true
  },
  "render": { "resolution": "1080p", "frameRate": 30 }
}
```

Both `media.useOnlyProvided` and `options.useOnlyProvidedMedia` should be
`true` — they belong to slightly different paths in the legacy code and setting
both is the safest way to forbid stock fill.

## Examples

- [`examples/branded-script.json`](examples/branded-script.json)
- [`examples/run.sh`](examples/run.sh)

## Failure modes

| Symptom | Fix |
|---|---|
| Final video pads with stock anyway | One of the two flags wasn't honored. Make sure both `media.useOnlyProvided: true` AND `options.useOnlyProvidedMedia: true` are set. |
| Video too short / dead air | Not enough assets. Add more `provided` items or set `mergeVideos: true` to loop the existing clips. |
| Wrong asset on a particular line | Pre-order assets in the array roughly in narrative order — Revid uses array order as a hint. |
| Asset URL 403 / 404 | Make sure assets are public (signed URLs work as long as they don't expire mid-render). |

## See also

- [`revid-script-to-video`](../revid-script-to-video/SKILL.md) for stock visuals.
- [`revid-shopify-product-promo`](../revid-shopify-product-promo/SKILL.md) for
  the product-page variant.
