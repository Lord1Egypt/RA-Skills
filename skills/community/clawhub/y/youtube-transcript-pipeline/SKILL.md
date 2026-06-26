---
name: youtube-transcript-pipeline
description: Generate, clean, correct, translate, and package YouTube interview transcripts with speaker-attributed timestamps into reusable deliverables. Use for workflows involving Deepgram transcription, diarization correction, bilingual output, and structured folder packaging for handoff.
---

# YouTube Transcript Pipeline

## Overview

This skill turns a YouTube link into a complete transcript package:
- speaker-labeled, timestamped transcript
- cleaned/interviewer-vs-main speaker correction passes
- optional Chinese translation preserving line format
- optional image/download + workspace packaging

Use this when user asks for: transcript production, diarization fixes, interview cleanup, Chinese translation of transcript, or reusable handoff folders.

## Quick Start

### Inputs
- YouTube URL
- Deepgram API key (Nova-3 for best results)
- preferred speakers (main/interviewer defaults if known)

### Outputs
Place all outputs in a structured folder:
- `transcripts/` (raw / cleaned / translated)
- `artifacts/` (audio + thumbnails)
- `scripts/` (workflow helpers)
- `snippets/` (small JSONs, helper files)
- `MANIFEST.txt`

## Workflow

### 1) Prepare assets
1. download audio from YouTube
2. split into manageable chunks (e.g., 180s)
3. run Deepgram chunked transcription with `nova-3`, word-level output if possible

Suggested command (adapt paths):
```bash
python3 resilient_dg_transcribe_resume.py \
  --audio-dir /tmp/dg_chunks_work2 \
  --max 0 --chunk-sec 180 --model nova-3 --timeout 240
```

### 2) Produce base transcripts
- keep all baseline artifacts (`transcript_*.json`, `transcript_speakers_*.txt`)
- do not delete intermediates; they are useful for audit

### 3) Fix speaker attribution
- apply conservative correction pass first (prefering **main speaker default**)
- review and accept swaps only for clear interviewer-style short questions/interjections
- keep line/timestamp count unchanged

### 4) Translate (optional)
- preserve format: `[$TS] Speaker: text`
- keep timestamps + speaker tags unchanged
- keep technical terms unless explicitly requested otherwise

### 5) Package for delivery
- create workbench folder with clear naming and manifest
- add short summary files (e.g., `summary_30s_zh.txt`, `summary_1min_zh.txt`)
- optional git init + commit for reproducibility

## Quality Rules (important)
- Preserve structure exactly unless user asks otherwise.
- Keep format and timestamps consistent across all versions.
- Use conservative speaker reassignment to avoid over-attributing interviewer lines.
- Append changes in memory logs for durable state (per workspace conventions).

## Resource Mapping

### scripts/
- `create_youtube_transcript_workbench.sh`: creates standardized output folders and manifest, optionally copies key files
- `translate_transcript_google.py`: batch-translates timestamped transcript while preserving format
- `rebuild_from_words.py`: optional word-level rebuild/reconciliation utility for diarization consistency

### references/
- `workflow.md`: detailed decision points for conservative speaker fixes and translation fallback handling
