# Video Content Analysis Workflow

An integrated workflow for processing video content, extracting keyframes, searching for related information, storing results in Supabase, and publishing documentation to Feishu Wiki.

## Features

- **Video Frame Extraction**: Extract keyframes at configurable intervals using ffmpeg
- **Content Search**: Automatically search the web for information related to frame content
- **Database Storage**: All metadata and results stored in Supabase Postgres database
- **Wiki Publishing**: Auto-generate analysis reports and publish directly to Feishu Wiki
- **Extensible**: Built as a ClawHub skill for easy extension and integration with other tools

## Tech Stack

- **Video Processing**: ffmpeg-python
- **Database**: Supabase (Postgres + Auth + Storage)
- **Search**: Google Custom Search API
- **Wiki**: Feishu OpenAPI
- **Language**: Python 3.10+

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy environment file and fill in credentials:
   ```bash
   cp .env.example .env
   ```

3. Set up Supabase schema:
   ```bash
   # Install Supabase CLI first
   supabase db push
   ```

## Usage

### Single video

```bash
python src/main.py single path/to/video.mp4 --user-id <uuid> --space-id <wiki-space-id>
```

### Batch processing

Process all videos in a directory:

```bash
python src/main.py batch /path/to/videos/ --user-id <uuid> --space-id <wiki-space-id>
```

With category auto-classification:

```bash
python src/main.py batch /path/to/videos/ \
  --user-id <uuid> \
  --space-id <wiki-space-id> \
  --categories '{"demo":["demo","presentation"],"tutorial":["tut","howto"]}'
```

Batch processing will:
- Discover all video files (`.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`, `.flv`, `.wmv`) in the directory
- Process each video (extract keyframes → search → store in Supabase)
- Auto-classify videos by filename keywords using the `--categories` mapping
- Publish individual analysis pages to Feishu Wiki
- Create a **category index page** per category linking to all its video analyses
- Track progress in a `batch_jobs` table in Supabase

## Workflow

1. **Upload/Input Video**: Provide path to video file
2. **Extract Keyframes**: System extracts frames at 10-second intervals
3. **Analyze Content**: (Optional) Run OCR/vision models on frames
4. **Web Search**: Search for related information about frame content
5. **Store Results**: Save all data to Supabase database
6. **Generate Report**: Create structured analysis report
7. **Publish**: Push report to Feishu Wiki

## ClawHub Skill

This tool is published as a ClawHub skill (v2.0.0 — with batch processing). Install it with:
```bash
clawhub install video-content-analyzer
```

## License

MIT