---
name: transcribe-any-video
description: Get transcripts of public videos from YouTube, TikTok, Instagram, X (Twitter), Facebook, LinkedIn, Reddit and Rumble with no accounts or API keys. Captions where they exist, transcripts made from the audio for TikTok videos without captions, and translated YouTube subtitles. Use this skill to summarise videos, quote them, repurpose content, or research what creators say.
---

# Transcribe Any Video: YouTube, TikTok, Instagram & More

![Transcribe Any Video: YouTube, TikTok, Instagram & More](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/transcribe-any-video.gif)

Paste a video link from almost any platform and get the words back as text: ready to summarise, quote, translate or turn into a post.

No platform account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=transcribe-any-video).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/transcribe-any-video.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “Summarise this YouTube video”
- “Transcribe this TikTok for me”
- “What does this Instagram reel say?”
- “Translate this YouTube video's subtitles into Spanish”
- “Turn this LinkedIn video post into a blog outline”

## When to Use This Skill

Use it when the user shares a public video link (YouTube, TikTok, Instagram, X, Facebook, LinkedIn, Reddit or Rumble) and wants its words.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ 8 video platforms│
│   (User Chat)   │     │ (data tools) │     │ (public data)    │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install plugin    │                       │
         │  2. Pair device once  │                       │
         │  3. Ask a question    │                       │
         │                       │  4. Fetch + trim      │
         │                       │  5. Charge credit     │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  Answer  │           │  Credit  │           │ Results  │
   │ in chat  │           │ ($0.50)  │           │ as JSON  │
   └──────────┘           └──────────┘           └──────────┘
```

ClawLink holds the data-provider accounts. The user never pastes a key, and nothing is installed beyond the plugin.

## Install

Install the ClawLink plugin from ClawHub when the user asks for it:

```bash
openclaw plugins install clawhub:clawlink-plugin
```

The install applies to the running Gateway: do not restart it. The ClawLink tools appear on your next turn, so end this turn and tell the user: "ClawLink is installed. Reply ok and I will give you your pairing link." On the next turn call `clawlink_begin_pairing`, give the user the link, and after they approve call `clawlink_get_pairing_status`. Pairing happens once; after that every tool below works with no further setup.

## Tool Reference

Prices are what ClawLink charges per call, from the user's credit. The tool's own description (via `clawlink_describe_tool`) always shows the current price.

### YouTube

| Tool | What it returns | Price |
|------|-----------------|-------|
| `youtubedata_video_captions` | Captions (transcript) of a YouTube video as text | $0.00282 |
| `seokeyworddata_youtube_subtitles` | Timed subtitles of a YouTube video, optionally machine-translated into another language | $0.009 |

### TikTok

| Tool | What it returns | Price |
|------|-----------------|-------|
| `tiktokdata_video_transcript` | A TikTok video's captions as text | $0.003 |
| `tiktokdata_video_audio_transcript` | Transcript made from a TikTok video's audio, for videos with no captions | $0.0264 |

### Instagram, X & Facebook

| Tool | What it returns | Price |
|------|-----------------|-------|
| `instagramdata_transcript` | Spoken-word transcript of an Instagram reel or video post | $0.00282 |
| `xdata_post_transcript` | Spoken-word transcript of an X video post by URL | $0.00282 |
| `facebookdata_post_transcript` | Spoken-word transcript of a public Facebook video post or reel by URL | $0.00282 |
| `facebookdata_ad_transcript` | Spoken-word transcript of a Meta Ad Library video ad by id or URL | $0.00282 |

### LinkedIn, Reddit & Rumble

| Tool | What it returns | Price |
|------|-----------------|-------|
| `linkedindata_post_transcript` | Transcript of the video in a LinkedIn post | $0.00282 |
| `redditdata_post_transcript` | Captions of a Reddit video post as plain text (transcriptNotAvailable when the video has none) | $0.00282 |
| `rumbledata_video_transcript` | Transcript of a Rumble video from its captions (WebVTT); transcriptNotAvailable when the video has none (the call is… | $0.00282 |

## Recipes

### Summarise any video

1. Pick the tool for the link's platform.
2. For TikTok, try `tiktokdata_video_transcript` first; if it finds no captions, use `tiktokdata_video_audio_transcript` (made from the audio).
3. Summarise, and quote the transcript for anything the user will publish.

### Translate a YouTube video

1. `seokeyworddata_youtube_subtitles` with `subtitles_translate_language` set to the target language.

## Code Examples

### YouTube captions

```bash
clawlink_call_tool --tool "youtubedata_video_captions" \
  --params '{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}'
```

### TikTok from audio

```bash
clawlink_call_tool --tool "tiktokdata_video_audio_transcript" \
  --params '{"url": "https://www.tiktok.com/@user/video/VIDEO_ID"}'
```

### Translated subtitles

```bash
clawlink_call_tool --tool "seokeyworddata_youtube_subtitles" \
  --params '{"video_id": "VIDEO_ID", "subtitles_translate_language": "es"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `transcript`); public-data tools show as connected for every user.
2. Call `clawlink_describe_tool` before the first call of a tool: it returns the parameters, defaults and price.
3. Treat the live catalog as the source of truth. If a tool named here is missing, say so; do not invent results.

## Execution Workflow

```
┌───────────────────────────────────────────────────────────┐
│  READ-ONLY, PAID PER CALL                                │
│  search → describe → call → summarise for the user       │
│                                                          │
│  Ask before: loops over many items, or a call that costs │
│  more than a few cents (the price is in the description) │
└───────────────────────────────────────────────────────────┘
```

1. Every tool here only reads public data; nothing is posted or changed.
2. Each call costs credit. Before looping over more than about ten items, or before a call priced above a few cents, tell the user what it will cost and ask.
3. A failed call is refunded automatically. Read the error's `hint`: it says what to change. Do not retry the same arguments unchanged.

## Notes

- Use the real link the user gave; placeholder ids like VIDEO_ID fail.
- Videos without captions return no transcript, except TikTok, where the audio tool transcribes the sound.
- Very long transcripts are cut at about 20,000 characters.
- Transcripts are for summarising and quoting; respect the creator's rights before republishing.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| No transcript | The video has no captions on that platform. For TikTok use the audio tool. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=transcribe-any-video; do not retry. |
| `data_provider_unavailable` | ClawLink's data provider is down. Nothing was charged. Try again later. |
| `no_result` | The provider found nothing for these arguments. Nothing was charged. |
| `invalid_arguments` | A parameter is missing or malformed. Call `clawlink_describe_tool` and fix it. |

## Troubleshooting

### Tools not visible after install

1. The tools appear on the turn after the install, not in the same turn.
2. If they still do not appear, the OpenClaw tool profile may hide plugin tools. This is a config change for the OpenClaw owner; do not change the config yourself. Tell the user: "Your OpenClaw tool profile hides plugin tools. In the Control UI (or `~/.openclaw/openclaw.json`), add `clawlink-plugin` to `tools.alsoAllow`, then ask me again."
3. On OpenClaw versions before 2.0, the tool list can load only in a new chat: tell the user to send `/new` and ask again.

### A tool keeps failing with correct input

Report it with `clawlink_report_issue` (or `clawlink_call_tool --tool "CLAWLINK_REPORT_ISSUE"`) instead of retrying. Reports are free and reach the ClawLink team.

## Resources


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=transcribe-any-video)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=transcribe-any-video)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [TikTok Trend Radar](https://clawhub.ai/hith3sh/skills/tiktok-trend-radar)
- [Creator Scout](https://clawhub.ai/hith3sh/skills/creator-scout)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=transcribe-any-video)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
