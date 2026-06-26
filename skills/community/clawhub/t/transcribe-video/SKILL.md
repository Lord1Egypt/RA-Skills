---
name: transcribe-video
description: Extract transcript or subtitles from a local video file. Use this skill whenever the user asks to transcribe a video, extract speech-to-text, get subtitles, or wants a text version of what's said in a video. Also trigger on "提取字幕", "视频转文字", "语音转文字", "transcribe", "extract audio text", or when the user references getting a script/transcript from any video file (mp4, mkv, mov, avi, webm). This skill is for LOCAL video files — for YouTube or other online URLs, use the download-video skill first to get the file, then transcribe it.
---

# Transcribe Video

Extract transcript text from a local video file. The skill checks for embedded subtitles first (faster and more accurate), and only falls back to API-based speech recognition if none are found.

## Step 1: Identify the video file

Confirm the video file path with the user. Supported formats: mp4, mkv, mov, avi, webm, and any format ffmpeg can handle.

## Step 2: Check for embedded subtitles

```bash
ffprobe -v quiet -select_streams s -show_entries stream=index,codec_name:stream_tags=language,title -of json "<video_path>"
```

- If subtitle streams exist → go to **Step 3a** (extract embedded subtitles)
- If no subtitle streams → go to **Step 3b** (API transcription)

## Step 3a: Extract embedded subtitles

If multiple subtitle tracks exist, prefer the one matching the video's primary language or ask the user which track to use.

```bash
# Extract as SRT (stream index 0 for first subtitle track; adjust if needed)
ffmpeg -i "<video_path>" -map 0:s:0 -c:s srt "<output_path>.srt" -y
```

After extraction, convert SRT to clean text:
- Remove sequence numbers
- Remove timestamp lines (lines matching `\d{2}:\d{2}:\d{2}`)
- Remove HTML-like tags (`<i>`, `</i>`, etc.)
- Join remaining non-empty lines

Save the clean transcript to `<video_name>.txt` next to the video file. Done — skip Step 3b.

## Step 3b: API-based transcription

Use the bundled transcription script. It reads credentials from `~/.transcribe_video.env`.

### Prerequisites check

1. Verify the env file exists:
   ```bash
   test -f ~/.transcribe_video.env && echo "OK" || echo "MISSING"
   ```

2. If MISSING, tell the user to create `~/.transcribe_video.env` with:
   ```
   OPENAI_API_KEY=your-key-here
   # Optional Base URL:
   # OPENAI_API_BASE=https://<base-url>/v1/
   # Optional Model Name:
   # TRANSCRIBE_MODEL=gpt-4o-transcribe
   ```
   Wait for the user to confirm before proceeding.

3. Verify dependencies:
   ```bash
   python3 -c "from openai import OpenAI; from dotenv import load_dotenv; print('OK')" 2>&1
   ```
   If missing: `pip install openai python-dotenv`

### Run transcription

```bash
python3 <skill_directory>/scripts/transcribe.py "<video_path>"
```

The script extracts audio (WAV, 16kHz mono), sends it to the API, and saves the transcript to `<video_name>.txt` next to the video file.

## Step 4: Report results

Tell the user:
- Where the transcript file was saved
- How many lines / approximate word count
- Whether it came from embedded subtitles or API transcription
- Display the first few lines as a preview
