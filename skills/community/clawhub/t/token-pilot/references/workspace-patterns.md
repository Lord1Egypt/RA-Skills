# Workspace File Organization for Minimal Token Cost

## Workspace Root = Auto-Injected

Every file in workspace root gets injected into the system prompt at session start.
Only keep essential .md files here:

```
workspace/
├── AGENTS.md      (~300 tok) — session startup rules
├── SOUL.md        (~400 tok) — personality
├── USER.md        (~100 tok) — human context
├── IDENTITY.md    (~150 tok) — name, vibe
├── MEMORY.md      (~300 tok) — curated long-term memory
├── TOOLS.md       (~200 tok) — environment notes
├── HEARTBEAT.md   (~50 tok)  — heartbeat checklist
├── memory/        — daily logs (NOT injected)
├── scripts/       — utility scripts (NOT injected)
└── docs/          — documentation (NOT injected)
```

**Target: <2000 tokens total for all workspace files.**

## Key Rules

1. **No scripts in workspace root** — move to `scripts/` subdirectory
2. **No temp/debug files** — delete .txt, .log, .tmp immediately
3. **No large docs** — put in `docs/` subdirectory
4. **MEMORY.md < 1500 chars** — distill ruthlessly, archive details to `memory/`
5. **AGENTS.md < 1500 chars** — rules only, no examples or tutorials
6. **SOUL.md < 2000 chars** — personality, not instruction manual

## MEMORY.md Maintenance

Every 3-5 days, review and compress:
- Remove entries older than 2 weeks unless they're permanent knowledge
- Merge similar entries
- Move project details to project-specific files
- Keep format: category → 1-line bullet points
- Target: 20-30 bullet points max

## Multi-Agent Workspace

For team workspaces with shared files:
- AGENTS.md (team rules) < 1000 chars
- Individual agent SOUL.md < 600 tokens each
- Detailed methodology → `references/` (loaded on-demand)
- Product knowledge → `shared/products/` (loaded on-demand)
