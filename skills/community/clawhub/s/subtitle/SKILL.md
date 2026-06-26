---
name: senseaudio-subtitle-generator
description: Generate synchronized subtitles (SRT/VTT/ASS) from video audio with precise timestamps. Use when users need subtitles, captions, or video transcription with timing.
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
      bins:
        - ffmpeg
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
    install:
      - kind: uv
        package: requests
      - kind: uv
        package: pydub
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---

# SenseAudio Subtitle Generator

Create accurate, synchronized subtitles for videos with proper timing, formatting, and multi-language support.

## What This Skill Does

- Extract audio from video files
- Transcribe audio with precise timestamps
- Generate subtitle files (SRT, VTT, ASS)
- Support multiple languages and translations
- Format subtitles with proper line breaks and timing

## Prerequisites

Install required Python packages:

```bash
pip install requests pydub
```

Note: You'll also need `ffmpeg` installed for video audio extraction:
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```


## Implementation Guide

### Step 1: Extract Audio from Video

```python
from pydub import AudioSegment
import subprocess

def extract_audio_from_video(video_file, output_audio="temp_audio.wav"):
    # Use ffmpeg to extract audio
    cmd = [
        "ffmpeg", "-i", video_file,
        "-vn",  # No video
        "-acodec", "pcm_s16le",  # PCM format
        "-ar", "16000",  # 16kHz sample rate
        "-ac", "1",  # Mono
        output_audio
    ]
    subprocess.run(cmd, check=True)
    return output_audio
```

### Step 2: Transcribe with Word-Level Timestamps

```python
import os
import requests

API_KEY = os.environ["SENSEAUDIO_API_KEY"]

def transcribe_for_subtitles(audio_file, language="zh"):
    url = "https://api.senseaudio.cn/v1/audio/transcriptions"

    headers = {"Authorization": f"Bearer {API_KEY}"}
    files = {"file": open(audio_file, "rb")}
    data = {
        "model": "sense-asr-pro",
        "language": language,
        "response_format": "verbose_json",
        "timestamp_granularities[]": ["word", "segment"],
        "enable_punctuation": "true"
    }

    response = requests.post(url, headers=headers, files=files, data=data)
    return response.json()
```

### Step 3: Generate Subtitle Segments

```python
def create_subtitle_segments(transcript_data, max_chars_per_line=42, max_duration=7):
    words = transcript_data.get("words", [])
    segments = []

    current_segment = {
        "start": 0,
        "end": 0,
        "text": ""
    }

    for word in words:
        word_text = word["word"]
        word_start = word["start"]
        word_end = word["end"]

        # Check if adding this word exceeds limits
        potential_text = current_segment["text"] + " " + word_text if current_segment["text"] else word_text

        if (len(potential_text) > max_chars_per_line or
            (current_segment["start"] > 0 and word_end - current_segment["start"] > max_duration)):
            # Save current segment
            if current_segment["text"]:
                segments.append(current_segment.copy())

            # Start new segment
            current_segment = {
                "start": word_start,
                "end": word_end,
                "text": word_text
            }
        else:
            # Add word to current segment
            if not current_segment["text"]:
                current_segment["start"] = word_start
            current_segment["end"] = word_end
            current_segment["text"] = potential_text

    # Add last segment
    if current_segment["text"]:
        segments.append(current_segment)

    return segments
```

### Step 4: Format as SRT

```python
def format_srt(segments):
    srt_content = ""

    for i, segment in enumerate(segments, 1):
        start_time = format_timestamp_srt(segment["start"])
        end_time = format_timestamp_srt(segment["end"])

        srt_content += f"{i}\n"
        srt_content += f"{start_time} --> {end_time}\n"
        srt_content += f"{segment['text']}\n\n"

    return srt_content

def format_timestamp_srt(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
```

### Step 5: Format as VTT

```python
def format_vtt(segments):
    vtt_content = "WEBVTT\n\n"

    for segment in segments:
        start_time = format_timestamp_vtt(segment["start"])
        end_time = format_timestamp_vtt(segment["end"])

        vtt_content += f"{start_time} --> {end_time}\n"
        vtt_content += f"{segment['text']}\n\n"

    return vtt_content

def format_timestamp_vtt(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"
```

## Advanced Features

### Multi-Language Subtitles

Generate subtitles in multiple languages:

```python
def generate_multilingual_subtitles(video_file, languages=["zh", "en"]):
    audio_file = extract_audio_from_video(video_file)
    subtitles = {}

    for lang in languages:
        # Transcribe in original language
        transcript = transcribe_for_subtitles(audio_file, language=lang)

        # If translating, use target_language parameter
        if lang != languages[0]:
            transcript = transcribe_for_subtitles(
                audio_file,
                language=languages[0],
                target_language=lang
            )

        segments = create_subtitle_segments(transcript)
        subtitles[lang] = format_srt(segments)

    return subtitles
```

### Subtitle Styling (ASS Format)

```python
def format_ass(segments, style="Default"):
    ass_header = """[Script Info]
Title: Generated Subtitles
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    ass_content = ass_header

    for segment in segments:
        start = format_timestamp_ass(segment["start"])
        end = format_timestamp_ass(segment["end"])
        text = segment["text"]

        ass_content += f"Dialogue: 0,{start},{end},{style},,0,0,0,,{text}\n"

    return ass_content

def format_timestamp_ass(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:01d}:{minutes:02d}:{secs:05.2f}"
```

### Subtitle Optimization

```python
def optimize_subtitles(segments):
    optimized = []

    for segment in segments:
        text = segment["text"]

        # Split long lines
        if len(text) > 42:
            words = text.split()
            mid = len(words) // 2
            line1 = " ".join(words[:mid])
            line2 = " ".join(words[mid:])
            text = f"{line1}\n{line2}"

        # Ensure minimum display time (1 second)
        duration = segment["end"] - segment["start"]
        if duration < 1.0:
            segment["end"] = segment["start"] + 1.0

        segment["text"] = text
        optimized.append(segment)

    return optimized
```

### Burn Subtitles into Video

```python
def burn_subtitles(video_file, subtitle_file, output_file):
    cmd = [
        "ffmpeg", "-i", video_file,
        "-vf", f"subtitles={subtitle_file}",
        "-c:a", "copy",
        output_file
    ]
    subprocess.run(cmd, check=True)
```

## Output Format

- SRT subtitle file
- VTT subtitle file (for web)
- ASS subtitle file (with styling)
- JSON with timing data
- Video with burned-in subtitles (optional)

## Tips for Best Results

- Use high-quality audio for better transcription
- Adjust max_chars_per_line for different video sizes
- Review and edit timestamps for perfect sync
- Test subtitles with video player before finalizing
- Consider reading speed (aim for 15-20 chars per second)

## Example Usage

**User request**: "Generate English subtitles for this video"

**Skill actions**:
1. Extract audio from video
2. Transcribe with word-level timestamps
3. Create subtitle segments with proper timing
4. Format as SRT file
5. Optionally create VTT for web use
6. Provide subtitle files for download

## Reference

API docs: https://senseaudio.cn/docs/speech_recognition
