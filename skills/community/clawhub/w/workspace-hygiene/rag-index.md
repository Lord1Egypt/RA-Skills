# RAG Index — Project READMEs

## Why Every Project Needs a README

`memory_search` can only find information that exists in searchable files. Daily memory logs capture events as they happen, but they scatter project context across dozens of date files.

A project README is a **single retrievable document** that answers: "What is this project and what's the current state?" When someone asks about a project, memory_search finds the README first, then supplements with daily logs.

## README Template

Every folder in `projects/` must have a `README.md`:

```markdown
# Project Name

**Status:** Active | Paused | Complete
**Owner:** steve | maggie | claire | ari | steve+maggie | etc.
**Started:** YYYY-MM-DD
**Last updated:** YYYY-MM-DD

## What This Is
1-2 sentences. What problem does it solve, who is it for.

## Current State
What's working, what's not, what's next. 3-5 bullet points max.

## Key Decisions
Decisions made about this project that are still in effect.
- [YYYY-MM-DD] Decision and reasoning

## Files
Key files in this folder and what they do.

## Blockers
What's preventing progress, if anything.
```

## Maintenance

- Update the README when significant milestones happen (not daily)
- `Last updated` date should reflect the most recent real change
- If a project moves to `archive/`, keep the README — it's the historical record

## What Makes a Good README for RAG

1. **Use the project name in the first line** — semantic search matches on this
2. **Include specific terms** — "Stripe," "PostgreSQL," "$500/mo" are retrievable. "The platform" is not.
3. **Keep it under 50 lines** — long READMEs dilute retrieval quality
4. **Update status honestly** — "Paused" is better than a README that says "Active" for a dead project

## Anti-Patterns

- **No README at all** — project is invisible to RAG
- **README that's just a file listing** — no semantic value
- **README written once and never updated** — misleading retrieval results
- **README that duplicates TASKS.md** — tasks change daily, README captures the arc
