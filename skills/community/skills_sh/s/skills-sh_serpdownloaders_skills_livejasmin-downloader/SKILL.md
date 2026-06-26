---
name: livejasmin-downloader
description: Record LiveJasmin private shows and cam sessions automatically
---

# LiveJasmin Downloader — Coming Soon (Browser Extension)

> Record and save LiveJasmin live cam streams as MP4 files directly from your browser. **This extension is currently in development and has not been released yet.**

LiveJasmin Downloader is an upcoming browser extension that will allow users to capture live video streams from the LiveJasmin platform without relying on third-party screen recorders or desktop applications. It is being built to work within the browser tab where the stream is playing, providing a single-click recording workflow that outputs standard MP4 files to your local machine.

- Record live cam streams from LiveJasmin in real time within the browser
- Save captured video as MP4 files to local storage
- Control recording start, stop, and duration from the extension popup
- Operate entirely inside the browser with no external software required
- Designed for Chrome, Edge, Brave, Opera, Firefox, and other Chromium browsers

## Status

**This extension is not yet available for download.** Development is in progress and a release date has not been announced. Sign up below to get notified when it launches.

:bell: **Get notified when this launches:** [Join the waitlist](https://serp.ly/livejasmin-downloader)

## Links

- :hourglass_flowing_sand: Waitlist: [Coming Soon — Sign Up](https://serp.ly/livejasmin-downloader)
- :question: Help center: [SERP Help](https://help.serp.co/en/)
- :bulb: Request features: [GitHub Issues](https://github.com/serpapps/livejasmin-downloader/issues)

## Preview

![LiveJasmin Downloader hero image](https://raw.githubusercontent.com/serpapps/livejasmin-downloader/refs/heads/main/assets/workflow-preview.webp)

## Table of Contents

- [Why LiveJasmin Downloader](#why-livejasmin-downloader)
- [Planned Features](#planned-features)
- [How It Will Work](#how-it-will-work)
- [Expected Formats](#expected-formats)
- [Who It's For](#who-its-for)
- [Use Cases We're Building For](#use-cases-were-building-for)
- [FAQ](#faq)
- [License](#license)
- [Notes](#notes)
- [About LiveJasmin](#about-livejasmin)

## Why LiveJasmin Downloader

LiveJasmin delivers live video through adaptive streaming protocols in the browser, and the platform does not offer any native option to save or download a stream for later viewing. Once a live session ends, the content is no longer accessible unless the performer has separately uploaded a recorded segment. There is no right-click save, no built-in DVR, and no export button.

Existing workarounds typically involve full-screen recording software that captures the entire desktop, which produces oversized files and requires manual cropping. Other approaches depend on command-line tools that demand technical knowledge to configure stream URLs, cookies, and output settings before anything can be recorded.

LiveJasmin Downloader is being designed to handle all of that inside the browser. The extension will detect the active video stream in the current tab, let you start and stop recording with a single click, and write the result to a standard MP4 file on your hard drive. No desktop software to install, no terminal commands to learn, and no post-processing to deal with.

## Planned Features

- Real-time recording of live video streams playing in the browser tab
- One-click start and stop controls accessible from the extension popup
- Automatic detection of the active video stream on the LiveJasmin page
- Output saved as MP4 with H.264 video and AAC audio for broad compatibility
- Adjustable recording quality based on available stream resolution
- File naming that includes timestamp and session details for easy organization
- Duration indicator showing elapsed recording time during capture
- Browser-native operation with no dependency on FFmpeg or other external tools
- Cross-browser support targeting Chrome, Edge, Brave, and Firefox

## How It Will Work

1. Install the extension once it is released from the browser extension store.
2. Navigate to the LiveJasmin website and open a live stream in your browser.
3. Click the extension icon in the toolbar to open the recording controls.
4. The extension detects the active video stream playing in the current tab.
5. Press the record button to begin capturing the live stream in real time.
6. Monitor the elapsed time and file size from the extension popup as it records.
7. Press the stop button when you are finished recording the segment you want.
8. The captured video is saved as an MP4 file to your default downloads folder.

## Expected Formats

- Input: LiveJasmin live video streams delivered via HLS or WebRTC in the browser
- Output: MP4 container with H.264 video and AAC audio

Exported files will be saved in a format compatible with most media players, video editors, mobile devices, and cloud storage services without any additional conversion.

## Who It's For

- Users who want to save live stream sessions for personal offline viewing
- Researchers studying live streaming platforms and performer interaction models
- Content analysts reviewing broadcast quality and delivery across platforms
- Individuals with limited bandwidth who prefer to watch saved content at a later time
- Users who want a local archive of streams they have already watched live

## Use Cases We're Building For

- Record a live session to watch again later when you are offline
- Save segments of a broadcast for personal reference or review
- Capture streams during low-traffic hours to watch during more convenient times
- Build a local archive of content you have access to through your account
- Preserve specific broadcast moments before they are no longer available on the platform

## Security & Scope

- Operates only on the page the user intentionally opens in the active browser tab
- Detects supported playback sources only for user-initiated downloads or exports
- Does not execute page instructions, shell commands, or arbitrary scripts from page content
- Does not follow unrelated links or perform actions outside the active workflow
- Limits support to the named platform, approved embedded contexts, and user-authorized sessions when required

## FAQ

**When will LiveJasmin Downloader be released?**
A release date has not been set. Sign up at the waitlist link above to be notified as soon as it is available.

**Does it record the stream in real time or download it after the fact?**
The extension captures the stream in real time as it plays in your browser tab. You need to keep the tab open and the stream playing for the duration of the recording.

**What video quality will be available?**
Output quality will depend on the stream resolution that LiveJasmin delivers to your browser, which can vary based on the performer's broadcast settings and your connection speed.

**Will it work with private or group sessions?**
The extension is being built to detect video streams in the active tab regardless of session type. Specific support details will be confirmed closer to release.

**Is it free?**
Pricing details will be announced closer to launch. SERP extensions typically include a free trial period.

**Does it require any external software like FFmpeg?**
No. The extension is designed to handle recording and file creation entirely within the browser using built-in web APIs.

## License

This repository is distributed under the proprietary SERP Apps license in the [LICENSE](https://raw.githubusercontent.com/serpapps/livejasmin-downloader/refs/heads/main/LICENSE) file. Review that file before copying, modifying, or redistributing any part of this project.

## Notes

- This extension is in development and is not available for download yet
- Only record content you have permission or legal right to save
- Video quality will depend on the source stream resolution provided by LiveJasmin
- Platform changes on LiveJasmin may affect functionality once the extension is released
- An active LiveJasmin account and internet connection will be required during recording
- Recording duration is limited by available disk space and browser memory constraints

## About LiveJasmin

LiveJasmin is a live cam streaming platform where performers broadcast video in real time to viewers through the browser. The platform uses adaptive streaming to deliver video at varying quality levels but does not provide any built-in option to save, download, or export a live session as a local file. LiveJasmin Downloader is being built to fill that gap for users who want to keep a local copy of live content they have already viewed through their account.
