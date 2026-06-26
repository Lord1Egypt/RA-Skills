# Memory Template — Search Engine

Create `~/search-engine/memory.md` with this structure:

```markdown
# Search Engine Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
<!-- Use case, traffic profile, and deployment constraints in natural language -->

## Retrieval Goals
<!-- What "good results" means for this user: precision, recall, freshness, latency -->

## Decisions
<!-- Chosen architecture and relevance policy decisions with rationale -->

## Notes
<!-- Risks, unresolved tradeoffs, and follow-up checkpoints -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning context | Gather constraints opportunistically |
| `complete` | Enough context to execute | Focus on delivery with minimal clarifications |
| `paused` | User asked to defer setup | Work with existing context only |
| `never_ask` | User asked to stop setup questions | Never request additional setup context |

## Key Principles

- Keep records in natural language, not rigid config blocks.
- Capture only context that improves retrieval decisions.
- Update `last` after each substantial working session.
- Track risks and assumptions explicitly to prevent hidden regressions.
- Never store secrets or sensitive identifiers unless explicitly requested.
