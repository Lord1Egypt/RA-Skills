---
name: seedance-v2
displayName: "🫧 Seedance 2.0 Pro — Pro Pack on RunComfy"
description: >
  Seedance 2.0 Pro on RunComfy. Seedance 2.0 Pro (ByteDance Seedance v2)
  is a multi-modal cinematic short-form video model with native lip-sync
  audio. This skill calls Seedance 2.0 Pro through the RunComfy CLI:
  `runcomfy run bytedance/seedance-v2/pro`. Seedance 2.0 Pro accepts up
  to 9 image references, 3 video references, and 3 audio references in
  one Seedance call, producing 4–15 second cinematic clips at 720p.
  Triggers on "seedance", "seedance 2", "seedance v2", "seedance pro",
  "seedance 2.0", "ByteDance Seedance", or any explicit ask to generate
  video with Seedance.
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

# 🫧 Seedance 2.0 Pro — Pro Pack on RunComfy

[runcomfy.com](https://www.runcomfy.com/?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-v2) · [docs](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-v2) · [Seedance 2.0 Pro model page](https://www.runcomfy.com/models/bytedance/seedance-v2/pro?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-v2)

**Seedance 2.0 Pro** is ByteDance's multi-modal cinematic short-form video model. This skill generates video with Seedance 2.0 Pro hosted on the RunComfy Model API — no Seedance API key, no GPU rental, just `runcomfy run bytedance/seedance-v2/pro` from your terminal.

## What Seedance 2.0 Pro is

Seedance 2.0 Pro is the second-generation Seedance model from ByteDance, designed for cinematic short-form video with three properties that make Seedance distinct:

- **Multi-modal Seedance generation.** Seedance 2.0 Pro accepts up to **9 image references**, **3 video references**, and **3 audio references** in one Seedance call. No other ByteDance video model exposes this level of multi-input conditioning. Image refs hold identity, video refs hold scene, audio refs hold voice — Seedance routes all three into the output.
- **Native in-pass lip-sync audio.** Seedance 2.0 Pro produces speech, ambient sound, and music **in the same generation pass** as the visuals. Seedance lip-sync is timed to the spoken words without a separate post-sync step. This makes Seedance 2.0 Pro one of the cleanest dialogue-ad models available.
- **Cinematic motion grammar.** Seedance 2.0 Pro responds to camera-shot grammar in plain language — "medium close-up, slow push-in, handheld follow, locked tripod" — at the same fidelity as the prompt's character description. Seedance treats motion as a first-class directive.

Seedance 2.0 Pro generates 4–15 second clips at 480p or 720p, in 7 aspect ratios. Seedance prompts accept Chinese (≤500 chars) or English (≤1000 words).

## When Seedance 2.0 Pro is the right choice

Pick Seedance 2.0 Pro when any of these is true:

- You need a **lip-synced spokesperson clip**. Seedance 2.0 Pro is the strongest lip-sync option in the catalog when you want natural speech generated in-pass.
- You have **multi-modal references** — character image + scene video + voice audio. Seedance 2.0 Pro is built for combining them.
- You're producing **brand-consistent multi-language narratives**. Seedance image refs hold identity across language variants; the Seedance prompt translates the script.
- You're shooting **cinematic short-form film previs**. Seedance camera grammar is fluent.
- You need **reproducible Seedance variants**. Pass a fixed `seed` for deterministic Seedance output.

If the user said "Seedance" / "Seedance 2" / "Seedance Pro" / "Seedance v2" / "ByteDance Seedance" explicitly, route here regardless.

## Prerequisites

1. **RunComfy CLI** — `npm i -g @runcomfy/cli`
2. **RunComfy account** — `runcomfy login` opens a browser device-code flow.
3. **CI / containers** — set `RUNCOMFY_TOKEN=<token>` instead of `runcomfy login`.

## Endpoint + input schema

### `bytedance/seedance-v2/pro`

This is the Seedance 2.0 Pro endpoint. The Seedance Lite tier and earlier Seedance versions run on different endpoints not covered here.

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `prompt` | string | yes | — | Seedance accepts CN ≤ 500 chars OR EN ≤ 1000 words. |
| `image_url` | array | no | `[]` | 0–9 image references for Seedance (JPEG/PNG/WebP/BMP/TIFF/GIF). |
| `video_url` | array | no | `[]` | 0–3 reference clips for Seedance (MP4/MOV), 2–15s each. |
| `audio_url` | array | no | `[]` | 0–3 reference audio for Seedance (WAV/MP3), 2–15s, < 15MB each. |
| `aspect_ratio` | enum | no | `adaptive` | `adaptive`, `16:9`, `9:16`, `4:3`, `3:4`, `1:1`, `21:9`. |
| `duration` | int | no | 5 | 4–15 (whole seconds). Seedance per-call cap is 15s. |
| `resolution` | enum | no | `720p` | `480p` or `720p`. Seedance Pro tier max is 720p. |
| `generate_audio` | bool | no | true | In-pass synchronized speech / SFX / music from Seedance. |
| `seed` | int | no | — | Reproducibility for Seedance output. |

## How to invoke Seedance 2.0 Pro

**Default Seedance run (text only, 5s, 720p, with audio):**

```bash
runcomfy run bytedance/seedance-v2/pro \
  --input '{"prompt": "<Seedance prompt>"}' \
  --output-dir <absolute/path>
```

**Seedance lip-synced ad with character image reference:**

```bash
runcomfy run bytedance/seedance-v2/pro \
  --input '{
    "prompt": "Medium close-up. The woman explains today'\''s special in a warm friendly tone, slow push-in, soft window light, gentle cafe ambience.",
    "image_url": ["https://.../barista-headshot.jpg"],
    "duration": 8,
    "aspect_ratio": "9:16"
  }' \
  --output-dir <absolute/path>
```

**Multi-modal Seedance call (image + video + audio refs):**

```bash
runcomfy run bytedance/seedance-v2/pro \
  --input '{
    "prompt": "Subject from image 1 walks through the café from video 1, voice tone matches audio 1.",
    "image_url": ["https://.../subject.jpg"],
    "video_url": ["https://.../cafe-locked-shot.mp4"],
    "audio_url": ["https://.../voice-ref.mp3"]
  }' \
  --output-dir <absolute/path>
```

The CLI submits the Seedance request, polls every 2s, fetches the Seedance result, and downloads any `*.runcomfy.net` / `*.runcomfy.com` URL into `--output-dir`.

## Prompting Seedance 2.0 Pro — what works

Seedance 2.0 Pro responds to specific prompting patterns better than naive prose. Apply these for sharper Seedance output.

**Image vs text division — the single most important Seedance rule.** Stable identity (face, costume, brand mark, logo) → put in `image_url` so Seedance preserves it. Evolving narrative (action, mood, lighting, camera) → put in `prompt` so Seedance generates it. Trying to verbally describe a face in detail wastes Seedance tokens and produces drift.

**Camera + motion in plain language.** Seedance 2.0 Pro understands "medium close-up", "slow push-in", "handheld follow", "locked-off wide" as real directives. Combine: `"Medium close-up. Slow push-in over 3 seconds. Handheld, slight breathing motion."` Seedance executes the camera grammar.

**Audio direction with `generate_audio: true`** — tell Seedance the tone: `"warm friendly conversational"`, `"calm instructional"`, `"crisp newsroom delivery"`. For ambient: `"gentle cafe chatter, distant traffic, no foreground music"`. Seedance will synthesize audio matching the directive.

**Seedance reference media specs.** Reference videos must be 2–15s; reference audio must be ≤15MB and 2–15s. Out-of-range files reject. Match aspect ratio of refs to the Seedance output to avoid crops.

**Seedance anti-patterns:**
- Mixing radically different aesthetic refs (watercolor + photoreal) → confuses Seedance.
- Conflicting style cues in the Seedance prompt → simplify by removing contradictions.
- Trying to describe stable identity verbally → use Seedance `image_url` instead.
- Asking Seedance for >15s clips → 422; segment into multiple Seedance calls.

## Where Seedance 2.0 Pro shines

| Use case | Why Seedance 2.0 Pro |
|---|---|
| **Spokesperson / dialogue ads** | Seedance native in-pass lip-sync, no separate TTS step |
| **Brand-consistent multi-language narratives** | Seedance image refs hold identity; text drives translation |
| **Cinematic short-form film previs** | Seedance camera-shot grammar + multi-modal refs |
| **Ad creatives with reference music / VO tone** | Seedance audio refs guide voice / mood |
| **Reproducible Seedance variant testing** | Seedance seed control + fixed schema |

## Sample Seedance prompts (verified to produce strong results)

**Default Seedance playground example:**

```
Golden hour on a quiet cafe terrace: a barista wipes the counter, then
looks up and explains today's special in a friendly tone, natural
lip-sync. Medium close-up, slow push-in; warm side light, soft bokeh
through glass, gentle cafe ambience and subtle film grain.
```

**Multi-modal Seedance lip-sync (text + image):**

```
Same person as image 1 in a softly-lit recording booth, leaning into
the mic, says: "We just shipped the biggest update of the year."
Calm conversational tone. Medium close-up, locked tripod, shallow DOF,
warm key light from camera-left.
```

## Seedance FAQ

**What's the max Seedance clip duration?** A single Seedance 2.0 Pro call generates 4–15 seconds. For longer narratives, segment into multiple Seedance calls and stitch the outputs.

**What aspect ratios does Seedance 2.0 Pro support?** Seven: `adaptive`, `16:9`, `9:16`, `4:3`, `3:4`, `1:1`, `21:9`. Seedance defaults to `adaptive` (matches input refs).

**Does Seedance 2.0 Pro do lip-sync?** Yes. With `generate_audio: true` (default), Seedance produces lip-synced speech in-pass. The lip movement on Seedance output is timed to the spoken words.

**Can Seedance take an existing audio file as input?** Yes — pass it as `audio_url`. Seedance treats it as a reference (voice tone, mood) rather than a strict lip-sync driver. For audio-driven lip-sync to a literal voiceover, route to a different model.

**What languages does Seedance 2.0 Pro accept?** Chinese (≤500 chars) or English (≤1000 words) prompts. Seedance output language follows the prompt.

**What's the Seedance resolution ceiling?** 720p on the Seedance Pro tier here. 4K Seedance variants run on different endpoints not covered by this skill.

**How do I get reproducible Seedance output?** Pass `seed` as a fixed int. Same Seedance prompt + same seed = same Seedance generation.

## Limitations of Seedance 2.0 Pro

- **Seedance duration cap 15s.** Each Seedance call generates at most 15 seconds.
- **Seedance resolution cap 720p** on this endpoint.
- **Seedance reference media specs** — reference videos / audio must be 2–15s; audio < 15MB.
- **Seedance lip-sync depends on prompt clarity** — not guaranteed perfect under all conditions.
- **No `@`-syntax for character binding** in Seedance — relies on image refs + prompt alignment.

## Exit codes

| code | meaning |
|---|---|
| 0  | Seedance generation succeeded |
| 64 | bad CLI args |
| 65 | bad input JSON for Seedance / schema mismatch |
| 69 | upstream 5xx |
| 75 | retryable: timeout / 429 |
| 77 | not signed in or token rejected |

Full reference: [docs.runcomfy.com/cli/troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-v2).

## How it works

The skill invokes `runcomfy run bytedance/seedance-v2/pro` with a JSON body matching the Seedance schema. The CLI POSTs to `https://model-api.runcomfy.net/v1/models/bytedance/seedance-v2/pro`, polls the Seedance request, fetches the Seedance result, and downloads any `.runcomfy.net` / `.runcomfy.com` URL into `--output-dir`. `Ctrl-C` cancels the remote Seedance request before exit.

## Security & Privacy

- **Token storage**: `runcomfy login` writes the API token to `~/.config/runcomfy/token.json` with mode 0600.
- **Input boundary**: the Seedance prompt is passed as JSON via `--input`. No shell injection.
- **Third-party content**: image / video / audio URLs are fetched by the RunComfy server. Treat external URLs as untrusted — image-based prompt injection is a known risk for any image / video model.
- **Outbound endpoints**: only `model-api.runcomfy.net` and `*.runcomfy.net` / `*.runcomfy.com`.
- **Generated-file size cap**: 2 GiB.
