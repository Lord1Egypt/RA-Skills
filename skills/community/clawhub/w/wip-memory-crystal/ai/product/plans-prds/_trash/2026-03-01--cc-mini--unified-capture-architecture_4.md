# Plan: Unified Capture Architecture for Memory Crystal

**Date:** 2026-03-01
**Author:** CC-Mini
**Triggered by:** 72-hour session data loss bug + product spec cleanup

**Also saved to:** `ai/plan/2026-03-01--cc-mini--unified-capture-architecture.md`

---

## Context

Memory Crystal captures conversations from multiple AI surfaces into one local database. Three problems triggered this plan:

1. **Critical bug:** cc-hook only fires on Claude Code's Stop hook. A 72-hour session produced zero Crystal chunks. Backfill is done, but the architecture is broken.
2. **Nomenclature confusion:** The existing plan conflated Relay and Cloud Search. They're fundamentally different products with different security models.
3. **Scope creep:** The previous plan included ChatGPT. Parker scoped this down to Claude surfaces + OpenClaw only. ChatGPT comes later.

---

## Surfaces (What We're Building For)

| Surface | Local files? | Capture method | Status |
|---------|-------------|---------------|--------|
| Claude Code CLI (local) | Yes, JSONL on disk | Cron job reads JSONL | BROKEN (Stop-only) |
| Claude Code CLI (remote from phone) | Yes, JSONL on Mini | Cron job reads JSONL | BROKEN (Stop-only) |
| Claude Desktop app (macOS) | No | Relay via MCP connector | NOT BUILT |
| Claude web (claude.ai) | No | Relay via MCP connector | NOT BUILT |
| Claude iOS | No | Relay via MCP connector | NOT BUILT |
| OpenClaw TUI (Lesa) | No files, gateway | agent_end hook (per-turn) | WORKING |

---

## Two Capture Paths

### Path 1: JSONL Poller (Claude Code CLI)

Claude Code writes JSONL to `~/.claude/projects/*/`. A cron job reads those files every minute and does everything: Crystal ingestion, MD session export, daily log, transcript archive.

```
Claude Code writes JSONL -> Cron job reads file -> Crystal ingest + MD export + daily log
```

**Primary:** Cron job via LDM Dev Tools (every minute)
**Backup:** Stop hook (redundancy flush on session end)

Both use the same watermark. Both call the same core logic. The Stop hook is a bonus pass, not the system you depend on.

### Path 2: Relay (Claude Desktop, Web, iOS)

Claude on non-CLI surfaces connects to a remote MCP server. Memories are encrypted and relayed to the Mini. The Mini's poller decrypts and ingests.

```
Claude (web/iOS/Desktop) -> MCP server -> encrypt AES-256-GCM -> Relay Worker (R2) -> Mini poller -> crystal.db
```

This is Relay. Write-only from the cloud. Search only works locally. The cloud sees encrypted blobs.

Cloud Search is a separate, opt-in product where a plaintext mirror is pushed to D1 + Vectorize so search works from anywhere. Different product, different security model, not in this plan's scope.

---

## What Gets Built

### Phase 1: Fix Claude Code CLI capture (urgent)

**Goal:** Conversation turns appear in crystal.db within 60 seconds. No dependency on Stop hook.

1. **Unify cc-poller.ts + cc-session-export into one capture job**
   - cc-poller.ts already does: Crystal ingestion, daily log, transcript archive
   - Add: MD session export (port from cc-session-export/cc-export-hook.js)
   - One process, one JSONL read, all outputs
   - File: `src/cc-poller.ts` (already written, needs session export added)

2. **Create ldm-job shell script**
   - `tools/ldm-jobs/crystal-capture.sh` in wip-dev-tools-private
   - Calls `node ~/.ldm/extensions/memory-crystal/dist/cc-poller.js`
   - Same pattern as backup.sh, branch-protect.sh, visibility-audit.sh
   - Logs to `/tmp/ldm-dev-tools/crystal-capture.log`

3. **Schedule via cron (every minute)**
   ```
   * * * * * bash ~/path/to/tools/ldm-jobs/crystal-capture.sh >> /tmp/ldm-dev-tools/crystal-capture.log 2>&1
   ```
   Or via LDM Dev Tools.app if FDA is needed.

4. **Thin down Stop hook to redundancy check**
   - cc-hook.ts becomes a thin wrapper: calls the same poller logic
   - No more "seed at end of file on first run" behavior
   - If poller already captured everything, Stop hook is a no-op (watermark is current)

5. **Remove cc-session-export as separate Stop hook**
   - Its logic is merged into the poller
   - Remove from `~/.claude/settings.json` Stop hooks
   - cc-session-export component stays in repo but is deprecated

**Files to modify:**
- `memory-crystal-private/src/cc-poller.ts` ... add session export logic
- `memory-crystal-private/src/cc-hook.ts` ... thin down to redundancy wrapper
- `wip-dev-tools-private/tools/ldm-jobs/crystal-capture.sh` ... new ldm-job
- `~/.claude/settings.json` ... remove cc-session-export hook
- `memory-crystal-private/package.json` ... add cc-poller to build

### Phase 2: Health monitoring

**Goal:** Know within 2 hours if capture is broken.

1. **`crystal health` CLI command**
   - Three-file consistency: JSONL vs MD vs chunks
   - Stale detection: JSONL active but chunks not growing
   - Per-session status
   - Already written in cc-poller.ts --health, needs to be wired into CLI

2. **Integrate with wip-healthcheck**
   - Add memory health check (runs every 3 min with existing LaunchAgent)
   - Alert threshold: chunks more than 2 hours stale while JSONL is active
   - Escalation: warn agent, then iMessage Parker

**Files to modify:**
- `memory-crystal-private/src/cli.ts` ... add `crystal health` subcommand
- `wip-healthcheck-private/healthcheck.mjs` ... add Crystal stale check

### Phase 3: Relay for Claude Desktop/Web/iOS

**Goal:** Claude on any surface can save memories to the Mini via encrypted relay.

This is the MCP server on Cloudflare Workers. Already designed in the previous plan. Key clarifications:

- **This is Relay, not Cloud Search.** Write-only from cloud. Search only works locally.
- **Scoped to Claude only.** ChatGPT/OpenAI comes later.
- **Agent IDs:** `claude-macos`, `claude-ios`, `claude-web`
- **MCP tools:** `memory_remember` (encrypt + relay), `memory_search` (returns "search available on local devices"), `memory_forget` (queue deprecation), `memory_status` (relay health)
- **OAuth 2.1 + DCR** for Claude connector auth
- **Submit to Anthropic Connectors Directory**

**Files (new repo: memory-crystal-cloud-private):**
- `src/index.ts` ... Worker entry
- `src/auth.ts` ... OAuth 2.1
- `src/mcp.ts` ... MCP tool definitions
- `src/relay.ts` ... encrypt + drop
- `wrangler.toml`, `migrations/`

### Phase 4: Cloud Search (separate product, future)

**NOT in this plan.** Cloud Search is when a plaintext mirror of crystal.db is pushed to Cloudflare D1 + Vectorize so search works from anywhere. Different security model. Opt-in. Paid. Requires wip-agent-pay integration. Separate plan when we get there.

---

## Architecture Summary

```
                          CLAUDE CODE CLI
                          (local + remote)
                               |
                          JSONL on disk
                               |
                     cron job (every 1 min)
                        |      |      |
                   Crystal  MD export  Daily log
                   ingest              breadcrumb
                        |
                        v
                    crystal.db  <---- OpenClaw agent_end hook (Lesa)
                        ^
                        |
                   Mini poller
                   (decrypt)
                        |
                   Relay Worker (R2)
                   (encrypted blobs)
                        |
                   MCP Server
                   (Cloudflare)
                        |
              ----------------------
              |         |          |
           Claude    Claude     Claude
           Desktop   Web        iOS
```

---

## Verification

### Phase 1 (CLI capture)
```
[ ] Cron job runs every minute
[ ] New session turn appears in crystal.db within 60 seconds
[ ] MD session export updates within 60 seconds
[ ] Daily log breadcrumb written
[ ] Stop hook is redundancy only (works but not depended on)
[ ] cc-session-export removed from settings.json
[ ] 72-hour session with remote disconnects loses zero data
```

### Phase 2 (Health)
```
[ ] crystal health shows three-file consistency
[ ] wip-healthcheck alerts if chunks are 2+ hours stale
[ ] Parker gets iMessage if memory stops working
```

### Phase 3 (Relay)
```
[ ] Claude Desktop connects via MCP connector
[ ] memory_remember encrypts and drops to relay
[ ] Mini poller picks up and ingests with correct agent_id
[ ] memory_search returns "search available on local devices"
[ ] Anthropic Connectors Directory submission prepared
```

---

## Build Order

Phase 1 is urgent. Phase 2 follows immediately. Phase 3 is the next project.

**Phase 1 estimate:** 1-2 days (poller mostly written, need session export + ldm-job + cron)
**Phase 2 estimate:** 1 day (health check mostly written, need CLI wiring + healthcheck integration)
**Phase 3 estimate:** 5-7 days (MCP server, OAuth, relay, testing, directory submission)
