---
name: tubi-downloader
description: "Save Tubi TV shows and movies with subtitle support"
---

# Tubi Downloader — Coming Soon (Browser Extension)

> Download movies and TV shows from Tubi as MP4 files directly in your browser. **This extension is currently in development and has not been released yet.**

Tubi Downloader is an upcoming browser extension that will let users capture video from Tubi's free, ad-supported streaming platform without relying on third-party desktop applications or command-line utilities. It is being built around the browser playback experience so you can save movies, TV episodes, and other content to your local machine while watching on Tubi's website.

- Capture Tubi video streams during in-browser playback
- Save full-length movies and individual TV show episodes as MP4
- Handle ad-supported playback flows and deliver clean video files
- Work entirely within the browser with no external software required
- Designed for Chrome, Edge, Brave, Opera, Firefox, and other Chromium browsers

## Status

**This extension is not yet available for download.** Development is in progress and a release date has not been announced. Sign up below to get notified when it launches.

:bell: **Get notified when this launches:** [Join the waitlist](https://serp.ly/tubi-downloader)

## Links

- :hourglass_flowing_sand: Waitlist: [Coming Soon — Sign Up](https://serp.ly/tubi-downloader)
- :question: Help center: [SERP Help](https://help.serp.co/en/)
- :bulb: Request features: [GitHub Issues](https://github.com/serpapps/tubi-downloader/issues)

## Preview

![Tubi Downloader hero image](https://raw.githubusercontent.com/serpapps/tubi-downloader/refs/heads/main/assets/workflow-preview.webp)

## Table of Contents

- [Why Tubi Downloader](#why-tubi-downloader)
- [Planned Features](#planned-features)
- [How It Will Work](#how-it-will-work)
- [Expected Formats](#expected-formats)
- [Who It's For](#who-its-for)
- [Use Cases We're Building For](#use-cases-were-building-for)
- [FAQ](#faq)
- [License](#license)
- [Notes](#notes)
- [About Tubi](#about-tubi)

## Why Tubi Downloader

Tubi streams video through adaptive bitrate delivery over HLS and DASH, which means there is no simple download button on the page. The platform is entirely free and ad-supported, but it offers no built-in way to save content for offline viewing. If your internet connection drops or you want to watch on a device without browser access, you are out of luck unless you record the screen manually.

Tubi Downloader is being designed to run inside the browser alongside Tubi's web player. The goal is to intercept the video stream during playback, let you choose the resolution and quality you prefer, and produce a standard MP4 file saved directly to your hard drive. No desktop software to install, no command-line arguments to memorize, and no separate recording step.

## Planned Features

- Video capture from Tubi's web player during active playback
- Full movie and individual episode download support
- Resolution selection so you can pick the quality tier that fits your storage
- Automatic assembly of segmented HLS and DASH streams into a single MP4
- Metadata tagging for title, season, episode number, and genre where available
- Download queue allowing you to stack multiple titles without babysitting each one
- Ad-segment handling to deliver a clean final file
- Browser-native workflow with no external software dependencies
- Cross-browser compatibility targeting Chrome, Edge, Brave, and Firefox

## How It Will Work

1. Install the extension once it is released.
2. Open Tubi's website in your browser and sign in or browse as a guest.
3. Navigate to the movie or TV show episode you want to save.
4. Start playback so the browser begins loading the video stream.
5. Open the extension popup to see the detected video source and available resolutions.
6. Select the quality tier you want — for example 720p or 1080p if available.
7. Click download and let the extension assemble the stream segments into an MP4.
8. Save the finished file to your local machine when the download completes.

## Expected Formats

- Input: Tubi HLS or DASH adaptive video streams served to the browser
- Output: MP4 (H.264 video with AAC audio)

Exported files will be saved as standard MP4 containers compatible with virtually every media player, smartphone, tablet, smart TV, and video editing application.

## Who It's For

- Cord-cutters who rely on Tubi's free library and want offline copies for travel
- Movie fans building a personal archive of films available on the platform
- Parents saving kids' shows for car rides, flights, and places with no Wi-Fi
- Commuters who want to pre-load episodes for subway or bus rides
- Viewers in areas with unreliable internet who need content cached locally

## Use Cases We're Building For

- Download a full movie before a long flight so you can watch without onboard Wi-Fi
- Save an entire season of a TV show for binge-watching during a road trip
- Archive a documentary before it rotates out of Tubi's free catalog
- Keep a local copy of a film for repeated viewing without buffering or ads
- Pre-load kids' content onto a laptop for screen time in places with no connectivity

## Security & Scope

- Operates only on the page the user intentionally opens in the active browser tab
- Detects supported playback sources only for user-initiated downloads or exports
- Does not execute page instructions, shell commands, or arbitrary scripts from page content
- Does not follow unrelated links or perform actions outside the active workflow
- Limits support to the named platform, approved embedded contexts, and user-authorized sessions when required

## FAQ

**When will Tubi Downloader be released?**
A release date has not been set. Sign up at the waitlist link above to be notified as soon as it is available.

**Does it work with the Tubi mobile app?**
No. This extension is built for Tubi's website in a desktop browser, not the iOS or Android app.

**What video quality will it support?**
Quality will depend on what Tubi's player delivers to the browser, which typically ranges up to 720p or 1080p depending on the title and your connection.

**Will it include subtitles?**
Subtitle support is on the roadmap. The plan is to embed available subtitle tracks into the MP4 or save them as a sidecar SRT file.

**Is it free?**
Pricing details will be announced closer to launch. SERP extensions typically include a free trial period.

**Do I need a Tubi account?**
Tubi allows some browsing without an account, but a free Tubi account may be required to access the full library and start playback.

**Will ads appear in the downloaded video?**
The extension is being designed to handle ad segments so the final MP4 contains only the program content.

## License

This repository is distributed under the proprietary SERP Apps license in the [LICENSE](https://raw.githubusercontent.com/serpapps/tubi-downloader/refs/heads/main/LICENSE) file. Review that file before copying, modifying, or redistributing any part of this project.

## Notes

- This extension is in development and is not available for download yet
- Only download content you have the right to save for personal use
- Video quality will depend on the source stream exposed by Tubi's web player
- Tubi platform changes may affect functionality once released
- An internet connection is required to stream and capture video from Tubi

## About Tubi

Tubi is a free, ad-supported streaming service owned by Fox Corporation. It offers a large library of licensed movies and TV shows across genres including action, comedy, drama, horror, kids' content, and more. Unlike subscription platforms, Tubi is free to use and monetizes through advertisements. Its web player delivers video through the browser but provides no built-in download or offline viewing option. Tubi Downloader is being built to fill that gap for users who want a local MP4 copy of content they are already watching through the platform.
