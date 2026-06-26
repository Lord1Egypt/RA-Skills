---
name: remotion-word-highlight-subtitles
description: Add word-level highlighted subtitles to local short videos using Whisper word timestamps and Remotion rendering.
version: 0.1.4
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - ffmpeg
        - ffprobe
        - whisper
        - node
        - npm
    emoji: "🎬"
---

# Remotion Word Highlight Subtitles

## Overview

This skill turns a local video into a subtitled video using the reusable "fine version": Whisper word timestamps plus Remotion-rendered current-word highlighting. Use this instead of plain SRT burn-in unless the user explicitly asks for simple static subtitles.

Detailed usage guide, README, and effect preview: https://github.com/0x00000003/remotion-word-highlight-subtitles

## Trigger Phrases

Use this skill for requests like:

- "给这个视频添加字幕：/path/to/video.mp4"
- "给这个视频加逐词高亮字幕"
- "按之前 Remotion 那个字幕方案处理这个视频"
- "重新转写 word timestamps，然后加当前词高亮字幕"

If the user only gives one video path, write the output next to the source video.

## Defaults

- Source: local `.mp4`, `.mov`, `.m4v`, or audio/video file with usable audio.
- Output: `<source-stem>_remotion逐词高亮字幕.mp4` in the same directory unless the user names another target.
- Transcription: Whisper with word timestamps, Chinese by default: `--language zh --word_timestamps True --output_format json`.
- Transcript QA: mandatory before rendering. Build a tiny glossary from the user prompt, folder/file names, visible context, and topic; correct obvious ASR mistakes in product/model/person/place names, English terms, numbers, and homophones.
- Caption data: Remotion caption chunks built from Whisper words, with token-level `startMs` and `endMs`. Long Whisper segments must be split by punctuation, timing gaps, duration, or length before rendering.
- Caption position: keep all captions in a screenshot-friendly lower band, slightly above the bottom UI area. Start around `height * 0.28` bottom padding, then adjust only if the source framing clearly needs it.
- Visual style: bold Chinese UI font, white base text, current token yellow, optional sparse keyword accent, and black shadow/outline for readability.
- Subtitle sizing: treat font size as a hard visual gate, not a loose style hint. For landscape 1080p footage, target `height * 0.056` (about `60px`) and never render below `56px`; for vertical `720x1280`, target `40-46px`. For other sizes, scale from height but enforce the same perceived size in still QA.
- Display punctuation: default subtitles are clean Chinese display text. Strip visible sentence punctuation from caption text and token text before rendering, including `。 ， 、 ？ ！ ： ； , . ? ! : ;`. Keep punctuation only for splitting/timing unless the user explicitly asks for verbatim punctuation.
- Verification: check the rendered file exists, keeps audio, matches the source duration closely, and visually inspect stills before accepting the style.

## Workflow

1. Inspect the source with `ffprobe` for width, height, fps, duration, and audio presence.
2. Build a small domain glossary before transcription. Include likely product names, model names, people, places, mixed Chinese/English terms, numbers, and terms hinted by the folder or filename.
3. Run Whisper word timestamp transcription. Prefer a cached/local model that works on the machine; `turbo` is a good default when available. Use `--initial_prompt` when the glossary contains high-risk names or English terms.
4. Do a mandatory transcript QA pass before rendering. Read every segment, compare it with the video's topic/context, and create a correction map for obvious ASR mistakes. Do not render while known mistakes remain.
5. Convert the Whisper JSON to `public/captions.json` using `scripts/whisper_json_to_captions.py`, passing corrections with `--replace` or `--replace-phrase`. Apply transcript corrections, merge terms, strip display punctuation, and keep the helper's caption splitting enabled if Whisper returns long paragraphs.
6. Build or reuse a small Remotion project in the video's folder. Copy the video to `public/input.mp4` or encode an H.264 compatibility copy as `public/input-h264.mp4`.
7. Set the Remotion composition to the exact source width, height, fps, and duration in frames.
8. Before the full render, render and inspect at least two stills from the Remotion composition: one long/two-line caption and one dense keyword/current-token caption. Fix muddy text, excessive outline, large dark backing, bad line breaks, too-small text, visible display punctuation, poor placement, or remaining typo/wrong-character subtitles before rendering the final video.
9. Render with Remotion to the output path next to the source.
10. Verify the final output with `ffprobe`; extract and inspect a still from the rendered video to confirm the final encoded file kept the approved subtitle look.

## Whisper Command

Use this shape, adjusting model and paths as needed:

```bash
whisper "/absolute/path/video.mp4" --model turbo --language zh --word_timestamps True --output_format json --output_dir "/absolute/path"
```

For names and mixed Chinese/English topics, add a short prompt rather than relying on Whisper to infer them:

```bash
whisper "/absolute/path/video.mp4" \
  --model turbo \
  --language zh \
  --word_timestamps True \
  --output_format json \
  --initial_prompt "本视频可能出现这些词：Cursor、Kimi 2.5、马斯克、AI大模型、转推、套壳。" \
  --output_dir "/absolute/path"
```

If Whisper fails on the video container, extract audio first:

```bash
ffmpeg -y -i "/absolute/path/video.mp4" -vn -ac 1 -ar 16000 "/absolute/path/video_audio.wav"
```

Then run Whisper on the WAV and keep the output naming clear.

## Mandatory Transcript QA

After Whisper finishes, print or read the segment transcript before building captions. Treat this as a required gate, not a nice-to-have.

Check especially:

- product, model, company, person, and place names
- mixed Chinese/English terms such as `Cursor`, `Kimi 2.5`, `ChatGPT`, `Claude`, `OpenAI`
- numbers, dates, model versions, and acronyms
- Chinese homophones that are plausible but wrong in context, such as "却" versus "圈" or "死腿" versus "转推"
- low-confidence words if the Whisper JSON includes probabilities

Create a short correction map and apply it before rendering. Use `--replace` for single-token fixes and `--replace-phrase` for words split across adjacent Whisper tokens.

Example:

```bash
python3 scripts/whisper_json_to_captions.py \
  "/absolute/path/transcript.json" \
  "/absolute/path/remotion-project/public/captions.json" \
  --replace-phrase "科舍=Cursor" \
  --replace-phrase "KMI 2.5=Kimi 2.5" \
  --replace-phrase "Kimi 2.5=Kimi 2.5" \
  --replace-phrase "AI却=AI圈" \
  --replace-phrase "死腿=转推" \
  --merge-term "Cursor" \
  --merge-term "Kimi 2.5" \
  --keyword "AI" \
  --keyword "Kimi 2.5"
```

If a correction is uncertain, prefer rerunning Whisper with a better `--initial_prompt` or inspect the relevant audio/video moment before deciding. Report the correction map in the final response.

## Caption JSON

Remotion should load `public/captions.json` with this shape:

```json
[
  {
    "text": "我们用手机随便拍张照片",
    "startMs": 0,
    "endMs": 1600,
    "tokens": [
      { "text": "我们", "startMs": 0, "endMs": 300, "keyword": false },
      { "text": "手机", "startMs": 440, "endMs": 700, "keyword": true }
    ]
  }
]
```

Use the helper script:

```bash
python3 scripts/whisper_json_to_captions.py \
  "/absolute/path/transcript.json" \
  "/absolute/path/remotion-project/public/captions.json" \
  --keyword "提示词" \
  --keyword "Codex" \
  --replace-phrase "错识别词=正确词" \
  --max-caption-chars 28 \
  --max-caption-duration-ms 4200 \
  --split-gap-ms 260 \
  --min-punctuation-caption-ms 900
```

Run the transcript QA pass before this conversion command. If any correction changes adjacent tokens into one display term, also pass that final term with `--merge-term` or a same-text `--replace-phrase` so the highlight appears as a clean word instead of broken characters.

By default, `scripts/whisper_json_to_captions.py` strips visible display punctuation from final caption text and tokens while still using punctuation as a split signal. Do not pass `--keep-display-punctuation` unless the user explicitly asks for verbatim transcript punctuation. If building JSON manually, remove punctuation-only tokens and trim trailing punctuation before rendering.

The helper splits long Whisper segments by visible length, duration, punctuation, and word timing gaps. Keep this behavior on for short-video subtitles; otherwise a single Whisper paragraph can become an unreadable multi-line caption.

## Remotion Caption Layer Requirements

The caption layer should:

- Use `OffthreadVideo` for the source video.
- Load `captions.json` with `delayRender`, `continueRender`, and `staticFile`.
- Find the active caption by `currentMs >= startMs && currentMs < endMs`.
- Highlight the active token when `currentMs` is within the token's timing.
- Use keyword coloring only as a secondary accent; the current spoken token is the main effect.
- Keep `letterSpacing: 0`.
- Render clean display subtitles without sentence-final punctuation. Do not show comma, period, question mark, exclamation mark, colon, semicolon, or dunhao tokens unless the user asked for verbatim punctuation.
- Treat caption size as a hard gate. For 1080p landscape, the rendered subtitle should be around `60px` and never below `56px`; if a still looks like small UI annotation text, enlarge and rerender.
- Keep all captions at the normal position; do not include special screenshot-sentence placement unless the user explicitly asks.
- Do not use `WebkitTextStroke` as a thick Chinese subtitle outline. It easily eats the white fill at small resolutions. Prefer multi-direction `textShadow`; if `WebkitTextStroke` is used at all, keep it at or below `1.5px` and verify a still.
- Do not use a large semi-transparent rounded black rectangle behind the whole caption by default. If the footage truly needs backing, use a very subtle per-line backing, opacity `<= 0.16`, tight padding, and verify it does not look like a dark banner.

Reject and revise any still where the caption has muddy/gray text, a thick black halo, a large black box, clipped words, awkward wrapping, visible sentence punctuation, text that is too small for the frame, or placement over the mouth/chin in a talking-head video.

Use these style constants as the baseline:

```tsx
const captionBottom = Math.round(height * 0.28);
const isLandscape = width >= height;
const baseCaptionFontSize = Math.round(height * (isLandscape ? 0.056 : 0.032));
const minCaptionFontSize = isLandscape && height >= 1000 ? 56 : Math.round(height * 0.032);
const captionFontSize = Math.max(baseCaptionFontSize, minCaptionFontSize);
const captionMaxWidth = Math.round(width * 0.88);
const activeColor = "#FFE45C";
const keywordColor = "#D6FFF8";
const outlinePx = Math.min(3, Math.max(1.5, captionFontSize * 0.055));
```

Use a clean shadow outline rather than a heavy stroke:

```tsx
const textShadow = [
  `${outlinePx}px 0 0 rgba(0, 0, 0, 0.96)`,
  `-${outlinePx}px 0 0 rgba(0, 0, 0, 0.96)`,
  `0 ${outlinePx}px 0 rgba(0, 0, 0, 0.96)`,
  `0 -${outlinePx}px 0 rgba(0, 0, 0, 0.96)`,
  `0 ${outlinePx * 1.4}px ${outlinePx * 1.4}px rgba(0, 0, 0, 0.72)`,
].join(", ");
```

For a `1920x1080` landscape video, this yields about `fontSize: 60`, and it must not fall below `56`. For a `720x1280` vertical video, this is roughly `paddingBottom: 358`, `fontSize: 41`, `maxWidth: 634`, and a `2px` outline. For the original `2160x2974` source that inspired this skill, the equivalent bottom padding was about `830`.

## Keyword Handling

If the user does not specify keywords, infer a small set from the transcript:

- product/tool names: `Codex`, `Remotion`, `Whisper`
- content objects: `提示词`, `照片`, `手机`, `封面`
- place names or nouns that carry the video's hook
- numbers or outcomes that are important to the promise

Keep keyword highlighting sparse. Too many colored words makes the active yellow word less clear.

## Output Naming

Prefer:

```text
<source-stem>_remotion逐词高亮字幕.mp4
```

If iterating for the same source, add `_v2`, `_v3`, etc. Do not overwrite the user's source file.

## Final Response

Tell the user the output path, mention that it used the reusable Remotion + Whisper word timestamp flow, and include the transcript correction map or say no corrections were needed. If any verification step could not be run, say that plainly.
