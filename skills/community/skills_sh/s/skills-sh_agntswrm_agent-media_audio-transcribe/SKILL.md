---
name: audio-transcribe
description: Transcribes audio to text with timestamps and optional speaker identification. Use when you need to convert speech to text, create subtitles, transcribe meetings, or process voice recordings.
compatibility: Requires Node.js 18+. Run via npx agent-media@latest or npm install -g agent-media.
---

# Audio Transcribe

Transcribes audio files to text with timestamps. Supports automatic language detection, speaker identification (diarization), and outputs structured JSON with segment-level timing.

## Command

```bash
npx agent-media@latest audio transcribe --in <path> [options]
```

## Inputs

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input audio file path or URL (supports mp3, wav, m4a, ogg) |
| `--diarize` | No | Enable speaker identification |
| `--language` | No | Language code (auto-detected if not provided) |
| `--speakers` | No | Number of speakers hint for diarization |
| `--out` | No | Output path, filename or directory (default: ./) |
| `--provider` | No | Provider to use (local, fal, replicate, runpod) |

## Output

Returns a JSON object with transcription data:

```json
{
  "ok": true,
  "media_type": "audio",
  "action": "transcribe",
  "provider": "fal",
  "output_path": "transcription_123_abc.json",
  "transcription": {
    "text": "Full transcription text...",
    "language": "en",
    "segments": [
      { "start": 0.0, "end": 2.5, "text": "Hello.", "speaker": "SPEAKER_0" },
      { "start": 2.5, "end": 5.0, "text": "Hi there.", "speaker": "SPEAKER_1" }
    ]
  }
}
```

## Examples

Basic transcription (auto-detect language):
```bash
npx agent-media@latest audio transcribe --in interview.mp3
```

Transcription with speaker identification:
```bash
npx agent-media@latest audio transcribe --in meeting.wav --diarize
```

Transcription with specific language and speaker count:
```bash
npx agent-media@latest audio transcribe --in podcast.mp3 --diarize --language en --speakers 3
```

Use specific provider:
```bash
npx agent-media@latest audio transcribe --in audio.wav --provider replicate
```

## Extracting Audio from Video

To transcribe a video file, first extract the audio:

```bash
# Step 1: Extract audio from video
npx agent-media@latest audio extract --in video.mp4 --format mp3

# Step 2: Transcribe the extracted audio
npx agent-media@latest audio transcribe --in extracted_xxx.mp3
```

## Providers

### local

Runs locally on CPU using [Transformers.js](https://huggingface.co/docs/transformers.js), no API key required.

- Uses Moonshine model (5x faster than Whisper)
- Models downloaded on first use (~100MB)
- Does NOT support diarization — use fal or replicate for speaker identification
- You may see a `mutex lock failed` error — ignore it, the output is correct if `"ok": true`

```bash
npx agent-media@latest audio transcribe --in audio.mp3 --provider local
```

### fal

- Requires `FAL_API_KEY`
- Uses `wizper` model for fast transcription (2x faster) when diarization is disabled
- Uses `whisper` model when diarization is enabled (native support)

### replicate

- Requires `REPLICATE_API_TOKEN`
- Uses `whisper-diarization` model with Whisper Large V3 Turbo
- Native diarization support with word-level timestamps

### runpod

- Requires `RUNPOD_API_KEY`
- Uses `pruna/whisper-v3-large` model (Whisper Large V3)
- Does NOT support diarization (speaker identification) - use fal or replicate for diarization

```bash
npx agent-media@latest audio transcribe --in audio.mp3 --provider runpod
```
