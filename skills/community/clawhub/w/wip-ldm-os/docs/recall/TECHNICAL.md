# Recall ... Technical Reference

## Boot Sequence

Recall is implemented as a SessionStart hook. When Claude Code opens a session, the boot hook loads context files in order:

```
1. CLAUDE.md                    Identity + structure (harness config)
2. SHARED-CONTEXT.md            Current state (under 50 lines)
3. Most recent journal           Narrative from last session
4. Daily logs (today + yesterday) Recency
5. Full history (cold start)     Dream Weaver narrative
6. CONTEXT.md                    Agent's own state
7. SOUL.md                       Who this agent is
8. Agent journals                Check for newer entries
9. Agent daily logs              Check for newer entries
```

## Key Files

| File | What |
|------|------|
| `src/boot/boot-hook.mjs` | SessionStart hook (reads + injects context) |
| `src/boot/boot-config.json` | Which files to load, in what order |
| `src/boot/installer.mjs` | Deploys boot hook to `~/.ldm/shared/boot/` |

## How It Works

The boot hook reads `boot-config.json` to determine which files to load. Each entry specifies a path pattern and priority. Files are read in priority order and concatenated into the session context.

The hook runs with a 15-second timeout. If any file is missing, it's skipped silently. The boot sequence is additive. It never modifies files, only reads them.

## Harness Differences

**Claude Code CLI:** Full boot sequence. Identity, context, journals, daily logs all loaded via SessionStart hook.

**OpenClaw:** Has its own boot sequence (workspace files). Recall provides backup context loading if the harness boot fails or is incomplete.

## Session Registration

On boot, Recall also registers the session in the Agent Register (`~/.ldm/sessions/`). This enables other sessions to discover this one via `ldm sessions`.

## Connection to Total Recall

Recall loads context at session start. [Total Recall](../total-recall/TECHNICAL.md) fills the memory that Recall serves. Total Recall imports historical conversations, generates multi-cadence summaries (daily/weekly/monthly/quarterly), and writes everything to Memory Crystal. On the next session start, Recall picks up the new data automatically.

Without Total Recall, Recall only has what was captured going forward. With Total Recall, Recall has the complete history.
