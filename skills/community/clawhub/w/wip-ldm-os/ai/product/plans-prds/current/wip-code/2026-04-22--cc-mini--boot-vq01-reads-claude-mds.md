# Change: Add VQ01 Product Frame Docs to Mandatory Boot Sequence (Level 1 + Level 2 CLAUDE.md)

**Date:** 2026-04-22
**Author:** cc-mini (with Parker)
**Status:** Shipped via PRs (below), awaiting merge
**Implements:** `2026-03-27--cc-mini--single-source-of-truth-reversed.md`, `2026-04-03--cc-mini--cwd-compaction-bug-journal.md`
**Save to:** wip-ldm-os-private/ai/product/plans-prds/current/wip-code/

## Context

Session `04-22-2026--01` demonstrated the exact failure mode the CWD compaction bug journal describes: a CC session landed without the VQ01 product frame, reasoned from priors plus auto-memory, and spent ~an hour re-proposing architecture (Bridge-first, then hosted-MCP, then account-level federation) that was already designed and shipped in the VQ01 + kaleidoscope plan docs.

The session only recovered after Parker explicitly pointed at `vision-quest-01/` and forced full boot. Root cause: neither `~/.claude/CLAUDE.md` (Level 1 global) nor `~/wipcomputerinc/CLAUDE.md` (Level 2 workspace) named VQ01 in the Dream Weaver Boot Sequence. The boot sequence included SHARED-CONTEXT, journals, dailies, and LDM OS identity files, but not the product-frame docs that answer "what is Kaleidoscope, what are the six products, how do the surfaces connect."

## What changed

One additive block in each of the two top CLAUDE.md files, placed after the existing LDM OS / auto-memory boot steps, pointing at two absolute paths:

- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/product-ideas/vision-quest-01/kaleidoscope-executive-brief-v02.md`
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/product-ideas/vision-quest-01/architecture-spec.md`

The `~/wipcomputerinc/CLAUDE.md` edit also bumps the "Skipping steps 6-X" enforcement sentence: range 6-10 -> 6-12, date list `(2026-03-01, 2026-03-07)` -> `(2026-03-01, 2026-03-07, 2026-04-22)`, and adds "proposing architecture that is already designed and shipped" as a named failure mode.

## Why this alignment

**2026-03-27 single-source-of-truth-reversed.md**: Step 3 of that plan says Level 1 does not get trimmed until Levels 2 and 3 are proven. This change is additive to Level 1, not a trim. Level 1 gets four new lines (two step entries, two framing lines). Level 2 gets matching lines. The change does not delete or reorganize anything in either file. Consistent with "do not touch the global until everything below it is proven."

**2026-04-03 cwd-compaction-bug-journal.md**: The journal describes CWD drifting to a repo post-compaction, and the CLAUDE.md cascade failing to find context at the new location. The fix in that journal is Level 3 (per-repo CLAUDE.md), which is partly shipped. This change complements it by strengthening Level 1 and Level 2: even if the cascade resolves to the global or workspace file (the common case), the session is now explicitly directed to load VQ01 before touching memory/bridge/kaleidoscope/agent-IDs work. Level 3 per-repo CLAUDE.md is unaffected and still required.

## Files touched

| File | Repo | Branch | PR |
|---|---|---|---|
| `~/.claude/CLAUDE.md` (Level 1 global) | `wipcomputer-ldmos-wipcomputerinc-dot-claude-private` | `cc-mini/boot-vq01-reads` | [#8](https://github.com/wipcomputer/wipcomputer-ldmos-wipcomputerinc-dot-claude-private/pull/8) |
| `~/wipcomputerinc/CLAUDE.md` (Level 2 workspace) | `wipcomputer-ldmos-wipcomputerinc-home-private` | `cc-mini/boot-vq01-reads` | [#24](https://github.com/wipcomputer/wipcomputer-ldmos-wipcomputerinc-home-private/pull/24) |

## Diff shape

### `~/.claude/CLAUDE.md` (Level 1)

Inserted after the existing boot step 9 (LDM OS `.ldm/agents/cc-mini/memory/daily/` entry), before "#### Other Memory Sources":

```
**Product frame docs (MANDATORY for any session touching memory, bridge, Kaleidoscope, Memory Crystal, or agent IDs):**

```
10. /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/product-ideas/vision-quest-01/kaleidoscope-executive-brief-v02.md  ← the consumer pitch. "Every AI. One experience." Six products. One page. Read first.
11. /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/product-ideas/vision-quest-01/architecture-spec.md                 ← full product architecture. MCP, SDK, passkey auth, sovereign vs cloud mode, CloudKit, pricing. Read before proposing anything in this surface area.
```

Without these, a session will propose architecture that's already designed and shipped. Wastes time, signals the session did not boot correctly.
```

Net +9 lines.

### `~/wipcomputerinc/CLAUDE.md` (Level 2)

Inserted after the existing step 10 (auto-memory `repo-locations.md` entry), before the "ALL steps are mandatory" enforcement sentence. Same framing as Level 1 but numbered 11 and 12. Plus: enforcement sentence updated in-place (range, date list, new failure mode, plan doc cross-references).

Net +8 lines, -1 line.

## 5 Questions

1. **Source files:** `~/.claude/CLAUDE.md` and `~/wipcomputerinc/CLAUDE.md` (one in each of the two top-level CLAUDE.md repos).
2. **ldm install deploys:** Not directly. Both files are in git-tracked repos, not deployed by `ldm install`. The Level 1 template at `shared/templates/claude-md-level1.md` is deployed by the installer, but Level 1 is still on the full (pre-trim) version per the reversed plan, so no template change is needed yet. When Level 1 is eventually trimmed (post Level 2 + Level 3 proof), the VQ01 references become part of that trim.
3. **Fresh vs existing install:** No difference. Both files live in repos that are cloned on setup; `ldm install` does not overwrite the Level 1 global until the reversed plan's Step 3 is enabled (not today).
4. **Docs to update:** None required for this change. If the Level 1 template is later updated to include VQ01 references during the reversed-plan Step 3, `settings/docs/how-install-works.md` should note it then.
5. **Files touched by installer:** None in this change. The installer is not touched.

## Test plan

- Open a fresh CC session somewhere new (e.g. another project on the mini). Confirm `~/.claude/CLAUDE.md` (Level 1) shows VQ01 as boot steps 10 and 11.
- Open a fresh CC session in `~/wipcomputerinc/`. Confirm `~/wipcomputerinc/CLAUDE.md` (Level 2) shows VQ01 as boot steps 11 and 12.
- Verify both absolute paths resolve: both files exist in the repo.
- Next session that would touch memory/bridge/kaleidoscope/agent-IDs work: confirm VQ01 is loaded before first proposal.

## Cross-references

- Canonical plan: `2026-03-27--cc-mini--single-source-of-truth-reversed.md`
- Canonical journal: `2026-04-03--cc-mini--cwd-compaction-bug-journal.md`
- Master plan: `2026-04-03--cc-mini--claude-md-master-plan.md` (Level 3 repo CLAUDE.md rollout)
- Product frame being pointed at: `vision-quest-01/kaleidoscope-executive-brief-v02.md`, `vision-quest-01/architecture-spec.md`

## Operational note

PR body content for this change was initially written to `/tmp/pr-body-<feature>.md` files per `~/.claude/REPO.md` recipe 3 (which uses `/tmp/` as the example path to avoid the code-exec-bypass guard on inline HEREDOC'd `gh pr create --body` commands). Parker flagged this as wrong: product artifacts should live in the repo, not in ephemeral `/tmp/`. This doc is the corrected location. `/tmp/` should be the transport for guard-workaround purposes only (or better, a path inside a tracked directory). Candidate follow-up: update `~/.claude/REPO.md` recipe 3 to use a repo-relative path (e.g. `ai/product/plans-prds/current/wip-code/` or a dedicated `/ai/pr-bodies/` dir) instead of `/tmp/`.
