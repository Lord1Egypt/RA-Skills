---
name: web-video-transcribe-docx
description: Offline-first workflow for turning Chinese web page video or audio into text and Word deliverables. Use when Codex needs to (1) extract playable media streams from arbitrary web pages, including pages that expose MP4, M3U8, MPD, or separate audio streams, (2) download direct media URLs with common headers such as Referer or Origin, (3) run local Chinese ASR with SenseVoice via sherpa-onnx, (4) clean or chapterize the transcript conservatively, or (5) produce TXT and DOCX files from the result. Toutiao pages are a supported special case, not the only target.
license: MIT-0
metadata: {"openclaw":{"requires":{"anyBins":["python","python3","py"]}},"author":"qu_yw","version":"1.0.0","category":"media-transcription"}
---

# Web Video Transcribe Docx

## Overview

Use the bundled scripts to extract media, download it, transcribe it offline, and render DOCX output.

Prefer the deterministic scripts before hand-rolling new code.

Use `{baseDir}` when constructing file paths inside this skill so the instructions stay portable across agents and marketplaces.

## Environment

- Require Python 3 and local filesystem access.
- Require network access for first-run model download and for fetching page or media URLs.
- Require a local Chrome or Edge browser only when extracting media from a web page.

## Quick Start

1. Run `python {baseDir}/scripts/bootstrap_env.py` once in the target environment.
2. For a generic web page URL, run `python {baseDir}/scripts/pipeline_web_to_docx.py <url> --output-dir <dir>`.
3. For a direct media URL, run `python {baseDir}/scripts/download_url.py <url> <output>` and then `python {baseDir}/scripts/transcribe_sensevoice.py --input <file> --output-txt <txt> --output-docx <docx>`.
4. For a local media file, run `python {baseDir}/scripts/transcribe_sensevoice.py --input <file> --output-txt <txt> --output-docx <docx>`.
5. If the user asks for a polished reading version rather than a raw transcript, read [references/cleanup-guidelines.md](references/cleanup-guidelines.md), produce a refined `.txt`, and then render it with `python {baseDir}/scripts/transcript_to_docx.py`.

## Example Requests

- "Transcribe the Chinese audio from this web video and export it as a Word document."
- "Turn this MP4 into a transcript, then reorganize it into chaptered reading notes."
- "This page needs a `Referer` header for media download. Extract the media stream and convert it to DOCX."

## Workflow

### 1. Classify the source

- **Generic page URL**: Use `python {baseDir}/scripts/pipeline_web_to_docx.py` first. If the page is especially stubborn and it is a Toutiao page, `python {baseDir}/scripts/pipeline_toutiao_to_docx.py` and `python {baseDir}/scripts/extract_toutiao_media.py` remain available as site-specific fallbacks.
- **Direct media URL**: Use `python {baseDir}/scripts/download_url.py`, then transcribe.
- **Local file**: Transcribe directly.

### 2. Preserve raw outputs

- Keep the raw transcript as its own `.txt`.
- If you produce a cleaned or chapterized version, save it as a separate file.
- Do not overwrite the raw transcript unless the user explicitly asks.

### 3. Prefer the audio stream

- If a page exposes a dedicated audio stream, prefer downloading that instead of the full video stream.
- If the page only exposes a video stream, let ffmpeg decode audio during transcription.
- If the page exposes HLS or DASH manifests, prefer downloading them through the bundled downloader or pipeline instead of raw HTTP GET.

### 4. Refine conservatively

- Preserve meaning.
- Fix obvious ASR mistakes, punctuation, paragraph breaks, headings, and chapter boundaries.
- Do not invent quotes or historical claims that are not supported by the transcript.
- If a passage is too noisy to restore confidently, keep it neutral instead of fabricating detail.

### 5. Stay within scope

- Only download URLs that the user supplied directly or that the extractor captured from the target page.
- Do not request, store, or exfiltrate cookies, access tokens, or account credentials.
- Do not attempt to bypass DRM, login walls, or geo-restriction controls.
- If a page requires authenticated browser state that is not already available, say so plainly and stop at the supported boundary.

### 6. Render deliverables

- Use `python {baseDir}/scripts/transcript_to_docx.py` for generic TXT-to-DOCX rendering.
- Use the raw transcript for auditability and the refined transcript for reading quality.

## Scripts

- `scripts/bootstrap_env.py`
  Install or verify the Python packages used by this skill.
- `scripts/extract_web_media.py`
  Open a generic web page in a real browser, capture likely media URLs plus common download headers, and emit a JSON manifest.
- `scripts/extract_toutiao_media.py`
  Open a Toutiao page in a real browser, capture audio/video URLs, and emit a JSON manifest with the same schema as the generic extractor.
- `scripts/download_url.py`
  Download a direct media URL to disk with a stable user agent, optional headers, and HLS/DASH handling.
- `scripts/transcribe_sensevoice.py`
  Download the SenseVoice model on demand, segment media, run offline ASR, and emit TXT and optional DOCX.
- `scripts/transcript_to_docx.py`
  Render timestamped transcripts or chapterized notes into a Word document.
- `scripts/pipeline_web_to_docx.py`
  Run the generic end-to-end pipeline: extract, download, transcribe, and render.
- `scripts/pipeline_toutiao_to_docx.py`
  Run the Toutiao-specialized end-to-end pipeline for cases where the generic extractor is not preferred.

## References

- Read [references/workflow.md](references/workflow.md) for dependency expectations, command examples, output layout, and troubleshooting.
- Read [references/cleanup-guidelines.md](references/cleanup-guidelines.md) before polishing a noisy transcript into a chapterized reading copy.
- Read [references/publishing.md](references/publishing.md) when preparing marketplace metadata, tags, versioning, or ClawHub publish commands.

## Validation

- Run `python {baseDir}/scripts/bootstrap_env.py` before first use in a fresh environment.
- Validate the skill folder with `skill-creator/scripts/quick_validate.py`.
- Prefer testing `--help` and one representative happy path after changing the scripts.
- If extraction fails on a page, capture a direct media URL with browser tooling and continue with the downloader + transcriber.
- Do not promise support for DRM-protected streams, authenticated cookies, or sites that only expose encrypted EME playback.
