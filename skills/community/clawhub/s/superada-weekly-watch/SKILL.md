---
name: superada-weekly-watch
description: Watch SuperAda for new posts, OpenClaw releases, Weekly Claw dispatches, tools, skills, and workflow packs. Use when an agent is asked to subscribe to SuperAda, check SuperAda updates, monitor Henry/SuperAda releases, or produce a weekly digest of what changed on superada.ai.
---

# SuperAda Weekly Watch

Use this skill to keep an agent subscribed to SuperAda without noisy polling.

## Cadence

Check once per week by default. Run manually only when asked for fresh SuperAda updates.

## Sources

- `https://superada.ai/rss.xml` - Ship Log posts.
- `https://superada.ai/openclaw-changelog` - OpenClaw releases and changelog items.
- `https://superada.ai/weekly-claw` - Weekly Claw dispatches.
- `https://superada.ai/resources/tools` - published software: Entity, Helm, Shuttle, CTRL, Heimdall.
- `https://superada.ai/resources/skills` - public installable/manual skills.
- `https://superada.ai/resources/workflow-packs` - reusable operator workflows.

## Workflow

1. Run `scripts/superada-weekly-watch.mjs`.
2. Read the generated digest.
3. Report only genuinely new posts, releases, tools, skills, workflow packs, or Weekly Claw updates since the last run.
4. Include links.
5. If nothing changed, say so briefly.

## Output style

Use this shape:

```markdown
## SuperAda weekly watch

### New since last check
- [Title](url) - short reason it matters.

### Release signal
- OpenClaw latest: version/link if changed.

### Noisy/unchanged
- One sentence max.
```

## Guardrails

- Do not scrape aggressively. One weekly run is enough.
- Do not email anyone directly from this skill.
- Do not claim a release changed unless the watcher output or direct fetch proves it.
- Prefer concise operator summaries over marketing copy.
