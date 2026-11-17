# Reading-speed limits and the method behind them

## What CPS measures

```
CPS = characters in the cue ÷ seconds on screen
```

- **Characters**: everything the eye reads, spaces and punctuation included;
  only the line break between two rows and formatting tags are left out. Some
  tools skip spaces or punctuation, so their numbers come out lower for the
  same cue. Compare like with like.
- **Seconds**: end time minus start time, which is how long the cue is on
  screen, not how long the speaker took to say it.

## Limits in the major style guides

| Guideline | Reading speed | Line length | Lines | Duration |
|---|---|---|---|---|
| Netflix, English (adult) | up to 20 CPS | 42 characters | 2 max | 5/6 s to 7 s |
| Netflix, English (children's) | up to 17 CPS | 42 characters | 2 max | 5/6 s to 7 s |
| Netflix, Simplified Chinese (adult) | up to 9 CPS | 16 characters | 2 max | 5/6 s to 7 s |
| Netflix, Japanese | up to 4 CPS | 13 full-width characters | 2 max | 5/6 s to 7 s |
| BBC | 160–180 words per minute (≈ 14–16 CPS) | about 68% of a 16:9 frame width | 2 (3 if nothing important is covered) | about 0.3 s per word minimum |

The skill's Latin default is 17 CPS, the conservative ceiling: it leaves room
for slow readers and people reading in a second language. Use 20 for adult
programs when the user asks for the Netflix adult limit.

Pick the threshold by the **script on screen**, not the source language: an
English translation of a Chinese video is checked as English.

## Converting words per minute

English averages about 5.4 characters per word including the following space:

| WPM | ≈ CPS |
|---|---|
| 140 | 12.6 |
| 160 | 14.4 |
| 180 | 16.2 |
| 200 | 18.0 |
| 220 | 19.8 |

## Why timing comes before text

ScribeToAny measured machine-made subtitles of a 2 min 48 s English voiceover
(447 words, 189 WPM while speaking), cut into cues of at most 84 characters and
7 seconds, each cue timed exactly to its first and last word:

| Step | Cues | Median CPS | Over 17 CPS | Over 20 CPS | Shorter than 5/6 s |
|---|---|---|---|---|---|
| A. Cues timed to the words | 69 | 19.3 | 47 (68%) | 29 (42%) | 17 |
| B. + end extended into the following pause | 69 | 15.5 | 20 (29%) | 9 (13%) | 9 |
| C. + short neighbours merged | 41 | 15.5 | 10 (24%) | 3 (7%) | 1 |

After B and C, bringing every cue to 17 CPS meant cutting 40 of 2,399
characters (1.7%). One recording, one voice, clean pauses: real conversation
has fewer pauses, so condensing matters more there. The order still holds:
fix the timing before you cut words.

Full write-up: https://scribetoany.com/blog/subtitle-reading-speed-cps

## Sources

- Netflix, English (USA) Timed Text Style Guide:
  https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide
- Netflix, Timed Text Style Guide: General Requirements:
  https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements
- Netflix, Chinese (Simplified) Timed Text Style Guide:
  https://partnerhelp.netflixstudios.com/hc/en-us/articles/215986007-Chinese-Simplified-Timed-Text-Style-Guide
- Netflix, Japanese Timed Text Style Guide:
  https://partnerhelp.netflixstudios.com/hc/en-us/articles/215767517-Japanese-Timed-Text-Style-Guide
- BBC Subtitle Guidelines:
  https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/
