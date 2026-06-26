---
name: seedance-2-prompt-engineer
description: >
  Use this skill whenever a user wants to generate, improve, or convert a video prompt for Seedance 2.0.
  Triggers on: "make a Seedance prompt", "create a video prompt for Seedance", "I want to generate a video",
  "convert my idea to a Seedance prompt", "help me prompt Seedance", "optimize my video prompt",
  or any request involving Seedance 2.0 video generation. Also triggers when a user describes a scene,
  character, or action they want animated and has not yet written a structured prompt.
  Always use this skill before writing any Seedance 2.0 prompt — do NOT attempt to write one from memory.
---

# Seedance 2.0 Prompt Engineering Skill

## Purpose

Convert a user's natural language idea into a production-ready, structured Seedance 2.0 prompt
using multimodal references (images, videos, audio) and best practices derived from the official
Seedance 2.0 documentation and community knowledge.

---

## Workflow: How to Use This Skill

### Step 1 — Gather context from the user

Ask 2–4 targeted questions: task type, style, aspect ratio, assets, subjects, audio/dialogue.
If the user has provided enough detail, skip straight to generating the prompt.

### Step 2 — Load references as needed

Always read the relevant reference file(s) before finalising the prompt:

| User need | Reference file |
|---|---|
| Camera angles, movement, lens choices | `camera-angles.md` |
| Visual styles, art direction, aesthetics | `styles.md` |
| Common generation problems + fixes | `common-issues.md` |
| Prompt best practices, structure, modes | `best-practices.md` |

### Step 3 — Output the final prompt

Use the standard output format below. Never skip sections.

---

## Standard Output Format

The core prompt formula (from official Seedance 2.0 documentation):

```
Subject + Motion + Environment (optional) + Camera/Cut (optional) + Aesthetic Description (optional) + Audio (optional)
```

Apply this formula per shot. Use the full structured output below:

```
=== SEEDANCE 2.0 PROMPT ===

Mode: [Text-Only | First-Frame | Last-Frame | All-Reference]

Assets Mapping:
- @image1: [what it controls — identity, scene, style, etc.]
- @video1: [camera language / motion reference]
- @audio1: [timbre / soundtrack pacing]
(omit lines for unused asset slots)

Subject Definitions:
- Define [2–3 stable features] in @imageN as <Subject1>.

Final Prompt:
[style descriptor], [aspect ratio], [duration]s.

Shot 1: [camera + movement] Subject + motion. Environment. Aesthetic. Audio cue.
Shot 2: [camera + transition] Subject + motion. Environment detail.
...

Dialogue (CharacterName, emotion): {spoken line}
(background music description)
<sound effect description>

Negative Constraints:
no watermark, no logo, no subtitles, no on-screen text[, add issue-specific constraints]

Generation Settings:
Duration: Xs
Aspect Ratio: [16:9 | 9:16 | 1:1]

=== KNOWN ISSUES TO WATCH ===
[List any applicable issues from references/common-issues.md with their workarounds]
```

---

## Platform Limits (Seedance 2.0)

- Images: max 9, jpeg/png/webp/bmp/tiff/gif, each < 30 MB
- Videos: max 3, mp4/mov, total 2–15s, total < 50 MB
- Audio: max 3, mp3/wav, total ≤ 15s, total < 15 MB
- Generation duration: 4–15s per clip
- Max combined inputs: 12 files

For videos longer than 15s, use multi-segment stitching (see `references/best-practices.md` § Multi-Segment).

---

## Quick Reference: Task Types

| Task | Prompt phrasing to use |
|---|---|
| Reference (extract style/motion) | "Referencing @videoN's [camera/style/motion], generate…" |
| Edit (modify original) | "Strictly edit @videoN, change [X] to [Y]" |
| Extend (continue in time) | "Extend @videoN, generate…" |
| Extend backwards | "Extend @videoN forward, generate…" |
| Combined | "Referencing @imageN's [aspect], strictly edit @videoX, [edit details]" |

> ⚠️ In Edit and Extend tasks, refer to the video as `<videoN>` — NOT `reference video N`.
> Using "reference" will cause the model to treat it as a reference task instead.

---

## Subject Definition Rules

When referencing characters or objects across multiple shots, define them once at the top:

```
Define the [2–3 stable features: outfit, hair, type] in @imageN as <Subject1>.
```

- Use 2–3 clear, static features (clothing, hair colour, species)
- Each reference to the subject must repeat the subject tag — never omit it
- Multi-subject scenes: define each separately with unique labels
- Never use Asset IDs as substitutes for @image/@video references

---

## Special Characters in Prompts

| Content type | Symbol | Example |
|---|---|---|
| Background music | `()` | `(upbeat jazz playing in background)` |
| Sound effects | `<>` | `<distant thunder>` |
| Dialogue / TTS | `{}` | `{Hello, world.}` — non-English: `say in Japanese {こんにちは}` |
| On-screen captions | `【】` | `【Chapter 1: Departure】` |

> ⚠️ Never use `--` in prompts. Everything after it is silently ignored by the model.

---

## IP / Moderation Safety

- Never use franchise names, character names, or brand terms
- Replace recognisable features with original descriptors
  - ❌ Named glowing chest device from a famous armoured superhero → ✅ `"crystalline energy core embedded in the chest plate"`
  - ❌ Named red-and-gold powered armour suit → ✅ `"custom exo-suit with smooth ceramic panels and an amber visor"`
  - ❌ Named small electric creature with a lightning-bolt tail → ✅ `"tiny round creature with sparking fur and a forked tail"`
- Add explicit negative constraints for any inferable IP terms
- If rejected, escalate: rename → redesign signature features → change character type entirely

---

## Files in This Skill

| File | Purpose |
|---|---|
| `SKILL.md` | This file — master instructions |
| `camera-angles.md` | Full camera language vocabulary with Seedance-specific notes |
| `styles.md` | Visual style library — descriptors, examples, camera defaults per style |
| `best-practices.md` | Prompt formula, modes, text generation, video editing, multi-segment |
| `common-issues.md` | Known bugs, workarounds, and prompt-level fixes |
