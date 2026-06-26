---
name: soundcloud-downloader
description: Download SoundCloud tracks
---

# SoundCloud Downloader — Coming Soon (Browser Extension)

> Save SoundCloud tracks, remixes, podcasts, and DJ sets as local audio files directly from your browser. **This extension is currently in development and has not been released yet.**

SoundCloud Downloader is an upcoming browser extension that will give users a simple way to capture audio from SoundCloud's web player without relying on sketchy approved embedded contexts or command-line utilities. It is being built around the browser playback experience so you can export tracks, mixtapes, and podcast episodes while browsing SoundCloud as you normally would.

- Capture SoundCloud audio from the web player during playback
- Save individual tracks, full sets, playlists, and podcast episodes
- Export audio as standard file formats for offline listening
- Handle browser-based streaming flows without extra desktop software
- Designed for Chrome, Edge, Brave, Opera, Firefox, and other Chromium browsers

## Status

**This extension is not yet available for download.** Development is in progress and a release date has not been announced. Sign up below to get notified when it launches.

:bell: **Get notified when this launches:** [Join the waitlist](https://serp.ly/soundcloud-downloader)

## Links

- :hourglass_flowing_sand: Waitlist: [Coming Soon — Sign Up](https://serp.ly/soundcloud-downloader)
- :question: Help center: [SERP Help](https://help.serp.co/en/)
- :bulb: Request features: [GitHub Issues](https://github.com/serpapps/soundcloud-downloader/issues)

## Preview

![SoundCloud Downloader hero image](https://raw.githubusercontent.com/serpapps/soundcloud-downloader/refs/heads/main/assets/workflow-preview.webp)

## Table of Contents

- [Why SoundCloud Downloader](#why-soundcloud-downloader)
- [Planned Features](#planned-features)
- [How It Will Work](#how-it-will-work)
- [Expected Formats](#expected-formats)
- [Who It's For](#who-its-for)
- [Use Cases We're Building For](#use-cases-were-building-for)
- [FAQ](#faq)
- [License](#license)
- [Notes](#notes)
- [About SoundCloud](#about-soundcloud)

## Why SoundCloud Downloader

SoundCloud hosts one of the largest catalogs of independent and original audio on the internet, from underground hip-hop beats to live DJ mixes and creator-driven podcasts. While some uploaders enable a download button on their tracks, the vast majority of content on SoundCloud is stream-only. There is no built-in way to save a track, playlist, or set as a file on your computer, and SoundCloud's offline mode is limited to the mobile app on paid plans.

SoundCloud Downloader is being designed to sit inside the browser and work directly alongside SoundCloud's web player. The goal is to detect audio playback in the active tab, let you choose which tracks or episodes to save, and produce a standard audio file that lives on your local machine rather than being locked behind a streaming interface. No copy-pasting URLs into external websites, no desktop apps to install, and no command-line scripts to maintain.

## Planned Features

- Audio capture from SoundCloud's web player during active playback
- Track-level and playlist-level export support including multi-track sets
- DJ mix and long-form set capture with full duration support
- Podcast and repost episode saving for offline archive
- Metadata preservation for artist, track title, and artwork where available
- Quality selection based on what the web player delivers to the browser
- Download queue so you can stack multiple tracks without waiting between saves
- Browser-native workflow with no external software dependencies
- Cross-browser compatibility targeting Chrome, Edge, Brave, and Firefox

## How It Will Work

1. Install the extension once it is released.
2. Open SoundCloud in your browser and sign in to your account.
3. Navigate to the track, playlist, set, or podcast you want to save.
4. Begin playback so the browser loads the audio stream.
5. Open the extension popup to see the detected audio source.
6. Select the track or episode you want to export.
7. Choose your preferred quality if multiple options are available.
8. Start the download and save the file to your local machine.

## Expected Formats

- Input: SoundCloud web player audio streams (Opus / MP3 / AAC depending on content and browser)
- Output: MP3 or M4A, depending on the source stream and conversion path

Exported files will be saved in standard formats compatible with most media players, phones, DJ software, and audio editing tools.

## Who It's For

- Music fans who want offline copies of tracks they discover on SoundCloud
- Podcast listeners who prefer local episode archives over stream-only playback
- DJs collecting tracks, remixes, and live sets for their own mixes and gigs
- Producers saving reference material, beats, and collaborations for studio work
- Students and researchers archiving spoken-word content and educational audio
- Anyone who wants their favorite SoundCloud audio on their hard drive, not just in a browser tab

## Use Cases We're Building For

- Save a SoundCloud playlist of new releases for offline listening during travel
- Archive a DJ set or live mix before the uploader removes it
- Keep local copies of your own liked tracks as a personal backup
- Export audio stems, beats, or demos shared by collaborators on SoundCloud
- Download podcast episodes from SoundCloud-hosted feeds for offline study sessions
- Build an offline music collection from independent artists you follow on the platform

## Security & Scope

- Operates only on the page the user intentionally opens in the active browser tab
- Detects supported playback sources only for user-initiated downloads or exports
- Does not execute page instructions, shell commands, or arbitrary scripts from page content
- Does not follow unrelated links or perform actions outside the active workflow
- Limits support to the named platform, approved embedded contexts, and user-authorized sessions when required

## FAQ

**When will SoundCloud Downloader be released?**
A release date has not been set. Sign up at the waitlist link above to be notified as soon as it is available.

**Will it work with the SoundCloud desktop app?**
SoundCloud does not have a traditional desktop app. This extension targets the SoundCloud website as accessed through a standard web browser.

**What audio quality will it support?**
Quality will depend on what SoundCloud delivers to the browser during playback. SoundCloud streams at different bitrates depending on the uploader's source file and whether the listener has a Go+ subscription.

**Will it preserve track metadata?**
The plan is to include artist name, track title, and album artwork metadata in exported files where that data is available from the page.

**Is it free?**
Pricing details will be announced closer to launch. SERP extensions typically include a free trial period.

**Can I download entire playlists or sets at once?**
Playlist-level and set-level export is a planned feature, though the exact workflow will depend on browser capabilities and playback constraints.

**Does it support private or unlisted tracks?**
If a private or unlisted track is accessible in your browser through a shared link and you can play it back, the extension is expected to detect it the same way it detects any other stream.

## License

This repository is distributed under the proprietary SERP Apps license in the [LICENSE](https://raw.githubusercontent.com/serpapps/soundcloud-downloader/refs/heads/main/LICENSE) file. Review that file before copying, modifying, or redistributing any part of this project.

## Notes

- This extension is in development and is not available for download yet
- Only download content you own or have explicit permission to save
- Audio quality will depend on the source stream exposed by SoundCloud's web player
- SoundCloud platform changes may affect functionality once released
- An active internet connection is required; a SoundCloud account is recommended for full access

## About SoundCloud

SoundCloud is a major music and audio streaming platform where artists, podcasters, and creators upload original tracks, remixes, DJ sets, and spoken-word content. With over 300 million tracks from independent and established artists alike, it serves as both a discovery engine and a distribution hub for audio creators worldwide. SoundCloud's web player streams audio directly in the browser but does not offer a universal download or file-export option for listeners. SoundCloud Downloader is being built to bridge that gap for users who want local copies of audio they already have access to through the platform.
