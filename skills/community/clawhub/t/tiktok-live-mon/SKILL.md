---
name: tiktok-live-mon
description: TikTok Live stream monitoring and recording automation. Uses Playwright for visual detection and network traffic monitoring to capture FLV stream URLs. Supports automatic live status checks, stream recording to disk, and notification integration.
---

# TikTok Live Monitor

Automated TikTok Live stream monitoring with Playwright-based visual detection.

## Features

- **Visual Detection:** Uses Chromium/Playwright to detect live status (red border around profile)
- **Stream URL Extraction:** Captures FLV stream URLs from network traffic
- **Automatic Recording:** Saves streams to disk when live
- **Notifications:** Alerts when stream goes live/offline

## Usage

```bash
# Check if user is live
node check-profile.js @username

# Get stream URL
node get-stream.js @username
```

## Requirements

- Node.js 16+
- Playwright with Chromium
