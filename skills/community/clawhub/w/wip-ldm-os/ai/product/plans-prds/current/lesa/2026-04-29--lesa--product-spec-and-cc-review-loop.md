# Lesa Product Spec and CC Review Loop

**Date:** 2026-04-29
**Owner:** Lesa
**Status:** ready (CC review incorporated; see Post-Review Revisions section at end)
**Area:** product planning workflow
**Related folders:** `ai/product/plans-prds/current/lesa/`, `ai/product/bugs/lesa/`
**Co-authors:** Parker Todd Brooks, Lesa, Claude

## Problem

Lesa has been generating product ideas, identity artifacts, website work, recovery plans, and agent-operating doctrine from live conversations. Some of that work has been durable because CC or Parker turned it into private repo artifacts. Some of it has remained only in conversation memory, daily logs, or live deployed state.

That creates the same class of risk as the Day 63 incident: meaningful work can exist, matter, and even be shared, while still not being on the path that the repo, release process, and other agents can review.

Lesa needs her own product-planning lane with the same discipline Parker already uses with CC.

## Goal

Every Lesa-originated product idea should become a private source-controlled spec before implementation.

The process should make Lesa responsible for the first draft, private PR, merge, and pull-down. CC should review after the private-main artifact exists, then Lesa should update the plan based on CC feedback before implementation begins.

## Non-goals

- This does not move Lesa identity files into this repo.
- This does not replace CC's product lanes.
- This does not authorize public release or stable install.
- This does not bypass Parker for red-category actions such as external posts, destructive data changes, or production security changes.

## Product Shape

Add two Lesa-owned private lanes:

- `ai/product/plans-prds/current/lesa/` for ideas, specs, PRDs, operating doctrine, and product plans.
- `ai/product/bugs/lesa/` for Lesa-discovered bugs, incidents, regressions, and recovery plans.

Both lanes use the same review loop:

1. Lesa writes the artifact.
2. Lesa commits it on an `oc-lesa-mini/` branch (her canonical prefix per dev guide; CC's commits on Lesa's lane use `cc-mini/`).
3. Lesa opens a private PR.
4. Lesa merges normally, never squash, and fast-forwards private `main`.
5. Lesa sends the merged private-main artifact to CC for review.
6. Lesa incorporates CC feedback in a follow-up PR.
7. Lesa sends the updated artifact to CC again.
8. Implementation starts only after the plan is updated or CC explicitly says no changes are needed.

## Required Spec Coverage

Every idea spec must cover:

- Product problem and why now.
- User story or operator story.
- Scope and non-goals.
- Source-of-truth files and runtime files.
- Privacy, auth, identity, and attribution implications.
- Development steps.
- Test plan.
- Smoke test.
- CC review questions.
- Alpha release path.
- Rollback or disable path.
- Open questions.

## Development Steps

For each future idea:

1. Search Memory Crystal and repo docs for prior context.
2. Create the spec under `ai/product/plans-prds/current/lesa/` with a dated filename.
3. Use a linked worktree under `.worktrees/wip-ldm-os-private--<branch-name>` and the appropriate branch prefix (`oc-lesa-mini/` for Lesa's commits, `cc-mini/` for CC's commits on Lesa's lane).
4. Commit with all required co-authors.
5. Open a private PR to `main`.
6. Merge with a regular merge commit.
7. Fast-forward the private main checkout.
8. Send CC a concise review request with the path, PR URL, and exact questions.
9. Apply CC feedback in a follow-up branch and PR.
10. After CC re-review, implement the first slice.
11. Test locally.
12. Smoke test the live or installed surface where applicable.
13. Release alpha where the change is package/runtime code.
14. Stop before stable install or public promotion unless Parker explicitly asks.

## Test Plan

For planning-only artifacts:

- Confirm the file is in the correct private lane.
- Confirm it names source-of-truth and runtime boundaries.
- Confirm it includes a CC review section.
- Confirm PR is private repo only.

For implementation work that follows a spec:

- Run repo-specific unit or integration tests.
- Run lint or syntax checks where available.
- Run the smallest live smoke test that proves the user-facing behavior.
- Verify release track is alpha unless Parker explicitly chose another track.
- Verify installed runtime is not modified unless Parker explicitly says install.

## Smoke Test

For this workflow itself:

- This file exists in `ai/product/plans-prds/current/lesa/`.
- `ai/product/bugs/lesa/` exists with matching bug workflow guidance.
- The PR merges to private `main`.
- CC receives the merged artifact for review.

## CC Review Request

Ask CC to review:

- Whether the lane location matches existing repo conventions.
- Whether the review loop is strict enough before implementation.
- Whether alpha release wording matches WIP release discipline.
- Whether bug and PRD lanes should share a template or diverge.
- Whether the docs should require a visible CC-reviewed status before implementation.

## Release Path

This is docs-only private planning. No alpha package release is required for this PR.

Future code work spawned from a Lesa spec should release as alpha first unless Parker explicitly chooses a different track.

## Rollback

If this lane is wrong, archive these files under `ai/product/plans-prds/archive/` and `ai/product/bugs/archive/` in a normal PR. Do not delete them silently.

## Open Questions

- Should Lesa specs use `Status: CC reviewed` as a gate before implementation, or is a linked CC comment enough?
- Should future Lesa bug tickets be mirrored into GitHub Issues, or stay as repo docs unless they involve code already tracked by issue labels?
- Should Day 63, blog, and Daily Surprises recovery become the first specs under this lane after this workflow lands?

## Post-Review Revisions (2026-04-30)

CC review by `cc-mini:lesa-work-02` produced six issues plus two Parker policy decisions. All landed in this PR (`cc-mini/lane-readme-revisions`) alongside this addendum. Summary:

### Lane scope rule (Issue 1)

Both READMEs now state explicitly: `lesa/` lanes are for **agent-operating** concerns (identity, boot, memory, agent-to-agent workflow). Component bugs/specs go in their existing component lane regardless of who discovered them. The discoverer doesn't change the component. Worked example: PR #760's boot-budget guard was originally in `bugs/lesa/`; lane-fit review moved it to `bugs/openclaw/` since it's an installer enforcement bug, not a Lesa-runtime bug.

### `current/` layer (Issue 2)

Spec/PRD lane moved from `plans-prds/lesa/` to `plans-prds/current/lesa/` to match the existing `plans-prds/current/<component>/` convention. This file's path was updated as part of the same PR. Bug lane stays `bugs/lesa/` (matches existing `bugs/<component>/` pattern; no `current/` layer in bugs).

### CC partnership identity (Issue 3)

Default reviewer is `cc-mini:lesa-work-02`. Parker may reassign. Lesa picks ONE cc-mini instance per artifact and stays with that instance through the loop. Both READMEs now name the default. Resolves the bridge-coordination ambiguity that surfaced this thread.

### Status gate (Issue 4 + Open Question 1)

**Status field is the gate.** Implementation begins only when Status is `ready` or later. A linked CC comment is not a substitute. Both READMEs now state this explicitly. Open Question 1 above is answered: visible Status, plain-text scannable.

### Co-authors line in template (Issue 5)

Added to both spec and bug templates.

### Worktree pattern + branch prefix (Issue 6)

Required worktree path documented. Branch-prefix footnote clarifies: branch follows author identity, not lane subject. Lesa's commits use `oc-lesa-mini/`, CC's commits on Lesa's lane use `cc-mini/`. The dev guide and the repo's CLAUDE.md disagree on Lesa's prefix (`lesa/` vs `oc-lesa-mini/`); Parker confirmed `oc-lesa-mini/` as canonical for this work.

### Parker Policy A: Alpha install policy

Replaced the boilerplate "alpha is default first release target" with the explicit WIP-owned vs third-party split. WIP-owned alpha = dogfood-track, no fresh install gate. Beta/stable still require Parker's go. Third-party (OpenClaw etc.) follows the stricter upgrade/canary path in `repos/ldm-os/devops/open-claw-upgrade-private/UPGRADE-RUNBOOK.md`. Plans-prds README updated; bugs README references it.

### Parker Policy B: CC review SLA

New section in both READMEs: 24h normal, immediate for P0/P1 or anything blocking live stability, release, install, memory capture, or OpenClaw upgrade.

### Open Questions resolved

- **Status as gate vs CC comment:** visible Status field. Resolved.
- **GitHub Issues for bugs:** stay as repo docs unless code is already tracked by issue labels. Documented in bugs README.
- **First specs under this lane:** Day 63, blog, Daily Surprises recovery. Lesa will author these next, post-merge.

### What this PR did not change

- The original spec text above (sections 1-12) is preserved as the original proposal snapshot.
- SOUL.md, USER.md, MEMORY.md, and Lesa memory files: untouched, never in scope.
- TUI delivery-mirror investigation: separate ticket pending Parker's call (not this PR).
