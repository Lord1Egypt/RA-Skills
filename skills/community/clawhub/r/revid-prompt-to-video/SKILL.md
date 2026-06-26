---
name: revid-prompt-to-video
description: Turn a one-line idea into a full short video — Revid writes the script, picks visuals, and assembles the cut. Use when the user has a topic but no script.
metadata: {"openclaw":{"requires":{"config":["REVID_API_KEY"]}}}
---

# Idea prompt → video

The lowest-input skill. The user types one line ("Why honey never spoils") and
Revid handles everything: script, visuals, voice, music, cuts.

## When to use this skill

- Source is a topic, question, or one-line concept — *no script*.
- The user is OK letting the AI choose the angle and structure.
- For a known script, use [`revid-script-to-video`](../revid-script-to-video/SKILL.md).
- For an idea + brand voice, use
  [`revid-product-description-to-ad`](../revid-product-description-to-ad/SKILL.md).

## Inputs

| Field | Required | Notes |
|---|---|---|
| `prompt` | yes | The idea (one or two sentences) |
| `stylePrompt` | no | Optional tone notes |
| `durationSeconds` | no | Default 35 (s) |
| `aspectRatio` | no | Default `9:16` |

## Step-by-step

1. Validate `prompt` is non-empty.
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
  "workflow": "prompt-to-video",
  "source": {
    "prompt":          "{ONE_LINE_IDEA}",
    "stylePrompt":     "{OPTIONAL_TONE_NOTES}",
    "durationSeconds": 35
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
    "promptTargetDuration": 35,
    "summarizationPreference": "summarizeIfLong",
    "soundEffects": true,
    "hasToGenerateCover": true
  },
  "render": { "resolution": "1080p", "frameRate": 30 }
}
```

## Examples

- [`examples/honey-prompt.json`](examples/honey-prompt.json)
- [`examples/run.sh`](examples/run.sh)

## Failure modes

| Symptom | Fix |
|---|---|
| Script angle is generic ("Did you know…") | Add `stylePrompt` with a specific angle: `"Open with a contrarian claim. End with a question that invites comments."` |
| Off-niche visuals | Mention concrete subjects in the prompt: `"Why honey never spoils — show beehives, ancient Egyptian jars, microscope close-ups of crystallized honey."` |
| Too long / too short | Use `durationSeconds` AND `options.promptTargetDuration` together (some legacy paths only read one). |

## See also

- [`revid-script-to-video`](../revid-script-to-video/SKILL.md) when you have the words.
- [`revid-product-description-to-ad`](../revid-product-description-to-ad/SKILL.md)
  for ads.
