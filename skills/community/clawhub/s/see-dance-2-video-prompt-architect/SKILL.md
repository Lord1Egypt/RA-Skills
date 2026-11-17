---
name: see-dance-2-video-prompt-architect
description: Turn rough video ideas into structured English or Chinese Seedance-oriented prompt packs, exact reference bindings, shot sequences, and focused debugging loops. Use for text-to-video, image-to-video, multimodal reference, product clips, cinematic scenes, transitions, or loops; do not use for account support, live model comparisons, or claims about official provider behavior.
metadata:
  openclaw:
    homepage: https://see-dance-2.com/prompts/seedance-2-0
    version: 1.0.0
---

# See Dance 2 Video Prompt Architect

Turn one visual idea into production-ready video instructions. This Skill is a text-only workflow by default. Its optional MCP adds deterministic, read-only helpers and never generates media, calls a provider, reads an account, compares live prices, or spends credits.

See Dance 2 is an independent AI video workspace. Do not present this Skill, the MCP, or the site as official documentation for ByteDance, Seedance, or any other provider or model.

## Gather the minimum brief

Identify only details that materially change the result:

- Workflow: text-to-video, image-to-video, multimodal reference, or video-to-video.
- Subject and environment.
- One primary visible action per shot.
- Camera framing, movement, and pace.
- Duration and aspect ratio when known.
- The exact role of each `@Image`, `@Video`, or `@Audio` reference.
- Identity, product geometry, composition, motion, timing, or audio that must remain stable.
- Delivery goal: product clip, cinematic beat, social post, transition, loop, or sequence.

Never invent model-specific controls, limits, input support, prices, or availability. Use the current product interface when exact settings matter.

## Build the prompt

Write in this order:

1. Subject and scene.
2. One observable subject action.
3. Camera framing and one motivated camera move.
4. Lighting and visual treatment.
5. Duration and aspect ratio if confirmed.
6. Reference bindings and continuity constraints.
7. A short artifact-focused avoid list.

Keep subject motion separate from camera motion. Avoid competing actions, contradictory camera commands, and long style lists.

For image-to-video, preserve identity, layout, lighting direction, and geometry unless transformation is requested. For multimodal reference work, preserve every token exactly and assign one role per reference. For video-to-video, state which source motion, timing, camera path, and scene structure must survive.

Write in the user's language unless another language is requested. Never translate, renumber, or remove `@Image1`, `@Video1`, or `@Audio1`-style tokens.

## Plan sequences

Give every shot one purpose and one action. Include timing, framing, subject action, reference binding, continuity anchor, and intended end frame. Use each final frame as the next shot's visual anchor. Preserve screen direction, identity, wardrobe or product geometry, and lighting unless a deliberate transition changes them.

## Debug one axis at a time

Revise in this order:

1. Subject motion.
2. Camera motion or framing.
3. Reference bindings and continuity constraints.
4. Lighting or visual treatment.

Translate vague failures into observable corrections and remove competing instructions before adding detail.

## Use the optional MCP

- `build_seedance_prompt` creates a structured prompt pack.
- `plan_reference_sequence` creates a 1–6 shot reference-aware plan.
- `diagnose_seedance_prompt` identifies missing controls.
- `get_see_dance_2_resources` returns canonical site resources.

Connect the stdio server with:

```bash
openclaw mcp add see-dance-2 \
  --command npx \
  --arg -y \
  --arg github:gpt-img-2/see-dance-2-prompt-mcp \
  --include 'build_seedance_prompt,plan_reference_sequence,diagnose_seedance_prompt,get_see_dance_2_resources'
```

Then run `openclaw mcp doctor see-dance-2 --probe`. If the installed release lacks the `mcp` command group, add `npx -y github:gpt-img-2/see-dance-2-prompt-mcp` as a Stdio server in MCP settings. The MCP is optional; never imply it ran when unavailable.

## Return a compact deliverable

For one shot, return `Prompt`, optional `Reference bindings`, `Continuity constraints`, `Avoid`, and one `Revision move`. For sequences, return a numbered shot plan, shared continuity rules, and one assembly note.

## Canonical resources

- Create workspace: https://see-dance-2.com/create
- AI video generator: https://see-dance-2.com/ai-video-generator
- Seedance 2.0 prompt library: https://see-dance-2.com/prompts/seedance-2-0
- Prompt architecture guide: https://see-dance-2.com/blog/awesome-seedance-2-0-prompts-guide
- Omni reference guide: https://see-dance-2.com/blog/seedance-2-0-omni-reference-guide
- Raw Skill: https://see-dance-2.com/skills/see-dance-2-video-prompt-architect/SKILL.md
- MCP source: https://github.com/gpt-img-2/see-dance-2-prompt-mcp
- ClawHub listing: https://clawhub.ai/gpt-img-2/skills/see-dance-2-video-prompt-architect
