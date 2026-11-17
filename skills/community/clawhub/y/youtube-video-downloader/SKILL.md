---
name: youtube-video-downloader
description: YouTube Video Downloader — paste a YouTube video link and get watermark-free video download URLs instantly (multiple resolutions supported). Use when you need to download YouTube videos, save YouTube videos, or get YouTube video direct links. Triggers: YouTube video download, yt video download, youtube video download, YouTube video parser, download YouTube video, youtube download.
---

# YouTube Video Downloader

Parse YouTube video links via the [redfox.hk](https://redfox.hk/settings/api-keys?source=clawhub) API and return watermark-free video download URLs (resources may include video and audio files in various formats).

---

## Overview

- **Platform Support**: YouTube
- **Content Type**: Video/Audio (MP4 / WebM / M4A and other formats; resources may include video and audio files)
- **Input**: Paste a YouTube video link (one link per request; batch upload not supported)
- **Output**: Returns the video download URL directly — copy it into your browser or download tool to save
- **Link Display Rule**: Download and cover links must be displayed in full; never use `...` or any form of truncation
- **Field Display Rule**: The returned result must fully display the following fields:
  - Description (desc): full text displayed line by line, no truncation
  - Resource list: for each resource object, display its type, duration (durationSeconds), download link (downloadUrl), and cover link (coverUrl)
  - When the API does not return a resources array, automatically fall back to extracting top-level fields with the same names for compatibility

---

## Usage

### Example Command

Download a YouTube video:

```bash
python3 "$SKILL_PATH/scripts/downloader.py" "https://www.youtube.com/watch?v=xxxxx"
```

### First-Time Setup

Configure your API Key first, then run:

```bash
# Set environment variable
export REDFOX_API_KEY=ak_your_key

# Parse the video and get the download link
python3 "$SKILL_PATH/scripts/downloader.py" "https://www.youtube.com/watch?v=xxxxx"
```

> Visit [redfox.hk](https://redfox.hk/settings/api-keys?source=clawhub) to register and get your API Key.

### Ongoing Usage

Configuration options (choose one):

| Method | Command |
|------|------|
| **Environment Variable** (recommended) | `export REDFOX_API_KEY=ark_your_key` |
| **CLI Argument** | `python3 "$SKILL_PATH/scripts/downloader.py" "<link>" --api-key ark_your_key` |
| **Config File** | `echo '{"api_key":"ark_your_key"}' > ~/.qoder/apis/redfox.json` |

---

## Key Features

| Feature | Description |
|------|------|
| **Watermark-Free Direct Link** | API automatically returns watermark-free video download URLs |
| **Multiple Resources** | Returns multiple resources (video files, audio files, etc.); all download links listed sequentially — pick what you need |
| **Paste & Parse** | Just paste the video link — no extra steps needed |
| **Instant Results** | Parsing completes and returns the download URLs immediately — copy and use |

---

## Common Use Cases

| Scenario | Example Link | Description |
|------|----------|------|
| Save YouTube videos | `https://www.youtube.com/watch?v=xxxxx` | Get watermark-free video/audio download links |
| Offline YouTube Shorts collection | `https://www.youtube.com/shorts/xxxxx` | Parse and copy the link to download and save |
| Content remixing | Any YouTube video link | Download clips for editing and creative use |
| Asset backup | Any YouTube video link | Back up your favorite videos locally |

### Supported Link Formats

| Platform | Link Format | Example |
|------|----------|------|
| YouTube Regular Video | `https://www.youtube.com/watch?v=<videoId>` | Standard video link |
| YouTube Shorts | `https://www.youtube.com/shorts/<videoId>` | Shorts short video |
| YouTube Short Link | `https://youtu.be/<videoId>` | Share short link |

---

## FAQ

**Q: How do I get my API Key?**
A: Visit [redfox.hk](https://redfox.hk/settings/api-keys?source=clawhub) to register and obtain your token.

**Q: Does the downloaded video have a watermark?**
A: No. The API returns watermark-free video direct URLs.

**Q: Does it return multiple resources?**
A: Yes. The API typically returns multiple resources, which may include video files and audio files in different formats (such as mp4, webm, m4a, etc.). Each resource's download link is listed in full — just pick what you need.

**Q: Can I upload multiple links at once?**
A: No. Only one link can be parsed per request. Batch upload will cause parsing failure.

**Q: What if parsing fails?**
A: Make sure the link is complete, the video still exists, and is not region-restricted. Deleted or restricted videos cannot be parsed.

---

## Learn More

This tool is built on the [redfox.hk](https://redfox.hk/settings/api-keys?source=clawhub) `parseWork/videoDownload/youtube` API. Visit the official website for more API capabilities and documentation.
