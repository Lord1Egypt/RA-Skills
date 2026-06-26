# Migration Playbook

Use this when converting an ad-hoc workspace into Shared Memory OS.

## Goals
- Keep useful memory
- Reduce duplication
- Avoid destructive rewrites
- Preserve private-vs-shared boundaries

## Steps
1. Identify current memory files
2. Decide which file becomes HOT (`MEMORY.md`)
3. Keep chronological notes in daily files
4. Split ongoing work into `memory/projects/*.md`
5. Move reusable rules into `decisions.md`, `routines.md`, `corrections.md`
6. Add routing docs: `memory/index.md`, `memory/rules.md`
7. Wire heartbeat through `HEARTBEAT.md`
8. Update workspace `AGENTS.md`

## What not to do
- Do not mass-delete old memory first
- Do not dump everything into HOT
- Do not treat one-off context as a stable preference
- Do not expose `MEMORY.md` in shared contexts

## Good migration outcome
- New agent can understand the system in a few reads
- Existing important history is still present
- Memory writes now have clear destinations
