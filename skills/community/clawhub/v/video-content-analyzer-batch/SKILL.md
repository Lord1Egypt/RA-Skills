---
name: video-content-analyzer
version: 2.0.0
description: Analyze video content, extract keyframes, search web for references, generate Feishu Wiki reports. Supports batch directory processing with category-based publishing.
author: ClawHub Team
license: MIT
tags: [video, analysis, wiki, search, supabase, batch]
---

# Video Content Analyzer

An integrated workflow for processing video content — extract keyframes, search for related information, store results in Supabase, and publish documentation to Feishu Wiki.

## Skills

### `process_video` — Single video analysis

Process a single video file: extract keyframes, search the web for related info, store in Supabase, publish analysis report to Feishu Wiki.

**Parameters:**
- `video_path` (string, required): Path to the input video file
- `user_id` (string, required): UUID of the user running the analysis
- `space_id` (string, required): Feishu Wiki space ID for publishing

### `batch_process` — Batch directory processing

Process all videos in a directory, auto-classify by filename keywords, store results in Supabase `batch_jobs` table, and publish categorized analysis reports to Feishu Wiki.

**Parameters:**
- `directory` (string, required): Path to directory containing video files
- `user_id` (string, required): UUID of the user running the analysis
- `space_id` (string, required): Feishu Wiki space ID for publishing
- `categories` (object, optional): Mapping of category names to keyword lists for auto-classification
  - Example: `{"demo": ["demo", "presentation"], "tutorial": ["tut", "howto"]}`
- `interval_seconds` (integer, optional): Keyframe extraction interval in seconds (default: 10)

**Supported video formats:** `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`, `.flv`, `.wmv`

**Batch workflow:**
1. Discover all video files in the specified directory
2. Process each video (keyframe extraction → web search → Supabase storage)
3. Auto-classify videos by filename keywords using the `categories` mapping
4. Publish individual analysis pages to Feishu Wiki
5. Create a category index page per category linking to all its video analyses
6. Track progress in `batch_jobs` table in Supabase

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SUPABASE_URL` | Yes | Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Yes | Supabase service role key |
| `GOOGLE_API_KEY` | Yes | Google Custom Search API key |
| `GOOGLE_SEARCH_ENGINE_ID` | Yes | Google Custom Search engine ID |
| `FEISHU_APP_ID` | Yes | Feishu app ID |
| `FEISHU_APP_SECRET` | Yes | Feishu app secret |
| `FRAMES_OUTPUT_DIR` | No | Directory for extracted frames (default: `./extracted_frames`) |

## CLI Usage

```bash
# Single video
python src/main.py single path/to/video.mp4 --user-id <uuid> --space-id <space-id>

# Batch processing
python src/main.py batch /path/to/videos/ --user-id <uuid> --space-id <space-id>

# Batch with categories
python src/main.py batch /path/to/videos/ \
  --user-id <uuid> \
  --space-id <space-id> \
  --categories '{"demo":["demo","presentation"],"tutorial":["tut","howto"]}'
```