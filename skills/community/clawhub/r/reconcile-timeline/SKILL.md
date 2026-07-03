---
name: reconcile-timeline
description: Re-anchor a long-form video timeline to the MEASURED voiceover. After TTS runs, the timeline segment start/end times are still the PREDICTED (155 wpm) values while the audio plays at the TTS engine's actual pace. On a multi-minute video this compounds across segments and desyncs image from audio. This skill walks each timeline segment's vo_line against the measured word timings (written into subtitles[] by elevenlabs-tts) and rewrites each segment's start_time/end_time to the real audio boundaries, then updates audio_duration to the measured total. No API call. Re-runnable. Run AFTER elevenlabs-tts and BEFORE the final video render, long-form only. Use when processing a long-form (schema_version 3.0-long) job where the voiceover has already been generated and measured word timings exist in input.json.
metadata: {"openclaw":{"requires":{"bins":["jq"]}}}
---

# reconcile-timeline

Re-anchor a long-form job's timeline segments to the measured voiceover, and fix
audio_duration. Long-form only. Shorts do not need this (their drift is sub-second).

## Why this skill exists

The brief's timeline segment times are PREDICTED from a 155 wpm assumption when
the brief was written. A TTS engine rarely speaks at exactly that pace. The
[elevenlabs-tts](../elevenlabs-tts/SKILL.md) skill measures the real per-word
timings (from the TTS engine's character alignment) and writes them into
subtitles[], but it does NOT update the timeline segments and does NOT update
audio_duration.

For a 30-second Short, predicted vs measured differ by a fraction of a second,
so a Shorts pipeline can ignore it. For a multi-minute long-form video the gap
grows across the runtime and the images visibly fall out of sync with the
voiceover by the end. This skill closes that gap by re-anchoring every segment
to the words it actually covers.

## Usage

Run the script directly:

```bash
bash skills/reconcile-timeline/scripts/reconcile.sh <job-folder>
```

Example (the bundled demo job):
```bash
bash skills/reconcile-timeline/scripts/reconcile.sh examples/demo-job
```

## What the script does

1. Validates input.json exists and is valid JSON
2. Guards against Shorts briefs (schema_version must be "3.0-long")
3. Verifies measured word timings exist in subtitles[]
4. Verifies every timeline segment has a non-empty vo_line
5. Positionally matches each segment's vo_line against the measured word stream
   and rewrites start_time/end_time to real audio boundaries
6. Safety-checks that total vo_line word count matches measured word count
   (within 5% tolerance)
7. Merges reconciled timeline back into input.json and verifies monotonicity

## Output

On success:
```
OK reconciled <N> segments to measured audio
audio_duration set to <S>s
```

On failure:
```
FAILED: <reason>
```
(with details to stderr, exit non-zero)

## Notes

- The script is self-contained and does NOT require creating any temp files
  in the job folder beyond a transient jq script (reconcile.jq) and a temp
  merge file, both cleaned up on success.
- If step 6 fails (word count mismatch), the fix is upstream: ensure every
  spoken stretch has a corresponding timeline segment with its vo_line.
- An end card, if your pipeline has one, is additional to audio_duration and is
  NOT part of the timeline sum.
- Run this BEFORE your final video render so the renderer receives the measured
  audio_duration.
