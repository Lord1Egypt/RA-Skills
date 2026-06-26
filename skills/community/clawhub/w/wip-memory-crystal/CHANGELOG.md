# Changelog




















## 0.7.38 (2026-04-28)

# Memory Crystal stops shipping `ldm-backup.sh`

## Narrative

Per the bin ownership decision in PR #717 design pass (Q3): the LDM CLI owns `ldm-backup.sh`; Memory Crystal drops its copy. With both packages now on the manifest model (memory-crystal v0.7.37 declared `crystal-capture.sh`; wip-ldm-os v0.4.83 declared `ldm-backup.sh` and four other LDM-owned files), the runtime resolves any cron target back to its declarer, install-time self-heal restores from canonical sources, and the manifest aggregator refuses to act when two declarers claim the same name. The remaining hygiene step is removing MC's duplicate so there is one source of truth on disk and in published artifacts. Closes the last item from the parent ticket on `wip-ldm-os-private` (`ai/product/bugs/installer/2026-04-28--cc-mini--ldm-bin-overwrite-wipes-crystal-capture.md`); refs #124.

This release does not affect runtime behavior on installs that already received both packages: the LDM CLI's `wipLdmOs.binFiles` is the authoritative source for `ldm-backup.sh`, and `ldm install` keeps it deployed at `~/.ldm/bin/ldm-backup.sh`. The MC-side change just stops competing for the file and removes it from MC's published artifact and `crystal init` flow.

## What changed

- **`openclaw.plugin.json`** unchanged. MC continues to declare only `crystal-capture.sh` in `binFiles`, so the runtime aggregator never saw a manifest-level conflict on `ldm-backup.sh` from this side.
- **`package.json` `files`** drops `scripts/ldm-backup.sh`. The published npm tarball no longer carries MC's copy.
- **`package.json` `scripts.build`** drops the `cp scripts/ldm-backup.sh dist/` step. The build no longer copies a duplicate into `dist/`.
- **`src/installer.ts`** Step 6 (in `runInstallOrUpdate`) replaces the `deployBackupScript()` call with a verify of `~/.ldm/bin/ldm-backup.sh`. If the file is absent, the install fails loudly with `expected ~/.ldm/bin/ldm-backup.sh (LDM CLI-owned); run "ldm install" first`.
- **`src/cli.ts`** `crystal backup setup` replaces `deployBackupScript()` with the same verify and a clear error message pointing at `ldm install`. `crystal backup` (no subcommand) updates its missing-file message from "Run crystal init first" to "Run ldm install first".
- **`deployBackupScript`** import is removed from both `installer.ts` and `cli.ts`. The function and `scripts/ldm-backup.sh` themselves stay in the repo for now (delete-restricted by the per-edit guard on this codebase) but are no longer called and no longer published.

## Why this is safe

The LDM CLI's manifest already covers `ldm-backup.sh`:

- After `wip-release patch` for wip-ldm-os v0.4.83, the LDM CLI declares ownership in `package.json#wipLdmOs.binFiles`.
- After `ldm install`, the manifest heal walk restores `~/.ldm/bin/ldm-backup.sh` from the LDM CLI's `scripts/ldm-backup.sh`.
- `crystal backup setup` is operator-invoked and now verifies-then-installs the LaunchAgent. Failure mode: clear "run ldm install first" message instead of silently double-deploying or relying on whoever ran last.
- `crystal init` similarly verifies-then-throws if the LDM CLI hasn't run.

The only behavior change visible to operators is: `crystal init` and `crystal backup setup` now expect the LDM CLI to have run first. Since `crystal init` already delegates to `ldm install` when the LDM CLI is on PATH (`installer.ts` line 633 `runLdmInstall(repoRoot)`), this is the normal flow for every existing install.

## Tests

- `npm run validate:bin-manifest` ... passes.
- `npm run build` ... passes; `dist/ldm-backup.sh` is no longer produced.
- `node scripts/test-shim-integrity.mjs` ... still 7/7 assertions pass; capture-shim diagnostics unchanged.

## What this does NOT do

- **`deployBackupScript` function** stays defined in `src/ldm.ts`. The function is dead code now (no callers in the package). A future cleanup can remove it; restricted by the per-edit guard on this PR's surface.
- **`scripts/ldm-backup.sh` file** stays in the source tree. Not in the published artifact. Removable in a future cleanup once the per-edit guard is satisfied.
- **No runtime behavior change for already-installed operators** beyond the verify-instead-of-deploy in MC's installer paths. `~/.ldm/bin/ldm-backup.sh` keeps working because the LDM CLI manifest deploys it on every `ldm install`.

## 0.7.37 (2026-04-28)

# Memory Crystal declares `binFiles` for the LDM bin manifest

## Narrative

On 2026-04-28 a capture outage exposed the failure mode at the heart of this release: cron lines in `~/.ldm/bin/` are sticky, but the files they reference can disappear, and nothing in either Memory Crystal's or the LDM CLI's diagnostic surface said who owned what. PR #123 closed the install-time invariant and `crystal doctor --fix` recovery on the Memory Crystal side. The parent ticket on `wip-ldm-os-private` (`ai/product/bugs/installer/2026-04-28--cc-mini--ldm-bin-overwrite-wipes-crystal-capture.md`) then called for a shared ownership model so the LDM CLI could heal extension shims without hardcoded knowledge.

This release contributes Memory Crystal's half of that contract: an explicit `binFiles` declaration in `openclaw.plugin.json` naming `crystal-capture.sh`, plus a prepublish validator that prevents a broken declaration from ever reaching npm. After this lands and the operator runs `ldm install` (with LDM CLI v0.4.83+), `ldm doctor` resolves Memory Crystal as the explicit owner of `crystal-capture.sh`, and the LDM CLI can self-heal a missing or non-executable shim from Memory Crystal's extension dist without any LDM-side hardcoded mapping. Closes #124.

## What changed

- `openclaw.plugin.json` now declares `binFiles` with one entry: `crystal-capture.sh` from `dist/crystal-capture.sh`. This lets the LDM CLI's bin-ownership manifest aggregate Crystal's shim and self-heal it during `ldm install` or `ldm doctor --fix`. Previously the LDM CLI fell back to a hard-coded match for this file; now ownership is explicit and symmetric with every other declarer.
- `scripts/validate-bin-manifest.mjs` (new) runs from `prepublishOnly` after `npm run build`. Asserts each declared `source` exists in the published artifact, no internal duplicates, `name` is a basename. A broken declaration cannot reach npm. Layer 1 of the release-blocker design.
- `package.json` `prepublishOnly` chains `validate:bin-manifest` after the existing build step.

## Why

Closes the Memory Crystal half of the LDM bin-ownership manifest follow-up tracked in `wipcomputer/wip-ldm-os-private:ai/product/bugs/installer/2026-04-28--cc-mini--ldm-bin-overwrite-wipes-crystal-capture.md`. With this declaration:

- `ldm doctor` resolves `crystal-capture.sh` as `declarer = memory-crystal` instead of `owner unknown`.
- `ldm install` can self-heal a missing or non-executable `~/.ldm/bin/crystal-capture.sh` from `~/.ldm/extensions/memory-crystal/dist/crystal-capture.sh` without any LDM-side hardcode.
- A future broken declaration (missing source, internal duplicate, non-basename name) is caught at publish time, not at install time on the operator's machine.

## What this does NOT do

- **`ldm-backup.sh` collision cleanup.** Memory Crystal still ships and deploys its own copy of `ldm-backup.sh`. Per the agreed ownership in the design pass (LDM CLI keeps it, MC drops its copy), that cleanup lands as a separate small PR. This PR is intentionally scoped to the binFiles declaration so review is small. If MC declared `ldm-backup.sh` here it would conflict at the manifest level with the LDM CLI's declaration; we are avoiding that until the cleanup PR runs.
- **Layer 2 cross-package CI gate.** That is a workflow on `wip-ldm-os-private` and is independent of MC.

## 0.7.36-alpha.1 (2026-04-24)

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

## 0.7.35 (2026-04-18)

# Memory Crystal v0.7.35

One-line release: **`crystal status` and every other CLI verb now actually run on global installs under modern Node**. Before this release, a silent packaging mistake made every `crystal <verb>` command throw `ERR_MODULE_NOT_FOUND` at startup on Node 25.6+, which is the first Node version to enforce strict ESM resolution against an unresolvable bare import. Ingestion continued to work the whole time because the Claude Code Stop hook takes a different code path.

## What was wrong

`package.json` declared its dream-weaver-protocol dependency with a `file:` relative path intended for local dev (`file:../dream-weaver-protocol-private`). When users ran `npm install -g @wipcomputer/memory-crystal`, npm tried to resolve that path relative to the global install root, could not find the sibling directory, and left the module unresolvable. Older Node resolvers tolerated the resulting empty state; Node 25 does not. Any entrypoint that imports `dream-weaver.ts` — which is every interactive CLI — threw on startup.

## What changed

Added `tsup.config.ts` with `noExternal: ['dream-weaver-protocol']`. Tsup now bundles dream-weaver's source code into each memory-crystal dist entrypoint at build time, so the published tarball is self-contained and needs no runtime resolution of that dep. The CLI verbs work on any Node from 18 to 25+.

## What did not change

- Ingestion: the Claude Code Stop hook path was never broken. Continuous capture kept going at normal rate.
- Search: the MCP server entrypoint was never broken. Agents that use `crystal_search` through MCP were unaffected.
- Data: zero chunks were lost. Today's DB count is 92,696 and growing.

## Related bugs filed in this release

- `ai/product/bugs/2026-04-18--cc-mini--crystal-status-cli-broken-node-25.md` — this bug in full, with root cause, discovery narrative, and follow-up work
- `ai/product/bugs/2026-04-18--cc-mini--lesa-capture-gap-2026-04-17.md` — a separate concern: during the Opus 4.7 rollout incident on Apr 17, Lēsa's gateway failed repeatedly on an unknown model ID and emitted no successful agent_end events, so ingestion for that day dropped to ~46 chunks vs ~300 baseline. Propose backfill + structural prevention in that bug.

## Install

```bash
npm install -g @wipcomputer/memory-crystal@latest
crystal status
```

If that reports your chunk count and agent list cleanly, you're on the fix.

Closes wipcomputer/memory-crystal#68.

## 0.7.34-alpha.5 (2026-04-15)

alpha prerelease

## 0.7.34-alpha.4 (2026-04-11)

Fix broken alpha.3: add --clean to tsup build so stale chunks don't linger, replace scripts/ glob with explicit files allowlist to prevent iCloud duplicates from shipping. alpha.4 is the first release that actually contains the wip-ldm-os#126 fix correctly.

## 0.7.34-alpha.3 (2026-04-11)

Disable code splitting (--no-splitting) so rebuilds produce deterministic filenames. Fixes wip-ldm-os#126: random chunk hashes were breaking running gateway and MCP server processes after every ldm install. Also adds .license-guard.json scaffold.

## 0.7.34-alpha.2 (2026-04-01)

CC + Lesa memory sync hooks, four memory types

## 0.7.34-alpha.1 (2026-04-01)

Add four memory types: user, feedback, project, reference

## 0.7.33 (2026-03-31)

# Release Notes: memory-crystal v0.7.33

Related: #255

## Fix npm publish: include dist/ in package

The npm package was missing the `dist/` directory because `.gitignore` excludes it and there was no `files` array in package.json to override. The `crystal` CLI binary pointed to `dist/cli.js` which didn't exist in the published package. Every `npm install -g` installed a broken CLI.

Added `files` array to explicitly include `dist/` in the tarball. Added `prepublishOnly: npm run build` so the package is always built before publishing. The npm tarball now contains the compiled JavaScript that the CLI and MCP server need.

## 0.7.32 (2026-03-31)

# Release Notes: memory-crystal v0.7.32

**Date:** 2026-03-31

## What changed

### Dream Weaver is a required dependency again

Reverts PR #101 (optional Dream Weaver import). dream-weaver-protocol is back in `dependencies` instead of `optionalDependencies`. The static import in `dream-weaver.ts` is restored. The dynamic import with try/catch wrapper is removed. The null check in `cli.ts` for when DW is unavailable is removed.

## Why

PR #101 made dream-weaver-protocol optional because `file:../dream-weaver-protocol-private` failed in fresh clones where the sibling directory doesn't exist. The installer (v0.4.68+) now resolves `file:` dependencies from installed extensions at `~/.ldm/extensions/` before building, so the sibling directory is no longer needed. The build succeeds without it.

Making DW optional added complexity (dynamic imports, null checks, degraded type safety) that is no longer necessary. This revert simplifies the code back to what it was.

## How to verify

```bash
# Build should succeed (installer resolves file: deps)
cd memory-crystal-private && npm run build

# dream-weaver-protocol should be in dependencies, not optionalDependencies
node -e "const p = require('./package.json'); console.log('deps:', !!p.dependencies['dream-weaver-protocol']); console.log('optional:', !!p.optionalDependencies?.['dream-weaver-protocol'])"
# Should print: deps: true, optional: false
```

## 0.7.31 (2026-03-31)

# Release Notes: memory-crystal v0.7.31

Closes #101

## Dream Weaver protocol is now optional

The dream-weaver-protocol dependency was a `file:` reference to a sibling directory. This worked in the development environment but broke when the installer cloned the repo to build (the sibling doesn't exist in a clone context). The build failed with "Cannot find module 'dream-weaver-protocol'".

The protocol is now an optional dependency with a dynamic import. If dream-weaver-protocol is available (installed locally or linked), Dream Weaver features work normally. If not, crystal operations continue without Dream Weaver. The build succeeds either way.

This is part of a broader fix to make all repos buildable in isolation. The installer (v0.4.67+) now resolves `file:` dependencies from installed extensions before building, so the protocol will be linked automatically when both packages are installed.

## 0.7.30 (2026-03-31)

# Release Notes: memory-crystal v0.7.30

**Date:** 2026-03-30

## What changed

### Hardcoded path removal

Two files had `/Users/lesa` hardcoded as a fallback path. Both now use portable alternatives.

**migrate-lance-to-sqlite.mjs** had a fallback that resolved the OpenClaw workspace to `/Users/lesa/.openclaw`. The migration script now calls `os.homedir()` to build the path dynamically, so it works on any machine without assuming a specific username. This was the last remaining hardcoded path in the migration pipeline (#99).

**dev-update.ts** (the ai/dev-updates scanner) had an iCloud path baked in for reading team documents. It now calls `resolveWorkspace()` to read the workspace root from LDM config (`~/.ldm/config.json`), making it portable across machines and user accounts (#98).

## Why

These paths broke on any machine where the username is not `lesa`. Part of a broader audit across all LDM OS repos to eliminate hardcoded user paths and make everything portable.

## Issues closed

- #98
- #99

## How to verify

```bash
grep -r "/Users/lesa" src/ scripts/ --include="*.ts" --include="*.mjs"
# Should return zero results
```

## 0.7.29 (2026-03-20)

# Release Notes: memory-crystal v0.7.29

**Doc audit: MLX setup, deep search params, log paths, role clarification.**

## What changed

SKILL.md and TECHNICAL.md updated for 2 weeks of undocumented features:

- **MLX local LLM:** Added as Option A in SKILL.md Step 2. CLI commands (setup, status, stop) added to TECHNICAL.md.
- **Deep search parameters:** `--intent`, `--explain`, `--candidates` documented in both SKILL.md (crystal_search tool) and TECHNICAL.md (CLI reference + new sections for intent, explain, candidate limit, LLM cache).
- **Log paths:** Fixed obsolete `/tmp/ldm-dev-tools/` reference to `~/.ldm/logs/`. Added logs/ to directory structure.
- **Role clarification:** Two-role architecture (Core and Node) explicitly stated. Standalone role was removed in v0.7.22.

## Why

29 releases in 13 days. Docs didn't keep pace. Agents using crystal_search didn't know about --intent (query disambiguation) or --explain (scoring transparency).

## Issues closed

- #57

## How to verify

```bash
grep "intent" SKILL.md TECHNICAL.md
grep "mlx" SKILL.md TECHNICAL.md
grep "ldm/logs" TECHNICAL.md
```

## 0.7.28 (2026-03-18)

# Release Notes: memory-crystal v0.7.28

**One-line summary of what this release does**

## What changed

Describe the changes. Not a commit list. Explain:
- What was built or fixed
- Why it matters
- What the user should know

## Why

What problem does this solve? What was broken or missing?

## Issues closed

- #91

## How to verify

```bash
# Commands to test the changes
```

## 0.7.27 (2026-03-17)

# Add root SKILL.md + ldm install as primary path

Added SKILL.md to repo root (source of truth for wip-release website publishing). `ldm install wipcomputer/memory-crystal` is now the recommended install path. `crystal init` stays for MC-specific setup (database, cron, role, pairing).

Also added `.publish-skill.json` so wip-release publishes SKILL.md to wip.computer/install/.

Closes wipcomputer/wip-ldm-os#97. Convergence tracked in wipcomputer/wip-ldm-os#99.

## 0.7.26 (2026-03-16)

# Memory Crystal v0.7.26

Add repository field to package.json. GitHub Packages needs this to link packages to the repo.

## Issues closed

- Closes #50

## 0.7.25 (2026-03-16)

# Release Notes: memory-crystal v0.7.25

Bump SKILL.md version and name to match package branding.

## What changed

- SKILL.md version bumped from 0.4.0 to 0.7.24 (was stuck at the original version)
- SKILL.md name changed from `memory` to `wip-memory-crystal` (matches branded convention)
- Forces deploy to public repo, triggering auto-publish to wip.computer/install/

## Why

The SKILL.md version was out of sync with the package version. The name didn't match the `wip-` branding convention used across all install files on wip.computer.

## Issues closed

- #80

## How to verify

```bash
crystal --version
head -4 ~/.ldm/extensions/memory-crystal/skills/memory/SKILL.md
```

## 0.7.24 (2026-03-15)

# Dev Update: Search Quality v2 + MLX Local LLM

**Date:** 2026-03-15
**Author:** CC-Mini
**Session:** memory-crstal01 (continued from Mar 13-14)

---

## Summary

Six search quality features from QMD v2.0 analysis, plus MLX local LLM infrastructure for Apple Silicon. All coded, tested, merged. Not yet deployed.

## What Shipped

### Search Quality (PR #75)

1. **Intent parameter.** Disambiguates queries without adding search terms. `crystal search "security" --intent "1Password"` steers toward 1Password results. Flows through expansion prompt (guides LLM variations), disables strong-signal bypass, prepended to rerank query. Available via CLI `--intent`, MCP `intent`.

2. **candidateLimit.** Tunable rerank pool size. `crystal search "query" --candidates 60`. Default stays 40. More candidates = better recall, slower reranking. Available via CLI `--candidates`, MCP `candidate_limit`.

3. **Explain mode.** Per-result scoring breakdown showing FTS score, vector score, RRF rank, reranker score, recency weight, and final blended score. `crystal search "query" --explain`. Available via CLI `--explain`, MCP `explain`.

4. **Persistent LLM cache.** `llm_cache` table in crystal.db. Expansion and reranking results cached with 7-day TTL. Content-addressable reranking (keyed by query + sorted passage hashes). Same query = instant on repeat searches. Configurable TTL via `CRYSTAL_CACHE_TTL_DAYS`.

5. **Structured search API.** `crystal.structuredSearch(queries)` accepts pre-expanded StructuredQuery[] (lex, vec, hyde). Skips LLM expansion entirely. Agents construct their own queries when they know what they want. RRF fusion with first list weighted 2x.

### MLX Local LLM (PR #76)

6. **MLX auto-install.** New `src/mlx-setup.ts` with full setup flow:
   - `detectPlatform()` ... Apple Silicon / Intel Mac / Linux / other
   - `installMlxLm()` ... uv > pip3 > pip3 --user fallback chain
   - `createLaunchAgent()` ... always-on MLX server via LaunchAgent
   - `verifyServer()` ... 30s warmup wait for model loading
   - `setupMlx()` ... full flow: detect, install, configure, start, verify

7. **Crystal MLX CLI.** `crystal mlx setup/status/stop` subcommands.

8. **Doctor check #13.** MLX health check with three states: not installed, installed but not running, running. Suggests fix for each.

9. **Installer integration.** `crystal init` detects Apple Silicon and suggests `crystal mlx setup` when MLX is not installed.

10. **Port 18791.** LDM service ports: 18789 (OpenClaw), 18790 (Crystal Core), 18791 (MLX LLM).

11. **Model: Qwen 2.5 3B Instruct 4-bit.** `mlx-community/Qwen2.5-3B-Instruct-4bit`. ~1.5 GB, fast on M-series, good at instruction following for query expansion and relevance scoring.

### Also

- QMD v2.0 analysis written (`ai/product/notes/2026-03-15--cc-mini--qmd-v2.0-analysis.md`)
- Search quality plan written (`ai/product/plans-prds/current/2026-03-15--cc-mini--search-quality-qmd-v2-port.md`)
- MLX plan moved from upcoming to current
- Stashed roadmap + readme-first updates recovered and committed (PR #74)
- README footer: QMD credit restored, CLA + dual license confirmed on both repos

## Files Changed

| File | Change |
|------|--------|
| `src/search-pipeline.ts` | Intent support, candidateLimit param, explain traces, DeepSearchResult type |
| `src/llm.ts` | Intent in expansion prompt, persistent DB cache (expansion + reranking), setLLMCacheDb() |
| `src/core.ts` | llm_cache table schema, deepSearch options, structuredSearch() method, StructuredQuery type |
| `src/mcp-server.ts` | intent, candidate_limit, explain params on crystal_search, LLM cache DB wiring |
| `src/cli.ts` | --intent, --candidates, --explain flags, crystal mlx subcommand |
| `src/mlx-setup.ts` | **NEW** ... full MLX setup, doctor check, state management |
| `src/doctor.ts` | MLX health check (#13) |
| `src/installer.ts` | MLX detection in crystal init flow |

## What This Enables

- **Free deep search.** MLX replaces OpenAI API calls for expansion + reranking. Zero cost per search.
- **Faster repeated searches.** Persistent cache means the LLM call happens once per unique query.
- **Smarter agent queries.** Structured search lets agents skip expansion when they know what they want.
- **Debuggable search.** Explain mode shows exactly why each result ranked where it did.
- **Offline search quality.** MLX works without internet. API fallback when MLX is down.

## 0.7.23 (2026-03-15)

# Release Notes: Memory Crystal v0.7.23

**Date:** 2026-03-15

## Search Quality v2 + MLX Local LLM

This release adds six search quality features ported from the QMD v2.0 analysis, plus the complete MLX local LLM infrastructure for Apple Silicon. Deep search is now disambiguatable, cacheable, debuggable, and can run entirely offline on Apple Silicon.

### Intent parameter

Disambiguates queries without adding search terms. `crystal search "security" --intent "1Password"` steers results toward 1Password-related security instead of repo permissions or agent secrets. Intent flows through the expansion prompt (guides LLM variations), disables strong-signal bypass (keyword match might not be what the caller wants), and is prepended to the rerank query. Available via CLI `--intent` and MCP `intent`.

### Persistent LLM cache

Expansion and reranking results are now cached in crystal.db (`llm_cache` table) with a 7-day TTL. Same query = instant on repeat searches. Reranking cache is content-addressable (keyed by query + sorted passage hashes), so identical content from different sessions shares cached scores. Configurable via `CRYSTAL_CACHE_TTL_DAYS` env var.

### Explain mode

Per-result scoring breakdown showing FTS score, vector score, RRF rank, reranker score, recency weight, and final blended score. `crystal search "query" --explain`. Available via CLI `--explain` and MCP `explain`. Makes search quality transparent and debuggable.

### candidateLimit

Tunable rerank pool size. `crystal search "query" --candidates 60`. Default stays 40. More candidates = better recall, slower reranking. Available via CLI `--candidates` and MCP `candidate_limit`.

### Structured search API

`crystal.structuredSearch(queries)` accepts pre-expanded StructuredQuery[] with typed sub-queries (lex, vec, hyde). Skips LLM expansion entirely. Agents construct their own queries when they already know what they want. RRF fusion with first list weighted 2x.

### MLX local LLM (Phase 3)

Complete auto-install infrastructure for running a local LLM on Apple Silicon:

- `crystal mlx setup` detects Apple Silicon, installs mlx-lm (uv > pip3 > pip3 --user), creates LaunchAgent for always-on server
- Model: `mlx-community/Qwen2.5-3B-Instruct-4bit` (~1.5 GB, fast on M-series)
- Port 18791 (18789 OpenClaw, 18790 Crystal Core, 18791 MLX)
- `crystal mlx status` and `crystal mlx stop` for server management
- `crystal doctor` check #13: MLX health (not installed / down / running)
- `crystal init` detects Apple Silicon and suggests MLX setup
- State file at `~/.ldm/state/mlx-server.json`

### Also in this release

- QMD v2.0 analysis documented (`ai/product/notes/`)
- Search quality plan written (`ai/product/plans-prds/current/`)
- MLX plan moved from upcoming to current
- Stashed roadmap + readme-first updates recovered (PR #74)

Closes #57, #63, #64.

## 0.7.22 (2026-03-14)

Remove standalone role

## 0.7.21 (2026-03-14)

Fix install URL

## 0.7.20 (2026-03-14)

Add CLA, dual LICENSE, standardize README footer

## 0.7.19 (2026-03-14)

Fix score normalization

## 0.7.18 (2026-03-13)

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

## 0.7.17 (2026-03-13)

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

## 0.7.16 (2026-03-13)

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

## 0.7.15 (2026-03-13)

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

## 0.7.14 (2026-03-13)

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

## 0.7.13 (2026-03-13)

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

## 0.7.12 (2026-03-13)

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

## 0.7.11 (2026-03-13)

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

## 0.7.10 (2026-03-13)

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

## 0.7.9 (2026-03-13)

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

## 0.7.8 (2026-03-13)

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

## 0.7.7 (2026-03-13)

Update install prompt to new standard format. Replaces old 3-question prompt with 4 explain questions, installed check, and dry-run before install.

## 0.7.6 (2026-03-13)

Update LDM delegation tips

## 0.7.5 (2026-03-13)

# Release Notes: Memory Crystal v0.7.5

## LDM OS Integration

Memory Crystal now works with LDM OS when it's available.

### crystal init delegates to ldm install

When the `ldm` CLI exists on PATH, `crystal init` delegates generic deployment to it. LDM OS handles the scaffold, interface detection, and extension deployment. Memory Crystal keeps its own setup: database backup, role configuration, pairing, cron jobs.

When `ldm` isn't available, `crystal init` works standalone like it always has. No new dependencies. No breaking changes.

### LDM OS tip

After install completes, Memory Crystal prints a tip: "Run `ldm install` to see more skills you can add." Helps users discover the rest of the ecosystem.

### Part of LDM OS

README now includes a "Part of LDM OS" section linking back to the LDM OS repo. Memory Crystal installs into LDM OS, the local runtime for AI agents.

## 0.7.4 (2026-03-11)

MCP fix (OPENCLAW_HOME env var), AgentId reads from LDM config instead of hardcoding, MCP registrations moved to user-level, 33 stale branches renamed, QMD v1.1.6 analysis documented

## 0.7.3 (2026-03-10)

Fix MCP registration to include OPENCLAW_HOME env var for memory-crystal MCP server

## 0.7.2 (2026-03-05)

Fix MCP detection in doctor and installer to check project-level and user-scope registrations

## 0.7.1 (2026-03-05)

Database backup, verification, and import in installer

## 0.7.0 (2026-03-05)

Delta sync, file sync, intelligent install & update

## 0.6.1 (2026-03-05)

Search quality: deep search with LLM query expansion + re-ranking, MCP sampling design, updated docs

## 0.6.0 (2026-03-04)

Dream Weaver integration, Crystal Core gateway, staging pipeline, commands channel.

- Dream Weaver narrative consolidation via `crystal dream-weave` (imports engine from dream-weaver-protocol)
- Crystal Core gateway (`crystal serve`) on localhost:18790, OpenAI-compatible endpoint
- Staging pipeline for new agents from relay (auto-detect, stage, backfill, dream-weave)
- Commands channel on relay Worker (nodes send commands to Core, Core sends results back)
- OpenClaw raw data sync to LDM after every agent_end turn (sessions, workspace, daily logs)
- Relay command support in cc-hook.ts (`sendCommand()` export)
- Harness-aware init flow (OpenClaw vs Claude Code, Core vs Node)
- Poller now detects new agents and routes to staging before live ingest

## 0.5.0 (2026-03-04)

Init discovery, bulk copy, OpenClaw parser, backfill, CE migration. Reorganize ai/ to ai/product/.

- `crystal init` discovers session files on the current machine (Claude Code + OpenClaw)
- `crystal backfill` embeds raw transcript files from LDM (Core: local embed, Node: relay to Core)
- `crystal migrate-embeddings` migrates context-embeddings.sqlite chunks into crystal.db ($0, copies embeddings directly)
- `src/discover.ts` auto-detects installed harnesses and session file locations
- `src/bulk-copy.ts` copies raw files to LDM transcripts (idempotent, skip if same size)
- `src/oc-backfill.ts` parses OpenClaw JSONL format into standard message format
- Workspace path added to LDM (`~/.ldm/agents/{id}/memory/workspace/`)



## 0.4.1 (2026-03-03)

Crystal Core/Node architecture, crystal doctor, crystal backup, crystal bridge, SKILL.md onboarding rewrite

## 0.3.3 (2026-03-02)

Fix bin entries: crystal and crystal-mcp commands were missing from v0.3.2 due to npm stripping ./ prefix paths

## 0.3.2 (2026-03-02)

Rewrite SKILL.md as complete agent install guide. Add crystal-mcp binary for clean MCP config. CLI search output matches MCP server (freshness icons, numbered results). Agents can now auto-detect and install for Claude Code CLI, Claude Desktop, and OpenClaw.

## 0.3.1 (2026-03-02)

Fix npm package: exclude ai/ folder from published tarball

## 0.3.0 (2026-03-02)

Phase 1 continuous capture, Cloud MCP server, QR pairing, crystal init, docs overhaul

## 0.2.0 (2026-02-28)

README overhaul, relay encryption, QR pairing spec, Grok/Lesa feedback, disable auto dev-updates
