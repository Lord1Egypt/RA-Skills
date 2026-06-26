---
name: video2podcast
description: Convert bookmarked videos from YouTube, X (Twitter), and other sites into a podcast RSS feed hosted on Cloudflare R2. Use when the user says things like "add this to my podcast feed", "add this video to my podcast", "sync my podcast feed", "put this YouTube video in my podcast", or "subscribe to this playlist as a podcast". Manages a persistent episode list and hosts audio files + feed.xml on Cloudflare R2.
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["ffmpeg"],
            "pip": ["yt-dlp", "boto3"],
          },
        "env":
          [
            {
              "key": "VIDPOD_R2_ACCESS_KEY",
              "description": "Cloudflare R2 API token access key",
              "required": true,
              "sensitive": true,
            },
            {
              "key": "VIDPOD_R2_SECRET",
              "description": "Cloudflare R2 API token secret",
              "required": true,
              "sensitive": true,
            },
            {
              "key": "VIDPOD_R2_ENDPOINT",
              "description": "R2 endpoint URL (https://<account_id>.r2.cloudflarestorage.com)",
              "required": true,
              "sensitive": false,
            },
            {
              "key": "VIDPOD_R2_BUCKET",
              "description": "R2 bucket name (e.g. podcast-feed)",
              "required": true,
              "sensitive": false,
            },
            {
              "key": "VIDPOD_PUBLIC_BASE",
              "description": "R2 public URL (https://pub-<hash>.r2.dev)",
              "required": true,
              "sensitive": false,
            },
            {
              "key": "VIDPOD_FEED_TITLE",
              "description": "Podcast feed title",
              "required": false,
              "sensitive": false,
            },
            {
              "key": "VIDPOD_FEED_AUTHOR",
              "description": "Podcast author name",
              "required": false,
              "sensitive": false,
            },
            {
              "key": "VIDPOD_COOKIE_BROWSER",
              "description": "Browser to read cookies from for age-restricted/SABR-protected videos (safari, chrome, firefox, or none). Default: safari. Cookies are read locally and never transmitted.",
              "required": false,
              "sensitive": false,
            },
          ],
        "install":
          [
            {
              "id": "ffmpeg",
              "kind": "brew",
              "package": "ffmpeg",
              "bins": ["ffmpeg"],
              "label": "Install ffmpeg (audio conversion)",
            },
            {
              "id": "yt-dlp",
              "kind": "pip",
              "package": "yt-dlp",
              "label": "Install yt-dlp (video downloader)",
            },
            {
              "id": "boto3",
              "kind": "pip",
              "package": "boto3",
              "label": "Install boto3 (Cloudflare R2 / S3 client)",
            },
          ],
      },
  }
---

# video-podcast

Turn any video URL into a podcast episode. Publishes a valid RSS feed to Cloudflare R2 that can be subscribed to in Apple Podcasts, Overcast, Pocket Casts, and any podcast app.

Supports YouTube, X (Twitter), and the ~1,000 other sites that [yt-dlp](https://github.com/yt-dlp/yt-dlp) supports.

---

## First-time Setup

### 1. Install dependencies

```bash
# Python packages
pip3 install yt-dlp boto3

# ffmpeg (required for audio conversion)
brew install ffmpeg        # macOS
sudo apt install ffmpeg    # Linux
```

### 2. Create a Cloudflare R2 bucket

1. Sign up at [cloudflare.com](https://cloudflare.com) (free tier is sufficient)
2. Go to **R2 Object Storage** → **Create bucket**
3. Name it anything — e.g. `podcast-feed`
4. Enable **Public access** on the bucket (R2 → bucket → Settings → Public Access → Enable)
5. Note the **r2.dev public URL** shown (e.g. `https://pub-abc123.r2.dev`)

### 3. Create an R2 API token

1. R2 → **Manage R2 API Tokens** → Create token
2. Set permissions: **Object Read & Write** on your bucket
3. Note the **Access Key ID** and **Secret Access Key**
4. Note your **Account ID** from the dashboard top-right

### 4. Configure the skill

Run the interactive setup:

```bash
python3 /path/to/skills/video-podcast/scripts/video_podcast.py setup
```

Or add these to `~/.openclaw/.env` manually:

```
VIDPOD_R2_ACCESS_KEY=your_access_key_id
VIDPOD_R2_SECRET=your_secret_access_key
VIDPOD_R2_ENDPOINT=https://<account_id>.r2.cloudflarestorage.com
VIDPOD_R2_BUCKET=podcast-feed
VIDPOD_PUBLIC_BASE=https://pub-<hash>.r2.dev

# Optional
VIDPOD_FEED_TITLE=My Video Podcast
VIDPOD_FEED_AUTHOR=Your Name
```

### 5. Add a cover image (optional but recommended)

Podcast apps display a 1400×1400px JPEG as artwork. Upload one to your bucket:

```bash
# Using AWS CLI (if installed)
aws s3 cp cover.jpg s3://podcast-feed/cover.jpg \
  --endpoint-url https://<account_id>.r2.cloudflarestorage.com \
  --content-type image/jpeg

# Or via the Cloudflare R2 dashboard — drag and drop cover.jpg into the bucket
```

The image must be named `cover.jpg` in the root of your bucket.

---

## Usage

### Add a single video

```bash
python3 video_podcast.py add "https://www.youtube.com/watch?v=..."
python3 video_podcast.py add "https://x.com/user/status/123456789"
python3 video_podcast.py add "https://vimeo.com/..."
```

### Sync a YouTube playlist

Add all videos from a playlist that aren't already in the feed:

```bash
python3 video_podcast.py sync-youtube PLxxxxxxxxxxxxxxxx
```

The playlist ID is the part after `list=` in the YouTube URL.

### List episodes

```bash
python3 video_podcast.py list
```

### Get the RSS feed URL

```bash
python3 video_podcast.py feed
```

### Remove an episode

```bash
python3 video_podcast.py remove "https://www.youtube.com/watch?v=..."
```

---

## How It Works

1. **yt-dlp** fetches the best available audio stream from the source URL — no browser automation, no screen capture.
2. **ffmpeg** converts the audio to MP3 (VBR ~130kbps).
3. The MP3 is uploaded to your **Cloudflare R2** bucket with a 7-day public cache header.
4. `feed.xml` is rebuilt and uploaded with `no-cache` headers so podcast apps always see the latest version.
5. Your podcast app polls the feed URL periodically and downloads new episodes automatically.

---

## Storage & State

| Location | Purpose |
|---|---|
| `~/.openclaw/video-podcast-state.json` | Episode list + processed URL GUIDs (deduplication) |
| R2 `<guid>.mp3` | Audio files (public, 7-day cache) |
| R2 `feed.xml` | Podcast RSS feed (public, no-cache) |
| R2 `cover.jpg` | Podcast artwork (optional) |

---

## Supported Sources

Any URL that yt-dlp supports, including:

- **YouTube** — videos and playlists
- **X (Twitter)** — public video tweets
- **Vimeo**, **SoundCloud**, **Twitch** clips, **Reddit** videos
- [Full list of 1,000+ supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

---

## Troubleshooting

**`ffmpeg not found`**
```bash
brew install ffmpeg   # macOS
sudo apt install ffmpeg  # Linux
```

**SSL errors with R2**
Make sure you're using Python 3.10+ with OpenSSL 3.x. On macOS the system Python (`/usr/bin/python3`) uses LibreSSL which may not work. Install Python via Homebrew:
```bash
brew install python@3.13
```

**Age-restricted YouTube videos**
yt-dlp needs your browser cookies:
```bash
yt-dlp --cookies-from-browser chrome "https://youtube.com/watch?v=..."
```
Then run `add` again — yt-dlp caches the cookies.

**X/Twitter videos fail**
Public tweets work without auth. Private accounts require cookies:
```bash
yt-dlp --cookies-from-browser chrome "https://x.com/user/status/..."
```

**Episode not appearing in podcast app**
Most podcast apps cache the feed for 1–24 hours. Force a refresh in the app, or check the feed directly: `python3 video_podcast.py feed`

---

## OpenClaw Agent Usage

When used via the OpenClaw agent, trigger phrases include:

- "Add this to my podcast feed: [URL]"
- "Add this video to my podcast"
- "Sync my podcast from playlist [ID]"
- "What's in my podcast feed?"
- "Remove [URL] from my podcast"

The agent will run the appropriate subcommand and report back the result.
