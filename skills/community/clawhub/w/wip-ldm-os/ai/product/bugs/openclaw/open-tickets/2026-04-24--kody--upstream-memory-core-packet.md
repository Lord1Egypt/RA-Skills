# OpenClaw upstream packet: memory-core OOM and restart safety

**Date:** 2026-04-24
**Author:** Kody, with Parker
**Status:** accepted upstream main after `v2026.4.26`; fork-side fix promoted live
**Related local artifacts:**
- `ai/product/bugs/openclaw/2026-04-24--cc-mini--main-sqlite-oom-artifact.md`
- `ai/product/plans-prds/current/openclaw/2026-04-24--cody--openclaw-config-runtime-split.md`
- `ai/product/bugs/openclaw/2026-04-24--cc-mini--unified-reliability-triage.md`

## Summary

OpenClaw upstream `2026.4.24` does not appear to address the memory-core failure mode we hit on Lēsa.

## Status update, 2026-04-27

The narrow production fix is now carried on WIP's OpenClaw `v2026.4.25` fork branch and promoted live for Lēsa.

- Fork PR: `wipcomputer/openclaw#4`
- Merge commit: `c188a3647c11fde080f8e6475e20380aa9671f35`
- Live version after promotion: `OpenClaw 2026.4.25 (c188a36)`
- Live probes after promotion: `/healthz` green, `/readyz` green
- Live gateway after promotion: PID stable after `launchctl kickstart -k`
- Memory Crystal hook gate: `plugins.entries.memory-crystal.hooks.allowConversationAccess=true` present
- Companion hook gates: `compaction-indicator` and `session-export` also present

The upstream packet is accepted but not live-retired. Both memory-core fixes landed on upstream `main` after stable `v2026.4.26`, so WIP must keep the current fork carry live until either the next stable release includes both commits or a post-`v2026.4.26` WIP build is canaried and promoted.

Upstream PRs opened from this packet:

- Seed cache stream/yield: <https://github.com/openclaw/openclaw/pull/73067>; accepted via maintainer PR #73118 as `983fd775e2ca000d5c7b95e0281eeb19eb12059b`.
- Fallback chunk scoring bounded top-K: <https://github.com/openclaw/openclaw/pull/73069>; accepted via maintainer PR #73100 as `864c4f7ff492f0f514c12557d44f0d6b509231fc`.

Post-promotion caveats:

- The first `v2026.4.25` startup blocked external `agent_end` hooks until the hook flags were re-applied and the LaunchAgent was kickstarted again. The second clean startup did not show the typed-hook block messages.
- `v2026.4.25` normalizes the runtime model route to `openai/gpt-5.5` in logs, while source config may still carry `codex/gpt-5.5`. Treat `openai/gpt-5.5` plus Codex runtime as the accepted v25 live spelling.
- A stale duplicate `tavily` plugin warning references an older worktree. This is not blocking readiness, but should be cleaned in the config/plugin provenance follow-up.
- `listChunks()` remains unfixed in the live WIP build and should stay tracked as R2.A.3 until WIP canaries/promotes a build containing upstream commit `864c4f7ff4`.

Two upstream memory-core paths still materialize large SQLite result sets into V8 heap:

1. `seedEmbeddingCache()` in `extensions/memory-core/src/memory/manager-sync-ops.ts`
   - Fixed on upstream `main` after `v2026.4.26` by `983fd775e2`.
   - Local production DB has 435,136 rows and about 8.08 GiB serialized embedding payload.
   - Previous behavior crashed with V8 heap OOM at `StatementSync::All`.
2. `listChunks()` / fallback vector scoring in `extensions/memory-core/src/memory/manager-search.ts`
   - Fixed on upstream `main` after `v2026.4.26` by `864c4f7ff4`.
   - Local production DB has 323,249 rows, about 424 MiB text and about 5.30 GiB embedding payload.
   - This is the secondary broad-recall OOM path after the seed cache path is fixed. The PR streams candidates and maintains a bounded exact top-K.
   - PR CI is green as of 2026-04-27 after rebasing onto `upstream/main` `78d3fce5f9`.

Our fork's first patch changed `seedEmbeddingCache()` to `.iterate()`. Canary against the real production `main.sqlite` passed:

```text
rows: 435,136
embedding payload: 8.08 GiB
duration: about 117s
RSS: about 214 MB
Abort trap: none
live gateway disturbance during canary: none
```

Live promotion then proved the heap OOM was gone, but exposed a second issue: the synchronous iterate loop blocked the event loop long enough for `/health` to time out. `wip-healthcheck` killed the gateway after one 30s timeout. Next patch should add cooperative yielding inside the seed loop so the gateway can answer health probes while seeding.

## Recommended upstream sequence

### 1. PR: stream `seedEmbeddingCache` and yield during long seeds

This is the narrow, high-confidence upstream PR.

Scope:

- Replace `.all()` with `.iterate()` in `seedEmbeddingCache()`.
- Yield to the event loop every N rows, for example every 500 or 1000 rows.
- Keep memory bounded and keep `/health` responsive during large cache seeds.
- Add logging around row count, duration, and cache-seed completion if the local logging pattern supports it.

Why both changes belong together:

- `.iterate()` fixes V8 heap materialization.
- Cooperative yield fixes event-loop starvation during large but successful seeds.
- Shipping only `.iterate()` turns a crash into a watchdog kill under large data.

Suggested PR title:

```text
fix(memory-core): stream embedding cache seed without blocking health
```

Suggested PR body:

```markdown
## Summary

`seedEmbeddingCache()` currently calls `.all()` over the entire `embedding_cache` table. Large memory stores can materialize multiple GiB of serialized embeddings into V8 heap and crash inside `StatementSync::All`.

This changes the seed path to stream rows with `.iterate()` and periodically yield to the event loop so health probes and other gateway work are not starved during large seeds.

## Evidence

On a production-size memory-core database:

- `embedding_cache`: 435,136 rows
- serialized embedding payload: about 8.08 GiB
- old path: V8 heap OOM at `StatementSync::All`
- streamed path canary: RSS held around 214 MB and completed in about 117s

Without cooperative yielding, the streamed path completes but can block gateway probes long enough for watchdogs to restart the gateway. On OpenClaw `v2026.4.23`, `/health` was the live probe we observed. On `v2026.4.25+`, use the protected `/healthz` and `/readyz` probes for promotion gates; legacy `/health` can hang behind later handlers even when the protected probes are healthy.

## Testing

- memory-core test suite
- production-size read-only canary against a copied target DB
- verified no V8 `Reached heap limit`, no `Abort trap: 6`, and no `StatementSync::All` crash signature
```

### 2. PR: bounded fallback vector scoring over chunk embeddings

An upstream PR was accepted via maintainer PR #73100: <https://github.com/openclaw/openclaw/pull/73069>.

Status as of 2026-04-27: PR CI is green after rebasing onto current upstream main and adding the current-upstream lint-suppression allowlist row for `src/test-utils/plugin-runtime-env.ts`. That allowlist row is a CI compatibility fix for upstream's test-helper move, not part of the memory-core behavior change.

PR title:

```text
fix(memory-core): bound fallback vector chunk scoring
```

PR body summary:

```markdown
`listChunks()` in `extensions/memory-core/src/memory/manager-search.ts` currently runs an unbounded `.all()` over `chunks` and selects the `embedding` column.

On a large memory store this can materialize several GiB of text and serialized embeddings into V8 heap:

- `chunks`: 323,249 rows
- text payload: about 424 MiB
- embedding payload: about 5.30 GiB

This appears to be the secondary OOM path after fixing `seedEmbeddingCache()`.

Fix shape:

- stream candidates with `.iterate()`
- maintain bounded exact top-K results for cosine similarity instead of materializing all candidates
- preserve ranking semantics by only evicting a candidate when a strictly better score arrives

This is separate from the seed-cache PR because ranking semantics are different and need their own focused test.
```

### 3. Issue: restart/doctor config normalization must fail closed

Open an issue first. The fix may span restart, doctor, schema migration, and config writer identity.

Suggested issue title:

```text
gateway restart should not silently rewrite openclaw.json with stale schema knowledge
```

Suggested issue body:

```markdown
We observed a restart path rewriting `~/.openclaw/openclaw.json` through stale schema knowledge. The result stripped configured model/provider fields and changed the live agent route after restart.

Config normalization should behave like a migration tool:

- preserve unknown fields by default
- fail closed on unknown model/provider/plugin keys rather than silently stripping them
- show a preflight diff before mutation
- stamp writer identity, writer version, schema version, source config hash, and reason
- keep model names tied to provider/auth route resolution, not just string names

Observed runtime consequence:

- primary model route changed away from the intended Codex GPT-5.5 configuration
- fallback and product workflow keys could be lost without a clear mutation audit

Workaround used locally:

- restart LaunchAgent directly with `launchctl kickstart -k`
- avoid CLI restart paths that run normalization until this is fixed
```

## Local WIP-owned follow-ups

These are probably not upstream OpenClaw PRs unless OpenClaw owns the equivalent component:

1. Healthcheck policy:
   - Do not kill the gateway after one 30s health-probe timeout during active work. For `v2026.4.25+`, probe `/healthz` and `/readyz`, not legacy `/health`.
   - Require multiple consecutive failures or stronger stuck-run signals.
   - Distinguish event-loop busy from process dead.
2. Config deploy pipeline:
   - Git tracks desired config and manifests.
   - Runtime state stays outside git.
   - Deploy validates invariants before writing `~/.openclaw/openclaw.json`.
3. Image-generation regression:
   - Treat `imageGenerationModel` and `mediaGenerationAutoProviderFallback: false` as runtime contract keys.
   - Add them to config invariant validation.

## Operator guidance

Do not upgrade Lēsa to raw `openclaw@2026.4.26` expecting this specific failure to disappear. As of the `v2026.4.25` promotion, the live system is safe because WIP carries the seed-cache stream/yield patch on the fork build. Upstream `main` now has equivalent memory-core fixes, but stable `v2026.4.26` does not. Keep the local fork patch until WIP canaries and promotes a post-`v2026.4.26` build or a later stable release containing `983fd775e2` and `864c4f7ff4`.
