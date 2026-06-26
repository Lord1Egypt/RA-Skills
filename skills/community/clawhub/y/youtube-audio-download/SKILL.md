---
 name: youtube-audio-download
 description: Download YouTube video audio and convert to MP3. Supports age-restricted videos with cookies.
 tools:
   - download_audio
---

# Youtube Audio Download

## Usage

```bash
python scripts/download_audio.py <URL> [--cookies cookies.txt] [--output-dir dir]
```

## Parameters

- `url` (required): YouTube video URL
- `cookies_path` (optional): Path to cookies.txt for age-restricted videos
- `output_dir` (optional): Output directory, default: "works/audio"

## Returns

```json
{
  "success": true,
  "audio_path": "H:/works/audio/video_title-xxxxx.mp3",
  "title": "Video Title",
  "duration": 1200,
  "file_size_mb": 15.5
}
```

## Tools

## download_audio

Download YouTube audio to MP3


## Workflow Integration

This skill is part of the YouTube translation workflow:
1. **youtube-audio-download**: Download audio from YouTube
2. **doubao-launch**: Launch Doubao translation window
3. **audio-play**: Play the downloaded audio
4. **doubao-capture**: Capture translated subtitles

## Execution

All skills execute on Windows Python via WSL cross-platform call:
```
wsl -> python.exe scripts/download_audio.py ...
```

## Error Handling

All skills return JSON with `success` field:
- `success: true` - Operation completed
- `success: false` - Check `error_code` and `error_message`

## Notes

- Windows GUI automation requires visible desktop (no RDP disconnect)
- Output files are stored in Windows `works/` directory
- WSL accesses Windows files via `/mnt/h/...`
