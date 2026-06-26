# Dev Update: Orphan Cleanup, DELETE Trigger, Doctor Fix

**Date:** 2026-03-13
**Author:** CC-Mini
**Session:** memory-db-fix

---

## What Happened

Parker ran the Memory Crystal install prompt and `crystal doctor` reported "Embeddings: FAILING ... no provider configured in env." Investigation revealed two separate issues:

### Issue 1: Doctor False Positive

`checkEmbeddingProvider()` in `doctor.ts` only checked `process.env.OPENAI_API_KEY`. But the cron job and hooks resolve the key from 1Password via the SA token at `~/.openclaw/secrets/op-sa-token`. The doctor didn't know about this path.

**Fix:** Added `checkOpEmbeddings()` helper to `doctor.ts` that checks for the SA token file, then does a live `op read` to verify it works. Doctor now reports `ok: openai (via 1Password)` instead of `fail`.

### Issue 2: Orphaned Vectors and FTS Entries

On 2026-03-11, 141,652 bulk file-scan chunks were correctly deleted from the `chunks` table. Parker said: "Why are we indexing documents?" These were raw file scans (Python venv packages, TypeScript source, vendor code) with no conversational context.

The deletion used raw SQL (`DELETE FROM chunks WHERE agent_id = 'system'`). But Memory Crystal had no DELETE trigger. The corresponding entries in `chunks_vec` (sqlite-vec) and `chunks_fts` (FTS5) were left orphaned.

**Impact:**
- 141,651 orphaned vectors (~875 MB)
- 141,652 orphaned FTS entries
- ~7% of search queries hit phantom results (silently filtered out)
- Database: 1.96 GB (should have been ~1 GB)

**Fix (three parts):**

1. **DELETE trigger** added to `initChunksTables()` in `core.ts`:
```sql
CREATE TRIGGER IF NOT EXISTS chunks_cleanup AFTER DELETE ON chunks
BEGIN
  DELETE FROM chunks_vec WHERE chunk_id = OLD.id;
  INSERT INTO chunks_fts(chunks_fts, rowid, text) VALUES('delete', OLD.id, OLD.text);
END;
```

2. **`cleanOrphans()` method** added to Crystal class in `core.ts`. Counts orphaned vec/FTS entries, deletes vec orphans in batches of 1000, rebuilds FTS5 from scratch.

3. **`crystal cleanup` CLI command** added to `cli.ts`. Handles the full workflow: backup, pause cron, clean orphans, VACUUM, resume cron. Supports `--dry-run`.

**Cleanup results:**
- 141,651 orphaned vectors removed
- FTS rebuilt from 73,813 chunks in 5.7s
- Database: 1.96 GB -> 1.45 GB (525 MB saved)
- Verification: chunks = FTS entries = 73,813. Match: YES
- Zero orphans remaining

### Side Discovery: Plaintext SA Token

During investigation, discovered that `~/.openclaw/secrets/op-sa-token` is a plaintext 1Password SA token readable by any process running as `lesa`. This is the bootstrap credential that unlocks all secrets. Bug report filed. Long-term fix: Lesa iOS app with remote biometrics (product doc written).

### Product Rule Established

Memory Crystal indexes conversations only. File content that appears in conversation turns (agent reads a file, discusses it) is captured as part of the conversation. Raw directory scanning without conversational context is not what Memory Crystal is for.

## Files Changed

| File | Change |
|------|--------|
| `src/core.ts` | Added `chunks_cleanup` DELETE trigger, `cleanOrphans()` method |
| `src/cli.ts` | Added `crystal cleanup` command, updated imports and USAGE |
| `src/doctor.ts` | Added `checkOpEmbeddings()` for 1Password detection |
| `ai/product/bugs/2026-03-13--orphaned-vectors-and-fts-after-bulk-delete.md` | Bug report |

## Related (wip-secrets-ios-private)

| File | What |
|------|------|
| `ai/product/product-ideas/lesa-app-remote-biometrics.md` | Lesa app: remote biometrics for agent computers |
| `ai/product/bugs/2026-03-13--plaintext-sa-token-on-disk.md` | Plaintext SA token bug report |

## Status

- Code deployed and running (cleanup already executed)
- Not yet committed / PR'd / released
- Needs: branch, commit, PR, merge, `wip-release patch`
