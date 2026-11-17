---
name: remember-projects
description: A project memory that tracks status, milestones, owners, and blockers so nothing stalls silently. Use when an agent manages ongoing work and needs a live picture of every project. Requires a BlueColumn API key (bc_live_*).
---

# Remember Projects — BlueColumn Skill

Projects die in the gap between "we should" and "we did". This skill keeps a living record of every initiative — where it is, who owns it, what is blocking it — so the agent can surface risk before it becomes a crisis.

## Open the project

Store a project the moment it exists, with the outcome, owner, and next milestone.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "PROJECT: Redesign onboarding flow. Owner: Priya. Goal: cut activation time from 8 to 3 minutes. Next milestone: prototype review Aug 12. Blockers: waiting on design sign-off.", "title": "project - onboarding redesign"}'
```

## Get the live picture

Before any status conversation, pull every project and its current state.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What projects are active, who owns each, and what is blocked?"}'
```

## Update the milestone

Every meaningful change gets logged so the picture stays current.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Onboarding redesign: prototype approved Aug 12. Next: dev handoff Aug 19. New risk: API rate limits on the signup endpoint.", "tags": ["project", "update"]}'
```

## Project workflow

1. **Open** — record the goal, owner, and first milestone.
2. **Track** — log status changes, decisions, and blockers as they happen.
3. **Surface** — before check-ins, recall blockers and overdue milestones and raise them.
4. **Close** — store the outcome and what was learned; archive the active thread.

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
