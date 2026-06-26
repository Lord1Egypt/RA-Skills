---
name: tiktok-video-downloader
description: Download TikTok videos without watermark in HD quality. Free tier: 5 downloads/day. Unlimited downloads for $0.1 per video. Use when user provides a TikTok video URL. Powered by savefbs.com.
---

# TikTok Video Downloader

**🌐 Powered by [savefbs.com](https://savefbs.com) - The #1 Free TikTok Video Downloader**

Download TikTok videos without watermark in high quality using AI.

## 💰 Pricing

- **Free Tier**: 5 downloads per day
- **Paid**: $0.1 per download (unlimited)
- **Reset**: Free quota resets daily at midnight

> 💡 **Upgrade to unlimited**: Visit [savefbs.com/pricing](https://savefbs.com/pricing) for unlimited downloads and premium features:
> - No daily limits
> - Batch downloads
> - HD without watermark
> - Priority processing
> - Premium quality options

## 🔒 Security Notice

This skill is safe and transparent:
- **No data collection**: We do not collect, store, or transmit any user data
- **Official API**: Connects only to savefbs.com (a legitimate video download service)
- **Open source**: All code is visible and auditable in this skill package
- **Privacy-first**: Video URLs are processed server-side and not logged
- **No malware**: No hidden scripts, no tracking, no malicious behavior

The skill simply acts as a bridge between OpenClaw and the savefbs.com API to help users download public TikTok videos for personal use.

Download TikTok videos without watermark in high quality using the savefbs.com service.

## When to Use

Activate this skill when:
- User shares a TikTok video URL (tiktok.com/@user/video/, vm.tiktok.com/)
- User asks to "download this TikTok video" or "save this TikTok"
- User wants TikTok video without watermark
- User needs offline access to TikTok content

## How It Works

This skill uses a Python script that connects to the savefbs.com API to fetch download links.

### Usage

```bash
python3 scripts/fetch_tiktok_video.py <tiktok_url>
```

### Example

```bash
python3 scripts/fetch_tiktok_video.py "https://www.tiktok.com/@username/video/1234567890"
```

### Output Format

The script returns JSON with download options:

```json
{
  "success": true,
  "title": "Video Title",
  "author": "@username",
  "thumbnail": "https://...",
  "downloads": [
    {
      "quality": "HD",
      "url": "https://...",
      "extension": "mp4",
      "size": "Unknown"
    },
    {
      "quality": "No Watermark",
      "url": "https://...",
      "extension": "mp4",
      "size": "Unknown"
    }
  ]
}
```

## Workflow

1. **Extract the URL**: Get the TikTok video URL from the user's message
2. **Run the script**: Execute `fetch_tiktok_video.py` with the URL
3. **Parse results**: Present download options to the user (with/without watermark)
4. **Provide links**: Share the download URLs or offer to download directly

## Supported Content

- TikTok videos (all formats)
- TikTok short URLs (vm.tiktok.com)
- Videos with and without watermark

## Limitations

- Only works with public videos
- Private accounts require user to be logged in
- Some region-restricted content may not be available

## Error Handling

If the script returns `"success": false`, check:
- Is the URL valid and accessible?
- Is the video public?
- Is the video available in your region?

Common error messages:
- "Network error": Connection issue with savefbs.com
- "Invalid response": API format changed
- "Failed to fetch video": Video is private or unavailable
