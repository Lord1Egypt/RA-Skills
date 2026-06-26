# Dev Update: Relay Deploy + LDM Decoupling

**Date:** 2026-03-03 11:45 PST
**Author:** CC-Mini
**Branch:** cc-mini/decouple-openclaw-paths
**PR:** #20

## What happened

### 1. Relay Worker deployed to Cloudflare

The multi-device sync relay is live:
- URL: `https://memory-crystal-relay.wipcomputer.workers.dev`
- R2 bucket: `memory-crystal-relay`
- Auth tokens generated and set for cc-mini, cc-air, lesa-mini
- Tokens stored in 1Password ("Memory Crystal Relay Auth Tokens" in Agent Secrets)
- Health check passing, drop/pickup/confirm tested end-to-end

### 2. Memory Crystal decoupled from OpenClaw

Parker caught that all paths were hardcoded to `~/.openclaw/`. A standalone Claude Code CLI user would get a `.openclaw` directory they didn't ask for. Memory Crystal is an LDM OS component, not an OpenClaw feature.

**10 files changed:**
- `ldm.ts`: added `secrets/` and `state/` to LdmPaths, new migration helpers
- `crypto.ts`: relay key resolves via `resolveSecretPath` (LDM first, then .openclaw)
- `core.ts`: resolveConfig prefers `~/.ldm/memory/`, opRead checks both secret locations
- `cc-hook.ts`, `cc-poller.ts`, `poller.ts`, `mirror-sync.ts`: state files via LDM
- `mcp-server.ts`, `openclaw.ts`, `dev-update.ts`: state via LDM

**New LDM directories created:**
- `~/.ldm/secrets/` (mode 700, has crystal-relay-key + op-sa-token)
- `~/.ldm/state/` (has watermarks, capture state, metrics)

**Fallback chain:** every path resolver checks `~/.ldm/` first, then `~/.openclaw/` for migration. Existing installs keep working. New installs get LDM only.

### 3. All systems verified healthy

| System | Status |
|--------|--------|
| Memory Crystal | 170,099 chunks, 229 memories, 4 agents |
| Context Embeddings | 15,701 chunks, 0 NULL vectors |
| CC Capture | Running, last poll 21:06 UTC, 53 files tracked |
| LDM State | Migrated to `~/.ldm/state/`, writes going there |
| LDM Secrets | Migrated to `~/.ldm/secrets/` |
| Relay Worker | Live, health OK, tested with real tokens |

## What's next

1. Merge PR #20
2. Configure Mini env vars (CRYSTAL_RELAY_URL, CRYSTAL_RELAY_TOKEN)
3. Parker tests on MacBook Air (install, pair, sync)
4. Clean up memory-crystal-py-private directory (leftover from yanked SDK)
