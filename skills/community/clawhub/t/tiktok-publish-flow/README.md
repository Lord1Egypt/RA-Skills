# tiktok-publish-flow

TikTok posting automation for OpenClaw agents: post **videos**, **photos with TikTok music**, and **edit captions** on TikTok Studio (web) via Playwright — no official API, no third-party paid services, zero credits.

Born from real production use (24.09.2026): 3 videos + 1 photo-with-music + 1 caption edit, all successful.

## How it works

- One-time QR login (from the phone's TikTok app); the session persists in a Chromium profile.
- `scripts/tiktok_post3.py` — video posts (handles TikTok's "Continue to post?" check dialog automatically).
- `scripts/tiktok_photo_music.py` — photo posts with a music track picked from TikTok's own sound picker.
- `scripts/tiktok_edit_post.py` — edit an existing post's caption, with a wrong-post guard.

Scripts are portable: override `TIKTOK_PROFILE_DIR` / `TIKTOK_SHOTS_DIR` (defaults under `~/.tiktok-poster/`).

## Requirements

- Python 3.10+, `playwright` (`pip install playwright && playwright install chromium`)
- Node not required. ffmpeg only if you produce the videos yourself.

## Safety

- The flow posts under the account owner's authorization. For crons, run posting in a dedicated subagent, and check the content list first to avoid duplicates (the owner may post manually in parallel).
- Edited posts show "Under review" for a while — that's normal, the post stays live.

Full procedure, verified traps and the Higgsfield-connector dead-end notes: see [SKILL.md](SKILL.md).
