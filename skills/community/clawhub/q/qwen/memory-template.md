# Memory Template — Qwen

Create `~/qwen/memory.md` with this structure:

```markdown
# Qwen Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
<!-- What the user is building and why -->
<!-- Example: Migrating support automation from OpenAI-compatible backend to hosted Qwen -->

## Surfaces
<!-- Hosted region, local server, or hybrid route in natural language -->
<!-- Example: Default to Singapore hosted Qwen for production, Ollama local for quick experiments -->

## Workloads
<!-- Winning route per workload -->
<!-- Example: Coding agent uses Qwen3-Coder on vLLM; strict JSON normalization uses smaller deterministic route -->

## Constraints
<!-- Hardware, privacy, cost, latency, and approval boundaries -->
<!-- Example: Apple Silicon laptop only, avoid models that trigger swap or require cloud upload -->

## Notes
<!-- Repeated failures, parser quirks, or migration gotchas -->
<!-- Example: Local tool calls fail unless output is normalized in a second pass -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning routes | Keep refining workload defaults |
| `complete` | Stable Qwen workflow exists | Ask fewer setup questions |
| `paused` | User said not now | Avoid new setup prompts |
| `never_ask` | User rejected setup | Never request more setup details |

## Key Principles

- Store routes and constraints, not secrets.
- Record the execution surface before saving model preferences.
- Keep notes short enough to improve the next routing decision.
- Update `last` after meaningful Qwen work.
