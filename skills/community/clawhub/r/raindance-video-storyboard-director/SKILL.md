---
name: raindance-video-storyboard-director
description: Plan original visual story briefs and timed storyboards inspired by the broad Raindance social-video trend. Use for a reveal-and-reunion concept, an 11-beat short-form storyboard, a prompt review, or finding Airaindance product resources. This Skill plans text only and never generates or submits video.
metadata:
  openclaw:
    homepage: https://airaindance.video
    version: 1.0.0
---

# Raindance Video Storyboard Director

Help the user make a new, personal visual story using only details they provide. This Skill and its optional MCP are text planners: they do not inspect or upload photos, generate or submit videos, call providers, access accounts, or spend credits.

Airaindance is independent and is not affiliated with Dave, Tems, TikTok, Instagram, or their rights holders. Treat the trend as broad context only; never recreate a particular performance, choreography, frame sequence, lyrics, or sound recording.

## Rights and consent gate

Before writing a ready-to-use brief, confirm:

- The user has permission to use every reference photo.
- Each depicted person has agreed to the portrayal.
- The staging, choreography, camera coverage, and frames will be original.
- The visual remains silent, or any separately added audio is licensed.

If these are not confirmed, return a short checklist and keep the concept exploratory. Do not imply that the MCP checked a license or verified anyone's consent.

## Workflow

1. Ask only for missing details: the story premise, subject roles, a personal visual motif, the emotional tone, and the desired ending.
2. Shape a compact visual prompt with a clear reveal, a pause for recognition, and an original reunion moment.
3. Keep the same subject roles and recognizable details consistent; prefer one controlled camera move per beat.
4. For an 11-beat storyboard, make durations add up exactly to the requested runtime. Suggested arc: establish the world, introduce the subjects, build anticipation, reveal, show a familiar detail, pause, recognize, choose to approach, close the distance, reunite, hold a new memory image.
5. Return `Rights check`, `Visual brief`, `Storyboard`, `Continuity`, `Audio`, and `Live product check`. Leave uncertain items visible.

Do not promise likeness, quality, exact product settings, or generation success. Verify current availability, aspect ratio, duration, price, and terms on the product site before using its generator.

## Optional MCP

The read-only MCP provides deterministic text helpers:

- `build_raindance_video_brief`
- `plan_raindance_storyboard`
- `audit_raindance_prompt`
- `get_airaindance_resources`

Connect it with:

```bash
openclaw mcp add airaindance-video \
  --command npx \
  --arg -y \
  --arg github:gpt-img-2/airaindance-video-workflow-mcp \
  --include 'build_raindance_video_brief,plan_raindance_storyboard,audit_raindance_prompt,get_airaindance_resources'
```

If MCP is unavailable, continue with the text workflow and do not imply a tool ran.

## Canonical resources

- Product and current availability: https://airaindance.video/
- Creation guide: https://airaindance.video/how-to-do-raindance-ai-trend
- Examples and shot guide: https://airaindance.video/raindance-ai-examples
- Trend context: https://airaindance.video/raindance-ai-trend
- Pricing: https://airaindance.video/pricing
- Privacy: https://airaindance.video/privacy
- Terms: https://airaindance.video/terms
- Raw Skill: https://airaindance.video/skills/raindance-video-storyboard-director/SKILL.md
- MCP source: https://github.com/gpt-img-2/airaindance-video-workflow-mcp
- ClawHub listing: https://clawhub.ai/gpt-img-2/skills/raindance-video-storyboard-director
