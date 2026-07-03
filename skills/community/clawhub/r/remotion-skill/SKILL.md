---
name: Remotion
description: >
  Best-practice guidance for building, editing, and debugging Remotion video
  projects with React and TypeScript. Use this skill for Remotion compositions,
  animations, transitions, media playback, captions, text effects, charts,
  Tailwind styles, Lottie, Three.js or React Three Fiber scenes, dynamic
  metadata, asset loading, video/audio duration probes, frame extraction, and
  render-safe timing or sequencing.
---

# Remotion

Build and debug Remotion videos with focused references for React,
TypeScript, animation timing, media assets, captions, transitions, charts, 3D,
and render-safe composition structure.

Use this skill when you are creating a Remotion project, editing a composition,
adding motion, syncing audio or video, building captions, rendering charts,
using Lottie or 3D, measuring text, loading assets, or checking media duration
and dimensions.

## What This Helps With

| Area | Use it for |
| --- | --- |
| Compositions | Set up compositions, stills, folders, default props, and dynamic metadata. |
| Animation | Use frame-based timing, interpolation, easing, springs, sequencing, and transitions. |
| Media | Add local or remote images, video, audio, GIFs, trimming, looping, volume, and playback speed. |
| Captions | Import SRT captions, display subtitles, and work with transcription workflows. |
| Typography | Load fonts, use Tailwind, fit text, and measure text or DOM nodes. |
| Data visuals | Build animated charts with reusable chart examples. |
| Text effects | Add typewriter and word-highlight animation patterns. |
| 3D and motion assets | Work with Three.js, React Three Fiber, and Lottie. |
| Media inspection | Get audio/video duration, dimensions, decodability, and extracted frames. |

## Why This Remotion Skill

| This skill | Starting from scattered docs or memory |
| --- | --- |
| Groups Remotion topics into task-focused references. | Search across many docs pages before finding the right API. |
| Includes reusable examples for charts and text animations. | Rebuild common motion patterns from scratch. |
| Covers timing, sequencing, trimming, transitions, and media together. | Debug render timing and media behavior piecemeal. |
| Includes references for captions, fonts, Tailwind, 3D, Lottie, and media probes. | Jump between unrelated examples for common video-building tasks. |
| Encourages render-safe, deterministic Remotion patterns. | Risk preview-only logic that breaks or drifts during render. |

Use this when you want practical Remotion guidance organized around the video
task you are doing.

## How To Use

1. Identify the task: composition setup, animation, media, captions, text,
   charts, 3D, Lottie, metadata, measurement, or media inspection.
2. Open the matching reference file from `references/`.
3. Reuse the example assets when they match the task.
4. Adapt the code to the existing Remotion project structure and package
   versions.

## Reference Map

| File | Purpose |
| --- | --- |
| `references/compositions.md` | Compositions, stills, folders, default props, and metadata. |
| `references/animations.md` | Interpolation, easing, and frame-based animation basics. |
| `references/timing.md` | Timeline timing, frame math, and animation coordination. |
| `references/sequencing.md` | Scene order, offsets, delays, and timeline layout. |
| `references/transitions.md` | Transitions between scenes and visual states. |
| `references/trimming.md` | Trim media and control start or end timing. |
| `references/assets.md` | Asset loading and project media organization. |
| `references/images.md` | Images, sizing, loading, and render-safe usage. |
| `references/videos.md` | Video playback, timing, and media behavior. |
| `references/audio.md` | Audio playback, volume, speed, pitch, and looping. |
| `references/display-captions.md` | Display captions and subtitles in compositions. |
| `references/import-srt-captions.md` | Import SRT captions. |
| `references/transcribe-captions.md` | Caption transcription workflow notes. |
| `references/fonts.md` | Font loading and typography. |
| `references/tailwind.md` | Tailwind usage in Remotion. |
| `references/measuring-text.md` | Measure and fit text. |
| `references/measuring-dom-nodes.md` | Measure DOM nodes for layout. |
| `references/charts.md` | Animated chart patterns. |
| `references/text-animations.md` | Typewriter and word-highlight text effects. |
| `references/3d.md` | Three.js and React Three Fiber patterns. |
| `references/lottie.md` | Lottie animation usage. |
| `references/gifs.md` | GIF usage in Remotion. |
| `references/can-decode.md` | Check whether media can be decoded. |
| `references/extract-frames.md` | Extract video frames. |
| `references/get-audio-duration.md` | Get audio duration. |
| `references/get-video-dimensions.md` | Get video dimensions. |
| `references/get-video-duration.md` | Get video duration. |

## Example Assets

| File | Purpose |
| --- | --- |
| `assets/charts-bar-chart.tsx` | Reusable animated bar chart example. |
| `assets/text-animations-typewriter.tsx` | Typewriter text animation example. |
| `assets/text-animations-word-highlight.tsx` | Word-highlight text animation example. |
