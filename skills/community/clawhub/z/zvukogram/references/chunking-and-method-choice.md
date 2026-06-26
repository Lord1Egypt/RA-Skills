# /text vs /longtext vs chunking — practical guide

Source: https://zvukogram.com/node/api/

## 1) Decision rule (fast & reliable)

1) If the text chunk is **<= 1000 chars** and you want the result **immediately** → use **`/text`**.
2) If total text is **up to 1,000,000 chars** and you can wait / poll → use **`/longtext`**.
3) If you need **timecodes / cuts** → use **`/subs`**.
4) If you want **instant results for a long text** (and control over pacing/voices) → **chunk yourself** and call `/text` multiple times.

## 2) Why chunking is often better for podcasts

Chunking (many `/text` calls) gives you:

- “Edit points” between segments (easy to cut/reorder)
- Multi-voice flows (one voice per request) + merge
- More stable prosody (each chunk is a clean sentence/paragraph)
- No queue waiting for `/longtext` (you get each part as soon as it’s ready)

Trade-off:
- More API calls; you need merging and slightly more bookkeeping.

## 3) Safe chunking strategy

Goals:
- Keep each chunk **<= 1000 characters** (hard API limit for `/text`).
- Avoid breaking inside SSML tags.
- Prefer splitting on **paragraphs → sentences**.

Recommended approach:

1) Normalize whitespace.
2) Split by blank lines (paragraph boundaries).
3) Within a paragraph, split by sentence punctuation (`.`, `!`, `?`, `…`).
4) Accumulate sentences until adding one would exceed your limit (use ~900–950 chars as a safety buffer).

### SSML-aware rule

If you use SSML tags like `<sub>...</sub>` or `<say-as ...>...</say-as>`, never cut inside a tag pair.

If you must chunk SSML-heavy text, chunk **before** tagging or ensure each chunk is well-formed XML fragments.

## 4) Merging audio

Two common patterns:

### A) ffmpeg concat demuxer (most reliable)

Create `list.txt`:

```text
file 'part_001.mp3'
file 'part_002.mp3'
file 'part_003.mp3'
```

Then:

```bash
ffmpeg -y -f concat -safe 0 -i list.txt -acodec copy out.mp3
```

### B) concat protocol (works for some mp3, less universal)

```bash
ffmpeg -y -i "concat:part1.mp3|part2.mp3|part3.mp3" -acodec copy out.mp3
```

## 5) Polling /result correctly

Only needed for `/longtext` or `/subs`.

- Start polling `/result` with `id`.
- Typical interval: **2 seconds**.
- For very long jobs: **5 seconds**.
- Stop when `status` is:
  - `1` → ready (`file` present)
  - `-1` → error (`error` present)

## 6) Non-negotiable production rule

If text exceeds `/text` limits, do **not** silently truncate it.
That is a production bug, not a fallback strategy.
Use SSML-safe chunking or switch to `/longtext`.

## 6) Limits recap

- `/text`: max **1000 characters** per request
- `/longtext` and `/subs`: max **1,000,000 characters**

(From official API docs.)
