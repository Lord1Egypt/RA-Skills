---
name: six-layer-memory
description: Set up or repair a local-first six-layer memory structure for an OpenClaw/Codex workspace. Use when a user wants durable HOT/WARM/COLD/CURATED memory files, local maintenance helpers, and per-workspace memory hygiene. This public package does not include cloud sync, external API upload, secret collection, cookies, or login-state handling.
version: 2.0.4
---

# Six-Layer Memory

Use this skill when the user wants a workspace to keep memory proactively instead of relying on chat context alone.

## What this skill sets up

- HOT: `memory/SESSION-STATE.md`
- WARM: local vector/index refresh when source material changes
- COLD: `memory/decisions/`
- CURATED: `MEMORY.md` plus daily logs
- LOCAL-AUTO: optional local maintenance log and digest checks, with no external API calls

## Workflow

1. Pick the target workspace.
2. Run `scripts/install_workspace.sh <workspace>`.
3. Review the created files before adding any schedule.
4. Add periodic execution only after the user confirms the schedule:

```cron
0 6 * * * /usr/bin/python3 <workspace>/memory/auto_memory_6layer.py --workspace <workspace> --daily --source memory-daily
```

5. Validate with `memory/check_memory_layers.sh`.

## Bundled scripts

- `scripts/install_workspace.sh`
- `scripts/auto_memory_6layer.py`
- `scripts/memory_writer.py`
- `scripts/check_memory_layers.sh`

## Notes

- This skill is designed per workspace. Repeat installation for each agent workspace.
- Do not overwrite HOT state with synthetic “all good” status text.
- Prefer one canonical HOT file path: `memory/SESSION-STATE.md`.
- Keep `MEMORY.md` for durable facts only. Put operational notes elsewhere.
- Do not store API keys, access tokens, cookies, login state, or customer private data in public skill files, shared templates, or examples.
- If a user wants cloud sync, treat it as a separate private extension: explain the risks, ask for explicit confirmation, and keep keys outside the published skill.

## References

- Local-first guide: `references/local-first-guide.md`
