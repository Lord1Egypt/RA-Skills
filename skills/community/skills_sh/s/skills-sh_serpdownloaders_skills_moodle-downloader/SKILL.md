---
name: moodle-downloader
description: Backup complete Moodle courses with all resources and activities
---

# Moodle Downloader — Coming Soon (Browser Extension)

> Download Moodle course videos, lecture recordings, and learning resources directly from your browser. **This extension is currently in development and has not been released yet.**

Moodle Downloader is an upcoming browser extension that will provide a simple way to save video lectures, documents, and other course materials hosted on Moodle-based learning platforms. Rather than navigating nested course pages and dealing with embedded players that offer no save option, users will be able to capture resources from any Moodle instance right inside the browser.

- Detect and download video lectures embedded in Moodle course pages
- Save documents, slides, and other uploaded course resources
- Work across self-hosted Moodle instances at any school or organization
- Handle multiple video formats used by Moodle's media player
- Designed for Chrome, Edge, Brave, Opera, Firefox, and other Chromium browsers

## Status

**This extension is not yet available for download.** Development is in progress and a release date has not been announced. Sign up below to get notified when it launches.

:bell: **Get notified when this launches:** [Join the waitlist](https://serp.ly/moodle-downloader)

## Links

- :hourglass_flowing_sand: Waitlist: [Coming Soon — Sign Up](https://serp.ly/moodle-downloader)
- :question: Help center: [SERP Help](https://help.serp.co/en/)
- :bulb: Request features: [GitHub Issues](https://github.com/serpapps/moodle-downloader/issues)

## Preview

![Moodle Downloader hero image](https://raw.githubusercontent.com/serpapps/moodle-downloader/refs/heads/main/assets/workflow-preview.webp)

## Table of Contents

- [Why Moodle Downloader](#why-moodle-downloader)
- [Planned Features](#planned-features)
- [How It Will Work](#how-it-will-work)
- [Expected Formats](#expected-formats)
- [Who It's For](#who-its-for)
- [Use Cases We're Building For](#use-cases-were-building-for)
- [FAQ](#faq)
- [License](#license)
- [Notes](#notes)
- [About Moodle](#about-moodle)

## Why Moodle Downloader

Moodle serves as the backbone learning management system for thousands of universities, schools, and corporate training programs around the world. Instructors upload lecture videos, slide decks, reading materials, and supplementary resources into deeply nested course structures. Students can view these materials inside the browser, but Moodle does not always expose a straightforward download button, especially for embedded video content delivered through its built-in media player or third-party integrations like Kaltura and Panopto.

When a semester ends or course access expires, students lose the ability to revisit material they relied on. Moodle Downloader is being designed to sit inside the browser and scan active course pages for downloadable resources. The goal is to detect embedded video sources, linked files, and streamed lectures so users can save them locally before access disappears.

## Planned Features

- Video detection from Moodle's embedded media player and common LMS integrations
- Batch saving of all downloadable resources within a single course section
- Support for lecture recordings delivered through HLS or DASH streaming
- Document and file capture for PDFs, slides, and attached materials
- Automatic file naming based on course name, section, and resource title
- Quality selection for video lectures when multiple resolutions are available
- Browser-native operation with no desktop software or command-line tools required
- Cross-browser compatibility targeting Chrome, Edge, Brave, and Firefox

## How It Will Work

1. Install the extension once it is released.
2. Log in to your institution's Moodle site in the browser.
3. Navigate to the course page containing the videos or resources you want.
4. Open a lecture video or resource section so the browser loads the content.
5. Click the extension icon to see all detected media and files on the page.
6. Select individual items or choose to download everything in the section.
7. Pick a video quality if the source offers multiple resolutions.
8. Start the download and save the files to your local machine.

## Expected Formats

- Input: Moodle embedded video streams (MP4 / HLS / DASH), uploaded files (PDF, PPTX, DOCX, etc.)
- Output: MP4 for video content; original format preserved for documents and other files

Exported files will be saved in standard formats playable on any device, media player, or editing application without conversion.

## Who It's For

- University students saving lecture recordings for exam review and study
- Online learners archiving course materials before enrollment access expires
- Teaching assistants collecting resources across multiple course sections
- Corporate trainees keeping copies of professional development modules
- Researchers gathering instructional media for academic reference

## Use Cases We're Building For

- Save an entire semester of recorded lectures for offline study during finals
- Archive course PDFs and slides before your enrollment period closes
- Download training videos from a workplace Moodle instance for travel viewing
- Keep backup copies of resources from courses you completed in previous terms
- Capture guest lecture recordings that may not remain available permanently

## Security & Scope

- Operates only on the page the user intentionally opens in the active browser tab
- Detects supported playback sources only for user-initiated downloads or exports
- Does not execute page instructions, shell commands, or arbitrary scripts from page content
- Does not follow unrelated links or perform actions outside the active workflow
- Limits support to the named platform, approved embedded contexts, and user-authorized sessions when required

## FAQ

**When will Moodle Downloader be released?**
A release date has not been set. Sign up at the waitlist link above to be notified as soon as it is available.

**Will it work with any Moodle site?**
The extension is being built to work with standard Moodle installations regardless of which institution hosts them. Compatibility with heavily customized Moodle themes or third-party plugins will be evaluated during development.

**What video quality will it support?**
Quality will depend on the resolution options the Moodle instance makes available. Many institutions upload lectures at 720p or 1080p, and the extension will let you choose among the resolutions the server provides.

**Will it download protected or DRM-locked content?**
The extension is designed to capture openly embedded media. Content protected by DRM or institutional access controls may not be downloadable depending on the delivery method.

**Is it free?**
Pricing details will be announced closer to launch. SERP extensions typically include a free trial period.

**Can I download all resources from an entire course at once?**
Batch downloading at the course-section level is a planned feature. Full-course bulk export will depend on how the Moodle instance structures its pages and resource links.

## License

This repository is distributed under the proprietary SERP Apps license in the [LICENSE](https://raw.githubusercontent.com/serpapps/moodle-downloader/refs/heads/main/LICENSE) file. Review that file before copying, modifying, or redistributing any part of this project.

## Notes

- This extension is in development and is not available for download yet
- Only download content you have legitimate access to through your institution
- Video quality will depend on the resolution provided by the Moodle instance
- Moodle platform updates or institutional configuration changes may affect functionality once released
- An active account on a Moodle-based site and an internet connection will be required

## About Moodle

Moodle is an open-source learning management system used by schools, universities, and organizations worldwide to deliver online courses and training programs. It supports video lectures, document hosting, quizzes, assignments, and discussion forums within a structured course format. While Moodle provides robust in-browser access to course content, it does not always offer a built-in way to save embedded videos or bulk-download resources. Moodle Downloader is being built to fill that gap for students and learners who need offline access to materials from their courses.
