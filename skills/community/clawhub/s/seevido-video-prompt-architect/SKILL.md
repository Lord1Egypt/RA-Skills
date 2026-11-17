---
name: seevido-video-prompt-architect
description: Turn rough video ideas into structured English or Chinese prompt packs, reference-aware sequences, continuity rules, and focused debugging loops. Use for text-to-video, image-to-video, reference-to-video, video-to-video, product clips, cinematic scenes, or multi-shot work; do not use for account support, live model comparisons, or claims about official provider behavior.
metadata:
  openclaw:
    homepage: https://seevido.org/ai-video-generator
    version: 1.0.0
---

# SeeVido Video Prompt Architect

Turn one clear visual idea into production-ready video instructions. This Skill is a text-only workflow by default. Its optional MCP adds deterministic, read-only helpers and never generates media, calls a provider, reads an account, compares live prices, or spends credits.

SeeVido is an independent AI media workspace. Do not present this Skill, the MCP, or the site as official documentation for Seedance, Kling, Wan, Grok, Veo, or any other provider or model.

## Gather the minimum brief

Ask only for details that materially change the result. Infer ordinary creative choices when enough context already exists.

Identify:

- Workflow: text-to-video, image-to-video, reference-to-video, or video-to-video.
- Subject and environment.
- One primary visible action per shot.
- Camera framing, movement, and pace.
- Duration and aspect ratio when known.
- The role of every `@Image`, `@Video`, or `@Audio` reference.
- Identity, product geometry, composition, motion, timing, or audio that must remain stable.
- Delivery goal: product clip, cinematic beat, social post, transition, loop, or sequence.

Never invent model-specific controls, limits, input support, prices, or availability. Use the current product interface as the source of truth when exact settings matter.

## Build the prompt

Write in this order:

1. Subject and scene.
2. One visible action.
3. Camera framing and one motivated camera move.
4. Lighting and visual treatment.
5. Duration and aspect ratio if confirmed.
6. Reference roles and continuity constraints.
7. A short artifact-focused avoid list.

Prefer observable instructions over abstract mood. Keep subject motion separate from camera motion. Avoid simultaneous competing actions, contradictory camera commands, and long style lists.

For image-to-video, preserve identity, layout, lighting direction, and geometry unless transformation is requested. For reference-to-video, keep every token exactly as supplied and assign one clear role per reference. For video-to-video, state which source motion, timing, camera path, and scene structure must survive.

Write in the user's language unless another language is requested. Never translate, renumber, or remove `@Image1`, `@Video1`, or `@Audio1`-style tokens.

## Plan sequences

Give every shot one purpose and one action. Include timing, framing, subject action, applicable reference role, continuity anchor, and intended end frame. Use the previous shot's final frame as the next visual anchor. Preserve screen direction, identity, wardrobe or product geometry, and lighting unless a deliberate transition changes them.

## Debug one axis at a time

Revise in this order:

1. Subject action or motion intensity.
2. Framing or camera path.
3. Reference roles and continuity constraints.
4. Lighting or style language.

Translate vague failures into observable corrections. Reduce competing instructions before adding detail.

## Use the optional MCP

When MCP tools are available:

- `build_video_prompt` creates a structured prompt pack.
- `plan_reference_sequence` creates a 1–6 shot plan.
- `diagnose_video_prompt` identifies missing controls.
- `get_seevido_resources` returns canonical site resources.

Connect the stdio server with:

```bash
openclaw mcp add seevido \
  --command npx \
  --arg -y \
  --arg github:gpt-img-2/seevido-prompt-mcp \
  --include 'build_video_prompt,plan_reference_sequence,diagnose_video_prompt,get_seevido_resources'
```

Then run `openclaw mcp doctor seevido --probe`. If the installed OpenClaw release does not expose the `mcp` command group, add `npx -y github:gpt-img-2/seevido-prompt-mcp` as a Stdio server in its MCP settings.

The MCP is optional. If unavailable, apply the same workflow manually and do not imply that a tool ran.

## Return a compact deliverable

For one shot, return `Prompt`, optional `Reference roles`, `Continuity constraints`, `Avoid`, and one `Revision move`. For sequences, return a numbered shot plan followed by shared continuity rules and one assembly note.

## Canonical resources

- AI video generator: https://seevido.org/ai-video-generator
- Models: https://seevido.org/models
- Seedance: https://seevido.org/models/seedance
- Kling: https://seevido.org/models/kling
- Wan: https://seevido.org/models/wan
- Prompt library: https://seevido.org/seedance-2-0-prompts
- Video-to-prompt tool: https://seevido.org/video-to-seedance-prompt
- Raw Skill: https://seevido.org/skills/seevido-video-prompt-architect/SKILL.md
- MCP source: https://github.com/gpt-img-2/seevido-prompt-mcp
- ClawHub listing: https://clawhub.ai/gpt-img-2/skills/seevido-video-prompt-architect
