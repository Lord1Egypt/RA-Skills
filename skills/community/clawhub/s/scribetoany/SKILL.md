---
name: scribetoany
description: Transcribe local audio or video files (MP3, M4A, WAV, MP4, MOV, WEBM…) or public X, Twitch, Loom, Google Drive and Dropbox links into text, SRT or VTT subtitles with the ScribeToAny CLI, with timestamps and optional speaker labels. Use when the user asks to transcribe a recording, meeting, interview, podcast, lecture or video on their computer, turn speech into text, or make subtitles or captions for a media file; also for "转写", "转文字", "做字幕", "语音转文字". Not for editing existing subtitle files.
license: MIT
metadata:
  openclaw:
    requires:
      bins:
        - node
    homepage: https://scribetoany.com/developers
---

# Transcribe with ScribeToAny

The `scribetoany` CLI uploads a file to the user's ScribeToAny account,
waits for the transcript and saves it next to where you run it. Results
go to stdout, progress to stderr. Every command takes `--json`.

## 1. Make sure the CLI runs

```bash
scribetoany --version
```

If it isn't installed, use `npx -y scribetoany` in place of `scribetoany`
everywhere below (Node.js 20+). Ask the user before running
`npm i -g scribetoany`.

## 2. Make sure the user is signed in

```bash
scribetoany auth status --json
```

Exit code 3 means not signed in. Run `scribetoany auth login`: it opens the
browser, where the user signs in and approves "ScribeToAny CLI", and waits
up to 5 minutes. Tell the user to approve it in the browser. If your shell
times out sooner, run it in the background and check `auth status` after.
On a remote machine or a sandbox without a browser, sign-in doesn't work
yet: ask the user to run the transcription on their own computer, or to
upload the file at https://scribetoany.com/dashboard.

## 3. Transcribe

```bash
scribetoany transcribe interview.m4a --format srt --json
```

- `--format txt|srt|vtt|json`: `txt` (default) has `[m:ss]` timestamps,
  `--no-timestamps` drops them. `json` is the segment list with start/end
  milliseconds and speakers.
- `--language <code>` when the user says which language is spoken (Whisper
  codes: `en`, `zh`, `ja`, `es`…). Leave it out to detect it.
- `--speakers` for interviews, meetings and podcasts with several voices;
  `--speakers 3` if the user knows how many.
- `--translate-to-english` to get English text from non-English speech.
- `--out <path>` picks the file (or a directory); without it the result is
  `./<file name>.<format>`. An existing file is not overwritten unless you
  add `--force`. `--out -` prints the transcript instead.
- Several files at once: `scribetoany transcribe a.mp3 b.mp3 --out transcripts/`.

Long recordings take several minutes after the upload. For anything over
about 10 minutes, don't block your shell:

```bash
scribetoany transcribe lecture.mp4 --no-wait --json   # prints the id
scribetoany get <id> --wait --format srt --json       # run in the background
```

With `--json`, `transcribe` and `get` print
`{ id, name, status, language, durationSec, planLimit, url, output }`,
where `output` is the saved file's path. `planLimit` is set when the
recording was longer than the plan allows per file and only its start was
transcribed: always tell the user, using its `message`.

## 4. Use the result

Read the saved file; for long transcripts, read it in parts instead of
printing all of it into the conversation. `url` opens the transcript in
the ScribeToAny editor, where the user can fix words and speakers.

Other commands: `scribetoany list --json` (recent transcripts and ids),
`scribetoany get <id> --format vtt` (any finished transcript again, in any
format), `scribetoany usage --json` (plan, files today, minutes left).

## Exit codes

| Code | Meaning | What to do |
|---|---|---|
| 0 | done | |
| 2 | bad input (missing file, unsupported type, output exists, bad option) | fix the command |
| 3 | not signed in or sign-in expired | `scribetoany auth login` |
| 4 | plan limit: daily files, monthly minutes or too many at once | show `scribetoany usage`; plans at https://scribetoany.com/pricing |
| 5 | transcription failed | show the error to the user; don't retry blindly |
| 6 | network or server error | retry once, then report |
| 7 | not finished yet | `scribetoany get <id> --wait` |

## Rules

- The file is uploaded to ScribeToAny and counts toward the user's plan.
  Check `scribetoany usage` before a large batch. Ask first when the user
  hasn't asked for a transcription, or the recording looks confidential.
- YouTube, TikTok and Instagram links can't be fetched: download the video
  first (with the user's say-so), then transcribe the file.
- Never print, log or copy the token, `SCRIBETOANY_TOKEN` or the
  credentials file (`~/.config/scribetoany/credentials.json`).
