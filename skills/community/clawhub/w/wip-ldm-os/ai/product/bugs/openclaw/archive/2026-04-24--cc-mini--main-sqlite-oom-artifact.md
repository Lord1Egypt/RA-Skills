# OpenClaw main.sqlite OOM forensic artifact (R1.D deliverable)

**Filed:** 2026-04-24 PST
**Author:** cc-mini (Claude Code on the Mac mini), Explore agent research + Claude Code verification
**Crash:** V8 heap OOM at `StatementSync::All` (Node built-in `node:sqlite`)
**Deliverable type:** R1.D forensic artifact for the v2 triage plan (`ai/product/bugs/memory-crystal/2026-04-24--cc-mini--unified-reliability-triage.md`). Research only. R2.A implements the bounded-read patch based on this.
**Snapshot:** `/Users/lesa/.openclaw/_snapshots/2026-04-24-forensic/` (R1.0)

## Summary

The OOM is **not** in OpenClaw "core" in the generic sense. The failing code is in the **`memory-core` bundled extension**, not in `src/gateway/` or `src/channels/`. The database `~/.openclaw/memory/main.sqlite` (16 GB) is memory-core's store. It has no relationship to Memory Crystal's `crystal.db` (1.84 GB, `better-sqlite3`, separate system).

Top culprit: `seedEmbeddingCache()` in `extensions/memory-core/src/memory/manager-sync-ops.ts` does an unbounded `.all()` over `embedding_cache` (435,136 rows; 8.68 GB of serialized embedding text). V8 heap cap of ~4 GB is exhausted during result-set materialization.

Secondary culprit: `listChunks()` in `extensions/memory-core/src/memory/manager-search.ts` does `SELECT ... FROM chunks WHERE model = ?` without LIMIT, loading 323,249 rows × 5.7 GB combined text+embedding bytes when the keyword-search fallback fires.

A third suspect from the initial research (`task_runs` loader) is misattributed: `task_runs` does not exist in `main.sqlite`. It lives in a separate sqlite db. Not relevant here.

## Binary under investigation

- OpenClaw `b2f401f` on `cc-mini/chat-completions-upstream-20260423`
- Worktree: `/Users/lesa/wipcomputerinc/repos/third-party-repos/ai-harness/openclaw/.worktrees/openclaw--upstream-main-20260423/`
- Released as `openclaw@2026.4.23`, binary at `/opt/homebrew/bin/openclaw` symlinked to that worktree's `openclaw.mjs`.

R2.A patches should base on this worktree HEAD (or later upstream with carry-forward).

## Stack signature (gateway.err.log)

```
FATAL ERROR: Reached heap limit Allocation failed ... JavaScript heap out of memory
... StatementSync::All ...
```

Driver: Node built-in `node:sqlite` (`DatabaseSync` / `StatementSync` / `.all()` / `.iterate()` / `.get()`).

## Database snapshot

File: `/Users/lesa/.openclaw/memory/main.sqlite` (17,093,337,088 bytes = **15.92 GB**)

Tables (verified via `PRAGMA`):

```
chunks
chunks_fts, chunks_fts_*            (FTS5 virtual tables)
chunks_vec, chunks_vec_*            (vector search virtual tables)
embedding_cache
files
meta
sqlite_sequence
```

**`task_runs` does not exist here.** The Explore agent's Suspect C was misattributed and is dropped from this artifact.

Verified row counts and sizes (read-only `sqlite3` queries against the live DB):

```
embedding_cache:  435,136 rows, SUM(LENGTH(embedding)) = 8,680,106,189 bytes ≈ 8.68 GB
chunks:           323,249 rows, SUM(LENGTH(text)) =     444,692,986 bytes ≈ 424 MB
                                SUM(LENGTH(embedding)) = 5,296,613,383 bytes ≈ 5.30 GB
```

`chunks` materialized as a full result set is **~5.7 GB of string payload** (text + embedding), far exceeding V8's ~4 GB heap cap on its own.

## Suspect A: `seedEmbeddingCache` ... PRIMARY OOM PATH

**File:** `extensions/memory-core/src/memory/manager-sync-ops.ts:214-220` (approx; verify exact lines against `b2f401f`)
**Function:** `seedEmbeddingCache(sourceDb: DatabaseSync): void`

Query (no LIMIT, no WHERE, no ORDER BY):

```sql
SELECT provider, model, provider_key, hash, embedding, dims, updated_at
FROM embedding_cache
```

Schema (verified):

```sql
CREATE TABLE embedding_cache (
  provider      TEXT NOT NULL,
  model         TEXT NOT NULL,
  provider_key  TEXT NOT NULL,
  hash          TEXT NOT NULL,
  embedding     TEXT NOT NULL,   -- large; 8.68 GB total
  dims          INTEGER,
  updated_at    INTEGER NOT NULL,
  PRIMARY KEY (provider, model, provider_key, hash)
);
```

**Row size:** 8.68 GB / 435,136 rows = **~19.96 KB/embedding average**. V8 strings are UTF-16, so in-heap size is ~2x. Materializing all 435K rows into a JS array alone consumes **~17 GB** of V8 heap before any downstream processing. This single call is the dominant OOM vector.

**Category:** memory recall (eager cache seed at init/warm).

**Proposed bounded-read patch (Suspect A):**

Two options, listed by preference.

*Preferred:* lazy, LRU-bounded cache. Do not pre-seed. Load individual cache entries on demand when `manager-search` or `manager-embed` needs them. Back the cache with `Map` + LRU eviction at a fixed size (e.g. 10K entries, bounded ~200 MB).

```ts
// Pseudocode, manager-embedding-cache.ts
class EmbeddingCache {
  private lru = new LRUMap<string, { embedding: string; dims: number }>(10_000);
  get(provider, model, providerKey, hash) {
    const key = `${provider}:${model}:${providerKey}:${hash}`;
    const hit = this.lru.get(key);
    if (hit) return hit;
    // sourceDb read ONE row
    const row = this.sourceDb.prepare(`
      SELECT embedding, dims FROM embedding_cache
      WHERE provider = ? AND model = ? AND provider_key = ? AND hash = ?
    `).get(provider, model, providerKey, hash);
    if (row) this.lru.set(key, row);
    return row ?? null;
  }
}
```

*Fallback if eager seed is required:* page via `.iterate()` in batches with awaited yields to the event loop.

```ts
function seedEmbeddingCache(sourceDb, cache, maxRows = 50_000) {
  const iter = sourceDb.prepare(`
    SELECT provider, model, provider_key, hash, embedding, dims
    FROM embedding_cache
    ORDER BY updated_at DESC
    LIMIT ?
  `).iterate(maxRows);
  let n = 0;
  for (const row of iter) {
    cache.set(row.provider + ':' + row.model + ':' + row.provider_key + ':' + row.hash, row);
    n++;
  }
}
```

Either keeps in-flight V8 memory well under 500 MB.

## Suspect B: `listChunks` ... SECONDARY OOM PATH

**File:** `extensions/memory-core/src/memory/manager-search.ts:246-252` (approx; verify against `b2f401f`)
**Function:** `listChunks(params: { db, providerModel, sourceFilter })`

Query:

```sql
SELECT id, path, start_line, end_line, text, embedding, source
FROM chunks
WHERE model = ? <optional sourceFilter.sql>
```

**No LIMIT.** Full 323K rows materialized if the filter is broad.

Schema (verified):

```sql
CREATE TABLE chunks (
  id          TEXT PRIMARY KEY,
  path        TEXT NOT NULL,
  source      TEXT NOT NULL DEFAULT 'memory',
  start_line  INTEGER NOT NULL,
  end_line    INTEGER NOT NULL,
  hash        TEXT NOT NULL,
  model       TEXT NOT NULL,
  text        TEXT NOT NULL,   -- ~1.4 KB avg, 424 MB total
  embedding   TEXT NOT NULL,   -- ~16 KB avg, 5.30 GB total
  updated_at  INTEGER NOT NULL
);
```

**Called from:** `manager-search.ts` keyword-search fallback when the vector index returns too few candidates.

**Category:** memory recall (fallback scan).

**Proposed bounded-read patch (Suspect B):**

Two options.

*Preferred:* add explicit `LIMIT` parameter at call sites and stream via `.iterate()` with early termination.

```ts
function listChunks(params: { db, providerModel, sourceFilter, limit = 5_000 }) {
  const iter = params.db.prepare(`
    SELECT id, path, start_line, end_line, text, embedding, source
    FROM chunks
    WHERE model = ? ${params.sourceFilter.sql}
    LIMIT ?
  `).iterate(params.providerModel, ...params.sourceFilter.params, params.limit);
  const out = [];
  for (const row of iter) out.push(mapRow(row));
  return out;
}
```

*Complementary:* defer the `embedding` column to a separate lookup. Most callers of `listChunks` only need `text` for keyword ranking. The embedding column is ~16 KB/row vs ~1.4 KB for text; dropping it shrinks the result set to ~1/12 the size.

```ts
// Default query: no embedding column. Callers that need it fetch separately by id.
SELECT id, path, start_line, end_line, text, source FROM chunks WHERE model = ? LIMIT ?
```

## R2.A implementation hint

Patching in the order A → B is correct. Suspect A is the init-time OOM; until it's fixed, the gateway may not live long enough to execute the search path that hits Suspect B. After A lands, Suspect B becomes the dominant OOM if a user triggers keyword-search fallback.

Also add (per v2 plan R2.B): slow-query logging wrapping SQLite calls; WARN on duration > 500 ms or row count > 10K. That instruments the next surprise.

## Stack trace correlation

The OOM stack lives inside `StatementSync::All` → `ExtractRowValues` → `NewStringFromUtf8`. That's V8 allocating the next string in the result set. Given:

- 8.68 GB of `embedding_cache` text (~17 GB in UTF-16 V8 heap alone)
- 5.70 GB of combined `chunks` text + embedding bytes
- ~4 GB default V8 heap cap

The crash almost certainly fires during `seedEmbeddingCache` eager seed on warm path. Confirm via `heap.log` if `--heap-prof` is available, or by instrumenting the call with `logger.info('seedEmbeddingCache start/end', { rows, bytes })`.

## Out of scope for R1.D

- No code changes (research artifact only).
- No running of `openclaw doctor --fix` or any destructive verb.
- No modification of `main.sqlite` itself.
- Memory Crystal (`crystal.db`, `better-sqlite3`, ~1.84 GB) is a different system; not relevant here. Conflating the two is the main failure mode of this investigation.
- The orphan `main.sqlite.tmp-*` files (71 of them) are correlated with this crash path (a crash during `.all()` likely leaves a vacuum/backup/tx temp in flight). R1.G tmp archive is now unblocked by this artifact since tmps are not load-bearing forensic evidence beyond what this doc captures.

## Cross-references

- v2 plan: `ai/product/bugs/memory-crystal/2026-04-24--cc-mini--unified-reliability-triage.md`
- Forensic snapshot: `/Users/lesa/.openclaw/_snapshots/2026-04-24-forensic/` (launchctl + logs + build/ref provenance)
- Triage R1 execution order: same v2 plan, §"v2 R1 execution order (forensic-first)"
- OpenClaw worktree: `/Users/lesa/wipcomputerinc/repos/third-party-repos/ai-harness/openclaw/.worktrees/openclaw--upstream-main-20260423/` at `b2f401f`
- Source lines (verify against `b2f401f`, linked via `git blame` in the worktree):
  - `extensions/memory-core/src/memory/manager-sync-ops.ts` ... `seedEmbeddingCache`
  - `extensions/memory-core/src/memory/manager-search.ts` ... `listChunks`
  - `extensions/memory-core/src/memory/manager-embedding-cache.ts` ... cache data structure

## Acceptance

- [x] Call site(s) named
- [x] Schema + row counts verified against live DB
- [x] Proposed bounded-read strategies per suspect
- [x] Category per suspect
- [x] Stack trace correlated
- [x] Suspect C from initial research dropped (misattributed)
- [ ] R2.A uses this as the patch spec
- [ ] R1.G tmp archive proceeds (this artifact unblocks)

## Pagination strategy: keyset, not OFFSET

With 300-400K rows, `OFFSET N LIMIT M` is not O(M). SQLite scans the first N rows, discards them, and returns the next M. At N=300,000 that can dominate query time even on SSD. **Use keyset (seek) pagination** for any paged read over these tables. One query per page; each page is O(log n) index lookup + O(M) sequential read.

### `chunks` table

Primary key is `id TEXT` (no auto-increment integer). Format of `id` is worth confirming (e.g. ULID / UUID v7 would sort lexicographically by creation time; random UUID v4 would not).

```sql
-- If id is monotonic-ish: keyset over id
SELECT id, path, start_line, end_line, text, source
FROM chunks
WHERE model = ? AND id > ?
ORDER BY id
LIMIT 1000;

-- If id is not monotonic: fall back to sqlite's internal rowid
SELECT rowid, id, path, start_line, end_line, text, source
FROM chunks
WHERE model = ? AND rowid > ?
ORDER BY rowid
LIMIT 1000;
```

### `embedding_cache` table

Composite primary key `(provider, model, provider_key, hash)`. No single monotonic column. Three options, preference order:

```sql
-- Option 1: use sqlite internal rowid (always present unless table is WITHOUT ROWID)
SELECT rowid, provider, model, provider_key, hash, embedding, dims
FROM embedding_cache
WHERE rowid > ?
ORDER BY rowid
LIMIT 1000;

-- Option 2: row-value keyset on the composite PK (standard SQL; sqlite supports it)
SELECT provider, model, provider_key, hash, embedding, dims
FROM embedding_cache
WHERE (provider, model, provider_key, hash) > (?, ?, ?, ?)
ORDER BY provider, model, provider_key, hash
LIMIT 1000;

-- Option 3: add a monotonic `cached_at_id INTEGER PRIMARY KEY AUTOINCREMENT` column via migration;
-- makes keyset trivial going forward. Requires ALTER TABLE + backfill + index; larger change.
```

First, verify the embedding_cache table has `WITHOUT ROWID` or not:
```sql
SELECT sql FROM sqlite_master WHERE name = 'embedding_cache';
```
If the result includes `WITHOUT ROWID`, Option 1 is unavailable; use Option 2 or 3.

### Why this matters for `seedEmbeddingCache`

If R2.A picks the eager-seed-but-paginated fallback (not the lazy-LRU preferred path), keyset pagination is the difference between minutes and milliseconds per page. With a lazy-LRU cache (preferred), keyset pagination is only needed for any "warm recent entries" preload; that preload should ORDER BY updated_at DESC + LIMIT N and does not need pagination at all.

### Why this matters for `listChunks`

Keyword-search fallback currently loads everything matching `model = ?` into memory. The replacement should page through in keyset order (above) and terminate as soon as the ranker has enough candidates. Early termination + keyset = no OOM + fast search.

### Do NOT use `OFFSET` in any R2.A patch

Even `OFFSET 10000 LIMIT 1000` on these tables can be slow enough to be a regression. Use keyset only.
