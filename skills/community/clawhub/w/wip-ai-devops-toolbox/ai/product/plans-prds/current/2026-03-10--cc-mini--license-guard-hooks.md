# Plan: License Guard Hooks + Release Gate

**Date:** 2026-03-10
**Author:** cc-mini
**Repo:** wip-ai-devops-toolbox-private

## Goal

Make license compliance automatic. Nobody should have to remember to run license-guard. It should block bad commits and bad releases the same way file-guard blocks identity file overwrites.

---

## Phase 1: Claude Code Hook

**Problem:** license-guard exists but is manual. You have to remember to run it. That means it doesn't get run.

**What to build:**
- CC Hook for license-guard, same pattern as `wip-file-guard/guard.mjs`
- Triggers on pre-commit or pre-push (whichever makes more sense for the check cost)
- Checks: LICENSE file exists, copyright matches config, CLA.md exists, README has license section
- Blocks the commit/push if any check fails
- Clear error message telling you what's wrong and how to fix it (`wip-license-guard check --fix`)

**Reference:** `tools/wip-file-guard/guard.mjs` for the hook pattern

**Status:** DONE. hook.mjs existed but was not wired. Fixed 2026-03-16: renamed to guard.mjs (matches deploy convention), added claudeCode.hook to package.json. Will register on next ldm install.

---

## Phase 2: wip-release Gate

**Problem:** You can release a repo that has wrong or missing licensing. wip-release doesn't check.

**What to build:**
- Step 0 in wip-release: run license-guard check before doing anything else
- If license-guard fails, abort the release with a clear message
- `--skip-license-check` escape hatch for edge cases (but warn loudly)

**Status:** DONE

---

## Phase 3: Repo Template / Standard Defaults

**Problem:** `wip-license-guard init` is interactive. For WIP Computer repos, the answers are always the same: copyright "WIP Computer, Inc.", license "MIT+AGPL", current year.

**What to build:**
- `wip-license-guard init --from-standard` flag that applies WIP Computer defaults without prompting
- Generates: `.license-guard.json`, `LICENSE` (dual MIT+AGPLv3), `CLA.md`, README license section
- Could also be part of a broader repo scaffolding command later

**Status:** DONE

---

## Done criteria

- [x] License-guard runs automatically on every commit/push via CC Hook
- [x] wip-release refuses to release if license-guard fails
- [x] New repos can be set up with one command (`wip-license-guard init --from-standard`)
- [ ] All WIP Computer repos get the same dual-license + CLA standard enforced automatically (requires running `wip-license-guard init --from-standard` across all repos)
