# remember() pre-chunks inputs + durable skip-cursor on workspace sync + scoped-op hardening

## Summary

Three changes, all landing together because they share a single branch and address the runtime-stability tier of the 2026-04-24 Lēsa reliability triage (Parker + Codex + Claude Code). Tracked at `wip-ldm-os-private/ai/product/bugs/memory-crystal/2026-04-24--cc-mini--unified-reliability-triage.md` (R1.B, R1.C, v2 plan).

### 1. `remember()` pre-chunks inputs before embedding (T1)

`src/core.ts` `Crystal.remember(text, category)` previously passed the entire text as a single chunk to `this.ingest([...])`, which embeds it in one request. The OpenAI `text-embedding-3-small` provider has a hard 8192-token cap per input. When OpenClaw's memory-crystal plugin called `remember()` on whole workspace `.md` files (`MEMORY-v1-backup-2026-02-16.md`, `TODO-from-history.md`, `lesa-full-history.md`, etc.), every call above ~32 KB failed with HTTP 400 `maximum input length is 8192 tokens.`. These errors fired on every `agent_end` hook, flooding `gateway.err.log` with 3-6 entries per 15-minute healthcheck window all day.

Fix: `remember()` now calls `this.chunkText(text, 400, 80)` before ingest. Single-chunk memories keep `source_id = memory:{id}` (backwards compatible). Multi-chunk memories use `source_id = memory:{id}:{i}`. The `memories` row is still one-per-fact; only the `chunks` table grows to multiple rows per memory. `forget(id)` operates on the `memories` row and is unchanged.

`token_count` reflects the chunk text's length, not the original memory text's.

### 2. Durable skip-cursor on workspace sync (N1)

`src/openclaw.ts` `syncWorkspaceMemory()` previously used a `Record<string, number>` watermark where the value was the last-seen mtime. On ingest failure, the watermark was not updated, so the same file retried on every `agent_end`. That's the "firehose" symptom.

New watermark entry shape:

```ts
interface WatermarkEntry {
  mtime: number;
  hash?: string;              // sha256(content).slice(0,16)
  failedKind?: 'permanent' | 'transient';
  failedAt?: number;
  ingestVersion?: number;
}
```

Skip logic (`shouldSkipFile`):

- Legacy `number` watermarks behave as before (skip if mtime unchanged).
- New-format success entries skip when mtime unchanged.
- Permanent failures (embedding-too-large / auth / unauthorized) on unchanged content are skipped until either the content changes (different hash) or the `ingestVersion` constant bumps.
- Transient failures back off for 1 hour.

`WATERMARK_INGEST_VERSION = 2` is set for this release. Bumping this constant forces a one-time retry of previously-failed files, which matters when new ingest logic (like T1 chunking) would change the outcome.

`saveWatermarks()` now runs on every cycle (was gated on `ingested > 0`), so failure state persists across restarts.

### 3. Scoped-op hardening in `opRead()` (R1.C)

`src/core.ts` `opRead()` previously invoked bare `op` via `execSync`, relying on the child process inheriting `PATH` correctly. For hook processes spawned outside a login shell, `op` could be unresolvable, causing `opRead` to return undefined even when the SA token file was present and valid.

Fix: `opRead` now resolves an absolute path from a small fallback list (`/opt/homebrew/bin/op`, `/usr/local/bin/op`, `/usr/bin/op`) and uses it in the `execSync` command. Falls back to bare `op` only if none of the standard paths exist. The SA token remains scoped to the `op` child process via `env: { ..., OP_SERVICE_ACCOUNT_TOKEN: saToken }`; it is never set on `process.env` and never leaked to the shell profile. This completes the scoped-hook pattern described in the v2 triage plan, replacing the earlier-proposed (and now withdrawn) global `.zshrc` export approach.

## Why these ship together

All three address runtime stability on the same cycle:

- T1 stops the embedding firehose at the source.
- N1 stops the retry loop even if a new failure mode appears.
- R1.C makes sure the fail-fast scoped-hook path added in the previous release (commit `e2501ce "Fail-fast on missing LLM provider in cc-hook and cc-poller"`) actually reaches `op` when PATH is hostile.

## What did NOT change

- `crystal.db` schema: unchanged.
- `memories` table: unchanged (still one row per `remember()` call).
- `forget()`, `search()`, `status()`: unchanged.
- `cc-hook.ts` and `cc-poller.ts` retry loops: unchanged (already landed `isPermanentError` in `e2501ce`).
- Chunk-size tuning: `chunkText(text, 400, 80)` matches the existing `syncCollection` convention at `core.ts:1322`. Raising chunk size (e.g. 1000-2000 tokens) to reduce per-memory fragmentation is a reasonable follow-up but out of scope for R1.

## Data migration

None. New watermark format is introduced alongside legacy support. Existing `workspace-memory-watermarks.json` files with raw `{path: mtimeMs}` entries continue to work via the `typeof entry === 'number'` branch in `shouldSkipFile`. New failures and successes write the richer shape. No one-shot migration required.

## Acceptance (per R1.B+C verify checklist)

- [x] Build passes (`npm run build`).
- [x] 50 KB `remember(text)` produces multi-chunk ingest without throwing on the 8192-token cap.
- [x] Previously-failed oversized workspace file retries on first cycle after `ingestVersion` bump, then succeeds (because of T1 chunking).
- [x] Same unchanged failing file does not retry every cycle (the firehose bug fix).
- [x] Transient classification uses 1-hour backoff, not permanent-skip.
- [x] Hook with no token exits fast via the already-landed `isPermanentError` path in `cc-hook.ts` / `cc-poller.ts`.
- [x] Hook with token invokes `op` via absolute path, with token scoped to the child process env only.

## Related

- Triage plan (v2): `wip-ldm-os-private/ai/product/bugs/memory-crystal/2026-04-24--cc-mini--unified-reliability-triage.md`
- OOM forensic artifact (adjacent but separate work): `wip-ldm-os-private/ai/product/bugs/openclaw/2026-04-24--cc-mini--main-sqlite-oom-artifact.md`
- Previously-landed fail-fast companion: commit `e2501ce "Fail-fast on missing LLM provider in cc-hook and cc-poller"`
