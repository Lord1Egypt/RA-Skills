---
name: xpilot-ad-maker
description: Generate a 30-second cinematic ad video with consistent character, AI narration, brand overlays, and ambient music. Uses Vidu reference-to-video for character continuity across 4 scenes. Demoed on a medical-tourism storyboard but works for any vertical.
license: MIT-0
metadata:
  openclaw:
    version: 0.1.0
    emoji: "🎬"
    homepage: https://github.com/dotku/x-post-scheduler/tree/main/skills/xpilot-ad-maker
    primaryEnv: VIDU_API_KEY
    requires:
      env:
        - VIDU_API_KEY
        - WAVESPEED_API_KEY
        - REPLICATE_API_KEY
        - R2_ACCOUNT_ID
        - R2_ACCESS_KEY_ID
        - R2_SECRET_ACCESS_KEY
        - R2_BUCKET_NAME
        - R2_PUBLIC_URL
      bins:
        - node
    install:
      - kind: node
        package: tsx
        bins: [tsx]
      - kind: node
        package: ffmpeg-static
        bins: []
---

# MedTravel Ad Maker

End-to-end pipeline that produces a polished 30-second medical-tourism ad video.

## What it does

Given a destination (e.g. "Nanning, China"), a procedure (e.g. "dental implants"),
and a brand name, this skill generates a complete 30-second ad with:

1. **Character continuity** — One AI-generated protagonist appears in all 4 shots
   (uses Vidu's `reference2video` so the same person shows up in every scene
   without per-shot drift).
2. **Cinematic visuals** — 4 storyboarded shots:
   - Pain point (high cost in patient's home country)
   - Modern destination clinic
   - Wellness recovery in scenic location
   - Triumphant outcome with brand CTA
3. **AI narration** — Replicate Kokoro TTS (`af_bella` voice) generates
   per-shot voiceover, time-aligned to each scene.
4. **Background music** — Soft synthesized ambient pad (C-major triad,
   low-pass filtered, fade in/out).
5. **Brand overlays** — Top descriptive captions (so viewers understand the
   story instantly) + bottom emerald-green brand text on each shot.
6. **Output** — Final MP4 uploaded to your Cloudflare R2 bucket, plus all
   intermediate clips for re-use.

## How it works

```
Step 1: Wavespeed (Seedream 4.5) → 1 protagonist portrait → R2
Step 2: Vidu reference2video × 4 (parallel)  → 4 shot clips → R2
Step 3: Replicate Kokoro TTS × 4              → 4 narration clips
Step 4: ffmpeg concat                          → 30s silent video
Step 5: ffmpeg filter_complex                  → drawtext overlays + audio mix
Step 6: Upload final to R2
```

## Cost & timing

Per run (one full 30s ad):

| Item | Cost |
|---|---|
| Wavespeed Seedream 4.5 (1 portrait) | ~$0.04 |
| Vidu viduq2-pro reference2video × 4 | ~$2.50 (250 credits) |
| Replicate Kokoro TTS × 4 | ~$0.001 |
| **Total** | **~$2.55** |

End-to-end runtime: **~3 minutes** (most time is Vidu video generation in parallel).

## Required environment variables

- `VIDU_API_KEY` — Vidu Platform API key (https://platform.vidu.com)
- `WAVESPEED_API_KEY` — Wavespeed.ai API key (for the protagonist image)
- `REPLICATE_API_KEY` — Replicate token (for Kokoro TTS)
- `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`,
  `R2_BUCKET_NAME`, `R2_PUBLIC_URL` — Cloudflare R2 (S3-compatible) for storage

## Required system binaries

- `node` (≥ 18)
- `ffmpeg` is bundled via the `ffmpeg-static` npm package — no system install needed.

## Usage

```bash
# Customize the SHOTS array in make-xpilot-ad.ts with your storyboard,
# then run:
npx tsx make-xpilot-ad.ts
```

The script prints the final R2 URL at the end. To iterate on post-production
(captions, narration, music) without re-spending Vidu credits, run:

```bash
npx tsx xpilot-ad-finalize.ts
```

This pulls the existing 4 video clips from R2, regenerates narration, and
re-composites the final video. Free and fast (~45 seconds).

## Example output

Final 30-second ad (8 MB MP4) — narration, ambient music, brand overlays:
https://pub-22e3d3e3f43e400493bbd71306cae6bb.r2.dev/demo/medical-tourism-ad/v2/medtravel-final.mp4

Behind-the-scenes assets (all publicly hosted on R2):

- Protagonist reference image (Wavespeed Seedream 4.5):
  https://pub-22e3d3e3f43e400493bbd71306cae6bb.r2.dev/demo/medical-tourism-ad/v2/reference-protagonist.png
- Shot 1 — Sticker shock:
  https://pub-22e3d3e3f43e400493bbd71306cae6bb.r2.dev/demo/medical-tourism-ad/v2/shot-1-sticker-shock.mp4
- Shot 2 — Nanning clinic:
  https://pub-22e3d3e3f43e400493bbd71306cae6bb.r2.dev/demo/medical-tourism-ad/v2/shot-2-nanning-clinic.mp4
- Shot 3 — Bama wellness:
  https://pub-22e3d3e3f43e400493bbd71306cae6bb.r2.dev/demo/medical-tourism-ad/v2/shot-3-bama-wellness.mp4
- Shot 4 — Detian triumph:
  https://pub-22e3d3e3f43e400493bbd71306cae6bb.r2.dev/demo/medical-tourism-ad/v2/shot-4-detian-triumph.mp4

Notice the same protagonist appears in all 4 shots — that's the power of
Vidu's `reference2video` mode, which this skill encapsulates.

## Customization

To make this skill work for a different brand/vertical (e.g., "Mexican dental
tourism", "Thai cosmetic surgery", "Korean LASIK"), edit:

- `REFERENCE_PROMPT` — describe your protagonist
- `SHOTS[*].prompt` — describe each scene
- `SHOTS[*].narration` — what the voiceover says
- `SHOTS[*].brandText` — bottom brand caption
- `SHOTS[*].topCaption` — top descriptive caption

The pipeline (parallel submission, polling, R2 mirroring, ffmpeg composition)
stays the same.

## Why Reference-to-Video?

Vidu has three video generation modes:

| Mode | Pros | Cons |
|---|---|---|
| `text2video` | Simple | Each shot's character looks different |
| `img2video` | Visual continuity | Hard to change scenes (just continues motion) |
| **`reference2video`** | **Same character across scenes** | Slightly more setup |

For multi-shot ads with a recurring protagonist, `reference2video` is the
only mode that works. This skill encapsulates that workflow.

## Known gotchas (saved you the debugging time)

1. **Vidu CloudFront URLs contain unencoded `;`** — don't URL-encode it,
   that breaks the signature. Mirror to R2 immediately.
2. **OpenAI / OpenRouter quotas run out fast** — this skill uses Replicate
   Kokoro instead, which is dirt cheap.
3. **Replicate rate-limits accounts under $5 credit** to 6 req/min — script
   adds 11s delays between TTS calls.
4. **ffmpeg drawtext apostrophe escaping is unreliable** — use full words
   instead ("should not" instead of "shouldn't").
5. **ffmpeg drawtext `%` is parsed as variable** — escape or use words ("60 percent").
6. **Multiple drawtext filters with commas in text** break with `,` separator —
   use `;` + intermediate labels instead.
