---
name: seedance-prompt-builder
description: builds, rewrites, audits, and troubleshoots prompts for doubao seedance 2.0 video generation. use for text to video, image referenced video, video reference, audio reference, video editing, video extension, track completion, storyboard prompts, prompt diagnosis, multimodal asset planning, subject anchoring, camera motion control, style constraints, subtitles or speech prompts, and common seedance failure fixes such as id drift, twins, watermark, subtitles, style drift, extension jumps, audio voice mismatch, and pronunciation issues.
---

# Seedance Prompt Builder

## Purpose

Create stable, production-ready prompts for Doubao Seedance 2.0 video generation and editing. Treat Seedance as a multimodal director: separate what is in the frame from how events unfold over time, then produce prompt instructions that are explicit, concise, and operational.

Use the official guide in `references/official-guide.md` as the primary source when task-specific details are needed. Use the compact references below for fast routing and output rules.

## Core workflow

1. Identify the task type before writing the prompt:
   - multimodal reference: extract a subject, motion, camera language, style, scene, sound, or voice from assets and generate a new video.
   - video editing: modify an existing video while unmentioned content stays unchanged.
   - video extension: continue a video forward or backward while preserving continuity.
   - track completion: bridge multiple videos with a transition.
   - combined task: reference one asset while editing or extending another asset.
2. Inventory assets as `image1`, `image2`, `video1`, `audio1`, etc. Preserve the user's numbering if provided.
3. Define subjects before complex prompts. Use stable labels and keep using the same labels throughout.
4. Prefer shot sequencing for complex scenes: `shot 1`, `shot 2`, `shot 3`. Do not default to exact timestamps unless the user asks.
5. Convert abstract emotions into visible body, face, gesture, breathing, and posture details.
6. Use one primary camera movement per shot. Avoid stacking push, pull, pan, tilt, orbit, and handheld movement inside one shot.
7. End with style, quality, and constraints tailored to the task.
8. Audit the final prompt for common Seedance failure modes before returning it.

## Required routing rule

For video editing and video extension tasks, refer directly to `videoN`. Do not write "reference videoN" for the edited or extended source video, because that can route the task as a reference-generation task instead of an edit or extension task.

## Output modes

Choose the most useful mode from the user's request:

### quick prompt
Return only a polished prompt ready to paste into Seedance.

### professional prompt
Use this structure:

```markdown
## Task type
[one task type]

## Asset map
- image1: [role]
- video1: [role]
- audio1: [role]

## Subject definitions
[definitions]

## Seedance prompt
[complete prompt]

## Checks
- [important stability checks]
```

### storyboard prompt
Use numbered shots. Each shot should include camera or transition, subject action and expression, scene or position changes, and optional audio.

### prompt audit
When the user provides an existing prompt, diagnose it first, then provide a rewritten prompt:

```markdown
## Main issues
1. [issue]
2. [issue]

## Rewritten prompt
[prompt]

## Why this should be more stable
[short rationale]
```

## Reference loading

Load these files only when relevant:

- `references/task-routing.md` for deciding reference, edit, extension, track completion, or combined tasks.
- `references/prompt-formulas.md` for prompt structure, subject definition, storyboard sequence, motion language, text, speech, and symbols.
- `references/troubleshooting.md` for common failure fixes.
- `references/examples.md` for adaptable examples.
- `references/official-guide.md` for the full uploaded official guide.

## Quality rules

- Prefer Chinese prompts when the user works in Chinese or the target platform is Seedance in Chinese. Use English only when requested.
- Keep the prompt concise but complete. Remove irrelevant script-like exposition.
- Put the most important reference assets early in the prompt.
- Avoid conflicting descriptions for the same subject.
- For character identity, prefer a face close-up plus a full-body or costume reference rather than multi-view sheets.
- For more than four characters, recommend generating grouped images first, then using those images for video generation.
- For special effects with precise logic, recommend using a reference video rather than describing the effect only in text.
- For subtitles, speech, and sound, use the symbol conventions from `references/prompt-formulas.md`.
- When no text is desired, explicitly add no-subtitle, no-text, no-logo, and no-watermark constraints in Chinese.
