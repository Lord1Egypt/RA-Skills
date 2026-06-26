# Bug: Three Over-Reach Docs Sitting in `plans-prds/current/wip-code/`

**Date:** 2026-04-22
**Filed by:** cc-mini (with Parker)
**Repo:** `wip-ldm-os-private` (both manifests and filing location)
**Priority:** low
**Status:** fix proposed, not yet shipped

## Summary

Three docs were added to `ai/product/plans-prds/current/wip-code/` on 2026-04-22 that describe work already completed. They belong in archive, not `current/`. Keeping them in `current/` pollutes the active-work folder and makes it harder to see what is actually open.

## The three files

On main in `wip-ldm-os-private`:

```
ai/product/plans-prds/current/wip-code/2026-04-22--cc-mini--boot-vq01-reads-claude-mds.md           (7587 bytes)
ai/product/plans-prds/current/wip-code/2026-04-22--cc-mini--boot-vq01-reads-pr-body-dotclaude.md    (1945 bytes)
ai/product/plans-prds/current/wip-code/2026-04-22--cc-mini--boot-vq01-reads-pr-body-wipcomputerinc.md (2112 bytes)
```

## What they are

All three describe one already-shipped change: adding VQ01 product frame docs as mandatory reads in the Dream Weaver Boot Sequence in `~/.claude/CLAUDE.md` (Level 1) and `~/wipcomputerinc/CLAUDE.md` (Level 2). That work shipped via two PRs (both merged to main on 2026-04-22):

- `wipcomputer-ldmos-wipcomputerinc-dot-claude-private` PR #8
- `wipcomputer-ldmos-wipcomputerinc-home-private` PR #24

The three docs:

1. `boot-vq01-reads-claude-mds.md` ... a consolidated change record for both PRs.
2. `boot-vq01-reads-pr-body-dotclaude.md` ... the PR #8 body text, saved as a file.
3. `boot-vq01-reads-pr-body-wipcomputerinc.md` ... the PR #24 body text, saved as a file.

## Why this is a bug

`ai/product/plans-prds/current/wip-code/` is for active plans. Post-ship artifacts accumulating there breaks the "what is actually open" signal.

The two PR body files are also redundant by design: the GitHub PR pages already store those bodies. A second copy on disk is duplication.

## Proposed fix

Move all three files to an archive location. Do not delete. `git mv` only.

Suggested archive path (Parker to confirm before the move):

```
ai/product/plans-prds/archive/wip-code/2026-04-22--cc-mini--boot-vq01-reads-claude-mds.md
ai/product/plans-prds/archive/wip-code/2026-04-22--cc-mini--boot-vq01-reads-pr-body-dotclaude.md
ai/product/plans-prds/archive/wip-code/2026-04-22--cc-mini--boot-vq01-reads-pr-body-wipcomputerinc.md
```

If `ai/product/plans-prds/archive/` does not exist yet, creating it is in scope of this fix.

## Steps

1. Confirm archive path convention with Parker (sibling `archive/` under `plans-prds/`, or per-category `wip-code/archive/`, or something else).
2. Create worktree on `wip-ldm-os-private`.
3. `git mv` all three files from `plans-prds/current/wip-code/` to the confirmed archive path.
4. Commit. Push. PR.
5. Merge. Pull main.
6. Verify: `ls ai/product/plans-prds/current/wip-code/` no longer shows the three files; `ls` on the archive path shows them.

## Verification

After landing:

```bash
# Files gone from current/
ls ~/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/wip-code/ | grep 'boot-vq01-reads'
# expected: no output

# Files present in archive/
ls ~/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/archive/wip-code/ | grep 'boot-vq01-reads'
# expected: three files listed

# Git history preserved
git log --follow -- ai/product/plans-prds/archive/wip-code/2026-04-22--cc-mini--boot-vq01-reads-claude-mds.md
# expected: original create + move visible in history
```

## Done when

- Three files are at `ai/product/plans-prds/archive/wip-code/` (or the confirmed archive path).
- `current/wip-code/` no longer contains them.
- This bug file is moved to `ai/product/bugs/dot-claude/archive/`.

## Co-authors

- Parker Todd Brooks
- Lēsa
- Claude Opus 4.7 (1M context)
