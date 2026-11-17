---
name: zombie-love-story-planner
description: Plan original, gentle zombie-reunion stories for partners, friends, family, or pets. Use for a five-beat encounter-to-memory storyboard, an original prompt, a consent and rights checklist, or public Zombie Love reference pages. This Skill is text-only and does not generate video.
metadata:
  openclaw:
    homepage: https://aizombie.art
    version: 1.0.1
---

# Zombie Love Story Planner

Help the user shape a new, emotionally clear zombie-reunion story. This Skill and its optional MCP only draft text; they do not inspect or upload photos, connect accounts or billing, access media history, call providers, or generate or submit video.

The project identity is Zombie Love Studio. Keep it independent; do not imply affiliation with aizombie.net or any other similarly named service. The matching local source tree is a visual prototype; consult the live public site for current published product information. Neither this Skill nor its MCP verifies uploads, generation, checkout, or output quality.

## Permission and consent first

Before preparing a generation-ready concept, confirm:

- The user has permission to use each reference photo.
- Every depicted person is comfortable with the portrayal.
- The scene and visuals will be original, not copied from a specific video, artwork, character, or frame sequence.
- The story is stylized and non-graphic, centered on recognition and reunion rather than harm.

If a check is missing, return a short checklist and keep the result exploratory. Do not say that a tool verified a license or consent.

## Plan the story

1. Identify the relationship and keep the roles clear: who is changed, and who recognizes them.
2. Choose a setting: snowy cabin, rain-soaked city, ruined chapel, or a user-described original place.
3. Ask for one specific memory detail only if it would make the ending more personal.
4. Use five beats: encounter, reveal, recognition, reunion, memory.
5. Preserve familiar subject traits through the reveal. Use restrained camera movement and a clear visual transition from suspense to warmth.
6. Return `Rights and consent`, `Story brief`, `Five-beat storyboard`, `Continuity`, `Warnings`, and `Capability check`.

Do not promise exact likeness, generation quality, output duration, price, or live availability. Use the public pages for current published claims, but do not say that this Skill or MCP has tested generation, checkout, privacy operations, or output quality.

## Optional MCP

The read-only MCP offers deterministic text helpers:

- `build_zombie_love_brief`
- `plan_zombie_reunion_storyboard`
- `audit_zombie_story_prompt`
- `get_zombie_love_resources`

Connect it with:

```bash
openclaw mcp add zombie-love-story \
  --command npx \
  --arg -y \
  --arg github:gpt-img-2/zombie-love-story-mcp \
  --include 'build_zombie_love_brief,plan_zombie_reunion_storyboard,audit_zombie_story_prompt,get_zombie_love_resources'
```

If MCP is unavailable, continue with the text workflow and do not imply a tool ran.

## Public reference pages

- Project homepage: https://aizombie.art/
- Story trend guide: https://aizombie.art/ai-zombie-trend
- Photo role guide: https://aizombie.art/ai-zombie-photo-guide
- Story concept previews: https://aizombie.art/ai-zombie-video-examples
- About: https://aizombie.art/about
- Privacy: https://aizombie.art/privacy
- Terms: https://aizombie.art/terms
- Raw Skill: https://aizombie.art/skills/zombie-love-story-planner/SKILL.md
- MCP source: https://github.com/gpt-img-2/zombie-love-story-mcp
- ClawHub listing: https://clawhub.ai/gpt-img-2/skills/zombie-love-story-planner
