---
name: video-edit-runcomfy
displayName: "🫧 Video Edit — Pro Pack on RunComfy"
description: >
  Video edit on RunComfy. This video edit skill transforms an existing
  video clip — restyle, background swap, outfit swap, motion transfer,
  color grade, or any other video edit task — by routing the video edit
  request to the right model in the RunComfy catalog. Video edit
  supports talking-head video edit, product video edit, and short-form
  video edit at up to 1080p. Calls `runcomfy run <model>/edit-video`
  through the local RunComfy CLI. Triggers on "video edit", "edit
  video", "video editing", "video-edit", "restyle video", "swap video
  background", "video outfit swap", "video color grade", or any
  explicit ask to edit a video.
emoji: "🫧"
homepage: https://www.runcomfy.com
license: MIT
clawdis:
  requires:
    bins:
      - runcomfy
    env:
      - RUNCOMFY_TOKEN
    config:
      - ~/.config/runcomfy
---

# 🫧 Video Edit — Pro Pack on RunComfy

[runcomfy.com](https://www.runcomfy.com/?utm_source=clawhub&utm_medium=skill&utm_campaign=video-edit-runcomfy) · [docs](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=video-edit-runcomfy) · [Video edit models](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=video-edit-runcomfy)

**Video edit on RunComfy.** This skill is the canonical video edit entry point for the RunComfy Model API: give it a source video URL and an edit instruction, and it returns the edited video. Video edit on RunComfy means transforming an existing clip — restyle, background swap, outfit swap, motion transfer, color grade — without re-shooting.

## What "video edit" means here

Video edit is the task of taking a source video and producing a transformed video that preserves identity, motion, or framing where you want, while changing what you specify. Video edit is distinct from text-to-video (no input clip) and from image-to-video (input is a still). Common video edit operations include:

- **Restyle video edit** — change look, lighting, atmosphere while keeping the subject and motion.
- **Background video edit** — swap the background of a talking-head or product video while preserving foreground identity.
- **Outfit swap video edit** — change wardrobe on the subject while keeping face, pose, and motion stable.
- **Motion transfer video edit** — transfer motion from a reference clip onto a target character.
- **Color grade video edit** — apply cinematic color, film grain, or commercial polish to an existing clip.
- **Packaging swap video edit** — replace product packaging design using a reference image, preserving the camera motion.

This skill picks the right video edit endpoint for the user's intent and calls `runcomfy run <model>/<edit-endpoint>` with the matching schema.

## When to use video edit on RunComfy

Pick video edit on RunComfy whenever:

- You have an **existing video** and want to **change** something about it — video edit is the right task.
- You want **identity-stable video edit** — the subject, brand, or product from the input clip must survive into the edited video.
- You want **fast video edit iteration** — RunComfy hosts the GPU; you don't deploy or rent.
- You're producing **video edit at scale** — multi-language video edit dubs, A/B variant video edit, batch video edit jobs across SKUs.

If the user said "video edit", "edit video", "restyle this video", "swap the background", "change the outfit", "transfer this motion", "color grade this clip", or showed a video and asked to transform it — route here.

## Video edit routes

| User intent | Video edit model | Why |
|---|---|---|
| Default video edit — restyle, background swap, color grade, packaging swap | `wan-ai/wan-2-7/edit-video` | Most versatile video edit model; identity + motion preservation, up to 1080p video edit output |
| Motion-transfer video edit (transfer motion from a reference clip) | `kling/kling-2-6/motion-control-pro` | Designed for motion-mapping video edit with identity hold |
| Lightweight outfit-swap / atmospheric restyle video edit | `decart/lucy-edit/restyle` | Fastest video edit pass for localized style changes; 720p |

The agent reads this table, classifies the user's video edit intent, and picks the matching endpoint.

## Prerequisites

1. **RunComfy CLI** — `npm i -g @runcomfy/cli`
2. **RunComfy account** — `runcomfy login`.
3. **CI / containers** — set `RUNCOMFY_TOKEN=<token>`.
4. **A source video URL** — formats and limits depend on the chosen video edit route.

## Default video edit — Wan 2.7 Edit-Video

The default video edit endpoint. Use for any general video edit task: restyle a talking-head video, swap a product background, replace packaging design with a reference image, apply a cinematic color grade. Up to 1080p video edit output.

### Schema

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `prompt` | string | yes | — | Video edit instruction. Lead with preservation goals, then state the change. |
| `video` | string | yes | — | Source video URL for video edit. MP4/MOV, 2–10s, ≤100MB. |
| `reference_image` | string | no | — | Optional reference for design-transfer video edit (e.g. packaging swap). |
| `resolution` | enum | no | (input) | `720p` or `1080p` for the video edit output. |
| `aspect_ratio` | enum | no | (input) | W:H. Defaults to source video aspect. |
| `duration` | int | no | 0 | `0` = match input; `2–10` truncates the video edit from the start. |
| `audio_setting` | enum | no | `auto` | `auto` regenerates audio; `origin` preserves source audio in the video edit output. |
| `seed` | int | no | — | Reproducibility for video edit variants. |

### Invoke

**Background swap video edit, identity preserved, audio kept:**

```bash
runcomfy run wan-ai/wan-2-7/edit-video \
  --input '{
    "prompt": "Preserve the speaker'\''s face, pose, and lip movement; change the background to a modern office with neutral lighting.",
    "video": "https://.../speaker.mp4",
    "audio_setting": "origin"
  }' \
  --output-dir <absolute/path>
```

**Packaging-swap video edit with reference image:**

```bash
runcomfy run wan-ai/wan-2-7/edit-video \
  --input '{
    "prompt": "Maintain the original framing and hand movement; replace the packaging design using the reference image.",
    "video": "https://.../hand-holding-package.mp4",
    "reference_image": "https://.../new-packaging.png",
    "audio_setting": "origin"
  }' \
  --output-dir <absolute/path>
```

## Motion-transfer video edit — Kling 2.6 Pro Motion Control

Use when the video edit transfers motion from a reference clip onto a target character. This isn't restyle video edit — it's motion-mapping video edit with identity hold.

| Field | Type | Required | Notes |
|---|---|---|---|
| `prompt` | string | yes | Describe the target motion / style for the video edit output. |
| `image` | string | yes (image orientation) | Reference for character / background consistency in the video edit. |
| `video` | string | yes | Motion-reference clip for the video edit. 10–30s depending on orientation. |
| `keep_original_sound` | bool | no | Preserve audio from the reference video edit input. |
| `character_orientation` | enum | yes | `image` (max 10s video edit output) or `video` (max 30s). |

```bash
runcomfy run kling/kling-2-6/motion-control-pro \
  --input '{
    "prompt": "A young american woman dancing",
    "image": "https://.../target-character.jpg",
    "video": "https://.../motion-reference-dance.mp4",
    "character_orientation": "image",
    "keep_original_sound": true
  }' \
  --output-dir <absolute/path>
```

## Lightweight video edit — Lucy Edit Restyle

Use when the video edit is a localized style modification — outfit swap, scene relight, atmospheric restyle — and identity preservation is critical. Faster and cheaper than Wan 2.7 Edit-Video; capped at 720p.

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `prompt` | string | yes | — | Natural-language video edit instruction. |
| `video_url` | string | yes | — | MP4/MOV/WEBM/GIF source for the video edit. |
| `resolution` | enum | no | `720p` | `720p` only for this video edit tier. |

**Outfit-swap video edit:**

```bash
runcomfy run decart/lucy-edit/restyle \
  --input '{
    "prompt": "Change outfit to professional business attire; preserve face and motion.",
    "video_url": "https://.../subject-walking.mp4"
  }' \
  --output-dir <absolute/path>
```

**Atmospheric video edit:**

```bash
runcomfy run decart/lucy-edit/restyle \
  --input '{
    "prompt": "Make lighting warm and golden hour; preserve face, pose, and motion.",
    "video_url": "https://.../subject-portrait.mp4"
  }' \
  --output-dir <absolute/path>
```

## Prompting video edit — what works

Video edit prompts behave differently from text-to-video prompts. The source clip already fixes most of the look — your prompt should drive the change, not redescribe the video.

- **Lead with preservation goals.** `"Preserve [face / pose / motion / framing / lip movement]; [then state the video edit change]"`. Tell the video edit model what NOT to change.
- **One edit direction per video edit call.** Compound video edits drift on motion. Pick one bucket — restyle OR background OR outfit OR color — per call.
- **Use `reference_image` only when the video edit needs an exact visual** (packaging swap, costume swap matching a target). Don't pass refs for general restyle video edit.
- **`audio_setting: "origin"`** for talking-head video edit where you don't want the soundtrack regenerated.
- **Localized change phrasing wins** for lightweight video edit. "Outfit", "lighting", "background" — pick one bucket.

## Video edit FAQ

**What's the max duration of a video edit clip?** Wan 2.7 Edit-Video: 2–10s. Kling Motion Control: 10s (image orientation) or 30s (video orientation). Lucy Edit Restyle: matches input.

**What video formats does video edit accept?** MP4, MOV (Lucy also takes WEBM and GIF). Source video edit input must be ≤100MB on Wan 2.7.

**Does video edit preserve face identity?** Yes — all three video edit routes are designed for identity preservation. State the goal explicitly: `"preserve face and motion"`.

**Can video edit keep the original audio?** Yes — set `audio_setting: "origin"` on Wan 2.7 Edit-Video, or `keep_original_sound: true` on Kling. Lucy preserves audio by default.

**What's the highest-resolution video edit available here?** 1080p on Wan 2.7 Edit-Video. Kling and Lucy cap at 720p.

**Video edit vs text-to-video on RunComfy?** Video edit transforms an existing clip (look largely fixed by source). Text-to-video starts from a prompt only (look generated). Use video edit when you have a clip; use text-to-video for novel content.

**Can I run multiple video edits in one call?** No. Each video edit call applies one direction; for compound video edits, chain calls and stitch.

## Limitations

- **Each video edit route inherits its model's limits.** Wan 2.7 Edit-Video: 2–10s, 1080p ceiling. Kling Motion Control: 10s or 30s by orientation. Lucy Edit Restyle: 720p, no aspect control.
- **No multi-route video edit blending.** This skill picks one video edit model per call. If you need outfit-swap + motion-transfer in the same video edit, that's two calls plus a stitch.
- **Brand-specific overrides** — if the user named a specific model variant, route to that brand skill (`wan-2-7`) instead of forcing it through this video edit router.

## Exit codes

| code | meaning |
|---|---|
| 0  | video edit succeeded |
| 64 | bad CLI args |
| 65 | bad input JSON for video edit / schema mismatch |
| 69 | upstream 5xx |
| 75 | retryable: timeout / 429 |
| 77 | not signed in or token rejected |

Full reference: [docs.runcomfy.com/cli/troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=video-edit-runcomfy).

## How it works

The skill picks one of three video edit endpoints (Wan 2.7 Edit-Video, Kling Motion Control, or Lucy Edit Restyle) based on user intent, and invokes `runcomfy run <endpoint>` with the matching JSON body. The CLI POSTs to the RunComfy Model API, polls the video edit request status every 2 seconds, and downloads the resulting video from the `*.runcomfy.net` / `*.runcomfy.com` URL into `--output-dir`. `Ctrl-C` cancels the in-flight video edit request.

## Security & Privacy

- **Token storage**: `runcomfy login` writes the API token to `~/.config/runcomfy/token.json` with mode 0600. Set `RUNCOMFY_TOKEN` env var in CI.
- **Input boundary**: the video edit prompt is passed as JSON via `--input`. The CLI does NOT shell-expand. No shell-injection surface.
- **Third-party content**: video / image URLs are fetched by the RunComfy server. Treat external URLs as untrusted — image-based prompt injection is a known risk for any video edit model.
- **Outbound endpoints**: only `model-api.runcomfy.net` and `*.runcomfy.net` / `*.runcomfy.com`. No telemetry.
- **Generated-file size cap**: the CLI aborts any video edit download > 2 GiB.
