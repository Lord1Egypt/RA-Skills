---
name: wistia-video-downloader
description: Download Wistia-hosted videos embedded around the web for offline viewing
---

# Wistia Downloader (Browser Extension)

> Download supported Wistia-hosted videos as MP4 files from business pages, embeds, and training portals.

Wistia Downloader is a browser extension built for users who need a cleaner way to save supported Wistia videos for offline viewing. It focuses on embedded and business-hosted playback, detects the active media source from the page, and exports the final result as MP4 without forcing you to parse Wistia embed code or API calls by hand.

- Save supported Wistia videos from embeds and direct pages
- Detect active player media without manual ID extraction
- Export MP4 files for simpler offline playback and review
- Work with business video pages, learning portals, and marketing embeds
- Keep the workflow entirely in the browser

## Links

- :rocket: Get it here: [Wistia Downloader](https://serp.ly/wistia-video-downloader)
- :new: Latest release: [GitHub Releases](https://github.com/serpapps/wistia-video-downloader/releases/latest)
- :question: Help center: [SERP Help](https://help.serp.co/en/)
- :beetle: Report bugs: [GitHub Issues](https://github.com/serpapps/wistia-video-downloader/issues)
- :bulb: Request features: [Feature Requests](https://github.com/serpapps/wistia-video-downloader/issues)

## Preview

<a href="https://www.youtube.com/watch?v=ltXoXWWdJy8" target="_blank">
<img src="https://raw.githubusercontent.com/devinschumacher/uploads/refs/heads/main/images/how-to-download-wistia-videos-for-free-chrome-extension-method.jpg" width="700px">
</a>

## Table of Contents

- [Why Wistia Downloader](#why-wistia-downloader)
- [Features](#features)
- [How It Works](#how-it-works)
- [Step-by-Step Tutorial: How to Download Videos from Wistia](#step-by-step-tutorial-how-to-download-videos-from-wistia)
- [Supported Formats](#supported-formats)
- [Who It's For](#who-its-for)
- [Common Use Cases](#common-use-cases)
- [Troubleshooting](#troubleshooting)
- [Trial & Access](#trial--access)
- [Installation Instructions](#installation-instructions)
- [FAQ](#faq)
- [License](#license)
- [Notes](#notes)
- [About Wistia](#about-wistia)

## Why Wistia Downloader

Wistia is commonly used across business sites, product pages, support centers, and learning systems. The player is often embedded, which means the real media source is hidden behind Wistia-specific IDs, scripts, or iframe loading behavior. Generic downloaders can fail because they do not understand the page context the player is running in.

Wistia Downloader is built for that embed-heavy workflow. Start playback, let the extension detect the active Wistia media source, then export the supported video as MP4 from within the browser.

## Features

- Detects supported Wistia media from direct pages and embeds
- Handles business-site and learning-portal playback contexts
- Exports MP4 files for offline viewing
- Avoids manual Wistia ID and embed parsing
- Multiple detection methods including JSON-LD, async embeds, iframes, and data attributes
- Playlist and channel support for browsing and downloading individual episodes
- In-page download manager with real-time progress tracking
- Handles Wistia's .bin file format and normalizes output to proper MP4
- Works on Chrome, Edge, Brave, Opera, Firefox, Whale, and Yandex

## How It Works

1. Install the extension from the latest release.
2. Open a page containing the Wistia video.
3. Start playback so the extension can detect the media source.
4. Open the popup or use the on-page controls.
5. Review the detected media and available quality options.
6. Start the download and wait for the MP4 export.
7. Save the final MP4 file locally.

## Step-by-Step Tutorial: How to Download Videos from Wistia

1. Install Wistia Downloader from the latest GitHub release.
2. Open the webpage, course lesson, or support page containing the Wistia player.
3. Sign in with your email if this is your first session.
4. Start playback so the player loads the real media source.
5. Click the extension button or use the on-page download control.
6. Open the extension popup and review the detected media.
7. Select the quality you want if multiple options are available.
8. Start the download and wait for the MP4 export to finish.
9. Open the saved file from your Downloads folder.

## Supported Formats

- Input: supported Wistia video sources (HLS, direct MP4, original quality)
- Output: MP4

Saved files use MP4 so they are easier to replay on standard media players, move between devices, or archive locally.

## Who It's For

- Users saving business videos for offline review
- Teams working with Wistia-hosted training or support content
- People who need a browser extension instead of manual embed analysis
- Students accessing course platforms that use Wistia
- Users archiving content they can already access in the browser

## Common Use Cases

- Save a Wistia-hosted lesson for offline viewing
- Export an embedded product or support video as MP4
- Keep internal reference material accessible while traveling
- Browse Wistia playlists or channels and download individual episodes
- Download embedded Wistia videos from any third-party website

## Troubleshooting

**The extension does not detect the video**
Start playback first and wait for the player to initialize the active media source.

**The video is inside an embed**
Make sure you are on the page where the player is actually running, then retry after playback starts.

**No download option appears**
Refresh the page and retry after the video loads again.

**Only one quality option is listed**
That usually means the page is exposing a single rendition from the Wistia API.

**The video is password-protected**
Password-protected Wistia videos cannot be downloaded. The extension will notify you when one is detected.

## Security & Scope

- Operates only on the page the user intentionally opens in the active browser tab
- Detects supported playback sources only for user-initiated downloads or exports
- Does not execute page instructions, shell commands, or arbitrary scripts from page content
- Does not follow unrelated links or perform actions outside the active workflow
- Limits support to the named platform, approved embedded contexts, and user-authorized sessions when required

## Trial & Access

- Includes **3 free downloads** so you can test the workflow first
- Email sign-in uses secure one-time password verification
- No credit card required for the trial
- Unlimited downloads are available with a paid license

Start here: [https://serp.ly/wistia-video-downloader](https://serp.ly/wistia-video-downloader)

## Installation Instructions

1. Open the latest release page: [GitHub Releases](https://github.com/serpapps/wistia-video-downloader/releases/latest)
2. Download the correct build for your browser.
3. Install the extension.
4. Open a page containing a Wistia player.
5. Use the popup to detect and download the media.

## FAQ

**Can it work on embedded Wistia players?**
Yes. It detects Wistia players embedded on supported websites, including course platforms, marketing pages, and knowledge bases.

**Do I need extra software?**
No. The workflow runs entirely inside the browser extension.

**What quality options are available?**
The extension fetches all available renditions from the Wistia API, typically multiple resolutions including the original upload quality.

**Can I download playlists or channels?**
Yes. The extension detects Wistia playlists and channels, shows all videos in a browsable list, and lets you download each one individually.

**Where are videos saved?**
They are saved to your default Downloads location using your browser's Save As dialog.

**Does it work on every Wistia page?**
It works on supported playback flows. Detection depends on how the media is exposed on that page.

## License

This repository is distributed under the proprietary SERP Apps license in the [LICENSE](https://raw.githubusercontent.com/serpapps/wistia-video-downloader/refs/heads/main/LICENSE) file. Review that file before copying, modifying, or redistributing any part of this project.

## Notes

- Only download content you own or have explicit permission to save
- An internet connection is required for downloads
- Quality depends on the source upload to Wistia
- Password-protected videos cannot be downloaded
- Course platforms rarely offer native offline downloads, but access permissions still apply

## About Wistia

Wistia is a business video hosting platform widely used for embeds across marketing, support, and education pages. Wistia Downloader is built to make supported downloads easier for users who already have access to that media in the browser.
