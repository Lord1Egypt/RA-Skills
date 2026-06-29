# Remotion Video Pipeline

**Platforms:** Claude · Openclaw · Codex
**Domain:** Video

## Purpose

A production-director playbook for short-form Remotion videos.
It standardizes an **audio-driven** workflow so every video follows the same process and no step cascades into rework.
It orchestrates and gates the pipeline; it delegates the actual Remotion composition code to a Remotion skill such as `remotion-best-practices`.

The governing principle:

```
audio    = the master timeline
SRT      = the time ruler
Remotion = the visuals generator
CapCut   = sound + final edit
```

## When to Use

- When you want to produce a Remotion knowledge/explainer short video with narration and on-screen subtitles
- When you want a repeatable script → audio → SRT → timeline → render → CapCut process instead of an ad-hoc one
- When you need the AI to recalibrate scene timing from real audio without rewriting the locked script
- When you want a structured `scenes.json` to drive Remotion instead of hand-editing composition code

## The Pipeline

```
1. AI: script + on-screen text + initial storyboard
   └─ 🚦 GATE 1: human confirms the script   (script is now LOCKED)
2. Audio: AI TTS or self-recording            (audio = master timeline)
3. SRT generated from the FINAL audio (Whisper default)   (SRT = time ruler)
4. AI recalibrates the timeline from the SRT — NEVER rewrites the script
   └─ 🚦 GATE 2: human confirms the timeline   (before any render)
5. AI emits scenes.json / timeline (structured data, not hand-edited code)
6. Remotion renders visuals + key subtitles + narration
   (composition code delegated to a Remotion skill)
7. Handoff bundle → CapCut
8. CapCut: BGM / SFX / transitions / final polish   (manual; checklist only)
```

Two mandatory STOP gates (Steps 1 and 4) protect the most expensive rework points.
Audio approval (Step 2) and a pre-render preview (Step 6) are optional recommended checks.

## Scope & Boundaries

- Remotion short-video pipelines only — not general video editing or other renderers.
- Tool-agnostic: audio via any TTS or self-recording; SRT via any speech-to-text (Whisper is the documented default). Nothing is hard-required.
- Defers composition code and rendering to a Remotion skill such as `remotion-best-practices`.
- Writes only the project's `scenes.json`/timeline and its asset folder, and confirms before overwriting existing files. Handles no credentials.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/open-skill-hub/issues) — improvements are welcome.
