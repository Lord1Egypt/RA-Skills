# Dev Update: Phase 1 Complete. Continuous Capture is Live.

**Date:** 2026-03-02 18:00 PST
**Author:** CC-Mini
**Branch:** cc-mini/cloud-mcp (4 commits this session)

---

## What We Did (Full Session)

### Critical Bug Fix: 72-Hour Data Loss

A 72-hour session (Feb 27 to Mar 1) produced zero Crystal chunks. The Stop hook only fires when a session ends. Long sessions, remote disconnects, and compactions never trigger Stop. The poller decouples capture from the session lifecycle.

- **cc-poller.ts**: Unified continuous capture. One JSONL read produces all three outputs: vector chunks, MD session exports, daily breadcrumb logs.
- **cc-hook.ts**: Thinned to redundancy wrapper. Checks watermark, flushes anything poller missed. If poller already captured everything, Stop hook is a no-op.
- **cc-session-export**: Deprecated. Logic merged into cc-poller.ts. README updated with deprecation notice (original content preserved).

### Backfill

- Reset all 51 session watermarks to byte 0
- Re-ingested 10,349 new chunks. All 51 sessions IN SYNC.
- cc-mini chunks: 2,929 to 13,291
- Total crystal.db: 168,711 chunks, 168,711 vector rows (matching)

### Cron Fix (Three Bugs Found and Fixed)

**Bug 1: error -1712.** `open -W LDMDevTools.app` fails at every-minute frequency. Fix: run from `~/.ldm/bin/crystal-capture.sh` via bare cron. No app needed. `~/.ldm/` is local (not iCloud), so no Full Disk Access required.

**Bug 2: op CLI popup.** The shell script called `op item get` which was wrong for two reasons: (a) service accounts require `--vault` flag, (b) macOS TCC pops a consent dialog for `op` from cron. Fix: removed `op` call from shell script entirely. The Node poller already has `opRead()` in core.ts that correctly uses `op read` with vault path and SA token via environment variable.

**Bug 3: op not on PATH.** Cron provides minimal PATH (`/usr/bin:/bin`). The `op` binary lives at `/opt/homebrew/bin/op`. `opRead()` calls it but cron can't find it. Fix: added `export PATH="/opt/homebrew/bin:$PATH"` to crystal-capture.sh.

**Verified:** Cron fires every minute. 3 chunks captured. 0 errors. Log at `/tmp/ldm-dev-tools/crystal-capture.log`.

### crystal init Deploys Everything

`crystal init` now does three things:
1. Scaffolds `~/.ldm/` directory tree (existing)
2. Copies `crystal-capture.sh` to `~/.ldm/bin/` (new)
3. Installs cron entry for every-minute capture (new)

New functions in `ldm.ts`: `deployCaptureScript()`, `installCron()`, `removeCron()`. The `installCron` filter is precise: only removes lines matching our tag or our entry. Won't touch other cron jobs.

### Source of Truth Established

`scripts/crystal-capture.sh` lives in the memory-crystal repo. Build copies it to `dist/`. `crystal init` deploys it to `~/.ldm/bin/`. The dev tools app has a downstream copy with a pointer comment. **Memory Crystal never depends on Dev Tools.**

### Docs Updated

- **TECHNICAL.md**: "How Does It Work with Claude Code CLI?" rewritten. Poller primary, Stop hook redundancy. Directory structure includes `bin/` and `extensions/`. `ldm.ts` docs include new functions. Project structure includes `cc-poller.ts` and `crystal-capture.sh`.
- **SKILL.md**: Added Setup section showing `crystal init`.
- **README.md**: `crystal init` added to the onboarding prompt block. One flow: user pastes prompt, agent reads SKILL.md, agent installs. No separate Quick Start section.

### Dream Weaver Consolidation

- Journal: `~/.ldm/agents/cc-mini/memory/journals/2026-03-02-the-capture-crisis.md`
- 8 Crystal memories stored (IDs 215-222): LDM folder structure, poller vs hook, Relay vs Cloud Search, LDM Dev Tools, capture crisis, Parker's preferences, context-embeddings, surface scope.

### v2 PRD Committed

Memory Crystal v2 Product Requirements Document committed to repo. Agent-self memory architecture: agent-perspective indexing, continuity namespace, write-back, provenance signing, cross-model portability.

---

## Commits (This Session)

| Hash | Message |
|------|---------|
| a949ab4 | Phase 1: Unified capture, cron fix, crystal init deployment |
| bfe8a84 | Add Memory Crystal v2 PRD: agent-self memory architecture |
| 393be98 | Fix cron PATH: op CLI not findable in minimal cron environment |
| d0bbd12 | Fix cron: PATH for op CLI, robust installCron filter, log dir |

---

## Files Changed

| File | Change |
|------|--------|
| `src/cc-poller.ts` | Unified capture (vectors + MD + daily log) |
| `src/cc-hook.ts` | Thinned to redundancy wrapper |
| `src/ldm.ts` | bin path, deployCaptureScript, installCron, removeCron |
| `src/cli.ts` | crystal init deploys script + cron |
| `package.json` | Build copies crystal-capture.sh to dist/ |
| `scripts/crystal-capture.sh` | NEW. Source of truth. PATH fix. No op call. |
| `TECHNICAL.md` | Rewritten Claude Code section, updated structure |
| `SKILL.md` | Added Setup section |
| `README.md` | crystal init in onboarding prompt |
| `ai/product/product-ideas/memory-crystal-v2-prd.md` | NEW. v2 PRD. |
| `ai/product/product-ideas/native-apple-app-crystal-sync.md` | NEW. Native app idea. |
| `ai/product/product-ideas/cli-capture-cron-fix.md` | NEW. Cron fix recommendation. |
| `ai/dev-updates/2026-03-02--16-00--*` | Capture crisis dev update |
| `ai/dev-updates/2026-03-02--17-00--*` | Cron fix dev update |
| `ai/plan/2026-03-01--*` | Unified capture architecture plan |

Also modified (not in repo):
- `~/.ldm/bin/crystal-capture.sh` (deployed)
- `wip-dev-tools-private/.../crystal-capture.sh` (downstream pointer)
- `LDMDevTools.app/.../crystal-capture.sh` (op call removed)
- `cc-session-export/README.md` (deprecation notice)
- Crontab (updated entry)

---

## Phase 1 Status: COMPLETE

All verification checks pass:

```
[x] Cron job runs every minute
[x] New session turn appears in crystal.db within 60 seconds
[x] MD session export updates within 60 seconds
[x] Daily log breadcrumb written
[x] Stop hook is redundancy only (works but not depended on)
[x] cc-session-export removed from settings.json
[x] No macOS popups from op CLI
[x] No dependency on LDM Dev Tools app
[x] crystal init handles full install (scaffold + deploy + cron)
```

---

## What's Next

### Immediate

1. **Merge to main + release.** `cc-mini/cloud-mcp` branch has everything. Merge, run `wip-release patch`. This is a shippable state.

2. **Organize AI folders.** Parker mentioned this. The `ai/` directory has grown organically. Needs structure review.

### Phase 2: Health Monitoring

3. **Wire `crystal health` into CLI.** The health check logic exists in cc-poller.ts (`--health` flag). Needs to be exposed as `crystal health` in cli.ts. Three-file consistency check: JSONL vs MD vs chunks. Stale detection.

4. **Integrate with wip-healthcheck.** Add Crystal stale check to the existing LaunchAgent (runs every 3 min). Alert threshold: chunks more than 2 hours stale while JSONL is active. Escalation: warn agent, then iMessage Parker.

### Phase 2.5: Agent Install Flow

5. **Test agent-to-agent install.** Paste the README prompt into a fresh Claude Code session. Verify it reads SKILL.md, explains the tool, and runs `crystal init` when the user says yes. This is the product flow. It needs to work end to end.

### Phase 3: Relay

6. **MCP server on Cloudflare Workers.** Claude Desktop, Claude Web, Claude iOS connect via OAuth 2.1. Encrypted relay to home machine. Already designed in the plan. Separate project.

### Future

7. **Memory Crystal v2.** Agent-perspective indexing. Continuity namespace. Write-back. The PRD is committed. This is where the product goes after Relay is validated.
