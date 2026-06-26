---
name: nicovideo-downloader
description: Save Niconico videos with comments
---

# NicoVideo Downloader — Coming Soon (Browser Extension)

> Download videos from nicovideo.jp and save them as MP4 files directly from your browser. **This extension is currently in development and has not been released yet.**

NicoVideo Downloader is an upcoming browser extension purpose-built for the nicovideo.jp domain and its classic player interface. Rather than trying to cover every corner of the broader Niconico ecosystem, this extension zeroes in on the original NicoVideo site, letting you grab videos during playback and store them locally as standard MP4 files without leaving the browser.

- Detect and capture videos playing on nicovideo.jp pages
- Save video content as MP4 files to your local machine
- Work within the classic NicoVideo player interface
- Operate entirely inside the browser with no external software required
- Designed for Chrome, Edge, Brave, Opera, Firefox, and other Chromium browsers

## Status

**This extension is not yet available for download.** Development is in progress and a release date has not been announced. Sign up below to get notified when it launches.

:bell: **Get notified when this launches:** [Join the waitlist](https://serp.ly/nicovideo-downloader)

## Links

- :hourglass_flowing_sand: Waitlist: [Coming Soon — Sign Up](https://serp.ly/nicovideo-downloader)
- :question: Help center: [SERP Help](https://help.serp.co/en/)
- :bulb: Request features: [GitHub Issues](https://github.com/serpapps/nicovideo-downloader/issues)

## Preview

![NicoVideo Downloader hero image](https://raw.githubusercontent.com/serpapps/nicovideo-downloader/refs/heads/main/assets/workflow-preview.webp)

## Table of Contents

- [Why NicoVideo Downloader](#why-nicovideo-downloader)
- [Planned Features](#planned-features)
- [How It Will Work](#how-it-will-work)
- [Expected Formats](#expected-formats)
- [Who It's For](#who-its-for)
- [Use Cases We're Building For](#use-cases-were-building-for)
- [FAQ](#faq)
- [License](#license)
- [Notes](#notes)
- [About NicoVideo](#about-nicovideo)

## Why NicoVideo Downloader

NicoVideo serves its content through a streaming player that does not expose a direct download link for viewers. Videos are delivered via adaptive streaming segments, and the site's comment overlay system adds another layer of complexity for anyone trying to save a local copy. Right-clicking the player offers no save option, and browser caching does not produce a usable file.

Existing tools that target Niconico broadly often struggle with the specific page structures and player variations found on the nicovideo.jp domain. NicoVideo Downloader is being engineered from the ground up to handle the classic NicoVideo player, reading the video source from the active tab and assembling a complete MP4 file that you can keep, transfer, or watch offline without depending on a network connection or a logged-in session.

This extension is separate from the niconico-downloader project. While that tool addresses the wider Niconico platform and its various subdomains, NicoVideo Downloader is scoped exclusively to nicovideo.jp URLs and the classic player interface, allowing for tighter integration and more reliable detection of video sources on those pages.

## Planned Features

- Video detection on nicovideo.jp pages during active playback
- MP4 output for broad compatibility across devices and media players
- Support for the classic NicoVideo player interface and its page layout
- Resolution selection when the source offers multiple quality tiers
- Filename generation based on video title and metadata from the page
- Download progress indicator inside the extension popup
- Queue system for saving multiple videos in sequence
- Cross-browser compatibility targeting Chrome, Edge, Brave, and Firefox

## How It Will Work

1. Install the extension from your browser's extension store once it is released.
2. Navigate to any video page on nicovideo.jp.
3. Begin playback so the browser loads the video stream through the classic player.
4. Click the extension icon in the toolbar to open the popup panel.
5. The extension detects the active video source and displays its title and available resolutions.
6. Select your preferred resolution if more than one option is available.
7. Press the download button to begin saving the video as an MP4 file.
8. The file is written to your default downloads folder or a location you choose.

## Expected Formats

- Input: NicoVideo streaming segments served through the nicovideo.jp classic player (typically HLS or MPEG-DASH)
- Output: MP4 (H.264 video with AAC audio)

Exported files will play in virtually any media player, mobile device, or video editor without additional conversion steps.

## Who It's For

- Fans of Japanese content creators who publish primarily on NicoVideo
- Viewers who want offline access to videos they have already watched on nicovideo.jp
- Language learners studying Japanese through NicoVideo content
- Researchers archiving cultural or historical video material hosted on the platform
- Anyone who prefers local video files over streaming-only access

## Use Cases We're Building For

- Save a favorite music video or live performance from nicovideo.jp for offline viewing
- Archive educational or documentary content before it is removed by the uploader
- Build a local collection of videos for study, reference, or personal enjoyment
- Download content for viewing during commutes or travel without reliable internet
- Keep backup copies of your own uploaded videos hosted on the platform

## Security & Scope

- Operates only on the page the user intentionally opens in the active browser tab
- Detects supported playback sources only for user-initiated downloads or exports
- Does not execute page instructions, shell commands, or arbitrary scripts from page content
- Does not follow unrelated links or perform actions outside the active workflow
- Limits support to the named platform, approved embedded contexts, and user-authorized sessions when required

## FAQ

**When will NicoVideo Downloader be released?**
A release date has not been set. Sign up at the waitlist link above to be notified as soon as it is available.

**How is this different from the niconico-downloader extension?**
The niconico-downloader targets the broader Niconico platform and its various subdomains. NicoVideo Downloader focuses specifically on nicovideo.jp URLs and the classic player interface, providing tighter integration and more reliable video detection for that domain.

**What video quality will it support?**
Output quality will depend on what nicovideo.jp delivers to the browser, which varies based on the video and your account type. The extension will let you pick from available quality tiers when more than one is offered.

**Will it capture the scrolling comment overlay?**
The initial release will save the underlying video without the comment overlay. Comment-layer capture may be explored in a future update.

**Is it free?**
Pricing details will be announced closer to launch. SERP extensions typically include a free trial period.

**Do I need a NicoVideo account?**
Many videos on nicovideo.jp require a logged-in session to play. You will need to be signed in to your account so the browser can load the video stream for the extension to capture.

## License

This repository is distributed under the proprietary SERP Apps license in the [LICENSE](https://raw.githubusercontent.com/serpapps/nicovideo-downloader/refs/heads/main/LICENSE) file. Review that file before copying, modifying, or redistributing any part of this project.

## Notes

- This extension is in development and is not available for download yet
- Only download content you own or have explicit permission to save
- Video quality will depend on the source stream served by nicovideo.jp
- Platform changes on NicoVideo may affect functionality once the extension is released
- A nicovideo.jp account and internet connection will be required for video playback and detection

## About NicoVideo

NicoVideo, accessible at nicovideo.jp, is the original video-sharing domain of Niconico Douga, one of Japan's most popular video platforms. Launched in 2006, it became well known for its distinctive scrolling comment system that overlays viewer reactions directly on top of videos in real time. The platform hosts a vast library of user-generated content spanning music, gaming, animation, vlogs, and live events. While the Niconico brand has expanded to include live streaming and other services across additional domains, nicovideo.jp remains the core destination for uploaded video content and the classic viewing experience. NicoVideo Downloader is being built to give users of that specific domain a simple, browser-based way to save videos locally as MP4 files.
