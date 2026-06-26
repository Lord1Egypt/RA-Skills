# Plan: Memory Crystal v0.5.0 ... Init Discovery + Raw Data Safety + Memory Consolidation

**Date:** 2026-03-04
**Author:** CC-Mini
**Repo:** `ldm-os/components/memory-crystal-private/`

## Context

Three problems converged into one plan:

1. **Raw data safety** (from `ai/plan/mem-consolidation/raw-data-gaps.md`): LDM is missing ~1,292 raw session files (~813MB) from both agents. The bulk copy to Mini was done manually, but this needs to be automated as part of init.

2. **Memory consolidation** (from `ai/plan/mem-consolidation/investigation.md`): Three vector databases exist (main.sqlite, context-embeddings.sqlite, crystal.db). Context-embeddings has ~3,108 unique Lēsa conversation chunks not in crystal. We need to migrate those into crystal and retire the CE plugin.

3. **Per-harness init** (Parker's direction): When you install Memory Crystal on any platform, init should discover THAT platform's session files, copy them to LDM, and relay them to Core for embedding. Init is scoped to the current harness only. Dream Weaver and embedding happen on the Core (mini), not the Node.

**The flow for a new device (e.g. MacBook Air):**
1. `crystal init --agent cc-air` on the Air
2. Crystal discovers CC-Air's local session JSONLs only
3. Copies them to `~/.ldm/agents/cc-air/memory/transcripts/`
4. Relays extracted messages to Core (mini) via existing relay Worker
5. Core's poller picks them up, embeds, runs Dream Weaver
6. Core's crystal.db now includes cc-air data
7. Mirror sync pushes searchable DB back to Air

**The flow for Mini (already installed):**
1. `crystal backfill` embeds the raw files we already copied to LDM
2. `crystal migrate-embeddings` merges CE's unique chunks into crystal
3. Disable CE plugin in openclaw.json
4. One database, one search, one truth

---

## Phase 1: Harness Discovery (`src/discover.ts` ... new file)

Detects which agent platforms are installed on THIS machine and returns session file locations. Does NOT look for other agents' data.

**Detection logic:**
- Claude Code: check `~/.claude/projects/` for subdirectories with `*.jsonl` files
- OpenClaw: check `~/.openclaw/agents/*/sessions/` for `*.jsonl` files
- OpenClaw workspace: check `~/.openclaw/workspace/` for `*.md` files

**Exports:**
```typescript
interface HarnessInfo {
  platform: 'claude-code' | 'openclaw';
  sessionDir: string;
  workspaceDir?: string;       // OpenClaw workspace (md files)
  filePattern: string;          // glob for session files
  agentIdDefault: string;       // suggested agent ID
}

interface DiscoveryResult {
  harnesses: HarnessInfo[];
  totalFiles: number;
  totalSizeBytes: number;
  breakdown: Array<{ platform: string; files: number; sizeBytes: number }>;
}

function discoverHarnesses(): HarnessInfo[]
function discoverAll(): DiscoveryResult
```

**Reuses:** Session file scanning from `cc-poller.ts:discoverSessionFiles()` (lines 144-166), generalized.

## Phase 2: Bulk Copy (`src/bulk-copy.ts` ... new file)

Copies raw session files from source locations to LDM transcripts. Idempotent (skips files that already exist with same size).

**Exports:**
```typescript
interface BulkCopyResult {
  filesCopied: number;
  filesSkipped: number;
  bytesWritten: number;
  durationMs: number;
}

function bulkCopyToLdm(
  sessionPaths: string[],
  agentId: string,
  options?: { workspace?: boolean; workspaceSrc?: string }
): BulkCopyResult
```

**Behavior:**
- Copies each JSONL to `~/.ldm/agents/{agentId}/memory/transcripts/{filename}`
- For OpenClaw: also copies workspace `*.md` files to `~/.ldm/agents/{agentId}/memory/workspace/`
- Raw files are NEVER modified (read-only copy)
- Skips files that already exist with same size

**LDM paths update** (`src/ldm.ts`):
- Add `workspace` to `LdmPaths` interface
- Add to `scaffoldLdm()` directory creation
- Path: `~/.ldm/agents/{agent_id}/memory/workspace/`

## Phase 3: OpenClaw Session Parser (`src/oc-backfill.ts` ... new file)

OpenClaw JSONL has a different format than Claude Code JSONL. This module parses OpenClaw sessions into the same message format used by cc-poller.

**Format difference:**
- Claude Code: `{"type":"user","message":{"role":"user","content":"..."}}`
- OpenClaw: `{"type":"message","message":{"role":"user","content":[{"type":"text","text":"..."}]}}`

**Exports:**
```typescript
function extractOpenClawMessages(filePath: string, lastByteOffset?: number): {
  messages: ExtractedMessage[];
  newByteOffset: number;
}
```

**Reuses:** Same `ExtractedMessage` type from cc-poller. Same watermark pattern.

## Phase 4: Backfill Command (`crystal backfill`)

New CLI command that triggers embedding of all raw files in LDM transcripts.

```
crystal backfill [--agent <id>] [--dry-run] [--limit <n>]
```

**For Core / Standalone:**
- Scans `~/.ldm/agents/{agentId}/memory/transcripts/*.jsonl`
- Auto-detects JSONL format (Claude Code vs OpenClaw)
- Extracts messages using appropriate parser
- Calls `crystal.ingest()` for embedding
- Watermark tracking prevents re-embedding
- `--dry-run` shows file count, estimated tokens, estimated cost (~$3 for full backfill)

**For Node:**
- Same scan and extraction
- Instead of local embed, calls `dropAtRelay()` from cc-hook.ts
- Core's existing `poller.ts` picks up blobs and embeds
- Rate-limited batching (10 blobs at a time) to avoid relay saturation

**Key principle:** Dream Weaver (embedding + narrative consolidation) happens on Core only. Node sends raw data to Core. Node gets mirror DB back.

## Phase 5: CE Migration (`crystal migrate-embeddings`)

Migrate ~3,108 unique conversation chunks from context-embeddings.sqlite into crystal.db.

```
crystal migrate-embeddings [--dry-run]
```

**Steps:**
1. Backup crystal.db (mandatory first step)
2. Open context-embeddings.sqlite read-only
3. For each chunk: SHA-256 hash text, check if crystal has it, insert if unique
4. Copy embedding blob directly (same model: text-embedding-3-small, 1536d, float32)
5. Zero API calls, zero cost, zero quality loss
6. Report: migrated count, skipped (duplicate) count

**Safety:**
- `--dry-run` shows what would migrate (no writes)
- CE is never modified (read-only)
- Crystal backed up before any writes
- If something goes wrong: restore crystal.db backup, re-enable CE plugin
- Embeddings are directly compatible (same model, dimensions, format)

**CE database schema** (from investigation):
```sql
-- conversation_chunks table
-- Fields: id, text, role, agent_id, session_key, turn_index, compaction_number,
--         token_count, created_at, embedding (BLOB float32[1536])
```

**Crystal target schema:**
```sql
-- chunks table + chunks_vec virtual table
-- Maps: text -> text, role -> role, agent_id -> agent_id,
--        session_key -> source_id, embedding -> chunks_vec
```

## Phase 6: Update `crystal init` Flow

Modify `src/cli.ts` init handler (line 451+):

After existing scaffold:
1. Call `discoverAll()` to find session files
2. Display summary:
   ```
   Discovered sessions:
     Claude Code: 447 files (535MB)
     OpenClaw:    748 files (154MB)
     Total:       1,195 files (689MB)

   Copy to LDM? [Y/n]
   ```
3. On confirm: run `bulkCopyToLdm()`
4. Report next steps based on role:
   - Core: `Run "crystal backfill" to embed all sessions (~$3).`
   - Node: `Run "crystal backfill" to relay sessions to Core.`

Support `--yes` / `-y` for non-interactive mode. Support `--skip-discover` to skip.

## Phase 7: Retire Context-Embeddings

After migration verified:

1. Remove `context-embeddings` from `openclaw.json` plugins list
2. Do NOT delete the plugin or database
3. `context-embeddings.sqlite` stays on disk as backup indefinitely
4. Gateway restart picks up the config change

**Update lesa-bridge** (separate task, not blocking):
- Option A: Point `lesa_conversation_search` at crystal.db
- Option B: Remove it entirely (crystal_search covers it)
- `lesa_memory_search` stays either way (workspace .md file search)

## Phase 8: Build + Version Bump

- Add discover.ts, bulk-copy.ts, oc-backfill.ts to tsup entry points
- Version bump to 0.5.0
- Update SKILL.md init section to mention discovery

---

## Execution Order

| Step | What | New/Modify | Depends On |
|------|------|------------|------------|
| 1 | `src/discover.ts` | new | nothing |
| 2 | `src/ldm.ts` (add workspace path) | modify | nothing |
| 3 | `src/bulk-copy.ts` | new | step 2 |
| 4 | `src/oc-backfill.ts` | new | nothing |
| 5 | backfill + init updates in `cli.ts` | modify | steps 1-4 |
| 6 | `crystal migrate-embeddings` in cli.ts | modify | nothing |
| 7 | package.json build + version | modify | all |
| 8 | build + test on Mini | - | step 7 |
| 9 | test backfill (Core, dry-run then real) | - | step 8 |
| 10 | run migrate-embeddings (dry-run then real) | - | step 8 |
| 11 | disable CE plugin in openclaw.json | - | step 10 |
| 12 | test on Air (Node init + relay backfill) | - | step 8 |

Steps 1, 2, 4, 6 have no dependencies and can be built in parallel.

---

## Critical Files

| File | Role |
|------|------|
| `src/cli.ts` | Command dispatch: init flow, backfill, migrate-embeddings |
| `src/ldm.ts` | Add workspace path to LdmPaths + scaffoldLdm |
| `src/cc-poller.ts` | Reference: JSONL parsing, watermarking, extractMessages() |
| `src/cc-hook.ts` | Reference: dropAtRelay() for Node mode |
| `src/poller.ts` | Core-side relay poller (already handles incoming relay drops) |
| `src/core.ts` | Crystal.ingest(), chunkText(), resolveConfig() |
| `src/role.ts` | detectRole() for Core/Node/Standalone branching |

## Files NOT Changed

| File | Reason |
|------|--------|
| `src/worker.ts` | Existing `conversations` channel is sufficient |
| `src/poller.ts` | Already handles relay drops from any agent |
| `src/mirror-sync.ts` | Existing mirror pull logic unchanged |
| `src/openclaw.ts` | Continues as agent_end hook unchanged |

## Verification

```bash
npm run build

# Phase 1-3: Init with discovery
node dist/cli.js init --agent cc-mini --yes    # Should show discovered files + copy

# Phase 4: Backfill
node dist/cli.js backfill --agent cc-mini --dry-run   # Show what would embed
node dist/cli.js backfill --agent cc-mini --limit 10   # Embed first 10 files as test
node dist/cli.js backfill --agent cc-mini              # Full backfill

# Phase 5: CE migration
node dist/cli.js migrate-embeddings --dry-run   # Show unique chunks count
node dist/cli.js migrate-embeddings              # Migrate

# Phase 7: Verify
node dist/cli.js doctor                          # Should show healthy
crystal search "test query"                      # Should hit migrated chunks
```

## Cost Estimate

| Operation | Files | Est. Tokens | Cost |
|-----------|-------|-------------|------|
| CC-mini backfill | 447 sessions | ~133M | ~$2.68 |
| OC-lesa-mini backfill | 748 sessions | ~38M | ~$0.77 |
| CE migration | 3,108 chunks | 0 (copy embeddings) | $0.00 |
| **Total** | | | **~$3.45** |

## Relationship to Prior Work

- **raw-data-gaps.md**: Bulk copy was done manually (748 + 133 + 476 files). This plan automates it as part of init.
- **investigation.md**: Documents the three databases and CE migration path. Phase 5 implements it.
- **v0.4.0 plan**: Built role, doctor, backup, bridge. This plan builds on that foundation.
- **roadmap Priority 4**: "Retire context-embeddings." This plan executes it.
