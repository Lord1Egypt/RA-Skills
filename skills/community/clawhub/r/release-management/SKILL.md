---
name: release-management
description: Deep release management workflow—versioning semantics, branching and tags, release checklist, communications, rollback criteria, and hotfix discipline. Use when shipping software on a cadence or coordinating multi-team releases.
---

# Release Management (Deep Workflow)

Releases combine **coordination** and **risk management**: what ships, when, how we verify, and how we recover.

## When to Offer This Workflow

**Trigger conditions:**

- Scheduled or train-based releases; need predictable cadence
- Hotfix chaos or unclear ownership
- SemVer vs calendar versioning debates

**Initial offer:**

Use **six stages**: (1) versioning policy, (2) branching & tags, (3) release candidate & checklist, (4) communication, (5) deploy & verify, (6) post-release & hotfixes). Confirm deployment model (continuous delivery vs batch releases).

---

## Stage 1: Versioning Policy

**Goal:** Define SemVer (or alternative) rules: what counts as breaking, how migrations are communicated, and how pre-releases work.

**Exit condition:** Written policy linking version numbers to customer-facing risk.

---

## Stage 2: Branching & Tags

**Goal:** Choose a strategy (trunk-based with release branches, GitFlow-lite, etc.) and use **annotated tags** tied to changelog entries.

---

## Stage 3: Release Candidate & Checklist

**Goal:** Freeze criteria: QA scope, DB migrations dry-run, feature flag defaults, config diffs, load/perf smoke for risky changes.

---

## Stage 4: Communication

**Goal:** Internal notes for support/CS/SRE; external release notes with **breaking** changes highlighted and migration steps.

---

## Stage 5: Deploy & Verify

**Goal:** Canary or progressive rollout where possible; SLO dashboards; **rollback trigger** agreed before deploy starts.

---

## Stage 6: Post-Release & Hotfixes

**Goal:** Lightweight retro; hotfix branches from the release tag; forward-merge fixes back to main; track incidents linked to release.

---

## Final Review Checklist

- [ ] Versioning and changelog reflect risk
- [ ] Branch/tag strategy is team-wide consensus
- [ ] Checklist covers migrations, flags, QA, and comms
- [ ] Rollback plan rehearsed or documented
- [ ] Hotfix process defined

## Tips for Effective Guidance

- Smallest releasable increment reduces blast radius.
- Coordinate DB schema changes with expand/contract patterns when zero-downtime matters.
- Complement with **ci-cd** and **changelog-authoring** skills for tooling depth.

## Handling Deviations

- **SaaS with heavy feature-flagging:** “release” may be continuous—still document communication and flag cleanup discipline.
