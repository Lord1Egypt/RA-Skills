# Memory Template - Trending Now

Create `~/trending-now/memory.md` with this structure:

```markdown
# Trending Now Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Activation Preferences
- When this skill should auto-activate
- When this skill should stay silent
- Proactive heartbeat mode vs explicit-only mode

## Monitoring Scope
primary_topics:
- topic name
- topic name
exclude_topics:
- noise source
geography: global | specific market
language_scope: english | multilingual

## Source Priorities
x_priority: high | medium | low
community_sources: reddit, forums, niche communities
publisher_sources: trade press, mainstream press
trend_tools: google trends, other public datasets

## Alert Policy
strictness: conservative | balanced | aggressive
min_score_to_alert: integer 0-100
active_hours: HH:MM-HH:MM
timezone: Area/City

## Outcomes
- Alerts sent and resulting decisions
- False positives and why they failed
- Topics promoted or demoted by evidence quality

## Notes
- Durable constraints and preferences
- Reliable source patterns to reuse

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context still evolving | Ask only what improves monitoring quality |
| `complete` | Stable monitoring setup | Focus on execution and periodic refinement |
| `paused` | Monitoring paused by user | Keep memory but stop proactive prompts |
| `never_ask` | User wants no setup prompts | Do not ask setup questions unless requested |

## Key Principles

- Keep memory concise and decision-oriented.
- Prefer natural language notes over rigid config dumps.
- Update `last` after meaningful monitoring sessions.
- Record misses and false positives to improve thresholds.
- Never persist secrets unless explicitly requested by the user.
