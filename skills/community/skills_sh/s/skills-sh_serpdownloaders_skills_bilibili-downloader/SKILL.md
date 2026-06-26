---
name: bilibili-downloader
description: Download Bilibili videos
---

# Bilibili Downloader — Coming Soon (Browser Extension)

> Save Bilibili videos, clips, and series as local MP4 files directly from your browser. **This extension is currently in development and has not been released yet.**

Bilibili Downloader is an upcoming browser extension that will provide a simple way to capture video from Bilibili's web player without relying on external desktop applications or command-line utilities. It is being built around the in-browser viewing experience so you can export individual videos, multi-part series, and short clips while watching on the site.

- Capture Bilibili video from the web player during playback
- Save single videos, multi-part episode series, and user-uploaded clips
- Export video as standard MP4 files for offline viewing
- Handle browser-based streaming workflows without extra desktop software
- Designed for Chrome, Edge, Brave, Opera, Firefox, and other Chromium browsers

## Status

**This extension is not yet available for download.** Development is in progress and a release date has not been announced. Sign up below to get notified when it launches.

:bell: **Get notified when this launches:** [Join the waitlist](https://serp.ly/bilibili-downloader)

## Links

- :hourglass_flowing_sand: Waitlist: [Coming Soon — Sign Up](https://serp.ly/bilibili-downloader)
- :question: Help center: [SERP Help](https://help.serp.co/en/)
- :bulb: Request features: [GitHub Issues](https://github.com/serpapps/bilibili-downloader/issues)

## Preview

![Bilibili Downloader hero image](https://raw.githubusercontent.com/serpapps/bilibili-downloader/refs/heads/main/assets/workflow-preview.webp)

## Table of Contents

- [Why Bilibili Downloader](#why-bilibili-downloader)
- [Planned Features](#planned-features)
- [How It Will Work](#how-it-will-work)
- [Expected Formats](#expected-formats)
- [Who It's For](#who-its-for)
- [Use Cases We're Building For](#use-cases-were-building-for)
- [FAQ](#faq)
- [License](#license)
- [Notes](#notes)
- [About Bilibili](#about-bilibili)

## Why Bilibili Downloader

Bilibili delivers video through adaptive streaming that splits audio and video into separate encrypted tracks, making it impossible to right-click and save a file from the page. The platform offers a limited offline cache inside its mobile app, but there is no native way to download a standard video file to your computer for local playback or archiving.

Bilibili Downloader is being designed to operate inside the browser alongside the Bilibili web player. The goal is to detect the active video stream, let you choose your preferred resolution, and merge the audio and video tracks into a single MP4 file that you can keep on your hard drive and play in any media player.

## Planned Features

- Video capture from Bilibili's web player during active playback
- Single video and multi-part series export support
- Resolution selection covering available quality tiers up to 1080p and beyond
- Automatic merging of separated audio and video streams into one MP4
- Danmaku (scrolling comment) overlay export as a sidecar subtitle file
- Download queue for saving multiple videos without waiting between each one
- Browser-native workflow with no external software dependencies
- Cross-browser compatibility targeting Chrome, Edge, Brave, and Firefox

## How It Will Work

1. Install the extension once it is released.
2. Open Bilibili in your browser and sign in to your account.
3. Navigate to the video, series, or clip you want to save.
4. Begin playback so the browser loads the video stream.
5. Open the extension popup to see the detected video source.
6. Select the video or episode you want to export.
7. Choose your preferred resolution if multiple quality levels are available.
8. Start the download and save the MP4 file to your local machine.

## Expected Formats

- Input: Bilibili web player video streams (DASH adaptive streams with separated audio and video tracks)
- Output: MP4 with merged audio and video in a single file

Exported files will be saved as standard MP4 containers compatible with most media players, mobile devices, and video editing applications.

## Who It's For

- Anime and donghua fans who want offline copies of shows they follow on the platform
- Language learners studying Mandarin through Bilibili's educational and entertainment videos
- Gaming enthusiasts who want to save tournament streams, walkthroughs, and commentary
- Researchers and students archiving lectures, tutorials, and documentary content
- Content creators collecting reference material from the platform for study or commentary

## Use Cases We're Building For

- Save an entire multi-part lecture or tutorial series for offline study
- Archive favorite music videos and concert performances before they become unavailable
- Keep local copies of anime episodes from your watchlist for travel or low-connectivity situations
- Download educational content for use in classrooms or presentations where internet access is limited
- Build a personal offline library of cooking, art, or technology videos for reference

## Security & Scope

- Operates only on the page the user intentionally opens in the active browser tab
- Detects supported playback sources only for user-initiated downloads or exports
- Does not execute page instructions, shell commands, or arbitrary scripts from page content
- Does not follow unrelated links or perform actions outside the active workflow
- Limits support to the named platform, approved embedded contexts, and user-authorized sessions when required

## FAQ

**When will Bilibili Downloader be released?**
A release date has not been set. Sign up at the waitlist link above to be notified as soon as it is available.

**Will it work with the Bilibili mobile app?**
No. This extension is built for the Bilibili website in a desktop browser, not the mobile application.

**What video quality will it support?**
Quality will depend on what the Bilibili web player delivers to the browser, which varies by account level and whether you have a premium membership.

**Will it save danmaku (scrolling comments)?**
Danmaku export is a planned feature. The goal is to save the scrolling comments as a sidecar subtitle file alongside the video.

**Is it free?**
Pricing details will be announced closer to launch. SERP extensions typically include a free trial period.

**Can I download multi-part series at once?**
Batch downloading across a multi-part video series is a planned feature, though the exact workflow will depend on browser and streaming constraints.

## License

This repository is distributed under the proprietary SERP Apps license in the [LICENSE](https://raw.githubusercontent.com/serpapps/bilibili-downloader/refs/heads/main/LICENSE) file. Review that file before copying, modifying, or redistributing any part of this project.

## Notes

- This extension is in development and is not available for download yet
- Only download content you own or have explicit permission to save
- Video quality will depend on the source stream exposed by Bilibili's web player and your account tier
- Bilibili platform changes may affect functionality once released
- An active Bilibili account and internet connection will be required

## About Bilibili

Bilibili is a major Chinese video sharing platform known for its anime, gaming, music, and educational content. It features a distinctive scrolling comment system called danmaku that overlays real-time viewer reactions on top of the video. The platform hosts both user-generated content and professionally licensed media, but does not provide a built-in option to export videos as local files. Bilibili Downloader is being built to fill that gap for users who want a standard MP4 copy of video they already have access to through their account.
