---
name: tracked-video-analysis
description: Analyze local or linked video files and convert them into structured summaries of features, functions, workflows, or topics. Use when a user wants a walkthrough/demo video reviewed, asks to extract and organize features from a video, needs category > function > description > benefit summaries, or wants a tracked local workflow for long/noisy video transcription. Especially useful when chat media is inaccessible and you need a reliable two-stage process with explicit progress files.
---

# Tracked Video Analysis

Use this skill for **long, noisy, or operationally awkward videos** where trust and visibility matter as much as the final summary.

The core idea is simple:

1. **Extract content first**
2. **Structure it second**
3. **Track both stages explicitly**

Never claim that a background process is still running unless a live OS process or a fresh status file proves it.

## Core workflow

### 1) Acquire the video reliably

Prefer this order:

1. direct local file
2. direct downloadable link
3. document upload
4. external file host fallback

If chat media is inaccessible, ask for a direct link instead of retrying vague media access indefinitely.

Use `tmp/video_analysis/` as the working directory.

### 2) Prepare local tools without root

Prefer workspace-local packages over system installs.

Useful local tools:

- `ffmpeg-static`
- `ffprobe-static`
- `@xenova/transformers`
- `wavefile`

If root/elevated package install is blocked, do **not** stall the task—install locally in the workspace when possible.

### 3) Run tracked extraction

Extraction should produce:

- `tmp/video_analysis/status.json`
- `tmp/video_analysis/progress.log`
- `tmp/video_analysis/transcript.jsonl`
- `tmp/video_analysis/analysis.md`

Rules:

- Prefer chunking over one-shot whole-video ASR.
- Prefer lighter ASR first for stability.
- Update status after each chunk.
- If a run dies, resume from files when practical instead of starting from zero automatically.

### 4) Run tracked final structuring

Structuring should produce:

- `tmp/video_analysis/final_status.json`
- `tmp/video_analysis/final_progress.log`
- `tmp/video_analysis/final_analysis.md`

This stage should:

- clean filler and repeated phrases
- group related chunks
- infer categories
- normalize wording
- convert raw transcript into the user’s requested format

### 5) Report status honestly

Use these rules:

- **Extraction running** → report `status.json`
- **Extraction complete, no final process running** → say so plainly
- **Final structuring running** → report `final_status.json`
- **Final result ready** → read `final_analysis.md` and answer normally

## Standard output formats

Common targets:

- **Category → function → description → benefit**
- **Category → function → short description**
- **Function list + timestamps**
- **Clean summary with confidence caveats**

For noisy ASR, prefer readable normalization over false precision.

## Status discipline

Do **not** say “the process is running” unless at least one of these is true:

- the OS process is alive
- the relevant status file is actively updating

If extraction finished, explicitly say:

- extraction is complete
- no live extraction process remains
- only structuring remains (if true)

## Read these files when needed

- Read `references/pipeline.md` for the canonical tracked workflow and failure handling.
- Use `scripts/transcribe_tracked_light.mjs` for extraction as a starting point.
- Use `scripts/final_structurer.py` for initial structuring as a starting point.

## Delivery style

Prefer concise, readable sections.

When the user wants a polished deliverable:

1. create a clean `.md` file
2. keep the structure visually pleasant
3. send it as a document/file if requested

## Practical note

This skill is optimized for **operational reliability**, not perfect transcription fidelity. If ASR is messy, produce a useful structured summary with explicit uncertainty rather than pretending the raw transcript is exact.
