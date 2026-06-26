# Release Pipeline Hardening + CI

**Date:** 2026-04-17 (Day 70 PST)
**Author:** cc-mini (in conversation with Parker)
**Status:** Planned ... pre-execution
**Type:** Structural / workflow master plan
**Severity:** High ... blocks confident releases across all LDM OS repos
**Affected:** `wip-ldm-os-private`, `wip-ai-devops-toolbox-private`, `memory-crystal-private`, and every other `-private` repo on the same release pipeline
**Related:**
- `2026-04-05--cc-mini--release-pipeline-master-plan.md` (earlier master plan)
- `2026-04-06--cc-mini--shared-universal-config-layer.md`
- `2026-04-08--cc-mini--silent-skip-without-license-guard-config.md`
- `master-plans/2026-04-09--cc-mini--master-plan-004-execution-order.md`

## Superseded / Consolidated By

This plan is consolidated into `ai/product/bugs/release-pipeline/2026-04-24--codex--canary-release-pipeline-master-plan.md`.

Keep this file for historical context and reasoning. Use the 2026-04-24 canary release pipeline master plan as the current implementation map.

---

## 1. Problem statement

Parker's observation (2026-04-17 session):

> "Two weeks ago we were pushing releases to the public repo once every 15 minutes ... I'd install and test. We changed to alphas, and now we have these alphas that you can install, but I don't know. We haven't pushed anything to public in a couple of weeks. I really don't know if the release notes are working, if anything is broken. There's no CI pipeline, from my understanding, to go 'Oh, this didn't break anything else.'"

Concrete symptoms observed this session:
1. **Orphan version bumps** in `devops/wip-ai-devops-toolbox-private` working tree (`wip-file-guard/package.json` 1.9.69 → 1.9.70, `wip-release/package.json` 1.9.74 → 1.9.75). Someone ran `wip-release patch`, the tool bumped `package.json`, then nothing else. No CHANGELOG, no tag, no publish, no commit. Evidence that `wip-release` can leave a repo half-released with no safety net.
2. **Two weeks of private-main changes have not reached public.** `wip-ldm-os-private` is at v0.4.73-alpha.34 with 23 unreleased commits on main. Drift is opaque until `deploy-public.sh` is run by hand, at which point a fortnight of diffs arrive at once.
3. **No automated test gate anywhere.** Alphas install on Parker's real machines. Breakages are discovered by hitting them. At 15-minute iteration this was fine; at 2-week backlog it is terrifying.
4. **No "last known good" mechanism.** If an alpha breaks `ldm doctor`, rollback is manual and requires remembering which version worked.
5. **Release-notes enforcement is at release time, not merge time.** `wip-release` correctly blocks publishing without a `RELEASE-NOTES-v{ver}.md` file, but nothing prevents a PR from merging without one. The gate is at the wrong end of the pipeline.

Why it matters now: Parker wants to return to "incredibly fast development, all day" ... alphas on every merge, stable releases to public at a cadence he trusts. The current pipeline has the right shape (four tracks, release-notes gate, private/public split) but lacks the safety net that makes confident daily shipping possible.

---

## 2. Root cause

The release pipeline enforces the right things **at the wrong point in time**.

| What's enforced | When | Correct? |
|---|---|---|
| Release notes file required | At `wip-release` time | Too late ... PR already merged |
| Alpha cannot deploy to public | At `deploy-public.sh` time | Correct |
| Never deploy back to source | At `deploy-public.sh` time | Correct |
| Four tracks (alpha / beta / hotfix / stable) | At `wip-release` time | Correct |
| Atomic package.json + CHANGELOG + SKILL.md | At `wip-release` time | Partial ... fails open on error |
| Broken code does not land | **NOWHERE** | Missing |
| Release does not break existing installs | **NOWHERE** | Missing |
| Rollback if release is bad | **NOWHERE** | Missing |

Structural pattern: humans trigger `wip-release` by hand. The tool does a multi-step mutation (edit `package.json`, edit `CHANGELOG.md`, git commit, git tag, npm publish, create GitHub release, run `deploy-public.sh`). If any step fails, the previous steps remain. Idempotence is partial. Rollback is manual.

The right pattern: pipeline-driven releases. Humans trigger a PR. CI runs the gate. Merge fires the release. Canary install validates it. Only then does anything reach end users.

---

## 3. What's already built (inventory before adding anything)

Before writing new tooling, document what exists so we don't duplicate. Reviewed in session on 2026-04-17.

### 3.1 `wip-release` (tools/wip-release/)

- CLI + module + MCP surface (`cli.js`, `core.mjs`, `mcp-server.mjs`)
- Four release tracks (alpha / beta / hotfix / stable) with distinct npm tags + public-sync behavior
- Version numbering: `X.Y.Z-alpha.N`, `X.Y.Z-beta.N`, `X.Y.Z`
- **Hard-enforced release-notes gate** at `core.mjs:309-315`:
  - No file → BLOCKED
  - File must come from disk, not inline string
  - Scaffolds `RELEASE-NOTES-v{version}.md` template when missing (`core.mjs:363-411`)
- **Atomic update** of root files: `package.json`, `CHANGELOG.md`, `SKILL.md` staged together (`core.mjs:185-210`)
- **Three-source priority for release notes**:
  1. `--notes="..."` inline (overrides file)
  2. `RELEASE-NOTES-v{ver}.md` in repo root (standard)
  3. `ai/dev-updates/` today's files (fallback)
- **Structured auto-generated release notes** with sections: Changes, Fixes, Docs, Files changed, Install, Attribution, Changelog
- **Post-merge rename** runs automatically as step 10 of stable release
- `--dry-run` and `--no-publish` flags

### 3.2 `deploy-public` (tools/deploy-public/)

- `deploy-public.sh` ... sync private-repo-code to public counterpart
- **Hard-enforced safety checks**:
  - Refuses to deploy if target == source (would destroy)
  - Refuses to deploy to any `-private` repo name
  - **Refuses to deploy alpha versions to public** (`package.json` version must not contain `-alpha`)
  - Verifies no GitHub redirect (catches renamed repos)
- Auto-creates public repo if missing
- Excludes from sync: `ai/`, `_trash/`, `.git/`, `.DS_Store`, `.wrangler/`, `.worktrees/`, `.claude/`, `CLAUDE.md`
- Uses rsync to ensure deletions propagate
- Creates PR on public repo, merges with `--merge` (never squash)

### 3.3 Branch + file guards (tools/wip-branch-guard, tools/wip-file-guard)

- `wip-branch-guard/guard.mjs` ... blocks file-modifying commands on main branch, provides the "worktree first" recipe
- `wip-file-guard/guard.mjs` ... blocks destructive edits to protected identity files
- Claude Code hooks + OpenClaw plugin lifecycle shapes

### 3.4 Documentation

- `DEV-GUIDE-GENERAL-PUBLIC.md` ... comprehensive workflow (branch → notes → PR → merge → release)
- `repos/ldm-os/library/documentation/how-releases-work.md`
- `wip-ai-devops-toolbox-private/REFERENCE.md`

### 3.5 What all of this adds up to

The **release side** of the pipeline is largely built and correct. The **pre-release side** (PR validation, CI) is absent. The **post-release side** (validation of the published artifact, rollback) is absent.

---

## 4. Architecture decision: keep LDM OS and devops-toolkit separate, integrate at install

### Parker's tension
> "I almost want to merge devops-toolkit into Lēsa ... Lēsa should be the base, and the rules should be governed by the devops toolkit. I'm trying not to define all these rules and have people take three months to figure out the right way to deploy."

### Decision: keep them separate, make them feel like one

Do not merge `wip-ai-devops-toolbox` into `wip-ldm-os` as a single npm package. Reasons:

1. **Scope.** `wip-ai-devops-toolbox` contains 13 sub-tools. Each has its own version cycle (`wip-release` alone is at 1.9.75-ish). Merging creates a monolith that forces LDM OS to release on every tool bump.
2. **Use cases diverge.** Dogfood / read-only / demo machines may want LDM OS runtime without publishing tools.
3. **Independent evolution.** Changes to `wip-release` do not need an LDM OS release. Separation lets each ship at its natural cadence.

Instead, tighten the handoff so **the user never thinks about the boundary**:

1. `ldm init` on a fresh repo auto-invokes `wip-repo-init` (from devops-toolkit) to scaffold the `ai/` structure.
2. `ldm install` detects commands that require devops-toolkit (e.g., first time user tries to release) and auto-installs `@wipcomputer/wip-ai-devops-toolbox` with a single prompt confirmation.
3. Error messages from LDM OS commands that belong to devops-toolkit include the exact `wip-*` command to use.
4. Both share a single CLAUDE.md onboarding narrative so a new user runs `ldm init`, gets the directory structure, the guards, the release tool, and the CI config, without ever googling "how do I set up a wip repo."

The mental model for users: **"Install LDM OS, get the WIP workflow for free."** Implementation stays as two packages.

---

## 5. Seven concrete updates to devops-toolkit + LDM OS

Ordered by impact. Items 5.1-5.5 + 5.7 live in devops-toolkit (release + CI tooling). Item 5.6 lives in LDM OS (`bin/ldm.js`) because it is the installer's responsibility.

### 5.1 `wip-release` atomicity (Layer 1)

**Problem:** `wip-release patch` is multi-step. Partial failure leaves orphan state (the exact bumps we just saw in devops-toolkit).

**Fix:**
- Wrap all mutations (package.json edit, CHANGELOG edit, SKILL.md edit, git add, git commit, git tag, npm publish, gh release create, deploy-public.sh) in a try/catch with explicit rollback.
- On error: `git reset --hard HEAD` + `git clean -fd <specific paths>` + restore original `package.json` from pre-bump cache.
- Record a rollback marker in `.wip-release-state.json` so the next invocation can finish or discard.
- Add `wip-release --recover` to resume or clean after interrupted run.

**Acceptance:**
- Kill `wip-release` mid-run with SIGINT → working tree returns to pre-run state automatically.
- Network error during `npm publish` → working tree returns to pre-run state, tag removed, version restored.
- No orphan bump can be observed in any repo's working tree.

### 5.2 `wip-release --rollback`

**Problem:** No way to unship a bad release. Must manually republish the previous version.

**Fix:**
- New subcommand: `wip-release --rollback <version>` (or default to last released).
- Unpublish-or-deprecate the npm tag (`npm deprecate` if unpublish window closed, which is 72 hours).
- Delete or unlist the GitHub release.
- Revert the `package.json` + `CHANGELOG.md` entries on a new commit (never squash or force-push history).
- Optionally run `deploy-public.sh` again with the prior version to re-sync public.

**Acceptance:**
- Release v0.4.74 accidentally → `wip-release --rollback` → v0.4.73 is `@latest` on npm again, GitHub release for v0.4.74 is marked "yanked."
- Private repo history shows both the bad release commit and the rollback commit (no history rewrite).

### 5.3 Pre-merge check tool (`wip-release check`)

**Problem:** Release-notes gate fires at release time. PRs can merge without notes. Discovery lag is hours to days.

**Fix:**
- New subcommand: `wip-release check` (or standalone `wip-pr-check`).
- Intended to run in GitHub Actions on every PR.
- Validates:
  - `RELEASE-NOTES-v{ver}.md` exists on the branch head, OR an `ai/dev-updates/YYYY-MM-DD--...md` file is present.
  - `package.json` version does not conflict with an existing published version.
  - If version has been bumped, the CHANGELOG entry matches.
  - Lint passes (per repo's eslint/prettier config if present).
  - `node --check` syntax check on all `.js` / `.mjs` entrypoints.
  - `ldm install --dry-run` (if the repo installs via ldm) completes without error.
- Exits non-zero on failure. Designed to be called from a GitHub Actions job that blocks merge.
- **Docs-updated check:** if any file matching `src/**/*.{js,mjs,ts}` changed vs base branch, verify at least one of `SKILL.md`, `TECHNICAL.md`, or `docs/*/TECHNICAL.md` also changed. This prevents the W3-style "technical docs need updates" warning we hit on 2026-04-17 from sliding through the release-time gate. Escape hatch: `[skip-docs]` in commit message or `docs-exempt` label on PR for pure infra / test / build-only commits.

**Acceptance:**
- PR that bumps version without a CHANGELOG entry → CI red.
- PR with no release notes file → CI red.
- PR that breaks syntax → CI red.
- PR that touches `src/` without updating any doc → CI red (unless `[skip-docs]` or exempt label).
- Clean PR → CI green in under 90 seconds on a macOS runner.

### 5.4 Shared CI workflow templates

**Problem:** Each repo's `.github/workflows/` drifts. Changes to CI logic require N PRs across N repos.

**Fix:**
- Define reusable workflows in `wipcomputer/.github/.github/workflows/` (the org profile repo, which GitHub recognizes as the central location):
  - `wip-ci.yml` ... pre-merge validation (calls `wip-release check` + whatever tests each repo defines).
  - `wip-canary.yml` ... post-merge alpha install + smoke scenario on an ephemeral macOS runner.
  - `wip-release.yml` ... triggered on merge to main; runs `wip-release` in appropriate mode based on branch/commit marker.
- Each private repo adds a tiny `.github/workflows/ci.yml`:
  ```yaml
  name: CI
  on: pull_request
  jobs:
    ci:
      uses: wipcomputer/.github/.github/workflows/wip-ci.yml@main
      secrets: inherit
  ```
- Changes to the shared workflow propagate to all repos on next PR.

**Acceptance:**
- Update `wip-ci.yml` once → every repo's next PR runs the new checks.
- New private repo created → added to CI coverage by dropping in the 5-line workflow.

### 5.5 LDM OS ↔ devops-toolkit handoff

**Problem:** User has to know `wip-ai-devops-toolbox` exists separately from LDM OS. Adds friction.

**Fix:**
- `ldm init` on a fresh repo directory detects "no ai/ structure" and invokes `wip-repo-init` via the user-installed devops-toolkit. If devops-toolkit is missing, it offers to install it with one prompt.
- `ldm install wipcomputer/wip-ai-devops-toolbox` is a documented first-run flow.
- LDM OS error messages that belong to the devops-toolkit domain (e.g., "you need to publish this package") link to the exact `wip-*` command.
- LDM OS CLAUDE.md template installed by `ldm init` includes the release workflow instructions inline, not "see devops-toolkit docs."

**Acceptance:**
- Fresh user runs `ldm install wipcomputer/wip-ai-devops-toolbox`. Next step they ask about ("how do I release?") returns "run `wip-release patch`" with no additional discovery required.
- No user reports "I didn't know I needed to install a separate toolkit."

### 5.6 Installer doc sync (LDM OS, `bin/ldm.js`)

**Problem:** Docs live in three places:
1. **Repo** (source of truth). `SKILL.md`, `TECHNICAL.md`, `docs/*/TECHNICAL.md`, and templates in `shared/docs/*.tmpl`. Edited by contributors in PRs.
2. **Home** (`~/wipcomputerinc/library/documentation/`). Human-facing per-user docs.
3. **`.ldm`** (`~/.ldm/library/documentation/`). Agent-facing per-user docs.

Parker's rule: we only edit the repo docs. The installer syncs repo → home + `.ldm` on every `ldm install` / `ldm install --update`. Today, `ldm install` does copy templates to `~/.ldm/` during initial scaffolding, but there is no explicit, documented, tested refresh path for the home + `.ldm` library docs when a new version of LDM OS is installed. Updates can silently miss the deployed copies, which is how docs in home + `.ldm` drift from the repo over time.

**Fix:**
- `ldm install` of `@wipcomputer/wip-ldm-os` and of any extension with a `shared/docs/` folder runs a **non-destructive doc sync** step:
  - For each `.md.tmpl` file in the installed package's `shared/docs/`, deploy to the corresponding path in `~/wipcomputerinc/library/documentation/` and `~/.ldm/library/documentation/`.
  - **Non-destructive:** if the deployed file has user-added content (detected by comparing against the previous template version), prompt the user. Options: keep local, overwrite, or merge (print diff, let user pick hunks).
  - If the deployed file is byte-identical to the previous installed template version, silently update it to the new template.
  - New template files → added.
  - Removed template files → NOT auto-removed (preserve user state). Log a notice.
- New subcommand: `ldm docs sync` ... force-refresh all deployed docs from currently installed packages without reinstalling. Useful when a user's local docs drift or they want to see the latest.
- New subcommand: `ldm docs status` ... report which deployed docs differ from the currently installed template version, for diagnostics.
- `ldm doctor` gains a "docs drift" check that reports without auto-fixing (fix requires `ldm docs sync` because it may prompt).

**Acceptance:**
- User installs v0.4.74 of LDM OS. `~/wipcomputerinc/library/documentation/how-releases-work.md` and `~/.ldm/library/documentation/how-extensions-work.md` reflect the v0.4.74 template content. No stale v0.4.72 text lingers.
- User has locally edited `~/wipcomputerinc/library/documentation/how-worktrees-work.md` with personal notes. Installing a new version that updates this template prompts the user with a diff rather than silently overwriting.
- `ldm docs status` correctly identifies the divergence.
- `ldm docs sync` refreshes everything after user confirmation.
- `ldm doctor` reports drift but does not auto-fix.

### 5.7 Branch hygiene (never stale, never loose)

**Parker's rule (2026-04-17):** every branch on every private repo is in exactly one of two states:
1. **Active** ... has a worktree checked out, work is happening.
2. **Merged** ... renamed with `--merged-YYYY-MM-DD` suffix to mark it as history.

There is no third state. A branch that is merged but not renamed is a bug. A branch that is not merged, has no worktree, and has no commits in the last N days is also a bug (abandoned work).

**Problem:** today 200+ merged branches sit on origin with no `--merged-DATE` suffix. The rename runs only as step 10 of `wip-release patch`, so repos that go weeks between stable releases accumulate a large "merged but unlabeled" pile. Humans can run `tools/post-merge-rename/post-merge-rename.sh` manually, but no one remembers to.

**Fix:**
- **Rename on merge, not on release.** New GitHub Action in `wipcomputer/.github`: `wip-rename-on-merge.yml` reusable workflow, triggered by `pull_request.closed` with `merged: true`. Runs `post-merge-rename.sh` against just the merged branch, pushes the renamed ref, deletes the old ref. Zero human touch per merge.
- **Abandoned-branch scan.** `wip-release check` (from §5.3) extended to detect branches that are not merged, have no worktree, and have no commits in the last 30 days. Report them in the dry-run output so humans can decide: resume, rename as `--abandoned-DATE`, or keep as active.
- **`ldm doctor` branch-hygiene check** per repo: counts branches in each state and warns if any are in the "limbo" state (merged-but-not-renamed or not-merged-no-worktree-stale).
- **One-time cleanup on shipping:** `wip-release patch` step 10 still runs the batch rename as a safety net. Covers the existing 200-branch backlog when we ship v0.4.74 today.

**Acceptance:**
- After v0.4.74 ships, all 200 existing merged branches on `wip-ldm-os-private` have `--merged-2026-04-17` suffix (or the relevant date they were merged).
- Any PR merged after the GitHub Action is live → within 30 seconds the branch is renamed on origin.
- `ldm doctor` on any private repo reports 0 branches in limbo.
- `wip-release check` running on a PR that leaves stale branches flags them.

---

## 6. CI layers

Three layers, each a separate deliverable. Each layer requires the previous.

### Layer 1: Fail-closed release + rollback (inside devops-toolkit)

Deliverables: §5.1 + §5.2.

Proves that `wip-release` can never leave a repo in a half-released state, and that any bad release can be reversed.

### Layer 2: Per-PR smoke tests (shared CI)

Deliverables: §5.3 + §5.4.

Every PR in every private repo runs a 60-90 second check: lint, syntax, release-notes gate, `ldm install --dry-run`, minimal scenario (init → register → basic smoke). Block merge on red.

### Layer 3: Canary install loop (ephemeral runner)

Deliverables: `wip-canary.yml` reusable workflow (new).

On merge to private main, auto-publish alpha. Auto-install alpha on an ephemeral macOS runner. Run Layer 2 smoke scenario against the installed binary (not the repo source). Ping Parker red or green. Parker manually promotes alpha → beta → stable.

Goal: every alpha is validated before Parker ever installs it on a real machine.

---

## 7. Phased execution (in order)

### Phase A: Release what we have (unblock the backlog)

A1. Release LDM OS (`wip-ldm-os-private`) from v0.4.73-alpha.34 to v0.4.73 or v0.4.74 (stable). 23 commits of pending changes. Requires writing `RELEASE-NOTES-v*.md` first.

A2. Run `wip-release patch --dry-run` to preview. Review. Then real `wip-release patch`.

A3. Verify `deploy-public.sh` chain ran successfully, public repo is current, npm `@latest` tag points at the new version.

A4. Parker dogfoods: fresh install via `Read wip.computer/install/wip-ldm-os.txt`. Run `ldm doctor`, `ldm init` on a test repo. Catalog anything broken.

A5. For each breakage found in A4, file a bug under the appropriate `ai/product/bugs/<category>/` in this repo. These become the forcing function for Layer 1.

### Phase B: Ship Layer 1 (atomic release + rollback)

B1. Create a new bug file under `devops/wip-ai-devops-toolbox-private/ai/product/bugs/code/` for the atomicity work ... cross-link this plan.

B2. Implement §5.1 in a PR against `wip-ai-devops-toolbox-private`. Unit-test with simulated failures.

B3. Implement §5.2 `wip-release --rollback` in a follow-up PR.

B4. Release devops-toolkit through the old (pre-Layer-1) pipeline. Last release before the new machinery is active.

B5. Dogfood the rollback on a test release.

### Phase C: Ship Layer 2 (per-PR CI)

C1. Create `wipcomputer/.github` repo if it does not already exist (check org).

C2. Implement §5.3 `wip-release check` subcommand in devops-toolkit.

C3. Write `wip-ci.yml` in `wipcomputer/.github`.

C4. Add 5-line `.github/workflows/ci.yml` to `wip-ldm-os-private` as the pilot.

C5. Open a test PR in `wip-ldm-os-private`. Verify CI runs, green on clean, red on intentional break.

C6. Fan out: drop the same 5-line workflow into `memory-crystal-private` and `wip-ai-devops-toolbox-private`.

C7. Release devops-toolkit again (now it runs under its own CI).

### Phase C2: Ship installer doc sync (LDM OS, §5.6)

C2-1. Implement `ldm docs sync` subcommand in `bin/ldm.js` + hook non-destructive doc sync into `ldm install` post-install step.

C2-2. Implement `ldm docs status` + `ldm doctor` drift check.

C2-3. Write test fixtures: a user-edited deployed doc + a repo template update → verify prompt fires, diff displayed, merge options correct.

C2-4. Release LDM OS (Phase A's sibling: this is the first release that includes the new sync behavior). Update `shared/docs/*.tmpl` to be the canonical source.

C2-5. Dogfood: run `ldm docs status` on Parker's machines. Expect drift report. Run `ldm docs sync`. Expect clean state after.

### Phase D: Ship Layer 3 (canary install)

D1. Provision an ephemeral runner config. Options: GitHub-hosted macOS runner, or a Parker-owned Mac as self-hosted (faster but less reproducible).

D2. Write `wip-canary.yml` reusable workflow.

D3. Extend `wip-release alpha` to trigger the canary workflow via a repo dispatch event.

D4. Smoke scenario: install → `ldm init` in tmp → `crystal init` → remember a string → search for it → assert retrieval → exit.

D5. Run on LDM OS first. Once green on 3 consecutive runs, enable for memory-crystal and devops-toolkit.

### Phase E: Memory Crystal release + fan-out

E1. With Layers 1-3 live in LDM OS and devops-toolkit, apply to memory-crystal-private.

E2. Release memory-crystal stable (currently v0.7.34-alpha.5 → v0.7.34 stable).

E3. Verify full pipeline (CI green → merge → alpha auto-publish → canary install green → Parker promotes to public).

### Phase F: Fan out to remaining 15+ private repos

F1. Audit each per the 2026-04-17 session (dirty trees, unmerged branches).

F2. Clean + release each.

F3. Drop in the 5-line `ci.yml`. Wait for next PR to prove inheritance.

---

## 8. Acceptance criteria (the binary check for "done")

At the end of this work, the following must all be true:

1. A fresh user can install LDM OS + devops-toolkit with one command and ship a working release without reading three months of docs.
2. No `wip-release` invocation can leave a repo in a half-released state.
3. Any release can be rolled back with one command.
4. No PR can merge without a `RELEASE-NOTES-v*.md` file and a green CI run. PRs touching `src/` without updating docs fail the gate.
5. Every alpha auto-installs on a canary, runs a smoke scenario, and reports red or green before Parker sees it.
6. Changes to CI logic happen in one place and apply to all repos.
7. LDM OS release pipeline is the reference implementation. Memory Crystal and devops-toolkit follow the same pattern with minimal repo-specific config.
8. Installing a new version of LDM OS (or any extension with `shared/docs/`) non-destructively refreshes `~/wipcomputerinc/library/documentation/` and `~/.ldm/library/documentation/` from the packaged templates, prompting on user-edited conflicts and preserving user state on template removals.
9. `ldm docs sync` + `ldm docs status` + `ldm doctor` drift check all work and are documented.
10. Every branch on every private repo is in one of two states: active (worktree checked out) or merged (renamed `--merged-YYYY-MM-DD`). Zero branches in "merged-but-not-renamed" limbo at any point. Rename fires within 30 seconds of PR merge.

---

## 9. Sequencing rationale

Why LDM OS first, not devops-toolkit first, not memory-crystal first:

- **LDM OS = the kernel.** Memory Crystal's `crystal init` auto-bootstraps `@wipcomputer/wip-ldm-os`. If LDM OS is stale, every downstream install drifts from the current truth.
- **LDM OS is already clean.** 0 dirty files, 0 unmerged branches (verified 2026-04-17). The cheapest repo to release right now.
- **Dogfooding the release surfaces the real pain points** before we build the CI. Otherwise we are building CI for a pipeline we have not actually run in two weeks.
- **Devops-toolkit second because its own release uses itself.** Chicken-and-egg. Releasing it before LDM OS is fine structurally, but changes to the release tooling affect LDM OS next, so we want LDM OS released first so the Layer 1 changes in devops-toolkit can be tested against it.
- **Memory Crystal third because it depends on both** and benefits from the full pipeline being live.

---

## 10. Open decisions

**D1. Version numbering for the LDM OS release.**
- Option a: v0.4.73 (drop the alpha suffix ... "the alpha became stable").
- Option b: v0.4.74 (next patch number ... clean break from alpha).
- Recommendation: **(b)** v0.4.74. Cleaner semver, avoids any confusion about whether "v0.4.73 stable" is the same as "v0.4.73-alpha.34."

**D2. Canary runner: GitHub-hosted or self-hosted?**
- GitHub macOS: reproducible, clean every run, costs minutes.
- Self-hosted on Parker's MBA or a dedicated VM: faster feedback, drift-risk.
- Recommendation: **GitHub-hosted macOS** for Layers 1-2. Revisit self-hosted only if we hit runtime costs.

**D3. Release notes authorship for this LDM OS release.**
- Option a: Auto-generated from 23 commits (most are ai/ docs, some are code).
- Option b: cc-mini drafts narrative notes, Parker reviews.
- Recommendation: **(b)**. 23 commits warrant a paragraph of context ... "what changed and why" ... not just an auto-sum.

**D4. Where to file the Phase B + C follow-ups.**
- Option a: All under `wip-ldm-os-private/ai/product/bugs/release-pipeline/` (keep plan and sub-bugs together).
- Option b: `wip-ai-devops-toolbox-private/ai/product/bugs/code/` (where the code lives).
- Recommendation: **Plan here, implementation bugs in devops-toolkit.** This plan is the parent; sub-bugs link back to it.

**D5. Canary smoke scenario: how ambitious?**
- Option a: minimal (install + load CLI + print version).
- Option b: end-to-end (install + init + remember + search + assert).
- Recommendation: **(b) for Layer 3**. Layer 1-2 can stay at (a) for speed; Layer 3 is where we buy confidence.

**D6. `.github` repo: private or public?**
- GitHub treats `wipcomputer/.github` as the org-profile repo, which is public by default.
- Reusable workflows in a public repo are accessible to public consumers (fine for our use).
- If we want them private, we need a second repo or use the `.github-private` convention.
- Recommendation: **public `.github`** ... reusable workflows are not secret and having them public documents our conventions.

---

## 11. Risks

- **R1. Releasing LDM OS now may surface install breakage in the field.** Mitigation: v0.4.74 is a small patch, dogfood before deploy-public sync if possible. Rollback to v0.4.73-alpha.34 is viable since no public release has shipped since then.
- **R2. `wip-release` atomicity rewrite may introduce its own bugs.** Mitigation: implement behind a flag (`WIP_RELEASE_ATOMIC=1`), soak-test on devops-toolkit releases first, flip default after three clean runs.
- **R3. GitHub Actions ephemeral runner may not match real user environments.** Mitigation: canary runs macOS-only to match Parker's machines; Linux/Windows support is a separate follow-up.
- **R4. Shared workflows in `wipcomputer/.github` are a single point of failure.** Mitigation: pin workflow version in consumer `ci.yml` (`@main` → `@v1.0`) once stable to prevent accidental global breakage.
- **R5. Scope creep.** This plan covers five updates and three layers. It is tempting to add "and also fix X." Resist. File new bugs for adjacent work.

---

## 12. Explicit out-of-scope for this plan

- License-guard, file-guard, repo-permissions-hook internals (separate bugs).
- Non-npm release targets (cargo, pip, gem, etc.).
- Public marketplace submissions (Anthropic, OpenAI).
- Migration of old feature branches to the post-merge-rename convention (already running).
- `.claude/` or `~/.ldm/` installer state refactor (separate bug series).

---

## 13. References

**Session transcript:** 2026-04-17, conversation between Parker and cc-mini leading to this plan. Covers the release cadence problem, the alpha-vs-public drift, the orphan version bumps in devops-toolkit, the architecture decision, the five concrete updates, and the phased execution.

**Existing planning docs:**
- `ai/product/bugs/release-pipeline/2026-04-05--cc-mini--release-pipeline-master-plan.md`
- `ai/product/bugs/release-pipeline/2026-04-06--cc-mini--shared-universal-config-layer.md`
- `ai/product/bugs/release-pipeline/2026-04-08--cc-mini--silent-skip-without-license-guard-config.md`
- `ai/product/bugs/master-plans/2026-04-09--cc-mini--master-plan-004-execution-order.md`
- `ai/product/product-ideas/vision-quest-01/priorities-2026-04-16.md` (which includes CI/release pipeline in the 4-12 week horizon)

**Tooling source (devops-toolkit):**
- `tools/wip-release/core.mjs` ... release pipeline, release-notes gate at :309-315, three-source priority, atomic root-files update
- `tools/wip-release/SKILL.md` ... four-track documentation
- `tools/deploy-public/deploy-public.sh` ... public sync, alpha block at :55-61
- `tools/wip-branch-guard/guard.mjs` ... main-branch commit block
- `DEV-GUIDE-GENERAL-PUBLIC.md` ... documented workflow

**LDM OS:**
- `bin/ldm.js` ... `ldm init`, `ldm install`, `ldm doctor`, `ldm status`
- `shared/` ... templates deployed by `ldm install`
- `package.json` ... currently at v0.4.73-alpha.34

---

## 14. Immediate next action

When this plan is merged, proceed to **Phase A1**: draft `RELEASE-NOTES-v0-4-74.md` covering the 23 commits, then `wip-release patch --dry-run` on `wip-ldm-os-private`.

---

*cc-mini, 2026-04-17. Written as a durable record so future-Parker and future-cc-mini can answer "did we do this?" against a concrete artifact instead of session memory.*
