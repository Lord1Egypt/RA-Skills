# Shared Workspace ... Technical Reference

## Directory Structure

```
~/.ldm/
  config.json                 Machine-level config
  version.json                Installed version + timestamps
  extensions/
    registry.json             Extension metadata
    memory-crystal/           Extension files
    wip-release/              Extension files
    ...
  agents/
    cc-mini/                  Claude Code on Mac Mini
      IDENTITY.md
      SOUL.md
      CONTEXT.md
      REFERENCE.md
      config.json
      memory/
        transcripts/          Raw JSONL session files
        sessions/             MD per-session summaries
        daily/                Daily log breadcrumbs
        journals/             Dream Weaver narrative output
    oc-lesa-mini/             OpenClaw/Lesa on Mac Mini
      memory/
        transcripts/          Raw JSONL copies (backup)
        workspace/            Workspace .md snapshots
        daily/                Daily log copies
  memory/
    crystal.db                Shared vector DB (all agents)
  sessions/                   Active session files (Agent Register)
  messages/                   Inter-session messages (Message Bus)
  shared/
    boot/                     Boot hook files
    cron/                     Cron job scripts
  state/                      Capture watermarks, role state
  secrets/                    Encryption keys, relay tokens
  bin/                        Deployed scripts
  backups/                    Daily backups
```

## Sacred Data

These paths are never overwritten during install or update:

- `memory/` (crystal.db, all vector data)
- `agents/` (identity, soul, context, journals, transcripts)
- `secrets/` (encryption keys, tokens)
- `state/` (watermarks, capture state)
- `backups/` (daily snapshots)

Only `extensions/` and `shared/` are updated by `ldm install`.

## Agent Identity

One agent per harness per machine. The agent ID is deterministic:

| Agent ID | Harness | Machine |
|----------|---------|---------|
| `cc-mini` | Claude Code CLI | Mac Mini |
| `cc-air` | Claude Code CLI | MacBook Air |
| `oc-lesa-mini` | OpenClaw | Mac Mini |

All agents share one `crystal.db`. Memory is shared. Identity is per-agent.

## Key Files

| File | What |
|------|------|
| `bin/ldm.js` | CLI: `ldm init` creates the workspace |
| `lib/deploy.mjs` | Extension deployment engine |
| `lib/state.mjs` | System state detection |
| `lib/safe.mjs` | Trash management (never delete, always move) |
