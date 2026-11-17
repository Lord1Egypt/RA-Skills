---
name: yaps-dictation
description: "Type with your voice using Yaps on desktop. Get set up, fix a problem, or recover a recent dictation. New users: install Yaps and sign in."
---

# Yaps Dictation

Read [the runtime guide](references/runtime.md) before the first operation. It defines `<yaps>`, account readiness, local permissions, and file handling.

Required Yaps version: 2.3.124 or newer. Check installed command help for later capabilities.

Feature readiness: Dictation engine, microphone permission, and platform text-insertion permissions. Current shortcuts are configured in Yaps Settings, not assumed from defaults.

## Workflow

Use the shared account/readiness checks and inspect `features list`. If no dictation engine is ready, explain the available modes and current download sizes before installing an authorized model. Direct the user to Yaps Settings > Shortcuts for the configured dictation key; do not assume Fn.

Microphone and accessibility permissions must be completed in the OS/Yaps flow. A feature flag is not proof that capture or paste works. During developer QA, first run existing synthetic fixture tests where available. Those can verify decoding and cleanup without requiring the user to speak; they do not prove microphone capture or insertion. For a complete voice-typing acceptance test, use a short dictation into the intended composer and the actual inserted text as evidence. Ask the user only for a remaining physical interaction that the available tools cannot perform. Distinguish capture failure, transcription failure, and insertion failure when diagnosing. Change shortcuts or engines only when the requested fix requires it.

For explicit recovery, use `<yaps> history-list --limit 10 --pretty`, restrict attention to dictation entries, and show only enough timestamp/text context to identify the requested item. Resolve ambiguity before saving a recovered transcript. Never browse history merely to prove setup works.

## Boundaries

- This skill cannot control a remote microphone or capture speech from a cloud VM.
- No background recording, broad history collection, or assumed OS permission.
- A successful settings check alone is not successful voice typing.
