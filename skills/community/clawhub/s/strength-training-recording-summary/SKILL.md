---
name: strength-training-recording-summary
description: "Create WorkoutSummary notes from strength-training recordings or transcripts. Accepts audio (.m4a, .mp3, .wav, .caf) and transcript files (.md, .txt, .srt, .vtt, .json); outputs total time, exercises completed, sets/reps, durations, and concise coach notes."
license: "MIT"
---

# Strength Training Recording Summary

Use this skill when the user wants a strength-training session recording or transcript converted into a compact summary note for future reference.

Process the timestamped transcript directly into the final `WorkoutSummary`. Do not insert a separate evidence-distillation and synthesis pipeline.

Load `references/summary-workflow.md` only when you need implementation details, transcription backend guidance, audio cleanup commands, dataset matching rules, or helper-script behavior.

For long transcripts processed in multiple windows, preserve the direct workflow but reconcile each boundary before writing the final note. Compare only the final exercise before and first exercise after the boundary. If they are one continuing exercise, keep each distinct completed set once and replace an earlier partial count with the later supported completed total. If they are different or continuity is unclear, keep both.

## Accepted Inputs

- Audio recordings: `.m4a`, `.mp3`, `.wav`, `.caf`
- Transcript files: `.md`, `.txt`, `.srt`, `.vtt`, `.json`
- Mixed-language trainer sessions, including Chinese/English audio or transcripts

## How To Invoke

The user can ask naturally, for example:

```text
Use strength-training-recording-summary on /path/to/workout.m4a
Summarize this strength training transcript: /path/to/session.md
Create a WorkoutSummary for my Chinese/English trainer recording
```

## Example Output

```text
WorkoutSummary 2026-06-20
Total length: 01:21:44
Exercises completed: 14

1. Dumbbell lateral raise, ~4 min total, 2 groups * 12 reps
- Keep shoulders down and stop before shrugging.

2. Goblet squat, ~3 min, 3 groups * 10 reps
- Slow the descent and keep pressure through the mid-foot.
```

## Summary Rules

- Start with `WorkoutSummary <date>`.
- Include total session length and number of completed exercises.
- Use duration on each exercise line, not raw timestamp ranges.
- For split/non-contiguous work, show the combined duration, e.g. `~4 min total`.
- Count completed groups/sets and reps from the transcript; mark approximate values with `~` when needed.
- Standardize exercise names against `hasaneyldrm/exercises-dataset` when practical, but do not mention `dataset match` in the final output.
- Put useful coach notes directly under the exercise without labels like `trainer-specific cue`.
- Preserve the user's requested output language when known.
- Never invent weights, reps, sets, pain details, diagnoses, or medical conclusions.
- Never add overlapping partial and completed counts from adjacent transcript windows as separate sets.

## Helper Scripts

Use bundled helpers when useful:

```bash
python scripts/calc_duration.py '03:50-05:17 07:51-10:00'
python scripts/match_exercises.py --lang zh --top-k 3 "哑铃侧平举"
```

## Transcription Notes

Prefer an input transcript when one already exists. For audio, use the best available transcription backend:

- local Whisper CLI when installed
- Groq Whisper when `GROQ_API_KEY` is configured
- OpenAI or another compatible API when the user has credentials ready

Do not embed API keys in the skill or output. If no transcription backend is ready, explain the options and ask which one the user wants to set up.
