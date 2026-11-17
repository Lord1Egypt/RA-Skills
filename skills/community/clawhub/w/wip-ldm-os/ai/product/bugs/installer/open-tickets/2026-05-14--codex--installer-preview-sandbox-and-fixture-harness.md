---
title: "Installer preview sandbox and fixture harness"
status: open
priority: P1
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-14
---

# Installer preview sandbox and fixture harness

## What it does

Adds one shared LDM OS installer environment layer that can run the real installer against cloned or synthetic AI OS state before touching live state.

There are two user-visible forms:

1. **Fixture harness** for coder and CI validation: create temp `HOME` / `LDM_ROOT` states that reproduce known legacy bugs, then run real `ldm install`, `ldm status`, and `ldm doctor` against them.
2. **Preview sandbox** for Parker dogfood and future users: copy the relevant parts of the current machine into a temp sandbox, apply the planned install or doctor mutation there, and show the before/after diff before live mutation.

## What it fixes

The alpha.28 -> alpha.29 -> alpha.30 installer loop exposed a structural test gap:

- alpha.28 cleanup ran but dedup reverted because duplicate directories remained under `~/.ldm/extensions/`.
- alpha.30 moved duplicate directories to `~/.ldm/_trash/`, but orphan hook entries remained in agent settings.
- `ldm doctor --fix` then hit a separate `src.startsWith is not a function` crash path.
- `ldm doctor` also reported a mismatch between counted issues and visible warnings.
- The install prompt let different AIs probe different package sets, producing a five-minute Codex run and a one-minute Claude Code run from the same prompt.

Those are not one repeated bug. They are multiple state surfaces being discovered on Parker's production machine because no pre-dogfood environment reproduces Parker-like legacy state.

The missing product answer is: "show me what will happen to my AI OS files before you rewrite, move, or fix them."

## Why this is a bug, not a product PRD

This is not a new app and not a greenfield product. It is a safety and correctness gap in the existing LDM OS installer contract.

`ldm install`, `ldm status`, and `ldm doctor` already mutate and report on:

- `~/.ldm/`
- `~/.ldm/extensions/registry.json`
- `~/.ldm/extensions/*`
- `~/.ldm/_trash/`
- `~/.claude/settings.json`
- `~/.openclaw/openclaw.json`
- `~/.ldm/agents/*/settings.json`
- LaunchAgent and cron-related health state

When the installer says it will rewrite or move any of those files, the expected behavior is not reassurance. The expected behavior is a reproducible sandbox proof and a diff.

## Ownership boundary

This lives in **LDM OS**, not in a new app and not primarily in AI DevOps Toolbox.

LDM OS owns:

- path resolution for `HOME`, `LDM_ROOT`, `.ldm`, `.claude`, and `.openclaw`
- extension registry schema and migrations
- install/update lifecycle
- `ldm status`, `ldm doctor`, `ldm install --dry-run`
- preview sandbox and fixture harness
- hook and MCP registration mechanics
- safe move, backup, revert, and `_trash` behavior
- user-facing "what will happen to my machine?" reporting

AI DevOps Toolbox owns:

- tool behavior, such as `wip-release`, `wip-repos`, guards, license tools, repo init, README formatting, and deploy-public
- product-specific metadata for its own tools
- upstream publish hygiene and guard false-positive bugs

The boundary is:

```text
Tool behavior belongs to DevOps Toolbox.
Deployment of tools into the user's AI operating system belongs to LDM OS.
```

`wip-install` in DevOps Toolbox is a standalone fallback. When LDM OS exists, it should delegate preview, install, status, and doctor behavior to `ldm`. It should not become a second owner of sandboxing or AI OS mutation.

## Proposed implementation

Add these LDM OS modules:

- `lib/installer-environment.mjs`: central path resolver for `HOME`, `LDM_ROOT`, `LDM_EXTENSIONS`, registry path, version path, `.claude`, `.openclaw`, agent settings, state, logs, and `_trash`. It must support an explicit `LDM_ROOT` override for tests and sandbox runs.
- `lib/installer-fixtures.mjs`: creates temp homes seeded from JSON fixtures and small directory templates. Used by test scripts and future CI.
- `lib/installer-preview-sandbox.mjs`: copies relevant live state into a temp sandbox, runs the requested install or doctor mutation there, captures before/after state, and prints a human-readable diff.

Add fixture data under:

```text
scripts/fixtures/installer/
```

Initial fixtures:

- `alpha28-dedup-reverts`: duplicate registry rows plus duplicate extension directories.
- `alpha30-orphan-hooks`: dedup directory move plus `.claude/settings.json` stale hook references.
- `doctor-startsWith-crash`: LaunchAgent plist drift or equivalent fixture that exercises the crashing fix path.
- `status-dryrun-discrepancy`: registry state where `ldm status` and `ldm install --dry-run` must report the same update set.
- `toolbox-bundled-parent-pin`: toolbox parent plus sub-tool content/version state where parent registry pin must update with deployed content.

Add commands:

```bash
ldm install --preview-sandbox
ldm doctor --preview-fix
```

Optional coder-only test command, if useful:

```bash
ldm install --fixture alpha28-dedup-reverts
```

If adding a public `--fixture` flag risks confusing users, keep fixture execution in `scripts/test-installer-fixtures.mjs` and expose only preview-sandbox commands through `ldm`.

## Acceptance

- `bin/ldm.js` and installer libraries use one environment resolver instead of each file hardcoding `join(HOME, ".ldm")` in its own way.
- Tests can run real `node bin/ldm.js install`, `status`, and `doctor` against a temp `HOME` and explicit temp `LDM_ROOT` without touching the operator's real `~/.ldm`, `~/.claude`, or `~/.openclaw`.
- The alpha.28 dedup-reverts fixture fails before the dedup-trash fix and passes after it.
- The alpha.30 orphan-hook fixture fails before the hook-config cleanup and passes after it.
- A fixture covers at least one skipped-file path: malformed JSON or unsupported settings shape produces a clear warning and no partial mutation.
- `ldm install --preview-sandbox` clones relevant live state to a temp directory, applies the install plan there, and prints a summary of files changed, directories moved, registry keys changed, settings entries removed/remapped, and protected files untouched.
- `ldm doctor --preview-fix` does the same for doctor fixes.
- Preview sandbox output includes the sandbox path and explicitly says the real machine was not changed.
- Preview sandbox output is clear enough that an AI following the install prompt can summarize what will be preserved, moved to `_trash`, rewritten, or left alone.
- No secrets are copied unless explicitly needed for the tested mutation. If a secret-bearing file is required for shape, the sandbox redacts secret values before writing or reporting.
- DevOps Toolbox `wip-install` remains a fallback and delegates to `ldm` for preview/install when LDM OS is present. Any direct mutation behavior left in `wip-install` is documented as emergency fallback only.

## Out of scope

- Building a separate app or UI.
- Rewriting every installer mutation in one PR.
- Moving DevOps Toolbox tools into LDM OS. The tools stay in DevOps. The installer-owned mutation and preview mechanics live in LDM OS.
- Fixing every current Phase 1 or Phase 2 installer bug. This ticket provides the harness those fixes should use.

## Related

- `ldmos-bugs-masterticket--installer.md`
- `ldmos-bugs-operating-procedure--installer-coder.md`
- `2026-05-13--cc-mini--installer-dedup-reverts-between-installs.md`
- `2026-05-14--cc-mini--installer-dedup-orphans-hook-configs.md`
- `2026-05-14--cc-mini--ldm-doctor-fix-crash-startsWith.md`
- `2026-05-14--cc-mini--ldm-doctor-issue-count-vs-visible-mismatch.md`
- `2026-05-14--cc-mini--installer-skill-efficient-probe-rules.md`
- AI DevOps Toolbox fallback installer: `devops/wip-ai-devops-toolbox-private/tools/wip-universal-installer/install.js`
