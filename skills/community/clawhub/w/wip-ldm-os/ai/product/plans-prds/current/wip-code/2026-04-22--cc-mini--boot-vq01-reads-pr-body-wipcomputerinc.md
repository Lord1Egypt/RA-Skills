# PR Body: `wipcomputerinc` CLAUDE.md Level 2 VQ01 Boot Reads

**Date:** 2026-04-22
**Author:** cc-mini (with Parker)
**Repo:** `wipcomputer-ldmos-wipcomputerinc-home-private`
**Branch:** `cc-mini/boot-vq01-reads`
**PR:** [#24](https://github.com/wipcomputer/wipcomputer-ldmos-wipcomputerinc-home-private/pull/24)

## Summary

Adds `kaleidoscope-executive-brief-v02.md` and `architecture-spec.md` as mandatory reads (steps 11 and 12) in the Dream Weaver Boot Sequence in `~/wipcomputerinc/CLAUDE.md` (Level 2 workspace).

Fires for any session touching memory, bridge, Kaleidoscope, Memory Crystal, or agent IDs. Without these, a session lands without the product frame and proposes architecture that is already designed and shipped. This is how 2026-04-22 started.

## Aligned with plan docs

- `wip-ldm-os-private/ai/product/plans-prds/current/wip-code/2026-03-27--cc-mini--single-source-of-truth-reversed.md` ... additive to Level 2 workspace CLAUDE.md (no trimming until Levels 2 + 3 are proven)
- `wip-ldm-os-private/ai/product/plans-prds/current/wip-code/2026-04-03--cc-mini--cwd-compaction-bug-journal.md` ... even when CWD drifts post-compaction, the workspace CLAUDE.md still directs the session to load VQ01 before any surface-area work

## Change

One additive block after step 10 (auto-memory):

```
11. /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/product-ideas/vision-quest-01/kaleidoscope-executive-brief-v02.md
12. /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/product-ideas/vision-quest-01/architecture-spec.md
```

Also updates the "Skipping steps 6-X" enforcement sentence:
- Bumps range: 6-10 -> 6-12
- Adds 2026-04-22 to the list of recurrence dates
- Adds one new failure mode: "proposing architecture that is already designed and shipped"
- Cross-references the two plan docs by path

## Test plan

- [ ] Open a fresh CC session in `~/wipcomputerinc/`
- [ ] Verify the boot sequence lists VQ01 as steps 11 and 12
- [ ] Verify the paths resolve (the files exist at the absolute paths given)
- [ ] Confirm next WIP-surface session loads them
