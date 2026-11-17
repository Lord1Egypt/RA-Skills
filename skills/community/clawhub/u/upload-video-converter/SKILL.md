---
name: upload-video-converter
description: Convert videos for compatibility and uploads — pick the right container/codec/bitrate for each destination (marketplaces, social platforms, ad managers, CMS), fix rejected uploads, and shrink files without visible quality loss.
---

# Upload Video Converter

Get any video file accepted by any upload target — the right format, size, and specs on the first try.

## Quick Reference

| Decision | Strong | Acceptable | Weak (avoid) |
|---|---|---|---|
| Default target | MP4 (H.264) + AAC, yuv420p | MOV (H.264) for Apple-centric flows | WebM/MKV/AVI for platform uploads |
| Size reduction | Re-encode with CRF 20-23 + right resolution | Two-pass to a bitrate target | Chopping resolution to 480p first |
| Resolution | Match destination max (usually 1080p) | Keep source if below max | Upscaling to "meet" a spec |
| Frame rate | Keep source (30/60) | Constant-rate conversion when required | Mixing variable frame rate into edits |
| Audio | AAC 128-192kbps stereo, 44.1/48kHz | Copy if already AAC | PCM/FLAC in upload files |
| Color | SDR BT.709, yuv420p | Tone-mapped HDR→SDR | Uploading raw HDR/10-bit to SDR-only targets |
| Verification | Probe output specs + test upload | Probe output specs | "Looks fine in my player" |

## Solves

1. **Rejected uploads** — the platform says "unsupported format," "file too large," or silently fails processing.
2. **Oversized files** — 2GB phone/screen recordings that need to hit a 500MB, 100MB, or 30MB cap without looking bad.
3. **Codec roulette** — HEVC/H.265, ProRes, VP9, or 10-bit sources that half the destinations can't ingest.
4. **Broken-looking results** — washed-out colors (HDR mishandled), out-of-sync audio, stuttering (VFR), or green artifacts (pixel format).
5. **One file, many destinations** — the same master needs different specs for a marketplace PDP, an ad manager, and a CMS.
6. **No way to verify** — teams re-upload blindly instead of probing the file against the destination's spec.

## Use when

- A video won't upload or gets rejected by a marketplace, ad platform, social site, or CMS
- A file must be converted to a specific format/codec/size requirement
- A file must be shrunk below a size cap with minimal quality loss
- Preparing one master for several destinations at once

## Do not use when

- The problem is aspect ratio or platform-fit composition (use social-video-resizer)
- The content itself needs editing or trimming (use a video cutter skill first)
- You need frame-accurate color grading or mastering work

## Inputs

- Source video file (or its probe data: codec, resolution, fps, bitrate, duration, size)
- Destination(s) and their published requirements (format, codec, size cap, length cap)
- Priority: max quality vs min size vs fastest turnaround
- Optional: audio requirements, caption/subtitle handling, HDR/SDR constraints

## Workflow

### Step 1 — Probe the source

Get codec, container, resolution, frame rate (and whether VFR), bit depth, pixel format, color space, audio codec, duration, size. Everything downstream depends on this. Commands in references/ffmpeg-recipes.md.

### Step 2 — Pin the destination spec

Look up the target's requirements (references/platform-upload-specs.md as baseline; the destination's current docs win). Note hard caps: size, duration, resolution, codec whitelist.

### Step 3 — Choose the conversion path

Decision order: (1) if source already complies → remux or pass through, don't re-encode; (2) if only the container is wrong → remux (`-c copy`); (3) otherwise re-encode to MP4/H.264/AAC/yuv420p at the destination's ceiling. Special cases (HDR, VFR, 10-bit, ProRes) in references/troubleshooting-guide.md.

### Step 4 — Hit the size budget

Compute the bitrate budget: `(size_cap_MB × 8192) ÷ duration_s − audio_kbps`. Prefer CRF mode when there's headroom; switch to two-pass bitrate targeting when the cap is tight. Drop resolution only after bitrate targeting alone would fall below sane quality floors (references/ffmpeg-recipes.md table).

### Step 5 — Convert and verify

Run the conversion, then probe the output and check against the spec: codec, size, duration, pixel format, audio. Play 10 seconds at start/middle/end for sync and artifacts.

### Step 6 — Deliver with a spec sheet

Report what was produced per destination: specs, size, what changed, any quality tradeoffs, and the exact command used (reproducibility). Follow references/output-template.md and check assets/conversion-checklist.md.

## Worked Example 1 — 1.8GB screen recording → 100MB course-platform cap

**Input:** 1.8GB MOV, 2560×1440 @ 60fps VFR (screen recording, HEVC 10-bit), 22 min, destination accepts MP4 ≤100MB, ≤1080p.

**Output (core section):**

> **Path:** full re-encode (HEVC 10-bit + VFR + over-res: three strikes, no remux possible).
> **Budget:** 100MB ≈ 819,200 kbit ÷ 1320s ≈ 620 kbps total → 128 kbps audio → ~490 kbps video. That's tight for 1440p60 but fine for screen content at 1080p with a low frame rate.
> **Decisions:** downscale to 1920×1080; force CFR 30fps (screen content, no fast motion); H.264 two-pass at 470 kbps; `-tune stillimage`-adjacent settings avoided (text clarity: use `-preset slow`, high profile); audio AAC 128k mono→stereo kept as source.
> **Result:** 96.4MB, text legible at 100% zoom, no VFR stutter.
> **Tradeoff noted:** fast cursor motion softens slightly at 30fps; acceptable for tutorial content. Command included for re-runs.

## Worked Example 2 — One master → marketplace PDP + Meta ads + email GIF-substitute

**Input:** 45s product master, ProRes 422, 3840×2160, 25fps, 4.2GB. Destinations: (a) marketplace video slot — MP4 H.264 ≤500MB ≤1080p; (b) Meta ad — MP4 ≤4GB, ≤30s needs trim flag; (c) email — needs <5MB looping clip.

**Output (core section):**

> **(a) Marketplace:** re-encode → 1920×1080, CRF 20, preset slow, AAC 160k → 58MB. Well under cap; CRF mode used since there's headroom.
> **(b) Meta ad:** blocked on duration — 45s master vs 30s placement guidance. Flagged for cut (product-video-cutter), then same encode ladder as (a); do not silently truncate.
> **(c) Email clip:** 8s highlight loop, 640×360, no audio, H.264 CRF 28 → 3.1MB MP4. Noted: animated GIF at this size would be ~3× larger and lower quality — recommend MP4 with autoplay-muted, GIF fallback only if the ESP requires it.
> **Verification:** all outputs probed (codec/size/duration) and spot-played; spec sheet attached per file.

## Common Mistakes

1. **Re-encoding when a remux would do** — if codecs already comply and only the container is wrong, `-c copy` preserves 100% quality in seconds.
2. **Ignoring VFR** — variable frame rate from phone/screen recordings causes stutter and audio drift in editors and some platforms; force CFR when converting.
3. **Uploading 10-bit/HDR to SDR-only targets** — causes washed-out or rejected uploads; convert to yuv420p BT.709 and tone-map HDR properly.
4. **Crushing resolution before optimizing bitrate** — a well-encoded 1080p at modest bitrate beats a 480p file at the same size.
5. **Upscaling to meet a spec** — never upscale; deliver the source resolution and note it.
6. **Forgetting the audio budget** — at tight size caps, 320k audio steals meaningful bitrate from video; 128k AAC is fine for speech.
7. **Trusting the preview player** — a file that plays locally can still fail platform ingest (pixel format, moov atom position); always probe and, when possible, test-upload. Add `-movflags +faststart` for web.
8. **One encode for all destinations** — size caps and codec whitelists differ; produce a ladder from one master, never re-encode an already-compressed output (generation loss).
9. **No reproducibility** — always deliver the exact command/settings used so the next batch doesn't start from scratch.

## Resources

- `references/output-template.md` — delivery spec-sheet template
- `references/platform-upload-specs.md` — baseline upload requirements by destination type
- `references/ffmpeg-recipes.md` — probe commands, encode ladders, size-budget math
- `references/troubleshooting-guide.md` — rejected uploads, HDR/VFR/sync fixes
- `assets/conversion-checklist.md` — pre-delivery checklist
