---
name: router9
description: >
  All-in-one AI skills via Router9 API — speech recognition, text-to-speech,
  image description, OCR, image generation, and file storage. Use when the user
  asks to transcribe audio, generate speech, describe or analyze images, extract
  text from images, generate images from text prompts, or manage files.
license: MIT
homepage: https://router9.com
compatibility: Requires Python 3.10+ and a Router9 API key (ROUTER9_API_KEY env var).
credentials:
  - name: ROUTER9_API_KEY
    description: Router9 API key, obtained from https://router9.com/settings/api-keys
    required: true
metadata:
  author: router9
  version: "1.0.2"
  homepage: https://router9.com
  origin: https://router9.com
  env:
    - name: ROUTER9_API_KEY
      required: true
      description: Router9 API key (https://router9.com/settings/api-keys)
  openclaw:
    primaryEnv: ROUTER9_API_KEY
    requires:
      env:
        - ROUTER9_API_KEY
      bins:
        - python3
allowed-tools: Bash(python:*) Bash(python3:*)
---

# Router9 Skills

Router9 provides AI-powered tools via a bundled CLI (`scripts/router9.py`).
Set the `ROUTER9_API_KEY` environment variable before use.

## Quick Reference

    # Transcribe audio to text
    python scripts/router9.py transcribe audio.mp3 --language en

    # Text-to-speech
    python scripts/router9.py tts "Hello world" -o speech.mp3 --voice alloy

    # Describe an image
    python scripts/router9.py describe photo.jpg --prompt "What breed is this dog?"

    # Extract text from an image (OCR)
    python scripts/router9.py ocr document.jpg

    # Generate an image
    python scripts/router9.py generate "A sunset over mountains" -o output.png

    # Upload a file
    python scripts/router9.py upload report.pdf

    # Download a file
    python scripts/router9.py download file-abc123 -o report.pdf

    # List files in storage
    python scripts/router9.py list

    # Delete a file
    python scripts/router9.py delete file-abc123

    # Check storage usage
    python scripts/router9.py usage

## 1. Speech Recognition (ASR)

Transcribe audio files to text. Use when the user needs to transcribe audio or
video files.

    python scripts/router9.py transcribe <file> [--language <code>]

- `file`: Audio file path (mp3, wav, m4a, webm, mp4)
- `--language`: ISO 639-1 language code (e.g. "en", "ja", "zh")

Output (JSON to stdout):

    { "text": "Transcribed content here...", "language": "en", "duration": 12.5 }

## 2. Text-to-Speech (TTS)

Convert text to spoken audio. Use when the user needs to generate speech or
audio from text.

    python scripts/router9.py tts <text> -o <output> [--voice <id>] [--format <fmt>]

- `text`: Text to synthesize (max 4096 characters)
- `-o`: Output file path (required)
- `--voice`: Voice ID (default: "alloy")
- `--format`: "mp3" (default), "wav", "opus"

Output: Writes audio file to `-o` path.

## 3. Image Description

Describe image content in natural language. Use when the user needs to analyze,
describe, or understand what is in an image.

    python scripts/router9.py describe <file> [--prompt <question>]

- `file`: Image file path (jpg, png, webp, gif)
- `--prompt`: Specific question about the image

Output (JSON to stdout):

    { "description": "A golden retriever sitting on a park bench..." }

## 4. OCR (Text Extraction)

Extract text from images — printed, handwritten, signs, and labels. Use when the
user needs to read text from an image or document scan.

    python scripts/router9.py ocr <file>

- `file`: Image file path (jpg, png, webp, gif)

Output (JSON to stdout):

    { "fullText": "Invoice #1234\nTotal: $150.00", "blocks": [...] }

## 5. Image Generation

Generate images from text prompts. Use when the user asks to create, generate,
or draw images.

    python scripts/router9.py generate <prompt> -o <output>

- `prompt`: Text description of the image to generate
- `-o`: Output file path (required)

Output: Saves generated image to `-o` path.

## 6. File Upload (Storage)

Upload a local file to agent storage using presigned URLs (direct-to-S3).

    python scripts/router9.py upload <file>

- `file`: Local file path to upload (max 50 MB)

Output (JSON to stdout):

    { "id": "file-abc123", "filename": "report.pdf", "sizeBytes": 204800 }

## 7. File Download (Storage)

Download a file from agent storage by its ID.

    python scripts/router9.py download <file_id> [-o <output>]

- `file_id`: The file ID returned from upload or list
- `-o`: Output file path (default: original filename)

Output (JSON to stdout):

    { "status": "ok", "file": "report.pdf" }

## 8. List Files (Storage)

List files in agent storage.

    python scripts/router9.py list [--page <n>] [--limit <n>]

- `--page`: Page number (default: 1)
- `--limit`: Items per page (default: 50)

Output (JSON to stdout):

    { "data": [{ "id": "file-abc123", "filename": "report.pdf", ... }], "pagination": { ... } }

## 9. Delete File (Storage)

Delete a file from agent storage.

    python scripts/router9.py delete <file_id>

- `file_id`: The file ID to delete

Output (JSON to stdout):

    { "status": "ok", "message": "File deleted." }

## 10. Storage Usage

Check storage usage and quota.

    python scripts/router9.py usage

Output (JSON to stdout):

    { "usedBytes": 1073741824, "limitBytes": 5368709120, "usedFormatted": "1.0 GB", "limitFormatted": "5.0 GB" }

## Quota

Usage is metered per billing period. Each tool has its own quota.
Check remaining quota in the Router9 dashboard at /settings/skills.
