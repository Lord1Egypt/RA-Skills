---
name: subtitle-srt-export
description: Export a standard .srt subtitle file from the MEASURED word timings in a job's input.json (written by elevenlabs-tts). Flattens the per-word timings into readable cues (max ~3.5s / ~10 words per cue, breaking on sentence punctuation) and writes <job>/subtitles.srt for upload to YouTube and other platforms. No API call. Re-runnable. Does not modify input.json.
metadata: {"openclaw":{"requires":{"bins":["jq","awk"]}}}
---

# subtitle-srt-export

Turn the measured word-level timings into a ready-to-upload `.srt` file. No API
call, never mutates `input.json`, safe to re-run.

## Why this skill exists

`elevenlabs-tts` writes accurate per-word timings into `input.json`'s
`subtitles[].words[]`. Those word timings are perfect for an on-screen karaoke
render but are too granular for a subtitle file — a platform wants a handful of
readable cues, not one cue per word. This skill groups the words into cues and
emits valid SRT.

## Inputs

A job folder path whose `input.json` already contains measured word timings
(run [elevenlabs-tts](../elevenlabs-tts/SKILL.md) first). Each word is
`{word, start, end}` under `subtitles[].words[]`.

## Usage

```bash
bash skills/subtitle-srt-export/scripts/export_srt.sh <job-folder>
```

Example (the bundled demo job):
```bash
bash skills/subtitle-srt-export/scripts/export_srt.sh examples/demo-job
```

## Cue grouping rules

A new cue starts when any of these is true:
- the previous word ended a sentence (`.`, `?`, `!`)
- the current cue would exceed ~3.5 seconds
- the current cue would exceed ~10 words

Tune the `$maxdur` / `$maxwords` constants at the top of the jq block to taste.

## Output

Writes `<job>/subtitles.srt` and prints:
```
Wrote <job>/subtitles.srt with <N> cues from <M> words
```

On a missing-timings precondition failure it prints an `ERROR:` line and exits
non-zero — run `elevenlabs-tts` first.
