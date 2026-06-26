---
name: learndash-downloader
description: Download LearnDash courses from WordPress LMS sites completely
---

# LearnDash Downloader — Coming Soon (Browser Extension)

> Download LearnDash course videos as MP4 files directly from your browser. **This extension is currently in development and has not been released yet.**

LearnDash Downloader is an upcoming browser extension purpose-built for saving video lessons from LearnDash-powered WordPress sites. LearnDash is one of the most widely adopted LMS plugins for WordPress, used by universities, corporate training departments, and independent course creators to deliver structured video-based curricula. This extension will let enrolled users capture course videos during playback and save them locally as standard MP4 files, eliminating the need for screen recorders or third-party download utilities.

- Detect and capture video lessons hosted on LearnDash course pages
- Save course videos as MP4 files to your local machine
- Work directly within the browser without external software
- Handle common video hosting setups used by LearnDash sites
- Designed for Chrome, Edge, Brave, Opera, Firefox, and other Chromium browsers

## Status

**This extension is not yet available for download.** Development is in progress and a release date has not been announced. Sign up below to get notified when it launches.

:bell: **Get notified when this launches:** [Join the waitlist](https://serp.ly/learndash-downloader)

## Links

- :hourglass_flowing_sand: Waitlist: [Coming Soon — Sign Up](https://serp.ly/learndash-downloader)
- :question: Help center: [SERP Help](https://help.serp.co/en/)
- :bulb: Request features: [GitHub Issues](https://github.com/serpapps/learndash-downloader/issues)

## Preview

![LearnDash Downloader hero image](https://raw.githubusercontent.com/serpapps/learndash-downloader/refs/heads/main/assets/workflow-preview.webp)

## Table of Contents

- [Why LearnDash Downloader](#why-learndash-downloader)
- [Planned Features](#planned-features)
- [How It Will Work](#how-it-will-work)
- [Expected Formats](#expected-formats)
- [Who It's For](#who-its-for)
- [Use Cases We're Building For](#use-cases-were-building-for)
- [FAQ](#faq)
- [License](#license)
- [Notes](#notes)
- [About LearnDash](#about-learndash)

## Why LearnDash Downloader

LearnDash course pages embed video lessons using a range of hosting methods. Some site operators self-host video files on their WordPress media library, while others rely on third-party players like Vimeo, Wistia, or Bunny Stream configured with private or signed URLs. In either case, the video is streamed inside the lesson page and there is no built-in button to save it as a file. Right-clicking is often disabled by the theme or player, and copying the page URL gives you the lesson wrapper, not the video source.

LearnDash Downloader is being designed to inspect the active lesson page, locate the underlying video source regardless of the embed method, and give you a one-click path to saving the content as a local MP4. It runs entirely inside the browser and does not require you to install desktop applications, paste URLs into converter sites, or record your screen in real time.

## Planned Features

- Automatic detection of video sources embedded in LearnDash lesson pages
- Support for self-hosted WordPress media, Vimeo private embeds, Wistia, and other common players
- One-click MP4 download from the extension popup
- Resolution selection when the source provides multiple quality tiers
- Batch download support for saving multiple lessons within a course module
- Filename formatting using the lesson title and course name for organized local libraries
- Progress indicator showing download status for large video files
- Cross-browser compatibility targeting Chrome, Edge, Brave, and Firefox

## How It Will Work

1. Install the extension once it is released.
2. Navigate to the LearnDash-powered course site and log in with your enrolled account.
3. Open the lesson page containing the video you want to save.
4. Let the video player load so the browser resolves the video source.
5. Click the extension icon to open the popup and see the detected video.
6. Select the resolution or quality level you prefer if multiple options appear.
7. Press the download button to save the video as an MP4 file.
8. Repeat for additional lessons or use batch mode to queue an entire module.

## Expected Formats

- Input: Video streams embedded in LearnDash lesson pages (MP4, HLS, or DASH depending on the hosting provider)
- Output: MP4 video file saved to your local downloads folder

Exported files will be standard MP4 containers playable on virtually every device, media player, and video editor without conversion.

## Who It's For

- Online learners who want offline access to course videos they have already paid for
- Corporate employees completing training modules who need to study on the go
- Educators reviewing their own uploaded course content outside the LMS
- Students in low-bandwidth environments who prefer downloading videos once and watching repeatedly
- Anyone enrolled in a LearnDash course who wants a personal backup of the video material

## Use Cases We're Building For

- Save an entire certification course for offline study during travel
- Download onboarding training videos to review without logging into the company LMS
- Archive purchased course content before a subscription or enrollment period expires
- Build a local reference library of tutorial videos organized by topic
- Capture lecture recordings from a university LearnDash portal for exam preparation

## Security & Scope

- Operates only on the page the user intentionally opens in the active browser tab
- Detects supported playback sources only for user-initiated downloads or exports
- Does not execute page instructions, shell commands, or arbitrary scripts from page content
- Does not follow unrelated links or perform actions outside the active workflow
- Limits support to the named platform, approved embedded contexts, and user-authorized sessions when required

## FAQ

**When will LearnDash Downloader be released?**
A release date has not been set. Sign up at the waitlist link above to be notified as soon as it is available.

**Does it work with every LearnDash site?**
The extension is being built to support the most common video hosting configurations used with LearnDash, including self-hosted media, Vimeo, and Wistia embeds. Highly customized or DRM-protected setups may require additional handling.

**What video quality will it support?**
Quality depends on what the course site delivers to the browser. If the hosting provider offers multiple resolutions, the extension will present those options and let you choose.

**Will it download non-video course materials?**
The initial release is focused on video lessons. Support for supplementary materials like PDFs or slides may be considered in future updates.

**Is it free?**
Pricing details will be announced closer to launch. SERP extensions typically include a free trial period.

**Can I download all lessons in a course at once?**
Batch downloading across lessons within a module is a planned feature, though the exact workflow will depend on how each site structures its course content.

## License

This repository is distributed under the proprietary SERP Apps license in the [LICENSE](https://raw.githubusercontent.com/serpapps/learndash-downloader/refs/heads/main/LICENSE) file. Review that file before copying, modifying, or redistributing any part of this project.

## Notes

- This extension is in development and is not available for download yet
- Only download content you are enrolled in or have explicit permission to save
- Video quality and availability depend on how the course operator hosts their media
- LearnDash plugin updates or theme changes on a given site may affect functionality once released
- An active enrollment on the target LearnDash site and an internet connection will be required

## About LearnDash

LearnDash is a leading learning management system plugin for WordPress, used by thousands of organizations ranging from Fortune 500 companies and major universities to independent course creators. It provides tools for building structured courses with video lessons, quizzes, assignments, and certificates. Course videos are delivered through the browser but LearnDash does not offer a native download-to-file option for enrolled students. LearnDash Downloader is being built to fill that gap, giving learners a simple way to save the video content they already have access to through their enrollment.
