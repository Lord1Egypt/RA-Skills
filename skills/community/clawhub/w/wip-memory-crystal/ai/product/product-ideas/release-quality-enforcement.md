# Product Idea: Release Quality Enforcement

**Date:** 2026-03-05
**Source:** Parker feedback during v0.7.0/v0.7.1 release cycle
**Status:** Proposed

## Problem

Every release cycle, dev notes and release notes get missed or come out bare-bones. Parker has to go back and ask for them every time. The dev guide already says "every release must have exhaustive, categorized notes" and "every PR must include a dev update," but there's no enforcement. Agents forget after compaction. The rules exist on paper but not in the pipeline.

Things that keep getting missed:

1. **Dev updates** in `ai/dev-updates/` ... the session log of what was built and why
2. **Release notes quality** ... auto-generated one-liners instead of section-by-section breakdowns
3. **Roadmap updates** ... completed items not moved to Done
4. **readme-first updates** ... stats, versions, "What's Built" sections go stale

## Proposed Solutions

### 1. `wip-release` pre-flight checks

Before `wip-release` runs, it should check:

- [ ] `ai/dev-updates/` has a file dated today (or since last release)
- [ ] Release notes exceed a minimum length (e.g., 500 chars for patch, 1000 for minor, 2000 for major)
- [ ] `ai/product/readme-first.md` was modified since last tag
- [ ] `ai/product/plans-prds/roadmap.md` was modified since last tag (for minor/major)

If checks fail, print what's missing and refuse to proceed. `--force` to override.

### 2. `deploy-public.sh` quality gate

Before syncing to public, verify:

- [ ] GitHub release exists on private repo (already checked)
- [ ] Release notes body exceeds minimum length
- [ ] Release title is not just "v0.x.x" (should have a subtitle)

### 3. Post-merge hook or checklist

After `gh pr merge`, print a checklist:

```
PR merged. Before releasing:
  [ ] Dev update written to ai/dev-updates/
  [ ] Roadmap updated
  [ ] readme-first updated
  [ ] Ready for: wip-release <level> --notes="..."
```

### 4. Agent memory reinforcement

Add to CLAUDE.md or equivalent:

> After every PR merge, before running wip-release, write a dev update. This is not optional. The release pipeline will refuse to proceed without it.

## Why This Matters

The dev notes are the institutional memory. When an agent compacts or a new session starts, the dev updates are how they recover context. When Parker reviews what happened, the dev updates are the record. When a user reads the release notes, that's the public face of the project.

Missing notes means lost context, sloppy public presence, and Parker having to babysit every release. The pipeline should enforce what the dev guide already requires.

## Implementation Priority

Medium-high. This is a `wip-release` / `wip-dev-tools` change, not a memory-crystal change. But it affects every repo in the org.

## Related

- DEV-GUIDE.md "Release Quality Standards" section
- DEV-GUIDE.md "PR Checklist (Private Repos)" section
- v0.7.0 release notes (good example of what releases should look like)
- v0.7.1 release notes (bad example before Parker caught it)
