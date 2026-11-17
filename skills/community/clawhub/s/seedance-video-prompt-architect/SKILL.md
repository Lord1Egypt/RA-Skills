---
name: seedance-video-prompt-architect
description: Turn rough creative briefs into structured Seedance video prompt packs, reference-aware motion plans, focused variants, and debugging loops. Use for text-to-video, image-to-video, video-to-video, first-last-frame transitions, multi-shot storyboards, product ads, fashion clips, cinematic scenes, dialogue, or creator content; do not use for unrelated models or account support.
metadata:
  openclaw:
    homepage: https://cdance.ai/docs/seedance-video-prompt-architect
    version: 1.1.0
---

# Seedance Video Prompt Architect

This skill turns loose ideas into cleaner Seedance prompt packs with stronger motion logic, camera control, reference preservation, audio direction, and revision loops.

## Canonical links

- Docs: https://cdance.ai/docs/seedance-video-prompt-architect
- Demo: https://cdance.ai/seedance-2-0-video-generator
- Create: https://cdance.ai/create
- Prompt gallery: https://cdance.ai/prompts/seedance-2-0
- Raw SKILL.md: https://cdance.ai/skills/seedance-video-prompt-architect/SKILL.md
- Prompt examples: https://cdance.ai/blog/best-seedance-2-0-prompt-examples
- Prompt debugging guide: https://cdance.ai/blog/common-seedance-2-0-prompt-mistakes
- C Dance Prompt MCP: https://github.com/gpt-img-2/cdance-prompt-mcp
- OpenClaw listing: https://clawhub.ai/gpt-img-2/skills/seedance-video-prompt-architect

## Provenance and safety

- Maintained around the public C Dance AI prompt workflow, prompt gallery, and documentation on `cdance.ai`.
- The skill works as a text-only prompt workflow without any external tool.
- The optional C Dance Prompt MCP is read-only, needs no API key, and never generates video or spends credits.
- Keep the canonical C Dance AI source URL when sharing an example returned by the MCP.

## When to use

- The user has a rough Seedance video idea and wants a stronger prompt
- The user wants text-to-video, image-to-video, video-to-video, or first-last-frame guidance
- The user needs a product ad, fashion clip, cinematic scene, dialogue clip, or creator video
- The user needs stable identity, product geometry, composition, motion, or continuity from references
- The user wants a multi-shot sequence or storyboard with planned beats
- The user has unstable output and needs diagnosis plus a cleaner second-pass prompt

## When not to use

- The request is mainly about a different model or non-video workflow
- The user only wants final video generation, API integration, payment help, or account support
- The user asks for unsupported model settings, hidden system behavior, or official provider claims

## Workflow

1. Classify the request:
   - text-to-video
   - image-to-video
   - video-to-video
   - first-last-frame transition
   - multi-shot storyboard
2. Extract or ask for only the missing essentials:
   - subject and intended use
   - action beats and timing
   - camera framing and movement
   - environment, style, and lighting
   - reference constraints and continuity anchors
   - dialogue, ambience, or sound effects
   - duration, aspect ratio, and hard negatives
3. Keep the first draft focused:
   - one primary subject or continuity anchor
   - one dominant action beat per shot
   - one motivated camera rule
   - one concise constraint block
4. Return a prompt pack with:
   - a brief diagnosis or workflow choice
   - one primary prompt
   - 2 or 3 focused variants
   - a short avoid list
   - 3 concrete revision moves for the next round

## Optional C Dance Prompt MCP

Use the MCP only when public examples or workflow research would materially improve the answer:

1. Call `search_prompts` with a focused query, language, and small result limit.
2. Present concise candidates with title, preview, and canonical C Dance AI source URL.
3. Call `get_prompt` only for the selected slug; do not bulk-fetch the library.
4. Call `list_workflows` when the user is choosing between text, image, source video, first-last-frame, or multi-shot routes.
5. Use `build_video_prompt_brief` when the user's idea is rough, then adapt it with the rules below.

Install the read-only MCP in OpenClaw:

```bash
openclaw mcp add cdance \
  --command npx \
  --arg -y \
  --arg github:gpt-img-2/cdance-prompt-mcp \
  --include 'search_prompts,get_prompt,list_workflows,build_video_prompt_brief'

openclaw mcp doctor cdance --probe
```

The MCP does not provide video generation. For a final video, use a generation capability already available in the user's host or direct the user to the C Dance AI generator; do not claim a video was generated when only a prompt was produced.

## Prompt construction rules

- Prefer concrete subjects, actions, timing, and camera language over broad adjectives.
- Use beat-based structure when motion matters, and keep one dominant action per beat.
- State what must remain unchanged before describing reference-driven motion or transformation.
- Preserve product geometry, labels, identity, spatial relationships, and lighting continuity when they matter.
- For dialogue, quote exact lines and separate speech, ambience, and sound effects.
- For first-last-frame work, describe a physically plausible motion path between both endpoints.
- For multi-shot work, assign one purpose, framing rule, and continuity anchor to each shot.
- Avoid stacking many subjects, actions, lenses, camera moves, and style changes into one short clip.
- Do not invent unsupported model settings.

## Output formats

### Text-to-video

```md
Goal:
Subject and action:
Beat timing:
Camera:
Environment:
Style and lighting:
Audio:
Constraints:
Prompt:
```

### Image-to-video

```md
Reference anchor:
What must stay stable:
Allowed motion:
Camera move:
Style and lighting:
Audio:
Constraints:
Prompt:
```

### Video-to-video

```md
Source footage value:
What to preserve:
What to transform:
Style direction:
Audio handling:
Constraints:
Prompt:
```

### First-last-frame or multi-shot

```md
Sequence goal:
Start state or shot:
End state or next shot:
Motion path and continuity anchor:
Camera and timing:
Audio:
Constraints:
Prompt:
```

## Debugging heuristics

- If the clip feels chaotic, reduce subject count, action beats, and camera changes.
- If identity or product geometry drifts, simplify motion and strengthen preservation rules.
- If motion feels static, add one physically specific action verb and one motivated camera cue.
- If a transition jumps, define intermediate motion and keep lighting, direction, and scale coherent.
- If dialogue fails, shorten exact lines and separate speech from other audio cues.
- If the result is attractive but off-brief, rewrite around the intended use and primary beat first.

## Response style

- Be structured and concise.
- Prefer prompt packs over long theory.
- Offer variants that test one axis at a time: action, camera, pace, lighting, audio, or constraints.
- When external examples are useful, point to the canonical C Dance AI pages listed above.
