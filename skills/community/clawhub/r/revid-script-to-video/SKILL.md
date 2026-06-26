---
name: revid-script-to-video
description: Turn an already-written script into a video with voiceover, auto-cut stock visuals, and captions. Use when the user has the words and wants Revid to handle production.
metadata: {"openclaw":{"requires":{"config":["REVID_API_KEY"]}}}
---

# Script → video

The script-to-video workflow is the lowest-friction path: you bring the words,
Revid brings the visuals + voice + captions + edit.

## When to use this skill

- The user pastes a finished script (or generates one in-conversation).
- They want full creative control over the *words*.
- They are happy with stock visuals (otherwise see
  [`revid-script-with-custom-media`](../revid-script-with-custom-media/SKILL.md)).
- For an idea-to-video flow, use
  [`revid-prompt-to-video`](../revid-prompt-to-video/SKILL.md).

## Inputs

| Field | Required | Notes |
|---|---|---|
| `text` | yes | The script. Use line breaks for scene boundaries. |
| `aspectRatio` | no | Default `9:16` |
| `voiceId` | no | Pick to match the script tone |
| `targetDuration` | no | Auto-derived from script length if omitted |

## Step-by-step

1. Validate `text` is non-trivial (>30 words) and within practical limits
   (~1500 words for a 5-min video).
2. POST `/render`.
3. Poll `/status`.

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
  "source":   { "text": "{SCRIPT}" },
  "aspectRatio": "9:16",
  "voice":    { "enabled": true, "voiceId": "aria-en-us", "stability": 0.6, "speed": 1.0, "language": "en-US" },
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
    "summarizationPreference": "no-summarization",
    "soundEffects": true,
    "hasToGenerateCover": true
  },
  "render": { "resolution": "1080p", "frameRate": 30 }
}
```

`summarizationPreference: "no-summarization"` — the user wrote the script for a
reason. Don't paraphrase it.

## Examples

- [`examples/honey-script.json`](examples/honey-script.json)
- [`examples/run.sh`](examples/run.sh)

## Failure modes

| Symptom | Fix |
|---|---|
| Script too long → exceeds context | Either split into multiple `/render` calls (one per chapter) or set `summarizationPreference: "summarize"`. |
| Voice mispronounces brand names | Inline phonetic spelling in the script ("Revid (rev-id)"). |
| Visuals don't match niche topic | Pre-author a few key shots and switch to [`revid-script-with-custom-media`](../revid-script-with-custom-media/SKILL.md). |
| Music drowns the voice | Lower music duck — currently no direct knob; switch `music.enabled: false` and add ambient sound effects via `options.soundEffects: true`. |

## See also

- [`revid-script-with-custom-media`](../revid-script-with-custom-media/SKILL.md)
  for full visual control.
- [`revid-prompt-to-video`](../revid-prompt-to-video/SKILL.md) when you want
  Revid to write the script too.
- [`revid-tweet-to-talking-head`](../revid-tweet-to-talking-head/SKILL.md) for
  short scripts with an avatar.
