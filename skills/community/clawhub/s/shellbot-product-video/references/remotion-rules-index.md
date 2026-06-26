# Remotion Rules Index

This folder mirrors the official Remotion skill rules structure so agents can load focused guidance per task:

- `references/remotion-rules/`

Use targeted loading instead of reading all files.

## Most-used rules

- `animations.md`: foundational motion patterns
- `timing.md`: interpolation and easing
- `sequencing.md`: timeline orchestration
- `transitions.md`: scene hand-offs
- `text-animations.md`: kinetic typography
- `videos.md`: video embedding and controls
- `audio.md`: trims, fades, levels, speed
- `display-captions.md`: subtitle display patterns
- `transcribe-captions.md`: subtitle generation pipeline
- `rendering.md`: render pipeline
- `compositions.md`: composition design
- `calculate-metadata.md`: dynamic duration/size from props

## Load-by-intent map

- If building scene choreography: load `animations.md`, `timing.md`, `sequencing.md`, `transitions.md`.
- If tuning typography and headlines: load `text-animations.md`, `fonts.md`, `measuring-text.md`.
- If integrating generated assets: load `images.md`, `videos.md`, `audio.md`, `assets.md`.
- If shipping vertical social videos: load `compositions.md`, `trimming.md`, `rendering.md`.
- If adding narration/captions: load `audio.md`, `transcribe-captions.md`, and `display-captions.md`.

## Source

Rules are copied from the local Remotion toolkit package in this workspace to make this skill self-contained.
