---
name: ship-it
description: Pre-launch operational-readiness checklist for a feature, release, or branch. Walks a fixed 10-category gate (logging, error handling, telemetry, feature flags, migrations, rollback, secrets, local-first storage, auth, update strategy), produces a structured report with PASS / GAP / N/A per item, every PASS backed by `file:line` evidence and every GAP cited as `no evidence found at <path>`. Final verdict groups findings as **Blocking** / **Should-fix** / **N/A with reason** / **Passing**. Use this skill whenever the user says "is this ready to ship?", "ship-it check", "/ship-it", "production checklist", "pre-launch checklist", "production readiness", "release readiness", "launch checklist", or asks whether a release is operationally safe — even if they don't explicitly say "ship-it skill". Use [`code-review`](../code-review/SKILL.md) for diff-level code quality (DRY, dead code, tests). Use `ship-it` for cross-cutting operational readiness. Never edits code unprompted — recommendation first, ask, then fix.
---

# Ship It

The operational gate I run before calling something done. Code review tells me the diff is clean; `ship-it` tells me the thing won't page me at 3am.

## When to use this skill

- "is this ready to ship?" / "ship-it check" / "/ship-it"
- "production checklist" / "pre-launch checklist" / "production readiness" / "release readiness" / "launch checklist"
- "can we deploy this?" / "anything missing before we ship?"
- The user names a branch, PR, release tag, or module and asks whether it's safe to release.

Do **not** auto-trigger when the user is asking about diff-level code quality, DRY, dead code, or test coverage — that's [`code-review`](../code-review/SKILL.md)'s job. If the trigger is ambiguous (e.g. bare "ready to ship?" with a working tree full of uncommitted edits), ask once whether they want the diff review or the operational checklist.

## Hard rules

- **Recommend, don't refactor.** This is an audit. Never edit code unprompted. After the report, ask per-blocker whether the user wants a fix drafted.
- **Evidence is mandatory.** Every PASS must cite `file:line`. "I checked, it looks fine" is not a PASS — that's a GAP labelled `couldn't verify`.
- **Name the probe.** Every PASS also names the exact check that produced its evidence — the grep pattern + path, the file you read, or the command you ran. If you didn't run a probe for an item, it's GAP labelled `not checked` — never PASS. A result you didn't observe doesn't exist.
- **N/A needs a reason grounded in the scope.** The justification must derive from an observed fact about *this* scope, with the probe that established it (e.g. *"no files under `migrations/` in the diff (`git diff --stat`) → migrations N/A"*) — never a guess from the project type. Don't fabricate gaps for categories that don't apply.
- **Stay in your lane.** Don't re-do `code-review`'s work. If the user asks about DRY / dead code / test coverage, defer.

## Workflow

### Phase 1 — Name the unit being shipped

Don't proceed until scope is named. Ask the user with `AskUserQuestion` if it isn't obvious:

- A specific PR / branch? → `git diff` against the base; scope the audit to changed files + their direct call graph.
- A feature flag? → grep the flag key; scope to gated code paths.
- A release tag / version bump? → `git diff <prev-tag>..HEAD`.
- A module / directory? → scope to that path.

Echo the scope back in one line before starting Phase 2 (*"Auditing branch `feat/billing-v2` against base `main` — 14 files changed."*).

### Phase 2 — Walk the 10 categories

For each category: state the criterion in one line, search the codebase for evidence, mark PASS / GAP / N/A. Use `Grep` and `Read` aggressively; spawn an `Explore` sub-agent for any category where the search would take more than 3 queries.

Record each probe as you run it — the report cites them. A probe is a specific `Grep` pattern + path, a `Read` of a named file, or a command with its observed output. A sub-agent's result counts as a probe only if the sub-agent names its own probes and citations; "the agent said it's fine" is not evidence. Where a check depends on the user (dashboards, runbooks, rollout plans), record their answer as the probe (*"user confirmed: alert added to Grafana billing board"*) — an unanswered question stays GAP.

#### 1. Logging

**What good looks like:** Structured logs (JSON or key=value), correlation / request IDs propagated, levels used correctly (`error` ≠ `info`), no secrets / tokens / PII in log output, errors logged with stack + context, not just the message.

**How to check:** Grep for the logger import and inspect call sites in changed files. Confirm a request-ID middleware exists upstream and that the new code paths inherit it. Grep for known secret-shaped variables being passed to log calls.

#### 2. Error handling

**What good looks like:** Each failure mode named (network, validation, auth, downstream 5xx), no `catch {}` / `except: pass` / `_ = ...` silent swallows, user-facing errors mapped to safe messages, retry / backoff on external-boundary calls (HTTP, DB, queues).

**How to check:** Grep for empty catches, bare `except`, error-swallowing patterns. Trace each new external call to see how failures propagate. Confirm idempotency where retries exist.

#### 3. Telemetry

**What good looks like:** New code paths emit metrics (counts, latencies, error rates), traces propagate (OpenTelemetry / equivalent context passed through), dashboards / alerts updated to include the new signal.

**How to check:** Grep for the metrics client in changed files. Confirm at least one counter and one latency histogram per significant code path. Ask the user whether the dashboards / alerts were updated — that's usually out-of-tree.

#### 4. Feature flags

**What good looks like:** New behavior gated behind a flag with a clear owner, documented default state for prod (almost always `off`), and a written ramp / cleanup plan (when does the flag get removed?).

**How to check:** Grep for the flag client; confirm new branches are gated. Read the flag definition file / dashboard config for owner + default. Ask the user for the cleanup plan if it isn't in the PR description.

#### 5. Migrations

**What good looks like:** Forward-compatible — the deployed code tolerates BOTH old and new schema for at least one release. Backfill plan named if columns are added. Runtime estimated against prod-size data (not just dev).

**How to check:** Read the migration files. Look for `ALTER TABLE` against large tables — flag any that take exclusive locks. Confirm the matching code reads `column ?? fallback` rather than assuming the new shape exists. Ask about backfill strategy.

#### 6. Rollback strategy

**What good looks like:** The change can be reverted by redeploying the previous artifact. Flag-on / flag-off is the rollback path where possible. Migrations are split from code deploys so revert never requires a DB rollback. There's a one-liner in the runbook.

**How to check:** Look for the runbook entry. Confirm migrations were merged in a separate commit / PR from the feature code (the "expand / migrate / contract" pattern). If a migration is destructive (DROP, NOT NULL added) call it out as blocking unless a rollback plan exists.

#### 7. Secrets

**What good looks like:** No secrets in code, config files, or logs. Rotation path documented. New env vars added to the secret store (Vault / AWS SM / Doppler / etc.), not just `.env.example`.

**How to check:** Grep changed files for high-entropy strings, common key shapes (`AKIA…`, `sk_live_`, `xoxb-`), and `.env*` diffs. Confirm any new env var also exists in the secret-store config (Terraform / Helm values / etc.).

#### 8. Local-first storage *(skip with N/A for pure server services)*

**What good looks like:** Offline behavior defined (queue + replay, or fail-fast), conflict resolution rule named for sync (last-writer-wins, CRDT, merge UI), schema version in the local DB, migration handles users upgrading from an older client.

**How to check:** Find the local store (IndexedDB / SQLite / Realm / AsyncStorage). Read its schema-version handling and migration code. If the PR changes the local schema, confirm the upgrade path exists.

#### 9. Auth

**What good looks like:** New endpoints / screens have **authorization** checks (not just authentication), tenant / org scoping enforced server-side (never trust client-sent IDs), no IDOR — `GET /orders/:id` verifies the order belongs to the caller — session / token handling unchanged or explicitly reviewed.

**How to check:** For each new route, read the handler top-to-bottom. Confirm: caller identity comes from the session, the resource is loaded scoped to that identity, no `where: { id: req.params.id }` without a tenant predicate. Missing authz on a new route is **blocking**.

#### 10. Update strategy

**What good looks like:** How users get the new version is named and tested.
- **Web:** deploy + cache-bust (hashed assets, SW update flow if applicable).
- **Desktop (Tauri / Electron):** auto-update channel signed and pointed at the right manifest.
- **Mobile:** store review window accounted for, forced-update path for breaking API changes.
- **CLI / SDK:** version pinning respected, breaking changes major-bumped.

**How to check:** Identify the artifact type and ask the user how the rollout happens. For desktop, read the updater config. For mobile + breaking changes, confirm there's a min-version-supported check on the backend.

### Phase 3 — Produce the report

Group findings into four buckets. Order matters — blocking first.

```markdown
# Ship-It Report — <scope>

## Blocking
- **<category>:** <one-line problem> — `<file:line>` or `no evidence found at <path>`

## Should-fix (non-blocking)
- **<category>:** <one-line problem> — `<file:line>`

## N/A
- **<category>:** <one-line reason grounded in the scope> (probe: `<what established it>`)

## Passing
- **<category>:** <one-line evidence> — `<file:line>` (probe: `<grep pattern / file read / command>`)
```

Same PASS, written badly and well:

- ❌ `**Logging:** structured logging in place — src/billing/` — no line, no probe; unverifiable, could have been written without looking.
- ✅ `**Logging:** new invoice paths log via structured logger with request ID — src/billing/invoice.ts:31 (probe: grep -n "logger\." src/billing/ → 6 call sites, all pass ctx.reqId)` — anyone can rerun the probe and land on the same line.

**Blocking = any one of:**
- Secrets in code / logs / committed config.
- Missing authz on a new endpoint or screen.
- Destructive migration with no rollback plan.
- No way to disable the new behavior in prod (no flag, no quick revert).
- Update strategy genuinely absent for the artifact type.

Everything else is should-fix.

### Phase 4 — Offer to fix

After the report, ask: *"Want me to draft fixes for the blocking items, or stop at the report?"* Wait for explicit go-ahead before editing.

## Examples

### Example 1: PR-scoped audit

**User:** "is this ready to ship?" *(currently on branch `feat/billing-v2` with an open PR)*

**Claude:**
1. Echoes scope: *"Auditing `feat/billing-v2` against `main` — 14 files changed."*
2. Walks the 10 categories, citing `file:line` per finding and the probe that produced it.
3. Reports: 2 blocking (missing authz on `POST /api/v2/invoices` — `no tenant predicate in routes/invoices.ts:24-51, read top-to-bottom`; no rollback for the `currency_code NOT NULL` migration), 4 should-fix, 1 N/A (local-first storage — *"no client-side store in scope: `grep -rl 'localStorage\|indexedDB' src/billing/` → 0 hits, server-only module"*), 3 passing with probes named.
4. Asks whether to draft fixes for the blockers.

### Example 2: Module-scoped audit

**User:** "ship-it check on the billing module"

**Claude:**
1. Scopes to `src/billing/**` (confirms the path exists first).
2. Skips the "diff vs base" framing — runs the 10 categories against the module's current state.
3. Marks update-strategy as N/A *("module is consumed by the web app's update flow — covered there, not here")* with a pointer to where it IS covered.

### Example 3: Anti-pattern — wrong skill

**User:** "review my diff"

**Claude:** "That's [`code-review`](../code-review/SKILL.md)'s territory — diff-level quality, DRY, tests. `ship-it` is for the operational gate (logging, flags, migrations, rollback, auth, etc.). Want me to run `code-review` instead, or did you mean the operational checklist?"

## Anti-patterns

- ❌ Marking a category PASS without a `file:line` citation. "Looks fine" is a GAP labelled `couldn't verify`.
- ❌ PASS on vibes — a PASS with no named probe (the grep / read / command that produced the evidence) is a GAP labelled `not checked`.
- ❌ N/A from a guess about the project type. Derive it from the scope and name the probe: *"no schema files in this diff (`git diff --stat`) → migrations N/A"*.
- ❌ Inventing GAPs in N/A categories. A server-only service genuinely has no local-first storage layer — say so and move on.
- ❌ Reviewing diff quality (DRY, dead code, missing tests) under the ship-it banner. Defer to `code-review`.
- ❌ Editing code mid-audit. The report comes first, then the user picks what to fix.
- ❌ Blocking on every missing dashboard or runbook entry. Telemetry without a dashboard is should-fix. Telemetry with secrets in the log line is blocking. Calibrate.
- ❌ Letting Phase 1 slide. Auditing "the whole repo" produces unactionable output. Force a scope.

## Notes

- Categories 1–7 + 9 apply to almost any service. Category 8 (local-first storage) is N/A for pure server work. Category 10 (update strategy) is where most teams underinvest — push on it.
- The 10-category list is deliberately fixed. Don't extend it ad-hoc — if you find yourself wanting to add "performance" or "i18n" as a category, that's a separate skill or a should-fix entry under the closest existing category.
- Pairs well with [`code-review`](../code-review/SKILL.md) (run code-review first for diff quality, then ship-it for operational readiness) and [`handoff`](../handoff/SKILL.md) (capture the report as the next-session pointer if shipping is deferred).
