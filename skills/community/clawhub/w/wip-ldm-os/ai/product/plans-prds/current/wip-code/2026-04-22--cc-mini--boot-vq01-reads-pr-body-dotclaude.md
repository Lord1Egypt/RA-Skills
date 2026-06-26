# PR Body: `.claude` CLAUDE.md Level 1 VQ01 Boot Reads

**Date:** 2026-04-22
**Author:** cc-mini (with Parker)
**Repo:** `wipcomputer-ldmos-wipcomputerinc-dot-claude-private`
**Branch:** `cc-mini/boot-vq01-reads`
**PR:** [#8](https://github.com/wipcomputer/wipcomputer-ldmos-wipcomputerinc-dot-claude-private/pull/8)

## Summary

Adds `kaleidoscope-executive-brief-v02.md` and `architecture-spec.md` as mandatory reads (steps 10 and 11) in the Dream Weaver Boot Sequence in `~/.claude/CLAUDE.md` (Level 1 global).

Fires for any session touching memory, bridge, Kaleidoscope, Memory Crystal, or agent IDs. Without these, a session lands without the product frame and proposes architecture that is already designed and shipped. This is how 2026-04-22 started.

## Aligned with plan docs

- `wip-ldm-os-private/ai/product/plans-prds/current/wip-code/2026-03-27--cc-mini--single-source-of-truth-reversed.md` ... additive to Level 1 (no trimming until Levels 2 + 3 are proven)
- `wip-ldm-os-private/ai/product/plans-prds/current/wip-code/2026-04-03--cc-mini--cwd-compaction-bug-journal.md` ... even when CWD drifts post-compaction, the global CLAUDE.md still directs the session to load VQ01 before any surface-area work

## Change

One additive block after the LDM OS boot steps:

```
10. /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/product-ideas/vision-quest-01/kaleidoscope-executive-brief-v02.md
11. /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/product-ideas/vision-quest-01/architecture-spec.md
```

Plus a one-paragraph "Without these..." note and cross-references to the two plan docs.

## Test plan

- [ ] Open a fresh CC session somewhere unrelated (e.g. a different project)
- [ ] Verify the boot sequence in `~/.claude/CLAUDE.md` lists VQ01 as steps 10 and 11
- [ ] Verify the paths resolve (the files exist at the absolute paths given)
- [ ] Confirm next WIP-surface session loads them
