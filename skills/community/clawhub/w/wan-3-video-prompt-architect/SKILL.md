---
name: wan-3-video-prompt-architect
description: Build and review production-ready prompts and short shot plans for WAN-30.video text-to-video or image-to-video work. Use when a user needs clearer subject motion, camera direction, scene continuity, audio direction, reference-image roles, or a pre-generation configuration check; do not use this Skill to claim official Alibaba or Wan affiliation, call a model provider, access an account, or spend credits.
metadata:
  openclaw:
    homepage: https://wan-30.video/wan-3-0
    version: 1.0.0
---

# Wan 3.0 Video Prompt Architect

Turn an idea into an inspectable prompt or short shot plan for the independent WAN-30.video workspace. Keep the user's subject and intent intact. Do not imply that this Skill, its optional MCP, or WAN-30.video is an official Alibaba or Wan project.

## Establish the production brief

Identify the generation mode, subject, visible action, environment, desired framing, camera movement, lighting, visual treatment, duration, aspect ratio, resolution, and audio direction. For image-to-video work, describe what each supplied image should control, such as the opening frame, closing frame, subject identity, product appearance, or composition.

If essential information is missing, choose a conservative default and label it. Do not invent an uploaded image, brand asset, performer identity, license, or model capability.

## Write an executable prompt

Order instructions by production importance:

1. Subject and defining visual details.
2. Visible action and timing.
3. Environment and spatial relationship.
4. Shot size, lens feel, and camera movement.
5. Lighting, palette, texture, and visual style.
6. Audio or ambience when requested.
7. A short list of exclusions that prevents likely failure without fighting the requested motion.

Prefer observable direction over abstract praise. Replace terms such as “cinematic” or “dynamic” with the actual shot, motion, light, pace, and composition that should appear. Keep one primary action per short shot and avoid contradictory camera commands.

## Plan multi-shot clips

Give every shot a duration and make the sum match the requested clip length. Preserve the subject, wardrobe, location logic, light direction, screen direction, and motion across cuts unless the user asks for a change. State the transition only when it matters.

For image-to-video prompts, do not ask a reference image to establish incompatible poses, locations, or camera angles at the same moment. Treat a closing image as an intended destination, not permission to replace the subject midway.

## Check before generation

At the time this Skill was published, WAN-30.video exposed Wan 3.0 text-to-video and image-to-video workflows with 4–15 second duration choices, 480p or 720p output choices, optional audio, and up to three images in the image workflow. These are site-specific interface facts, not universal claims about every Wan implementation. Recheck the live generator before relying on them because availability and pricing can change.

Flag:

- prompts longer than the currently displayed 2,500-character allowance;
- missing subject motion or scene context;
- mutually exclusive camera directions;
- a text-to-video request that assumes uploaded references;
- an image-to-video request without a starting reference;
- a duration, resolution, or reference count outside the currently displayed choices;
- audio requested without any audible event or ambience direction.

## Use the optional MCP

- `build_wan3_video_prompt` assembles a structured prompt from a production brief.
- `plan_wan3_shot_sequence` turns short shots into a timed continuity plan.
- `diagnose_wan3_video_prompt` checks prompt clarity and the current WAN-30.video configuration boundaries.
- `get_wan3_video_resources` returns canonical creation, guide, pricing, and policy URLs.

Connect the stdio server with:

```bash
openclaw mcp add wan3-video \
  --command npx \
  --arg -y \
  --arg github:gpt-img-2/wan3-video-prompt-mcp \
  --include 'build_wan3_video_prompt,plan_wan3_shot_sequence,diagnose_wan3_video_prompt,get_wan3_video_resources'
```

Then run `openclaw mcp doctor wan3-video --probe`. If the installed release does not expose an `mcp` command group, add `npx -y github:gpt-img-2/wan3-video-prompt-mcp` as a Stdio server in MCP settings. The MCP is optional; never imply it ran when unavailable.

## Return an inspectable result

Return `Mode`, `Prompt`, `Shot plan` when needed, `Reference roles`, `Configuration`, `Assumptions`, and `Preflight warnings`. Keep prompt text separate from commentary so it can be copied without cleanup.

## Canonical resources

- Wan 3.0 guide: https://wan-30.video/wan-3-0
- Text-to-video: https://wan-30.video/text-to-video
- Image-to-video: https://wan-30.video/image-to-video
- Pricing: https://wan-30.video/pricing
- Privacy policy: https://wan-30.video/privacy-policy
- Terms: https://wan-30.video/terms-of-service
- Raw Skill: https://wan-30.video/skills/wan-3-video-prompt-architect/SKILL.md
- MCP source: https://github.com/gpt-img-2/wan3-video-prompt-mcp
- ClawHub listing: https://clawhub.ai/gpt-img-2/skills/wan-3-video-prompt-architect
