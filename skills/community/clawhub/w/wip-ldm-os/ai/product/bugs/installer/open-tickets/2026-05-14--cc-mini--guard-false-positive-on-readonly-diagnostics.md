---
title: "Branch/file guard fires false-positive on read-only shell diagnostic commands (cat, grep, head, tail, jq)"
status: open
priority: P3
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private (bug doc only); fix lives in wip-branch-guard / wip-file-guard
created: 2026-05-14
---

## What it does

Read-only shell diagnostic commands (`cat <single-arg-no-redirect>`, `grep`, `head`, `tail`, `jq` with no write flag or redirect) do not trigger guard rules intended to block destructive operations. Arbitrary inline-code execution (`python3 -c`, `node -e`, `bash -c`, heredocs) remains subject to the guard; substring-based "looks safe" checks on inline code are fundamentally bypassable. JSON inspection should prefer safe shell shapes (`jq`) or a dedicated read-only helper, not inline code.

## What it fixes

2026-05-14 alpha.30 dogfood: during install-state inspection, attempting `python3 -c "import json; ..."` to read `~/.ldm/registry.json` triggered "BLOCKED: Code execution bypass detected." Attempting `cat ~/.ldm/...` for a related path triggered a destructive-command rule. Both are read-only inspections. The guard pattern is over-broad: it pattern-matches on the substring (e.g., a path or a `-c` flag) without distinguishing read from write.

User-facing impact: agents debugging installer state get blocked from basic inspection. Workaround is rephrasing the command, but the false positive erodes guard trust and slows down legitimate read-only diagnostic work.

## How to dogfood

1. From an agent session, run `cat ~/.ldm/registry.json`. Should NOT block.
2. From an agent session, run `jq '.extensions | keys' ~/.ldm/registry.json`. Should NOT block.
3. From an agent session, run `grep some-pattern ~/.ldm/registry.json`. Should NOT block.
4. Confirm destructive shell variants still block: `cat <input> > /protected/file`, `grep --write-files some-pattern <file>`, etc.
5. Confirm inline code execution stays guarded: `python3 -c "print(1)"` should still trigger the guard (or require explicit per-run approval), even though it's trivially read-only. The guard's contract is: command shape, not substring intent.

## Problem

The guard's "destructive command" and "code execution bypass" pattern matchers fire on substring presence (e.g., `-c`, a path containing a flagged substring) rather than on intent. Read-only inspection commands look superficially similar to destructive commands, so they get caught in the same rule.

Two patterns flagged in the 2026-05-14 dogfood:

- `python3 -c "<expression>"` triggered "Code execution bypass detected." Even read-only expressions match the rule.
- `cat <path>` triggered a destructive-command rule when the path contained a substring the rule pattern-matched against.

## Fix

Guard's matcher should:

1. **Allowlist read-only shell forms by command shape**, not by substring. The canonical read-only inspection shapes are:
   - `cat <single-arg-with-no-redirect>` (no `>`, `>>`, pipe to write).
   - `grep <pattern> <files>` with no `--write-files` or redirect.
   - `head <file>` / `tail <file>` with no redirect.
   - `jq <expr> <file>` (read-only by default; no `> /file` redirect).

2. **Do NOT broadly allowlist arbitrary inline-code execution.** `python3 -c`, `node -e`, `bash -c`, heredocs, `eval`, etc. stay subject to the guard because substring-based "is this safe inline code?" checks are fundamentally bypassable. Inline code that can write/spawn/import filesystem APIs remains blocked or requires explicit per-run user approval.

3. **For JSON inspection**, prefer safe shell shapes (`jq`, `cat | head`) or a dedicated read-only helper (e.g., a wrapper that reads JSON and prints without `eval`). Do not allowlist `python3 -c` for "reading JSON"; the same shape can do anything.

4. **Pattern-match on intent through command shape, not substring.** The matcher checks the parsed command structure (executable, args, redirects, pipes) against a small set of canonical read-only shapes.

## Acceptance

- Read-only shell diagnostic commands (`cat`, `grep`, `head`, `tail`, `jq` with no redirect/write flags) do not trigger guard false positives.
- Inline-code execution shapes (`python3 -c`, `node -e`, `bash -c`, heredocs) remain subject to the guard. Substring-based "looks safe" patterns explicitly NOT used.
- Test suite has three groups:
  - **Happy path**: each allowlisted shell shape passes without block.
  - **Destructive shell variants**: `cat <input> > <output>`, `grep --write-files`, etc., still block.
  - **Inline code**: `python3 -c "print(1)"` (trivially read-only) still blocked or requires explicit approval; `python3 -c "open('/x','w').write('')"` blocked; explicit user-approved inline code allowed via existing per-run approval path.

## Out of scope

- Re-architecting the guard's rule engine. Scoped fix: pattern-match on intent for the specific false-positive shapes named above.
- Removing the guard from agent workflows. It's working as designed for actual destructive operations; the goal is to reduce false positives on read-only diagnostics.

## Cross-repo note

The bug doc lives here per the "bug docs only live in `wip-ldm-os-private/ai/product/bugs/`" rule. The actual fix lands in `wip-branch-guard` and/or `wip-file-guard` (sub-tools of `wip-ai-devops-toolbox-private`). The fixing agent should propose the change there once the requirement is agreed.

## Related

- `2026-05-14--cc-mini--wip-release-bundled-subtool-version-bump.md` (sibling; same publish-hygiene pattern affects the same toolbox sub-tools where this guard lives).
- Surfaced by 2026-05-14 alpha.30 dogfood.
