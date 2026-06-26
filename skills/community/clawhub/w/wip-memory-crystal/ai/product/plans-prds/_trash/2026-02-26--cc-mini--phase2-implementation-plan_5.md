# Memory Crystal Phase 2 — Implementation Plan

## Context

Memory Crystal currently only produces vector DB embeddings (crystal.db at ~/.openclaw/memory-crystal/). It needs to become the universal archive manager for ~/.ldm/: producing JSONL transcript copies, MD session summaries, and hosting the shared crystal.db at the LDM root. cc-air designed the architecture and built the ephemeral relay code on `cc-air/phase2-relay`. This plan implements Priorities 1-3 from the roadmap on a new `mini/phase2-relay` branch.

## Branch

`mini/phase2-relay` forked from `main` (which now has cc-air's planning docs merged).

## Execution Order

The sequencing matters. Dependencies flow downward:

1. **LDM Scaffolding** (P2) ... file writes depend on directories existing
2. **crystal.db move** (P1c) ... everything must resolve the new DB path
3. **JSONL archive** (P1a) ... simple file copy, depends on scaffold
4. **MD session summaries** (P1b) ... depends on JSONL and scaffold
5. **Dev-update migration** ... parallel-safe, small scope
6. **Relay merge** (P3) ... touches cc-hook, core, mcp-server that P1/P2 already modified

---

## Step 1: LDM Scaffolding (Priority 2)

**New file: `src/ldm.ts` (~120 lines)**

Central module for all LDM directory knowledge. Every other file imports paths from here.

- `getAgentId()` ... resolves from `CRYSTAL_AGENT_ID` env var, default `cc-mini`
- `ldmPaths(agentId?)` ... returns object with all paths: `root`, `config`, `crystalDb`, `crystalLance`, `agentRoot`, `transcripts`, `sessions`, `daily`, `journals`
- `scaffoldLdm(agentId?)` ... creates full directory tree, writes/updates `~/.ldm/config.json` with agents array
- `ensureLdm(agentId?)` ... idempotent check, calls scaffoldLdm if needed

**Modify: `src/cli.ts`** ... add `crystal init [--agent <id>]` subcommand calling `scaffoldLdm()`

**Target structure:**
```
~/.ldm/
  config.json                              (version, agents array)
  memory/
    crystal.db                             (shared, all agents)
    lance/                                 (LanceDB dual-write, pending removal)
  agents/{agent_id}/
    memory/
      transcripts/   sessions/   daily/   journals/
```

**Verify:** `crystal init --agent cc-mini` creates all dirs, config.json has cc-mini in agents array.

---

## Step 2: crystal.db Move (Priority 1c)

**Strategy: symlink-first, hard move later.** The 1.5GB DB with 152K+ chunks must not be corrupted.

**Modify: `src/core.ts` resolveConfig()**

Change dataDir default resolution:
1. Explicit override (always wins)
2. `CRYSTAL_DATA_DIR` env var (for testing)
3. If `~/.ldm/memory/crystal.db` exists, use `~/.ldm/memory/`
4. Fall back to legacy `~/.openclaw/memory-crystal/`

This auto-detection means old deployments keep working until migration runs.

**Add to `src/cli.ts`: `crystal migrate-db` subcommand**

1. Calls `ensureLdm()`
2. Checks source exists at `~/.openclaw/memory-crystal/crystal.db`
3. Checks destination doesn't exist (or is symlink)
4. Copies crystal.db to `~/.ldm/memory/crystal.db` (copy first, never move)
5. Verifies copy by opening with better-sqlite3, checking chunk count
6. Creates symlinks: old path -> new path (for lance/ too)
7. Reports success

**Safety:** Gateway and CC must be stopped during migration. Script checks for locks via `lsof`.

**Verify:** `crystal migrate-db` succeeds, `crystal status` shows same chunk count, `crystal search "test"` returns results.

---

## Step 3: JSONL Archive (Priority 1a)

**Modify: `src/cc-hook.ts`**

Add `archiveTranscript(transcriptPath, agentId)` function:
- Calls `ensureLdm(agentId)`
- Copies full JSONL file to `~/.ldm/agents/{agent_id}/memory/transcripts/`
- Only copies if source is newer than destination (mtime check)
- Called early in `main()`, after kill-switch checks, before watermark logic

Also update `appendDailyLog()` to use `ldmPaths()` instead of the hardcoded `LDM_DAILY` constant.

**Verify:** Run CC session with capture enabled, check JSONL copy appears in transcripts/, file size matches source.

---

## Step 4: MD Session Summaries (Priority 1b)

**New file: `src/summarize.ts` (~200 lines)**

Two modes, configurable via `CRYSTAL_SUMMARY_MODE` env var:

**LLM mode (default):** Calls gpt-4o-mini (or configured provider) with condensed transcript. Returns title, slug, summary, key topics. Format:
```markdown
# Session Title
**Session:** {id}  **Date:** {date}  **Messages:** {count}
## Summary
2-4 sentences
## Key Topics
- topic1
- topic2
```

**Simple mode:** First user message becomes title. Concatenates first 10 messages as preview. No API call.

**Integration in `src/cc-hook.ts`:**
- After successful ingest, call summary generator
- Write to `~/.ldm/agents/{agent_id}/memory/sessions/YYYY-MM-DD--HH-MM-SS--{agent}--{slug}.md`
- Wrapped in try/catch (non-fatal ... ingestion is more important than summary)

**Config env vars:** `CRYSTAL_SUMMARY_MODE` (llm|simple), `CRYSTAL_SUMMARY_PROVIDER` (openai|google), `CRYSTAL_SUMMARY_MODEL` (gpt-4o-mini)

**Verify:** Run capture with both modes, check MD files appear in sessions/ with correct naming format.

---

## Step 5: Dev-Update Migration

**Modify: `src/dev-update.ts`**

- Change output from centralized `wip-dev-updates` repo to each repo's own `ai/` folder
- Update filename format to `YYYY-MM-DD--HH-MM-SS--{agent}--dev-update-{repo}.md`
- Remove git add/commit/push to wip-dev-updates (each repo manages its own ai/)
- Keep throttle logic (once per hour)

**Verify:** Run dev update, files appear in `<repo>/ai/` with correct naming.

---

## Step 6: Merge Relay Code (Priority 3)

**Strategy:** `git merge origin/cc-air/phase2-relay` into `mini/phase2-relay`, resolve conflicts.

**Conflict zones:**
- `src/cc-hook.ts` ... heaviest conflicts (P1 added archive+summary, relay added mode switching). Resolution: keep both. Relay mode still archives JSONL and generates summary locally before encrypting.
- `src/core.ts` ... relay adds RemoteCrystal + createCrystal at end. P1c changed resolveConfig. Different locations, should merge clean.
- `src/mcp-server.ts` ... relay changed Crystal import. Minor conflicts.
- `package.json` ... build script merge (manual).

**New files from relay (no conflicts):**
- `src/crypto.ts` ... take as-is, fix HOME default
- `src/worker.ts` ... take as-is
- `src/poller.ts` ... needs expansion (see below)
- `src/mirror-sync.ts` ... update paths to use ldmPaths()
- `wrangler.toml` ... take as-is

**Poller expansion (key change):**

After decrypting relay blobs and ingesting into crystal, the poller must also reconstruct the remote agent's full file tree on the Mini:

1. Write JSONL to `~/.ldm/agents/{drop.agent_id}/memory/transcripts/relay-{blob.id}.jsonl`
2. Generate MD summary to `~/.ldm/agents/{drop.agent_id}/memory/sessions/`
3. Append daily breadcrumb to `~/.ldm/agents/{drop.agent_id}/memory/daily/`

This reuses `generateSessionSummary()` from `summarize.ts` and `appendDailyLog()` from cc-hook (refactored to be importable).

**mirror-sync.ts updates:** Change mirror DB path from `~/.openclaw/memory-crystal/crystal.db` to `~/.ldm/memory/crystal.db` via ldmPaths().

**Build scripts update:** Add `src/ldm.ts` and `src/summarize.ts` to tsup entry points in package.json.

**Verify:**
- `npm run build` passes zero errors
- `crystal status` works from `~/.ldm/memory/crystal.db`
- `crystal search "test"` returns results
- cc-hook produces all three file types (JSONL, MD, crystal)
- `node dist/poller.js --status` shows "not configured" (no relay URL yet)
- `node dist/mirror-sync.js --status` shows mirror state

---

## Step 7: Deploy Updated Plugin

```bash
cd /path/to/memory-crystal
npm run build
cp -r dist skills openclaw.plugin.json package.json ~/.openclaw/extensions/memory-crystal/
cd ~/.openclaw/extensions/memory-crystal && npm install --omit=dev
openclaw gateway restart
```

---

## File Inventory

**New files (3):**
| File | Lines | Purpose |
|------|-------|---------|
| `src/ldm.ts` | ~120 | LDM scaffolding, path resolution |
| `src/summarize.ts` | ~200 | MD session summary generation (LLM + simple) |

**From relay branch (4):**
| File | Lines | Changes needed |
|------|-------|----------------|
| `src/crypto.ts` | ~113 | Fix HOME default |
| `src/worker.ts` | ~208 | Take as-is |
| `src/poller.ts` | ~350 | Expand for full file tree reconstruction |
| `src/mirror-sync.ts` | ~180 | Update paths to ldmPaths() |

**Modified files (7):**
| File | What changes |
|------|-------------|
| `src/core.ts` | resolveConfig() LDM path, RemoteCrystal merge |
| `src/cc-hook.ts` | JSONL archive, summary gen, relay mode, ldm imports |
| `src/mcp-server.ts` | createCrystal() factory, remote mode guards |
| `src/cli.ts` | `crystal init` and `crystal migrate-db` subcommands |
| `src/dev-update.ts` | Write to repo ai/ folder with new naming |
| `src/openclaw.ts` | Use createCrystal() for remote mode |
| `package.json` | Updated build scripts |

---

## Risk Mitigation

- **crystal.db:** Copy-first, symlink-second. Original never deleted. Rollback: remove symlink.
- **WAL files:** Stop gateway before migration. SQLite recreates WAL/SHM after copy.
- **Auto-detection:** resolveConfig checks LDM first, falls back to legacy. No breakage for unmigrated setups.
- **Private mode:** All new code paths check isPrivateMode() before writing.
- **Summary failure:** Non-fatal. Ingestion succeeds even if summary generation fails.
- **Build gate:** npm run build must pass before any deployment.

---

## End-to-End Verification

After all steps:
1. `crystal init --agent cc-mini` ... scaffolds ~/.ldm/
2. `crystal migrate-db` ... moves DB, creates symlinks
3. Run a CC session, let cc-hook fire
4. Check: JSONL in transcripts/, MD in sessions/, chunks in crystal.db, breadcrumb in daily/
5. `crystal search "something from the session"` ... returns the new content
6. `crystal status` ... shows updated chunk count
7. Gateway restart ... OpenClaw plugin initializes with new paths
8. Lesa conversation ... crystall plugin captures to shared crystal.db
