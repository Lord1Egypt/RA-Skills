# STH Video Template Generation Skill

Generate videos for Sing The Hook (STH) song templates using a two-stage video generation pipeline.

## Overview

This skill processes song template IDs from a CSV file, fetches data from PostgreSQL, generates videos via Imagine MCP, and updates the database with results. All videos are generated in **9:16 (vertical)** aspect ratio by default.

## Setup & Environment Variables

This skill requires the following environment variables to be set in your OpenClaw environment:

| Variable | Description | Default |
|----------|-------------|---------|
| `STH_DB_HOST` | PostgreSQL Host | `localhost` |
| `STH_DB_PORT` | PostgreSQL Port | `5432` |
| `STH_DB_NAME` | PostgreSQL Database Name | `sth_db` |
| `STH_DB_USER` | PostgreSQL Username | `postgres` |
| `STH_DB_PASSWORD` | PostgreSQL Password | (Required) |
| `STH_MCP_ENDPOINT` | Imagine MCP API Endpoint | (Required) |
| `STH_MCP_API_KEY` | Imagine MCP API Key | (Required) |
| `STH_GCS_KEY_PATH` | Path to GCS Service Account JSON key | (Required for uploads) |
| `STH_NOTIFY_TARGET` | Telegram ID for notifications | (Optional) |

## Workflow

### Step 1: Parse Input CSV

Read the CSV file provided by the user. Expected columns:
- `Song Template ID` - The template ID to process
- `Status` - Current status (will be updated)

### Step 2: Generate Video Pipeline

1. **Check Audio Duration**: Downloads audio mix and checks duration using `ffprobe`.
2. **Generate Original Video**: Calls MCP `create-video` (Stage 1).
3. **Generate Final Video (infinitetalk)**: Lip-syncs video to audio (Stage 2).
4. **Trim Video**: Trims video to match exact audio duration.
5. **Upload to GCS**: Stores final video in Google Cloud Storage.
6. **Update Database**: Saves final video URLs to `song_templates` table.

## Usage

When the user asks to generate video templates for STH:

1. Ask for the CSV file or content.
2. Run the generator script:
   ```bash
   python3 sth_video_generator.py <csv_file>
   ```

## Dependencies

Install required Python packages:
```bash
pip3 install google-cloud-storage
```

Requires `ffmpeg` and `psql` to be installed on the host system.
