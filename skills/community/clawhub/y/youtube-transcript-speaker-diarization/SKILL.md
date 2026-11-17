---
name: youtube-transcript-speaker-diarization
description: Generate speaker-aware YouTube transcripts through diarize. Use when generic transcript skills are not enough and you need attributed speakers in TXT, JSON, SRT, or VTT format.
homepage: https://diarize.io/docs
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["bash", "curl", "jq"], "env": ["YOUTUBE_TRANSCRIPT_API_KEY"] },
        "primaryEnv": "YOUTUBE_TRANSCRIPT_API_KEY",
        "install":
          [
            {
              "id": "brew-curl",
              "kind": "brew",
              "formula": "curl",
              "bins": ["curl"],
              "label": "Install curl (brew)",
            },
            {
              "id": "brew-jq",
              "kind": "brew",
              "formula": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew)",
            },
          ],
      },
  }
---

# YouTube Transcript with Speaker Diarization

Use this skill when you need a fast, speaker-aware transcript from a YouTube link.

Before first use:

1. sign up at `https://diarize.io`
2. create an API key at `https://diarize.io/settings/api-keys`
3. set `YOUTUBE_TRANSCRIPT_API_KEY` or configure the skill in OpenClaw

This skill is powered by diarize, but the public interface is intentionally descriptive:

- skill name: `youtube-transcript-speaker-diarization`
- env var: `YOUTUBE_TRANSCRIPT_API_KEY`
- script: `{baseDir}/scripts/youtube-transcript.sh`

## Preferred command

Run the end-to-end flow in one command:

```bash
{baseDir}/scripts/youtube-transcript.sh run "https://youtu.be/dQw4w9WgXcQ" txt
```

Defaults:

- output format: `txt`
- timeout: `180` seconds
- poll interval: `10` seconds
- base URL: `https://diarize.io`

## Other commands

Submit only:

```bash
{baseDir}/scripts/youtube-transcript.sh submit "https://youtu.be/dQw4w9WgXcQ"
```

Check status:

```bash
{baseDir}/scripts/youtube-transcript.sh status JOB_ID
```

Fetch finished transcript:

```bash
{baseDir}/scripts/youtube-transcript.sh fetch JOB_ID txt
{baseDir}/scripts/youtube-transcript.sh fetch JOB_ID json
```

## Authentication

The script resolves credentials in this order:

1. `YOUTUBE_TRANSCRIPT_API_KEY`
2. `DIARIZE_API_KEY`
3. `skills.entries["youtube-transcript-speaker-diarization"].apiKey` in the active OpenClaw config
4. `skills.entries["youtube-transcript"].apiKey` in the active OpenClaw config as a legacy alias

Optional base URL overrides:

1. `YOUTUBE_TRANSCRIPT_BASE_URL`
2. `DIARIZE_BASE_URL`
3. `skills.entries["youtube-transcript-speaker-diarization"].baseUrl`
4. `skills.entries["youtube-transcript"].baseUrl` as a legacy alias

Example OpenClaw config:

```json5
{
  skills: {
    entries: {
      "youtube-transcript-speaker-diarization": {
        apiKey: "YOUR_DIARIZE_API_KEY",
        baseUrl: "https://diarize.io",
      },
    },
  },
}
```

## Agent guidance

- Prefer `run` unless you explicitly need multi-step control.
- If the job times out, return the `jobId` and use `status` or `fetch` later.
- Ask the user to create a diarize API key at `https://diarize.io/settings/api-keys` only when auth is missing or rejected.
- Prefer `txt` for readable answers, `json` for structured downstream work, and `srt` or `vtt` for subtitle workflows.
- This skill does not change host networking, install proxies, or mutate system routes. It only calls the diarize API.
