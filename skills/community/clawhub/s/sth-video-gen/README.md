# STH Video Template Generation

Automated video generation pipeline for Sing The Hook (STH) song templates.

## Quick Start

```bash
# Save your CSV with columns: "Song Template ID", "Status"
# Run the generator
python3 sth_video_generator.py your_templates.csv
```

## What It Does

1. Reads template IDs from your CSV
2. Fetches image URLs, video prompts, and audio mix URLs from PostgreSQL
3. Generates original video using `seedance1.5pro` model (image-to-video)
4. Generates final video using `infinitetalk` model (video-to-video lip-sync with audio)
5. Updates the database with video URLs and status

### Pipeline Diagram

```
image_url + prompt ──→ seedance1.5pro ──→ original_video
                                                     │
                                                     ↓
original_video + amix_url ──→ infinitetalk ──→ final_video (lip-synced)
```

## Status Flow

```
[Start] → seedance1.5pro → "original video generated"
        → infinitetalk → "final video generated"
        → DB Update → "Success"
        
Any failure → "Failed" (or last successful stage)
```

## Requirements

- Python 3
- PostgreSQL client (`psql`)
- curl
- Network access to:
  - Database: DATABASE_HOST:PORT
  - MCP: https://kansas3.8glabs.com/mcp

## CSV Format

```csv
Song Template ID,Status
template_001,Pending
template_002,Pending
```

## Output

The script updates the `song_templates` table with:
- `video_url` - Final video URL
- `video_url_seedream_v4` - Final video URL (duplicate for compatibility)
- `status` - Current processing status
