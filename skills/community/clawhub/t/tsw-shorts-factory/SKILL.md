---
name: tsw-shorts-factory
description: "Autonomous YouTube Shorts video factory — zero cost, no external video API required. Generates quote-based short-form videos daily using edge-tts (free Microsoft neural voices) + Pexels stock footage (free API) + MoviePy local assembly, then uploads to YouTube as drafts. Use when: setting up automated YouTube Shorts content pipelines, replacing broken video generation APIs, building faceless quote/motivation channels, or automating social video content at scale."
---

# TSW Shorts Factory

Zero-cost autonomous YouTube Shorts pipeline. Ships 3 videos/day, no paid APIs.

**Stack:** edge-tts (free) → Pexels clips (free API) → MoviePy (local) → YouTube upload

## Quick Deploy

```bash
# 1. Install dependencies
pip install moviepy edge-tts google-api-python-client google-auth-oauthlib pillow

# 2. Set Pexels API key (free at pexels.com/api)
export PEXELS_API_KEY="your_key_here"

# 3. Set up YouTube OAuth (one-time)
python3 scripts/yt_setup.py  # Opens browser for auth

# 4. Prepare quote library
cp assets/sample_quotes.json quote_library.json  # Or provide your own

# 5. Run once to test
python3 scripts/pipeline.py

# 6. Add to cron (3x daily)
# 0 8,14,20 * * * cd /your/path && python3 scripts/pipeline.py >> pipeline.log 2>&1
```

## Quote Library Format

```json
{
  "motivational": [
    {"quote": "Champions keep playing until they get it right.", "author": "Billie Jean King"},
    {"quote": "The secret of getting ahead is getting started.", "author": "Mark Twain"}
  ],
  "sports_quotes": [
    {"quote": "I am the greatest.", "author": "Muhammad Ali"}
  ]
}
```

Supported niches: `motivational`, `sports_quotes`, `business_quotes`, `film_tv_quotes`, `wisdom_philosophy`

## Video Output
- Format: MP4, vertical 1080x1920 (Shorts-optimized)
- Duration: matches TTS audio length (~15–45 seconds)
- Text overlay: quote + author, centered, white with black stroke
- Background: 4 rotating Pexels stock clips matched to niche
- Uploaded as **unlisted drafts** — human reviews before publishing

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PEXELS_API_KEY` | required | Free at pexels.com/api |
| `YT_TOKEN_FILE` | `~/.yt_token.pickle` | YouTube OAuth token |
| `OUTPUT_DIR` | `/tmp/tsw_output` | Video output directory |
| `AUDIO_DIR` | `/tmp/tsw_audio` | TTS audio cache |
| `CLIP_CACHE_DIR` | `/tmp/tsw_clips` | Pexels clip cache (reused) |

## Cost
- edge-tts: free (Microsoft neural voices via unofficial API)
- Pexels: free tier (25,000 requests/month)
- MoviePy: free (local ffmpeg)
- YouTube API: free (10,000 units/day quota)
- Total: **$0/month** for ~90 videos/month

## References
- YouTube setup: See `references/youtube-setup.md`
- Adding niches: See `references/niche-config.md`
- Troubleshooting: See `references/troubleshooting.md`
