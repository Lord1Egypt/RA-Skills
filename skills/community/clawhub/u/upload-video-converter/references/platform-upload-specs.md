# Baseline Upload Requirements by Destination Type

Platform specs change; treat these as baselines and confirm against the destination's current docs before large batches.

## Universal safe default

MP4 container, H.264 (High profile), yuv420p 8-bit, BT.709 SDR, CFR at source frame rate, AAC-LC stereo 128-192kbps 48kHz, `-movflags +faststart`. This passes ingest on the overwhelming majority of upload targets.

## Marketplaces / e-commerce

| Destination type | Typical caps | Notes |
|---|---|---|
| Amazon product video | MP4/MOV, ≤5GB, 1080p recommended | H.264 + AAC; longer processing on large files |
| Shopify product media | MP4/MOV, ≤1GB, up to 4K | 1080p is plenty for PDP slots |
| Etsy listing video | 5-15s, ≤100MB, ≥1080px | Short-loop format; no audio played |
| eBay video | MP4, ≤150MB typical | Conservative: 1080p H.264 |

## Social / ads

| Destination type | Typical caps | Notes |
|---|---|---|
| Meta (FB/IG) feed & Reels | MP4/MOV, ≤4GB | H.264 + AAC; Reels 9:16; keep ≤60s for ads practice |
| TikTok | MP4/WebM ok, ≤500MB (web) | 9:16 1080×1920; H.264 safest |
| YouTube | Most containers accepted, huge caps | Prefer high-bitrate H.264; VP9/AV1 transcode handled by YT |
| X (Twitter) | MP4, ≤512MB, ≤2:20 | H.264 High, AAC-LC explicitly required |
| LinkedIn | MP4, 75KB-5GB, ≤10min | Conservative H.264 ladder |

## CMS / email / docs

| Destination type | Typical caps | Notes |
|---|---|---|
| WordPress & generic CMS | Server-side limit often 32-512MB | Ask the admin; H.264 MP4 + faststart for streaming |
| Email embeds | Effectively <5MB | Most clients won't play video: use short muted MP4 where supported, GIF/static fallback |
| Course platforms (Teachable etc.) | Commonly ≤2GB per lesson | 1080p30 is the sweet spot for screen content |
| Slack/Teams sharing | ≤1GB practical | H.264 MP4 previews inline |

## Hard-cap math cheat table (H.264 + 128k AAC)

Approx max duration you can fit at good quality:

| Size cap | 1080p30 good (~5 Mbps) | 1080p30 acceptable (~2.5 Mbps) | 720p30 (~1.5 Mbps) |
|---|---|---|---|
| 30MB | ~48s | ~1:35 | ~2:40 |
| 100MB | ~2:40 | ~5:20 | ~8:50 |
| 500MB | ~13min | ~26min | ~44min |

If the required duration doesn't fit the cap at ≥1.5 Mbps 1080p, step down to 720p before starving the bitrate.
