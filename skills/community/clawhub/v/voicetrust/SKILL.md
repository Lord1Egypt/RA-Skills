---
name: voicetrust
description: Interpret VoiceTrust results for owner verification on voice/audio inputs. Use when you need the meaning of VoiceTrust fields, trust labels, command-gating decisions, or the minimal rule for handling voice messages alongside STT. For first-time setup or environment bootstrap, read `references/quickstart.md`.
---

# VoiceTrust

VoiceTrust answers one question: is this audio likely spoken by the enrolled owner?

Normal use:
- run STT for content
- run VoiceTrust for owner verification
- merge both before replying

Do not use this skill to define machine-specific commands.
Local routing and machine policy belong elsewhere.

## Runtime note

This skill bundle is lightweight:
- source code and setup docs are included
- large model files are not bundled
- owner enrollment data is local runtime state and must not be published

If model assets are missing, read `references/quickstart.md`.

## Output fields

VoiceTrust results may include:
- `speaker_match`
- `audio_quality`
- `overall_trust`
- `confidence`
- `identity_score`
- `trust_label`
- `decision`
- `decision_reasons`
- `speaker_id`
- `speech_duration`
- `speech_ratio`
- `vad_status`
- `failure_reason`
- `raw_scores.speaker_similarity`

## How to use the result

Use `trust_label` for concise rendering.
Use `decision` for command gating.
Do not treat audio quality alone as owner identity evidence.

### Trust label

- `high`: `identity_score >= 85` and `confidence >= 80` and no failure
- `medium`: `identity_score >= 72` and `confidence >= 68` and no failure
- `low`: everything else

Common downgrade signals:
- `vad_status != "ok"`
- `speech_duration < 2.5`
- `speech_ratio < 0.45`
- `speaker_match < 70`
- `failure_reason != null`

### Command gating

For voice command execution:
- use the normal path when `speech_duration >= 3.0`
- allow a short voice sample only when all of the following are true:
  - `speech_duration >= 1.2`
  - `speaker_match >= 85`
  - `confidence >= 85`
- in all cases, command execution still requires:
  - `speaker_match >= 78`
  - `confidence >= 80`
  - `identity_score >= 82`
  - `vad_status == "ok"`
  - `failure_reason == null`

Interpretation:
- `decision == "allow_command"` means command execution may proceed
- `decision != "allow_command"` means do not execute commands from this sample
- non-command voice content may still be handled normally
- music / non-speech / non-command audio should not enter the command path

CLI example:

```bash
uv run --python .venv/bin/python ../scripts/demo.py \
  --audio /path/to/sample.ogg \
  --speaker owner \
  --json
```

## Human rendering

Preferred compact format:
- `Voice trust: high / medium / low`
- `Details: match <x> - trust <y> - confidence <z> - identity <i> - quality <q>`
- if relevant: `Decision: allow_command / reject_command`

If degraded, say why briefly using `decision_reasons`.
Do not over-claim certainty.

## Failure handling

- If STT succeeds and VoiceTrust fails: keep transcript, report trust as unavailable or inconclusive.
- If VoiceTrust succeeds and STT fails: keep trust result, report transcription failure.
- If both fail: say the audio could not be processed reliably.
- If `decision != "allow_command"`, do not execute voice commands.

## First-time setup

For first-time setup, local installation, enrollment, or bootstrap, read:
- `references/quickstart.md`
