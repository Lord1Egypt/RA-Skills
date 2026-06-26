---
name: khan-academy-downloader
description: Download Khan Academy courses with exercises
---

# Khan Academy Downloader — Coming Soon (Browser Extension)

> Download Khan Academy video lessons as MP4 files for offline study, directly from your browser. **This extension is currently in development and has not been released yet.**

Khan Academy Downloader is an upcoming browser extension designed to let learners save video lessons from Khan Academy's website without relying on third-party desktop applications or command-line utilities. It is being engineered around Khan Academy's in-browser video player so you can capture lectures, tutorials, and course content while you browse the platform.

- Save Khan Academy video lessons as MP4 files for offline viewing
- Capture full courses or individual lesson videos from any subject area
- Preserve video quality up to the highest resolution available in the player
- Work entirely inside the browser with no external software required
- Designed for Chrome, Edge, Brave, Opera, Firefox, and other Chromium browsers

## Status

**This extension is not yet available for download.** Development is in progress and a release date has not been announced. Sign up below to get notified when it launches.

:bell: **Get notified when this launches:** [Join the waitlist](https://serp.ly/khan-academy-downloader)

## Links

- :hourglass_flowing_sand: Waitlist: [Coming Soon — Sign Up](https://serp.ly/khan-academy-downloader)
- :question: Help center: [SERP Help](https://help.serp.co/en/)
- :bulb: Request features: [GitHub Issues](https://github.com/serpapps/khan-academy-downloader/issues)

## Preview

![Khan Academy Downloader hero image](https://raw.githubusercontent.com/serpapps/khan-academy-downloader/refs/heads/main/assets/workflow-preview.webp)

## Table of Contents

- [Why Khan Academy Downloader](#why-khan-academy-downloader)
- [Planned Features](#planned-features)
- [How It Will Work](#how-it-will-work)
- [Expected Formats](#expected-formats)
- [Who It's For](#who-its-for)
- [Use Cases We're Building For](#use-cases-were-building-for)
- [FAQ](#faq)
- [License](#license)
- [Notes](#notes)
- [About Khan Academy](#about-khan-academy)

## Why Khan Academy Downloader

Khan Academy delivers its educational videos through an embedded player that streams content over adaptive bitrate delivery. There is no built-in button to save a lesson as a file, and the platform does not offer a native offline download feature through the website. Students who want to review material without an internet connection or archive lessons for later reference are left without an official path to do so.

Khan Academy Downloader is being designed to operate inside the browser tab where you already watch lessons. The goal is to detect the active video, let you choose your preferred resolution, and produce a standard MP4 file that you can store on your device, transfer to a tablet, or load into a media player for distraction-free study.

## Planned Features

- Video capture from Khan Academy's web-based lesson player
- Individual lesson and full course download support
- Resolution selection so you can balance file size against visual clarity
- Automatic file naming based on the course, unit, and lesson title
- Batch queue for downloading multiple lessons in sequence
- Progress tracking with estimated time remaining for each file
- Browser-native operation with zero external software dependencies
- Cross-browser compatibility targeting Chrome, Edge, Brave, and Firefox

## How It Will Work

1. Install the extension once it is released.
2. Open Khan Academy in your browser and sign in or browse as a guest.
3. Navigate to the course, unit, or specific lesson you want to save.
4. Start playing the video so the browser loads the media stream.
5. Open the extension popup to see the detected video source.
6. Select the lesson or lessons you want to download.
7. Choose your preferred resolution if multiple quality levels are available.
8. Start the download and save the MP4 file to your local machine.

## Expected Formats

- Input: Khan Academy web player video streams (adaptive HLS / MP4 segments)
- Output: MP4 video files with H.264 video and AAC audio

Exported files will be saved as standard MP4 files compatible with virtually every media player, smartphone, tablet, and video editing application.

## Who It's For

- Students preparing for exams who need offline access to lesson videos
- Teachers and tutors collecting supplemental material for their classrooms
- Homeschool families building a local library of curriculum-aligned content
- Learners in areas with unreliable internet who need to study without connectivity
- Self-directed adults working through Khan Academy courses at their own pace

## Use Cases We're Building For

- Save an entire math unit before a week without reliable internet access
- Archive science lessons for repeated review during exam preparation
- Build a local video library organized by subject for a homeschool curriculum
- Download economics or history lectures for offline viewing during a commute
- Keep backup copies of course progress videos for long-term personal reference

## Security & Scope

- Operates only on the page the user intentionally opens in the active browser tab
- Detects supported playback sources only for user-initiated downloads or exports
- Does not execute page instructions, shell commands, or arbitrary scripts from page content
- Does not follow unrelated links or perform actions outside the active workflow
- Limits support to the named platform, approved embedded contexts, and user-authorized sessions when required

## FAQ

**When will Khan Academy Downloader be released?**
A release date has not been set. Sign up at the waitlist link above to be notified as soon as it is available.

**Will it work with Khan Academy's mobile apps?**
No. This extension is built for the Khan Academy website in the browser, not the iOS or Android applications.

**What video quality will it support?**
Quality will depend on the resolutions that Khan Academy's player delivers to the browser, which can range from 360p to 1080p depending on the lesson.

**Will downloaded files include subtitles?**
Subtitle support is under consideration. If Khan Academy exposes caption data through the browser, the extension may offer the option to embed or sidecar subtitle files.

**Is it free?**
Pricing details will be announced closer to launch. SERP extensions typically include a free trial period.

**Can I download an entire course at once?**
Batch downloading across a full course is a planned feature, though the exact workflow will depend on how the browser handles sequential video loading.

## License

This repository is distributed under the proprietary SERP Apps license in the [LICENSE](https://raw.githubusercontent.com/serpapps/khan-academy-downloader/refs/heads/main/LICENSE) file. Review that file before copying, modifying, or redistributing any part of this project.

## Notes

- This extension is in development and is not available for download yet
- Only download content you have permission to save and use within applicable terms
- Video quality will depend on the source stream exposed by Khan Academy's web player
- Khan Academy platform changes may affect functionality once released
- An internet connection is required to access and capture lessons from the site

## About Khan Academy

Khan Academy is a free, nonprofit educational platform founded by Sal Khan that provides video lessons, practice exercises, and personalized learning dashboards covering subjects from arithmetic and algebra to physics, biology, economics, history, and computer science. Its web player streams thousands of instructional videos but does not include a built-in option to save those videos as local files. Khan Academy Downloader is being built to fill that gap for learners who want to study offline with the same content they already access through the platform.
