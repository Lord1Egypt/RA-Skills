---
name: speechmatics
description: Transcribe audio files (voice notes, recordings, podcasts) to text via the Speechmatics batch transcription API. Use when the user asks to transcribe audio, convert speech to text, or get a transcript of a recording, and Speechmatics is configured.
homepage: https://docs.speechmatics.com/introduction/batch-transcription
metadata:
  {
    "openclaw":
      {
        "emoji": "🗣️",
        "requires": { "bins": ["curl", "jq"], "env": ["SPEECHMATICS_API_KEY"] },
        "primaryEnv": "SPEECHMATICS_API_KEY",
        "install":
          [
            {
              "id": "apt",
              "kind": "apt",
              "packages": ["curl", "jq"],
              "bins": ["curl", "jq"],
              "label": "Install curl and jq (apt)",
            },
            {
              "id": "brew",
              "kind": "brew",
              "formula": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew)",
            },
          ],
      },
  }
---

# Speechmatics (batch transcription)

Transcribe an audio file via Speechmatics' async batch API. Submits a job, polls until complete, then writes the transcript.

## Quick start

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a
```

Defaults:

- Language: `en`
- Operating point: `enhanced` (better accuracy; use `standard` for faster/cheaper)
- Output: `<input>.txt` in the same directory
- Poll interval: 3s, timeout: 600s

## Useful flags

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.ogg --language da
{baseDir}/scripts/transcribe.sh /path/to/meeting.wav --operating-point standard
{baseDir}/scripts/transcribe.sh /path/to/call.mp3 --diarization speaker
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --format json --out /tmp/transcript.json
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --format srt --out /tmp/subs.srt
{baseDir}/scripts/transcribe.sh /path/to/long.wav --timeout 1800
```

Formats: `txt` (default, plain text), `json` (Speechmatics json-v2 with word timings), `srt` (subtitles).

## API key

The script reads the API key from (in order):

1. `--api-key <key>` flag
2. `SPEECHMATICS_API_KEY` environment variable (set by openclaw from the entry below)
3. `skills.entries.speechmatics.apiKey` in `$OPENCLAW_CONFIG_PATH` (default `~/.openclaw/openclaw.json`)

Configure via openclaw.json:

```json5
{
  skills: {
    entries: {
      speechmatics: {
        apiKey: "SPEECHMATICS_KEY_HERE",
      },
    },
  },
}
```

Override the API base (e.g. EU region or a proxy) with `--base-url` or `SPEECHMATICS_BASE_URL`. Default: `https://asr.api.speechmatics.com/v2`.

## Notes

- Supports most common audio formats (wav, mp3, m4a, ogg, flac, mp4, etc.) — Speechmatics transcodes server-side.
- File size limit: 2 GB per job.
- Batch jobs complete in roughly 1:10 wallclock to audio duration on `enhanced`; `standard` is faster.
- Always confirm any destructive follow-up (e.g. replying based on a transcript) before acting.
