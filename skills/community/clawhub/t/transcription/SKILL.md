---
name: transcription
description: Transcribe audio and video files using OpenAI Whisper API. Use when user wants to transcribe audio/video files, extract speech from media, or get text from recordings. Automatically handles audio extraction from video files.
---

# Transcription Skill

This skill provides transcription capabilities for audio and video files using the OpenAI Whisper API endpoint.

## Quick Start

**Send me an audio or video file** and I'll transcribe it automatically! Just attach the file to your message.

### Manual Usage

You can also run the script directly from the command line:

```bash
cd /home/openclaw/.openclaw/workspace/skills/transcription/scripts
python3 transcribe_audio.py inputfile.ogg
```

For video files:
```bash
python3 transcribe_audio.py video.mp4
```

## Supported Formats

**Audio:** mp3, wav, mp4, mpeg, mpga, m4a, ogg, webm, flac, aac, wma

**Video:** mp4, mov, avi, mkv, webm (audio extracted automatically)

## Usage Examples

How to use the python scripts for transcription:

python3 transcribe_audio.py inputfile.ogg

## Features

- **Extract timestamps** in output when needed
- **Batch processing** - send multiple files at once
- **Video support** - automatically extracts audio from video files
- **Multiple output formats** - text, JSON, SRT subtitles, VTT captions

## Technical Details

- **API Endpoint:** `http://192.168.0.11:8080/v1` (local Whisper endpoint)
- **Model:** whisper-small (default)
- **Temperature:** 0.0 (deterministic results)
- **Auto-extraction:** ffmpeg handles video → audio conversion

## Notes

- Ensure files are clear and not too noisy for best results
- Language auto-detection works well for most cases
- For batch processing, send files one at a time or specify "batch" in your request

---

**Scripts:** `scripts/transcribe_audio.py`, `scripts/transcribe_simple.py`  
**References:** `references/transcription_guide.md`