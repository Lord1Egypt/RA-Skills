---
name: vimeo-locked-captions
description: |
  Extract auto-generated captions/transcript from a privacy-locked (domain-restricted) Vimeo
  embed when the player refuses to play. Use when: (1) you need a transcript of a video
  interview/talk that's embedded as Vimeo on a third-party site (VC blog, conference page,
  paywalled article), (2) opening player.vimeo.com directly returns "video cannot be played
  here due to privacy settings" or "由于隐私设置，该视频无法在此处播放", (3) the host page
  publishes no transcript and yt-dlp / Whisper would be overkill. The player HTML leaks a
  signed captions.vimeo.com VTT URL even when playback is blocked — fetched with a correct
  Referer header.
author: Claude Code
version: 1.0.0
date: 2026-05-29
---

# Vimeo Locked-Embed Caption Extraction

## Problem

A page embeds a Vimeo video using `<iframe src="https://player.vimeo.com/video/{ID}?h={HASH}">`.
The video is "domain-restricted" — opening the player URL directly returns a privacy error,
and `yt-dlp` / browser automation also fail because Vimeo enforces the Referer check.

But you only need the **transcript**, not the video. Vimeo's auto-generated captions are
served from a separate signed URL that the player HTML embeds in a JSON config — and that
HTML is fetched whenever the Referer matches the allowed domain. So you can pull the
captions without ever playing the video.

## Trigger Conditions

- Page contains `<iframe src="https://player.vimeo.com/video/...">` and no transcript text.
- Direct visit to the player URL shows "Sorry / 抱歉 — video cannot be played here due to privacy settings."
- You want a transcript-driven analysis (interview, panel, fireside chat, conference talk).

## Solution

Three commands. Replace `{ID}`, `{HASH}`, and `{HOST}` with values from the embed.

```bash
# 1. Fetch the player HTML with the correct Referer and grep out the text_tracks JSON.
curl -s -H 'Referer: https://{HOST}/' \
  'https://player.vimeo.com/video/{ID}?h={HASH}' \
  | grep -oE '"text_tracks":\[[^]]*\]'
```

That returns something like:

```json
"text_tracks":[{"id":303147651,"lang":"en-x-autogen",
"url":"https://captions.vimeo.com/captions/303147651.vtt?expires=...&sig=...",
"kind":"subtitles","label":"English (auto-generated)",
"provenance":"ai_generated","default":true}]
```

```bash
# 2. Download the VTT (the signed URL works without Referer).
curl -s 'https://captions.vimeo.com/captions/{CAP_ID}.vtt?expires=...&sig=...' \
  -o /tmp/transcript.vtt

# 3. Strip WEBVTT cues/timestamps to get plain text.
awk '/-->/{next} /^[0-9]+$/{next} /^WEBVTT/{next} /^$/{next} {print}' \
  /tmp/transcript.vtt > /tmp/transcript.txt
wc -w /tmp/transcript.txt
```

## How to find ID, HASH, HOST

From the embed iframe's `src` attribute on the host page:

```
https://player.vimeo.com/video/1195836424?h=a0154d0f4b
                              └────┬────┘  └────┬────┘
                                  ID         HASH
```

`HOST` is the hostname of the page that embeds the iframe (e.g. `www.coatue.com`). If you
don't have the iframe URL, open the host page in playwright/devtools and inspect:

```js
[...document.querySelectorAll('iframe')].map(f => f.src)
```

## Verification

- VTT file should be > 1 KB and contain `WEBVTT` header + numbered cues.
- Stripped text file word count should be plausible for the video length (≈ 150 wpm
  for normal speech).

## Notes

- The VTT is **auto-generated** (`provenance":"ai_generated"`). Proper nouns and
  brand-name acronyms are often misheard ("Computer Use" → "CP", "Cherny" → "Cherney").
  Re-read the transcript with that bias in mind, especially for names, product
  codenames, and numbers.
- The signed URL has an `expires` parameter — typically valid for many days, but if
  it 403s, re-fetch step 1 to get a fresh signature.
- If `text_tracks` returns `[]`, the video has no captions enabled. Falling back to
  `yt-dlp --write-auto-subs` won't help (same Referer block); use Whisper on a screen
  recording instead.
- This works because Vimeo enforces playback restrictions on the **video stream** but
  not on the player's HTML config payload, which leaks the captions URL. This has been
  the behavior for years; if Vimeo ever closes it, the fallback is to drive the embed
  inside playwright with the correct Referer and read `player.getTextTracks()` via the
  Vimeo Player API.
- For multilingual content, `text_tracks` is an array — check `lang` field for other
  available subtitle tracks beyond auto-generated English.

## Example

Coatue × Boris Cherny interview, May 2026:

- Embed page: `https://www.coatue.com/blog/video/interview-with-claude-code-creator`
- Iframe src: `https://player.vimeo.com/video/1195836424?h=a0154d0f4b`
- Direct visit → "由于隐私设置，该视频无法在此处播放"
- One curl with `Referer: https://www.coatue.com/` → captions URL leaked
- Final transcript: 881 VTT lines / 2309 words / ~12 minutes of dialogue.

## References

- [Vimeo Player text-tracks docs](https://developer.vimeo.com/player/sdk/reference#texttrack)
  (Player API; useful as a fallback when the HTML scrape stops working)
- WebVTT spec: <https://www.w3.org/TR/webvtt1/>
