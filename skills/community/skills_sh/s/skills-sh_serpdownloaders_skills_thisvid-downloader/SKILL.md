---
name: thisvid-downloader
description: Download ThisVid Videos & Save them to your computer | ThisVid Downloader Browser Extension (Chrome, Firefox, Edge, Opera, Brave)
---

# ThisVid Downloader (Browser Extension)

> Download ThisVid videos as MP4 files directly from supported pages in your browser.

ThisVid Downloader is a browser extension for saving supported ThisVid videos without switching to network inspectors, scripts, or external download tools. It detects the media stream used by the player, shows available quality options when present, and exports the final file as MP4 for offline playback.

- Save supported ThisVid videos from watch pages
- Detect available resolutions exposed by the player
- Download MP4 output for easier playback across devices
- Skip generic downloaders that miss the main stream
- Keep the workflow simple and browser-based

## Links

- :rocket: Get it here: [ThisVid Downloader](https://serp.ly/thisvid-downloader)
- :new: Latest release: [GitHub Releases](https://github.com/serpapps/thisvid-downloader/releases/latest)
- :question: Help center: [SERP Help](https://help.serp.co/en/)
- :beetle: Report bugs: [GitHub Issues](https://github.com/serpapps/thisvid-downloader/issues)
- :bulb: Request features: [Feature Requests](https://github.com/serpapps/thisvid-downloader/issues)

## Preview

![ThisVid Downloader workflow preview](https://raw.githubusercontent.com/serpapps/thisvid-downloader/refs/heads/main/assets/workflow-preview.webp)

## Table of Contents

- [Why ThisVid Downloader](#why-thisvid-downloader)
- [Features](#features)
- [How It Works](#how-it-works)
- [Step-by-Step Tutorial: How to Download Videos from ThisVid](#step-by-step-tutorial-how-to-download-videos-from-thisvid)
- [Supported Formats](#supported-formats)
- [Who It's For](#who-its-for)
- [Common Use Cases](#common-use-cases)
- [Troubleshooting](#troubleshooting)
- [Trial & Access](#trial--access)
- [Installation Instructions](#installation-instructions)
- [FAQ](#faq)
- [License](#license)
- [Notes](#notes)
- [About ThisVid](#about-thisvid)

## Why ThisVid Downloader

ThisVid pages can vary a lot because uploads come from different sources and the site can expose either direct files or streaming variants. That makes generic tools unreliable. They often grab the wrong asset, miss the quality selector, or fail when playback only initializes after user interaction.

ThisVid Downloader is designed for that real workflow. Start the page, let the extension detect the stream, then export the version you want without leaving the browser.

## Features

- Detects supported ThisVid video streams from active pages
- Flashvars extraction and real-time HLS interception for reliable detection
- In-page download button built into the video player
- Reads available resolution variants when the source exposes them
- Right-click context menu for quick downloads
- Exports MP4 files for offline viewing
- Automatic saving into a dedicated THISVID folder
- Desktop notifications when downloads complete
- Works on Chrome, Edge, Brave, Opera, Firefox, Whale, and Yandex

## How It Works

1. Install the extension from the latest release.
2. Open ThisVid and visit a video page.
3. Start playback so the extension can detect the stream.
4. Open the popup or use the in-page download button.
5. Choose the quality or stream option you want.
6. Download the video as MP4.
7. Save the final file locally.

## Step-by-Step Tutorial: How to Download Videos from ThisVid

1. Install ThisVid Downloader from the latest GitHub release.
2. Open ThisVid and sign in if the page you want requires account access.
3. Visit the video page you want to keep.
4. Let the player load fully and press play.
5. Click the in-page download button on the player, or open the extension popup.
6. Wait for the video source to appear in the popup.
7. Select the resolution you want if multiple options are listed.
8. Start the download and wait for the MP4 export to finish.
9. Open the saved file from your Downloads folder.

## Supported Formats

- Input: supported ThisVid video streams (HLS, direct MP4)
- Output: MP4

Saved files use MP4 so they are easier to replay on standard media players, move between devices, or archive locally.

## Who It's For

- ThisVid viewers who want offline access to supported videos
- Users who need a cleaner alternative to manual stream extraction
- People archiving videos they are permitted to keep
- Non-technical users who want a simple browser extension workflow
- Anyone who wants cleaner download controls than generic downloader sites

## Common Use Cases

- Save a ThisVid video for later viewing
- Export the best available quality as MP4
- Avoid manually parsing player code for source URLs
- Keep local copies of videos you can already watch in the browser
- Use the in-page button or right-click menu for a faster download flow

## Troubleshooting

**The extension does not find the video**
Press play first and wait for the player to fully load.

**The download option appears empty**
Refresh the page and retry after playback starts again.

**Only one quality is listed**
Some uploads expose only one source. The extension can only list what the page provides.

**The download stopped partway through**
Check whether your internet connection dropped during the download.

**The page requires account access**
The extension only works on media you can already open and play in your active browser session.

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

Start here: [https://serp.ly/thisvid-downloader](https://serp.ly/thisvid-downloader)

## Installation Instructions

1. Open the latest release page: [GitHub Releases](https://github.com/serpapps/thisvid-downloader/releases/latest)
2. Download the correct build for your browser.
3. Install the extension.
4. Open a ThisVid watch page.
5. Use the popup to detect and download the media.

## FAQ

**Can I save ThisVid videos as MP4?**
Yes. Supported videos are exported as MP4 files.

**Do I need extra software?**
No. Everything runs through the browser extension.

**Where are videos saved?**
They are saved to your default Downloads location, typically inside a THISVID subfolder.

**What quality options are available?**
The extension detects all available qualities from flashvars and HLS playlists. Formats are sorted by quality with MP4 preferred over HLS.

**Does this work on Firefox?**
Yes. It supports Chrome, Edge, Brave, Opera, Whale, Yandex, and Firefox.

**Will it work on every upload?**
It works on supported playback flows. Availability depends on how that specific page exposes the media.

## License

This repository is distributed under the proprietary SERP Apps license in the [LICENSE](https://raw.githubusercontent.com/serpapps/thisvid-downloader/refs/heads/main/LICENSE) file. Review that file before copying, modifying, or redistributing any part of this project.

## Notes

- Only download content you own or have explicit permission to save
- An internet connection is required for downloads
- Must press play before the extension can detect the video stream
- Quality depends on the media exposed by ThisVid
- Source quality varies by upload since ThisVid hosts user-submitted content

## About ThisVid

ThisVid hosts user-uploaded videos with varying qualities and player behaviors from page to page. ThisVid Downloader is built to make supported downloads easier for users who already have access to the content in their browser.
