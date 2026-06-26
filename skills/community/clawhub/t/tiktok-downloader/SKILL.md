---
name: tiktok-downloader
description: "Download TikTok videos by URL or hashtag. Handles 403 errors, cookies, and user-agent rotation. Use for downloading TikTok videos, batch downloading from a list of URLs, or saving TikTok content for offline use."
---

# TikTok Downloader

This skill provides a robust workflow for downloading TikTok videos, overcoming common anti-bot measures like 403 Forbidden errors and login requirements.

## Core Workflow

### 1. Single Video Download
To download a specific TikTok video, use the provided script:

```bash
/home/ubuntu/skills/tiktok-downloader/scripts/download_tiktok.sh <VIDEO_URL> [OUTPUT_DIR]
```

### 2. Handling 403 Forbidden Errors
If `yt-dlp` fails with a 403 error, follow these steps:
1. **Navigate to the URL** using the browser tool to establish a session and cookies.
2. **Run the script again**. It is pre-configured to extract cookies from the browser's data directory (`/home/ubuntu/.browser_data_dir`).

### 3. Batch Downloading
For multiple videos:
1. Save all URLs to a text file (e.g., `urls.txt`).
2. Use `yt-dlp` with the following recommended flags:
   ```bash
   yt-dlp --no-warnings \
     --cookies-from-browser "chromium:/home/ubuntu/.browser_data_dir" \
     --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
     --add-header "Referer:https://www.tiktok.com/" \
     -o "%(uploader)s - %(title).80s.%(ext)s" \
     --batch-file urls.txt
   ```

## Best Practices

- **Browser Navigation**: Always visit at least one TikTok video page in the browser before starting a batch download to ensure cookies are fresh.
- **Hashtag Pages**: TikTok hashtag pages often require login. If a hashtag page fails to load, ask the user to log in via the browser or search for individual video URLs using the search tool.
- **Output Naming**: Use `%(uploader)s - %(title).80s.%(ext)s` to keep filenames organized and avoid filesystem length limits.
- **Rate Limiting**: For large batches, add `sleep` between downloads to avoid IP bans.
