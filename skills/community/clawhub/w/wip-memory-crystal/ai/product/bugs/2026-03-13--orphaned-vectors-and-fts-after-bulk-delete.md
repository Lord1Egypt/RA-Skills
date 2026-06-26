# Bug: Orphaned Vectors and FTS Entries After Bulk Chunk Deletion

**Date:** 2026-03-13
**Severity:** Medium (no data loss, but 875 MB wasted space + ~7% search inefficiency)
**Status:** Open (fix ready, needs review)
**Found by:** CC-Mini + Parker
**Affects:** Memory Crystal v0.7.4 (installed), crystal.db

---

## Summary

On 2026-03-11, a CC session deleted 141,652 chunks from the `chunks` table using raw SQL (`DELETE FROM chunks WHERE agent_id = 'system'`). These were bulk file-scan chunks (Python venv packages, TypeScript source, vendor code) that Parker decided should not be in Memory Crystal. The deletion was correct.

However, the corresponding entries in `chunks_vec` (sqlite-vec vectors) and `chunks_fts` (FTS5 full-text index) were NOT cleaned up. Memory Crystal has no DELETE trigger and no cleanup function. The CC session used raw SQL because no proper delete command exists.

## Current State

| Table | Rows | Should Be | Orphaned | Wasted |
|-------|------|-----------|----------|--------|
| `chunks` | 73,730 | 73,730 | 0 | 0 |
| `chunks_vec` (virtual) | 215,381 | 73,730 | 141,651 (65.8%) | ~875 MB |
| `chunks_fts` | 215,382 | 73,730 | 141,652 (65.8%) | ~50 MB |
| `memories` | 336 | 336 | 0 | 0 |

Database size: 2.0 GB. After cleanup: ~1.1 GB.

## Impact

- **No data loss.** All 73,730 conversation chunks are intact with working vectors.
- **Search works correctly.** Both FTS5 and vector search return valid results.
- **~7% search inefficiency.** Vector search hits orphaned chunk_ids that no longer exist. The two-step lookup in `searchVec()` (line 799 of core.ts) silently filters these out, but it wastes I/O and reduces the effective candidate pool. The code mitigates this by fetching 5x more results than needed (`fetchLimit = Math.max(limit * 5, 50)`).
- **875 MB wasted disk space.** The orphaned vectors are the bulk of it.
- **FTS5 BM25 scoring is slightly skewed.** Document frequency calculations include the orphaned entries, which could affect ranking. Negligible in practice.

## Root Cause

Memory Crystal has no mechanism for cascading deletes. When chunks are removed from the `chunks` table:

1. The FTS5 trigger (`chunks_fts_insert`) only fires on INSERT. There is no corresponding DELETE trigger.
2. sqlite-vec (`chunks_vec`) has no trigger at all. Inserts are done explicitly in the ingest transaction.
3. The codebase has no `deleteChunks()` function, no `cleanOrphans()` function, and no `crystal cleanup` CLI command.

The only way to remove chunks today is raw SQL, which leaves orphans.

## How to Reproduce

```sql
-- Insert a chunk (triggers FTS5 insert, explicit vec insert)
INSERT INTO chunks (text, text_hash, role, source_type, source_id, agent_id, token_count, created_at)
VALUES ('test', 'abc123', 'user', 'conversation', 'test', 'test', 10, datetime('now'));

-- Delete it (FTS5 and vec entries remain)
DELETE FROM chunks WHERE text = 'test';

-- Verify orphans exist
SELECT COUNT(*) FROM chunks_fts WHERE chunks_fts MATCH 'test';  -- returns 1
```

## Fix

### Part 1: Cleanup Script (one-time, run against live database)

Back up the database first, then:

```sql
-- 1. Remove orphaned vec entries
DELETE FROM chunks_vec WHERE chunk_id NOT IN (SELECT id FROM chunks);

-- 2. Rebuild FTS5 index (removes orphaned entries and recalculates)
INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild');

-- 3. Reclaim disk space
VACUUM;
```

Note: The vec DELETE requires the sqlite-vec extension to be loaded. Run this through the Memory Crystal node runtime, not raw sqlite3 CLI.

### Part 2: Add DELETE Trigger (code change in core.ts)

Add to the `initSqlite()` method, after the existing INSERT trigger:

```sql
CREATE TRIGGER IF NOT EXISTS chunks_cleanup_vec AFTER DELETE ON chunks
BEGIN
  DELETE FROM chunks_vec WHERE chunk_id = OLD.id;
  INSERT INTO chunks_fts(chunks_fts, rowid, text) VALUES('delete', OLD.id, OLD.text);
END;
```

This ensures that any future DELETE on `chunks` automatically cleans up both vec and FTS.

### Part 3: Add `crystal cleanup` CLI command

A proper cleanup command that:
1. Backs up the database
2. Counts orphaned entries
3. Deletes orphaned vec entries
4. Rebuilds FTS5
5. VACUUMs
6. Reports before/after sizes

### Part 4: Product Rule

Memory Crystal indexes conversations only. File content that appears in conversation turns (agent reads a file during conversation) is captured as part of the conversation. Raw directory scanning (`crystal_sources_add`, `crystal_sources_sync`) should be removed or clearly marked as an advanced/optional feature that most users should not enable.

## Timeline

- **2026-02-06:** First 211 chunks ingested (system setup + first conversations)
- **2026-02-10:** Phase 1 complete. LanceDB + SQLite dual-write architecture.
- **2026-02-16 to 2026-03-11:** File indexing runs, accumulating 141,652 "system" chunks from directory scans
- **2026-03-11 07:40 PDT:** Parker says "Why are we indexing documents?" CC session deletes system chunks via raw SQL
- **2026-03-13:** Orphaned vectors and FTS entries discovered during investigation

## Related

- `ai/product/notes/memory-analysis.md` (data location map)
- Doctor false-positive bug: `src/doctor.ts` `checkEmbeddingProvider()` only checks `process.env.OPENAI_API_KEY`, doesn't know about 1Password resolution path. Fix already applied (added `checkOpEmbeddings()` helper).
- sqlite-vec version: `0.1.7-alpha.2`. Consider upgrading to latest alpha.
