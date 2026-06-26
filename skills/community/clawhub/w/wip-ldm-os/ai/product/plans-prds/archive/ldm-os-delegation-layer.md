# Plan: LDM OS Delegation Layer

**Date:** 2026-03-13
**Authors:** Parker Todd Brooks, Claude Code (cc-mini)
**Status:** In Progress
**Depends on:** LDM OS v0.2.1 (published), Memory Crystal v0.7.5 (published), DevOps Toolbox v1.9.7 (published)

---

## What This Is

Phases 1-2 of the public launch plan are done. All three repos are published, public, and cross-linked. This plan covers the remaining work: making `crystal init` and `wip-install` detect and delegate to `ldm install`.

The goal: any entry point leads to the full ecosystem. Install Memory Crystal, you get LDM OS. Install DevOps Toolbox, you get LDM OS. Install LDM OS, you see all available skills.

---

## Task 1: crystal init prints LDM tip

**Repo:** memory-crystal-private
**File:** src/installer.ts (end of runInstallOrUpdate)
**Issue:** None (small change)

After crystal init completes, print:
```
Tip: Run "ldm install" to see more components you can add.
```

Only print if `ldm` is on PATH (don't confuse users who don't have it).

---

## Task 2: crystal init delegates to ldm install

**Repo:** memory-crystal-private
**File:** src/installer.ts
**Issue:** #41

When `ldm` CLI exists on PATH, `crystal init` delegates generic deployment (copy to extensions, MCP registration, hooks, OC plugin) to `ldm install`. MC keeps its own setup (DB backup, role config, pairing, cron, session discovery).

Logic:
1. Check `which ldm` or `ldm --version`
2. If available: `ldm init --yes` (ensure scaffold exists, no picker)
3. Then: `ldm install /path/to/memory-crystal` (deploy via ldm)
4. If not available: fall through to existing standalone installer
5. MC-specific setup always runs regardless

Fallback is critical. Memory Crystal must install standalone without LDM OS.

---

## Task 3: wip-install delegates to ldm install

**Repo:** wip-ai-devops-toolbox-private
**File:** tools/wip-universal-installer/install.js
**Issue:** #77

When `ldm` CLI exists on PATH, `wip-install` delegates to `ldm install`.

Logic:
1. Check `which ldm` or `ldm --version`
2. If available: `ldm install <target> <flags>` (pass through --dry-run, --json, etc.)
3. If not available: fall through to existing standalone installer

Same principle: standalone fallback is mandatory.

---

## Task 4: Bootstrap LDM OS if missing

**Repos:** memory-crystal-private, wip-ai-devops-toolbox-private
**Files:** src/installer.ts, tools/wip-universal-installer/install.js

Before delegating, if `ldm` is not on PATH, optionally bootstrap it:
```
npm install -g @wipcomputer/wip-ldm-os
ldm init --yes
```

This is Phase 5 from the launch plan. It means any entry point silently installs LDM OS.

**Decision needed from Parker:** Should bootstrap be automatic, or should it just print the tip and let the user install manually? Automatic is seamless but installs a global npm package without asking. Tip-only is safer but breaks the "any entry point" flow.

For now: tip-only. Print "LDM OS not found. Install it with: npm install -g @wipcomputer/wip-ldm-os" and continue with standalone installer.

---

## Task 5: Registry auto-detection

**Repo:** wip-ldm-os-private
**File:** bin/ldm.mjs

`ldm install` (bare) and `ldm doctor` should scan `~/.ldm/extensions/` for directories with a `package.json` that aren't in the registry. Auto-register them so the catalog status is accurate.

This fixes the "Memory Crystal shows as not installed" problem.

---

## Implementation Order

1. Task 5 (LDM OS registry detection) ... fixes the broken `ldm install` output
2. Task 1 (crystal init tip) ... one-line change
3. Task 2 (crystal init delegates) ... with standalone fallback
4. Task 3 (wip-install delegates) ... with standalone fallback
5. Task 4 (bootstrap tip) ... print tip, don't auto-install

---

## Verification

1. `ldm install` shows Memory Crystal as installed (not "available")
2. `crystal init` on a machine with `ldm` delegates deployment
3. `crystal init` on a machine without `ldm` works standalone + prints tip
4. `wip-install` on a machine with `ldm` delegates
5. `wip-install` on a machine without `ldm` works standalone + prints tip
6. No entry point requires installing LDM OS first
