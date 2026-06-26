# Audit Rules

## Canonical Root Files

These files — and only these files — should exist at the workspace root:

```
AGENTS.md
SOUL.md
MEMORY.md
USER.md
IDENTITY.md
HEARTBEAT.md
TASKS.md
TOOLS.md
STRUCTURE.md
```

Agent-specific files that are acceptable at root but not standard:
- `BUILDOUT.md` (Claire)
- `MEMORY-REFERENCE.md` (Claire)
- `BRAND-GUIDELINES.md` (Ari)

Any other `.md`, `.html`, `.json`, `.png`, or loose files at root = violation.

## Canonical Folders

```
docs/           — shared operational docs (symlinked for Claire/Ari)
memory/         — daily logs, weekly reviews, heartbeat state
scripts/        — agent-specific scripts
skills/         — installed skills
projects/       — one folder per active/paused project
reference/      — static reference material
archive/        — dead projects and deprecated files
avatars/        — agent identity images
```

Any folder at root not in this list = violation (flag for review).

## Project Folder Rules

- One folder per project
- Naming: lowercase, hyphens, no spaces
- Must contain a README.md (see rag-index.md)
- No nested project-within-project (e.g. `projects/myapp/sub-project/`)
- Dead projects move to `archive/`, not deleted

## Memory Rules

- One file per date: `YYYY-MM-DD.md`
- Topic files: `YYYY-MM-DD-topic.md` (lowercase topic, hyphens)
- No timestamp format: `YYYY-MM-DD-HHMM.md` = violation
- Weekly reviews: `weekly-review-YYYY-MM-DD.md`
- Entries should use tagged format (see memory-format.md)

## Cross-Agent Rules

- `docs/` in Claire and Ari workspaces must be symlinks to Maggie's `docs/`
- Agent-specific scripts stay in the agent's own `scripts/`
- No agent should write to another agent's SOUL.md, MEMORY.md, or USER.md
- STRUCTURE.md is the authority — if reality doesn't match, reality needs to change

## Severity Levels

| Severity | Meaning | Action |
|----------|---------|--------|
| ERROR | Structural violation (wrong root files, broken symlinks) | Fix immediately |
| WARN | Missing README, stale memory, untagged entries | Fix within a week |
| INFO | Minor naming inconsistency, old topic files | Fix when convenient |
