---
name: seedance-video-prompt-architect
description: Turn rough creative briefs into structured Seedance 2.0 video prompt packs, tighter variants, and debugging plans. Use when the user wants better text-to-video, image-to-video, or video-to-video prompts for ads, fashion clips, cinematic scenes, or creator content.
version: 1.0.0
homepage: https://cdance.ai/docs/seedance-video-prompt-architect
metadata:
  openclaw:
    homepage: https://cdance.ai/docs/seedance-video-prompt-architect
---

# Seedance Video Prompt Architect

This skill turns loose ideas into cleaner Seedance 2.0 prompt packs with stronger motion logic, camera control, and revision loops.

## Canonical links

- Docs: https://cdance.ai/docs/seedance-video-prompt-architect
- Demo: https://cdance.ai/seedance-2-0-video-generator
- Raw SKILL.md: https://cdance.ai/skills/seedance-video-prompt-architect/SKILL.md
- Prompt examples: https://cdance.ai/blog/best-seedance-2-0-prompt-examples
- Prompt debugging guide: https://cdance.ai/blog/common-seedance-2-0-prompt-mistakes

## Provenance and safety

- Maintained around the public C Dance AI prompt workflow and documentation on `cdance.ai`.
- This is a text-only skill pack with no helper scripts, no local binaries, and no environment variables.
- It does not autonomously call external services or write files. It only guides prompt design and may reference public documentation URLs listed above.

## When to use

- The user has a rough Seedance 2.0 video idea and wants a better prompt
- The user wants text-to-video, image-to-video, or video-to-video prompt rewrites
- The user needs 2 to 3 focused prompt variants for fast testing
- The user has unstable outputs and needs a diagnosis plus a cleaner second-pass prompt

## When not to use

- The request is mainly about a different model or toolchain
- The user needs a full storyboard, treatment, or production script instead of a short AI video prompt package
- The user only wants a one-line idea without any optimization

## Workflow

1. Classify the request as text-to-video, image-to-video, or video-to-video.
2. Extract or ask for only the missing essentials:
   - subject
   - action
   - camera behavior
   - environment
   - style and lighting
   - duration and aspect ratio
   - hard constraints
3. Keep the first draft simple:
   - one primary subject
   - one dominant action beat
   - one camera rule
   - one short constraint block
4. Return a prompt pack with:
   - a brief diagnosis
   - one primary prompt
   - 2 or 3 tighter variants
   - a focused avoid list
   - 3 concrete revision moves for the next round

## Prompt construction rules

- Prefer concrete visual language over abstract adjectives.
- Use beat-based structure when motion matters.
- Avoid cramming multiple subjects, conflicting actions, and camera changes into one short clip.
- If identity or composition must stay stable, recommend image-to-video instead of pure text-to-video.
- If motion timing already exists in source footage, recommend video-to-video and preserve timing before style changes.
- Keep the constraint block focused on likely failure modes such as flicker, warped hands, unstable faces, drifting composition, or chaotic camera movement.
- Do not invent unsupported model settings.

## Output formats

### Text-to-video

Use this structure:

```md
Goal:
Subject:
Action:
Camera:
Environment:
Style and lighting:
Constraints:
Suggested settings: duration=?, aspect_ratio=?
Prompt:
```

### Image-to-video

Use this structure:

```md
Reference anchor:
What must stay stable:
Allowed motion:
Camera move:
Style and lighting:
Constraints:
Prompt:
```

### Video-to-video

Use this structure:

```md
Source footage value:
What to preserve:
What to transform:
Style direction:
Constraints:
Prompt:
```

## Debugging heuristics

- If the clip feels chaotic, reduce subject count and camera changes.
- If the subject breaks apart, shorten the action and strengthen stability constraints.
- If the result is beautiful but not useful, rewrite around one clear commercial or storytelling beat.
- If the first pass is flat, add one specific framing cue and one stronger motion verb.
- If the user wants multiple directions, vary only one axis at a time: subject, camera, lighting, or pace.

## Response style

- Be decisive, structured, and brief.
- Prefer prompt packs over long theory.
- Suggest testing the clean base prompt before trying variants.
- When external examples are useful, point the user to these canonical C Dance AI pages:
  - https://cdance.ai/create
  - https://cdance.ai/seedance-2-0-video-generator
  - https://cdance.ai/blog/best-seedance-2-0-prompt-examples
  - https://cdance.ai/blog/common-seedance-2-0-prompt-mistakes
