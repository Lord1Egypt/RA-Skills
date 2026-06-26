---
name: revid-blog-to-avatar-video
description: Turn a blog post URL into a talking-head avatar video — the avatar reads a summarized script of the post against a clean background. Use when the user wants a personal/expert delivery vs an edited promo.
metadata: {"openclaw":{"requires":{"config":["REVID_API_KEY"]}}}
---

# Blog post → talking-head avatar video

Take any blog/article URL and produce a vertical (or square) talking-head video
with a chosen avatar reading a summarized version of the post.

## When to use this skill

- Source is a blog post / opinion piece / explainer with substantial body text.
- Output should feel like a *person delivering the take*, not an edited promo
  with stock b-roll.
- An avatar (image URL or `characterId`) is available, or the user accepts the
  default avatar.
- For an edited short with stock visuals, use
  [`revid-article-to-short`](../revid-article-to-short/SKILL.md) instead.

## Inputs

| Field | Required | Notes |
|---|---|---|
| `url` | yes | Blog post URL |
| `avatar.url` *or* `characterIds[]` | yes | The face. Either an image URL or a saved consistent character ID (see [character mgmt](#consistent-characters)). |
| `aspectRatio` | no | Default `9:16`. Use `1:1` for LinkedIn. |
| `voiceId` | no | Match it to the avatar's tone if known. |
| `targetDuration` | no | Default 60 (s) — talking heads can run longer. |

## Step-by-step

1. Validate the URL.
2. If the user gave an avatar image URL, set `avatar.url`. If they gave a saved
   character ID, set `characterIds: [id]` (and leave `avatar` omitted).
3. POST the payload below.
4. Poll `/status` (canonical loop in the Polling section below).
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
  "workflow": "article-to-video",
  "source": {
    "url": "{BLOG_URL}",
    "scrapingPrompt": "Extract the article body. Skip header, navigation, related posts, and footer."
  },
  "aspectRatio": "9:16",
  "avatar": {
    "enabled": true,
    "url": "{AVATAR_IMAGE_URL}",
    "removeBackground": true,
    "imageModel": "good"
  },
  "voice": {
    "enabled": true,
    "voiceId": "aria-en-us",
    "stability": 0.65,
    "speed": 1.0,
    "language": "en-US",
    "enhanceAudio": true
  },
  "captions": { "enabled": true, "position": "bottom", "autoCrop": true },
  "music":    { "enabled": false },
  "media": {
    "type": "moving-image",
    "density": "low",
    "animation": "soft",
    "placeAvatarInContext": true
  },
  "options": {
    "targetDuration": 60,
    "summarizationPreference": "summarize",
    "hasToGenerateCover": true
  },
  "render": { "resolution": "1080p", "frameRate": 30 }
}
```

Notes:

- `placeAvatarInContext: true` composites the avatar over a relevant background
  (vs a plain green-screen feel).
- `media.density: "low"` keeps cuts minimal so the talking head can carry the
  video.
- `music.enabled: false` is the default — voice-driven content reads better
  without competing audio.

## Consistent characters

If the user wants the **same face** across many posts, create a character once
and reuse the ID:

```bash
# 1. Create character
curl -s https://www.revid.ai/api/public/v3/consistent-characters \
  -H "Content-Type: application/json" \
  -H "key: $REVID_API_KEY" \
  -d '{ "name": "Maya", "imageUrl": "https://cdn.example.com/maya.jpg" }'
# → { "id": "ch_…" }

# 2. Use it in renders
{ "characterIds": ["ch_…"], "avatar": { "enabled": true } }
```

List existing characters with `GET /api/public/v3/consistent-characters`.

## Examples

- [`examples/blog-to-avatar.json`](examples/blog-to-avatar.json) — payload.
- [`examples/run.sh`](examples/run.sh) — end-to-end curl flow.

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
| Avatar lip-sync drifts on long copy | Lower `targetDuration` to 45 s, or switch `summarizationPreference: "summarize"` (already on). |
| Avatar background bleeds into video | Set `avatar.removeBackground: true` (default). For stubborn cases, pre-process the avatar image to a transparent PNG. |
| Background visuals distract from face | `media.density: "low"` and `media.animation: "soft"` (already on). For pure plain background, set `media.type: "custom"` + `media.useOnlyProvided: true` with a single neutral asset. |
| Voice doesn't match the avatar | Set `voice.voiceId` explicitly. The default voice is gendered female English — always override for other languages or personas. |
| `scrape failed` | Same as in [`revid-article-to-short`](../revid-article-to-short/SKILL.md): pre-scrape the post and switch to `script-to-video` with the avatar block intact. |

## See also

- [`revid-article-to-short`](../revid-article-to-short/SKILL.md) — same input,
  edited-short output.
- [`revid-tweet-to-talking-head`](../revid-tweet-to-talking-head/SKILL.md) —
  shorter form of the same talking-head pattern.
- [`revid-api-foundations`](../revid-api-foundations/SKILL.md).
