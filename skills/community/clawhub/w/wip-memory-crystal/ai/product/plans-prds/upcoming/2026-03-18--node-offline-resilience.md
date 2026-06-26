# Plan: Memory Crystal Node Offline Resilience

## Context

When Core (Mini) is offline, Node (Air) cannot embed chunks. Core is the only embedder. This means:
- Conversations captured on Node are dropped at the relay (24h TTL), then lost if Core doesn't pick up
- If relay is also down, 4 retries then data is lost entirely (no local queue)
- Node can't search new conversations because they were never embedded
- Parker travels with the Mini. Core could be offline for days.

Flagged during system health check on 2026-03-18. The architecture intentionally keeps Nodes stateless, but stateless means data loss when Core is unavailable.

## Solution: 7 Layers (each standalone, ship in order)

### Layer 1: Local Pending Queue (zero data loss)

When `dropAtRelay()` fails after retries, persist messages to `~/.ldm/state/pending-drops.jsonl`. Replay on next successful relay contact. ~35 lines.

**File:** `src/cc-hook.ts`

New functions after line 264:
- `writePendingDrop(messages)` ... append to `pending-drops.jsonl`
- `replayPendingDrops()` ... read file, attempt each drop, write back only failures

Modify `main()` relay catch block (lines 443-447):
- Catch relay failure, call `writePendingDrop()` instead of exit(1)
- Advance watermark (data is safe on disk)
- Call `replayPendingDrops()` at START of every relay attempt (FIFO ordering)

### Layer 2: Local Ingest Without Embedding (text-searchable)

When Core is unreachable, write chunks to local crystal.db WITHOUT vectors. FTS5 trigger fires automatically. Chunks are immediately text-searchable. ~50 lines.

**File:** `src/core.ts`

New method on Crystal class after `ingest()` (~line 645):
- `ingestTextOnly(chunks)` ... same as `ingest()` minus the `embed()` and `insertVec` calls. FTS5 trigger handles text indexing automatically.

**File:** `src/cc-hook.ts`

In the Layer 1 catch block, also call `crystal.ingestTextOnly()` so chunks are locally searchable immediately.

**File:** `src/cc-poller.ts`

Modify `pollOnce()` (lines 431-454): when `ingestLocal()` fails because no embedding provider (Node mode), fall back to `ingestTextOnly()`.

### Layer 3: Re-embed on Reconnection

When Core comes back and processes the pending queue, delta sync sends embedded chunks to Node. Node must upgrade its unembedded local copies. ~10 lines.

**File:** `src/core.ts`

Modify `importChunks()` (lines 695-739): currently skips chunks where `text_hash` exists. Change to: if chunk exists but has no vector in `chunks_vec`, INSERT the vector. Text-only chunks get upgraded to fully embedded.

### Layer 4: Search Graceful Degradation

When Node searches and some chunks lack vectors, fall back to FTS5-only for those. ~25 lines.

**File:** `src/core.ts`

Modify `search()` (lines 774-819): wrap `this.embed([query])` in try/catch. If no embedding provider, skip vector search entirely. Return FTS5 results with recency weighting.

**File:** `src/search-pipeline.ts`

Modify `deepSearch()` (line 79): same embed guard. Skip vector expansion when no provider available.

### Layer 5: Warning System (boot-time health report)

On session start, show what's working and what's not. Agents and Parker should know the state of the system immediately. ~40 lines.

**File:** `src/cc-hook.ts` (or new `src/health.ts`)

New function `checkHealth()` that reports:
- **Role**: Core or Node (and whether overridden via state file)
- **Relay**: reachable or not (quick HEAD request with 3s timeout)
- **Core reachable**: can the relay be reached and does Core have recent activity? (check last delta timestamp)
- **Pending queue**: N drops waiting (from `pending-drops.jsonl`)
- **Unembedded chunks**: N chunks without vectors (quick SQL count)
- **Embedding provider**: available or missing (OpenAI key, Ollama, etc.)
- **Last sync**: when was the last successful delta pull (from `mirror-sync-state.json`)

**File:** `src/cli.ts`

New command `crystal health` that runs `checkHealth()` and prints a summary:
```
Crystal Health (2026-03-18 16:30 PST)
  Role:         Node (auto-detected)
  Relay:        OK (https://relay.example.com)
  Core:         OFFLINE (last delta: 2h ago)
  Pending:      3 drops queued
  Unembedded:   47 chunks (FTS-only)
  Embeddings:   not available (Node mode)
  Last sync:    2026-03-18 14:30
```

**File:** `src/openclaw.ts` (Lesa's hook) and boot hook integration

On `agent_start` or session boot, run `checkHealth()` and inject warnings:
```
WARNING: Core has been offline for 2 hours. 3 pending drops queued.
47 chunks are text-searchable only (no semantic search).
Run `crystal promote` to enable local embedding on this device.
```

### Layer 6: Daily Status Digest

Automated daily summary of system health. Written to the shared daily log (`~/.ldm/memory/daily/`). ~30 lines.

**File:** `scripts/crystal-capture.sh` (or new `src/daily-digest.ts`)

Once per day (detect via state file `last-digest-date`), generate and append a digest:

```markdown
## [00:00] Crystal Daily Digest
- Role: Core | Chunks: 79,038 (+1,515 today) | Memories: 355
- Relay: OK | Last sync: 16:30 | Pending drops: 0
- Unembedded: 0 | Embedding provider: OpenAI
- Health: All systems operational
```

Or when things are broken:
```markdown
## [00:00] Crystal Daily Digest
- Role: Node | Chunks: 45,200 (+200 today) | Memories: 180
- Relay: OK | Core: OFFLINE 18h | Pending drops: 12
- Unembedded: 200 | Embedding provider: none (Node mode)
- WARNING: Core offline >12h. Consider `crystal promote` for local embedding.
```

Written to:
- `~/.ldm/memory/daily/YYYY-MM-DD.md` (shared log)
- `~/.ldm/agents/{agent}/memory/daily/YYYY-MM-DD.md` (agent's own log)

Triggered from `crystal-capture.sh` cron (runs every minute, digest runs once per day).

### Layer 7: Role Switching Workflow (promote/demote)

`crystal promote` and `crystal demote` already exist but need a complete workflow. ~60 lines.

**The problem:** Promoting a Node to Core requires an embedding provider. Demoting Core back to Node needs to reconcile chunks. The current commands just flip a state file flag with no validation or data handling.

**File:** `src/cli.ts` (promote block, lines 130-137)

Enhance `crystal promote` to:
1. **Check for embedding provider.** If no OPENAI_API_KEY/Ollama/Google, warn and ask for confirmation: "No embedding provider found. Promoted Core won't be able to embed. Continue? (y/n)" Or: attempt to resolve via 1Password (`opRead` for OpenAI key).
2. **Embed pending text-only chunks.** If Layer 2 created text-only chunks, offer to embed them now: "Found 47 unembedded chunks. Embed now? (y/n)"
3. **Start local capture.** Switch cc-hook from relay mode to local mode (or hybrid: embed locally AND drop at relay for the other Core to pick up later).
4. **Log the promotion** to shared daily log and `shared-log.jsonl` (Layer 5 of the shared awareness plan): `{"type":"alert","msg":"Air promoted to Core. Mini offline."}`

**File:** `src/cli.ts` (demote block, lines 140-151)

Enhance `crystal demote` to:
1. **Check for unsynced chunks.** If this device has chunks that the original Core doesn't have (embedded locally during temporary promotion), warn: "142 chunks were embedded locally. These need to sync to the original Core. Push to relay now? (y/n)"
2. **Push local chunks to relay.** Export chunks that are newer than the last delta sync and drop them at the relay for the original Core to pick up.
3. **Switch capture back to relay mode.** cc-hook resumes dropping at relay instead of local ingest.
4. **Log the demotion** to shared daily log.

**File:** `src/role.ts`

Add `getRoleHistory()` function that reads promote/demote events from `crystal-role.json` (or a separate `role-history.jsonl`). This lets the system know when roles changed and reconcile accordingly.

**The full travel workflow:**
```
# Parker packing Mini. Air takes over.
[Air] $ crystal promote
  Checking embedding provider... OpenAI API key found (via 1Password).
  Promoting to Core.
  47 unembedded chunks found. Embedding now... done.
  Capture mode: local (embed + relay backup).
  Logged: "Air promoted to Core. Mini offline."

# Parker traveling. Air is Core. Mini is off.
# All conversations embed locally on Air. Also dropped at relay as backup.

# Parker home. Mini back online.
[Mini] $ crystal status
  WARNING: Air was promoted to Core 3 days ago.
  412 chunks were embedded on Air during that period.
  Run `crystal sync` to pull Air's chunks.

[Air] $ crystal demote
  142 locally-embedded chunks not yet synced.
  Pushing to relay... done.
  Demoting to Node.
  Capture mode: relay.
  Logged: "Air demoted to Node. Mini resuming as Core."

[Mini picks up Air's chunks via relay poller. Done.]
```

## Files to Modify

All in `repos/ldm-os/components/memory-crystal-private/`:

| File | Layer | Changes |
|------|-------|---------|
| `src/cc-hook.ts` | 1, 2 | Pending queue write/replay, text-only ingest on failure |
| `src/core.ts` | 2, 3, 4 | `ingestTextOnly()`, `importChunks()` upgrade logic, `search()` embed guard |
| `src/cc-poller.ts` | 2 | Text-only fallback in `pollOnce()` |
| `src/search-pipeline.ts` | 4 | Embed guard in `deepSearch()` |
| `src/health.ts` (new) | 5, 6 | `checkHealth()`, `dailyDigest()` |
| `src/cli.ts` | 5, 7 | `crystal health` command, enhanced promote/demote |
| `src/openclaw.ts` | 5 | Boot-time health warnings for Lesa |
| `src/role.ts` | 7 | `getRoleHistory()`, role event logging |
| `scripts/crystal-capture.sh` | 6 | Daily digest trigger (once per day) |

## Implementation Order

1. **Layer 1** (pending queue) ... most critical, prevents data loss
2. **Layer 2** (text-only ingest) ... makes Node useful offline
3. **Layer 4** (search degradation) ... makes text-only chunks searchable
4. **Layer 3** (re-embed on reconnect) ... upgrade path when Core returns
5. **Layer 5** (warning system) ... visibility into what's broken
6. **Layer 6** (daily digest) ... ongoing status awareness
7. **Layer 7** (role switching) ... the travel workflow

Layers 1-4: ~120 lines across 4 files (data safety).
Layers 5-7: ~130 lines across 5 files (operational awareness + workflow).
Total: ~250 lines across 7 files.

## Verification

```bash
# Layer 1: Kill relay, run CC session, check pending-drops.jsonl exists
# Bring relay back, run another session, verify replay + empty queue

# Layer 2: Unset OPENAI_API_KEY on Node, run poller
# Verify chunks in `chunks` but NOT in `chunks_vec`

# Layer 4: On Node without API key, run `crystal search "test"`
# Verify FTS5 results returned

# Layer 3: Replay pending to Core, Core embeds, delta syncs back
# Verify previously unembedded chunks now have vectors

# Layer 5: Run `crystal health` on Node with Core offline
# Verify it shows Core OFFLINE, pending count, unembedded count

# Layer 6: Wait for cron cycle, check daily log for digest entry

# Layer 7 (full travel workflow):
# On Air: `crystal promote` -> verify embedding works
# Run CC sessions on Air -> verify local ingest + relay backup
# On Air: `crystal demote` -> verify chunks pushed to relay
# On Mini: verify Mini picks up Air's chunks via poller

# Full chain: Node offline -> text-searchable -> promote to Core ->
# full embedding -> demote back -> sync -> all chunks reconciled
```

## Key Design Decisions

**Watermark advances on pending write, not just relay success.** The data is persisted locally in `pending-drops.jsonl`. Not advancing would cause duplicate extraction. Dedup is handled by hash checks at relay and Core.

**Promote doesn't change the embedding model.** Both Core and temporary-Core use the same OpenAI text-embedding-3-small model via the same API key (1Password). Embeddings are compatible.

**Demote pushes, doesn't merge.** When demoting, the temporary Core pushes its locally-embedded chunks to the relay. The original Core picks them up and imports them (dedup by hash). No manual merge needed.

## What This Does NOT Include

- Relay-side TTL configuration (currently hardcoded 24h in Cloudflare Worker)
- Automatic role switching (always manual via `crystal promote/demote`)
- Changes to `mirror-sync.ts` (delta pull works unchanged)
- Multi-Core scenarios (only one Core at a time)
- Version bump / release (after verification)
