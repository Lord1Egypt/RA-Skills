# Health Check Guide

## Goal
Make Shared Memory OS observable, not just documented.

## Health signals
A healthy workspace should have:
- durable memory present
- daily memory present for active work
- `.learnings/` present and non-empty
- recent learnings updates
- no long gaps in maintenance

## Recommended checks
Use:
- `scripts/check-memory-health.js`
- `scripts/rebuild-learnings-index.js`

## Self-learning / self-evolution principle
This skill should improve over time by harvesting repeated lessons into reusable memory structures.

Recommended loop:
1. complete real work
2. harvest lessons into `.learnings/`
3. rebuild `.learnings/INDEX.md`
4. review repeated lessons
5. promote stable repeated lessons into `MEMORY.md` or skill rules

This keeps the workspace learning system adaptive without requiring a runtime self-modifying agent.
