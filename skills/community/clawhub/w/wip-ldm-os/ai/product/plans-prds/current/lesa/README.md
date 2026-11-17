# Lesa Product Specs and PRDs

This folder is Lesa's private planning lane for product ideas that should become real work inside LDM OS, Kaleidoscope, OpenClaw, Memory Crystal, Bridge, or adjacent WIP Computer systems.

Every non-trivial idea gets a product spec and PRD here before implementation begins.

## Lane Scope

`plans-prds/current/lesa/` is for **agent-operating** product planning that originates from Lesa: identity continuity work, boot/memory architecture, agent-to-agent workflow, her personal pages and blog, recovery doctrine, and operating norms.

**Component planning** (memory-crystal, openclaw, bridge, etc.) goes in its existing component lane regardless of who discovered or proposed it. Example: a memory-crystal feature spec lives in `plans-prds/current/memory-crystal/`, not here, even if Lesa wrote it.

If you cannot decide whether a spec is agent-operating or component, default to the component lane. The lane question should not block the spec.

## Required Workflow

1. Create one dated spec/PRD file in `plans-prds/current/lesa/` with the format `YYYY-MM-DD--<author-id>--<short-slug>.md`.
2. Cover the full path: product problem, user story, scope, architecture, implementation steps, tests, smoke tests, release path, rollback, and open questions.
3. Use a worktree under `.worktrees/wip-ldm-os-private--<branch-name>` rooted on the appropriate branch.
4. Commit the spec on the appropriate branch (see Branch Prefixes below), open a private PR, merge it normally with `--merge --delete-branch`, and fast-forward private `main`.
5. Send the merged private-main spec to CC for review.
6. Incorporate CC feedback in a follow-up private PR.
7. Send the updated spec back to CC for a final check.
8. Only after Status reaches `ready` does implementation begin.

## Spec Template

Each spec should include:

- `Status`: one of `idea | draft | CC review | ready | implementing | alpha shipped | archived`. **Implementation begins only when Status is `ready` or later.** This is the gate. A linked CC comment is not a substitute.
- `Owner`: Lesa unless another owner is explicit.
- `Co-authors`: Parker, Lesa, Claude (all three required on every commit).
- `Problem`: what hurts today.
- `Goal`: what should become true.
- `Non-goals`: what this will not solve.
- `User stories`: concrete user-visible outcomes.
- `Product shape`: screens, commands, files, APIs, or agent behavior.
- `Architecture`: source-of-truth paths, runtime paths, data flows, auth, privacy, and failure modes.
- `Implementation steps`: ordered development tasks.
- `Test plan`: unit, integration, manual, and migration checks.
- `Smoke test`: smallest live proof before calling it done.
- `CC review request`: specific questions for CC.
- `Release path`: alpha first unless Parker explicitly says otherwise.
- `Rollback`: how to undo or disable the change.
- `Open questions`: decisions not yet settled.

## CC Partnership

CC is Lesa's standing development partner, not an optional reviewer.

**Default reviewer:** `cc-mini:lesa-work-02`. Parker may reassign at any time. Lesa picks ONE cc-mini instance per artifact and stays with that instance through the review loop. Splitting review across multiple CC sessions creates the same coordination drift this lane is trying to prevent.

The default loop is: Lesa drafts, lands the private planning artifact, asks CC to review, updates from CC feedback, asks CC to verify the update, then implements.

CC's role: check process discipline, root cause / scope, missing evidence, test coverage, release path, rollback safety, and lane-fit.

Lesa's role: own the spec, land the updates, carry the work through verification.

### CC Review SLA

- **Normal/non-blocking specs and bugs:** 24h response window.
- **Immediate review (no SLA, jump-the-queue):** P0/P1, or anything blocking live stability, release, install, memory capture, or OpenClaw upgrade.

If CC cannot meet SLA, Lesa proceeds based on best judgment and surfaces the gap to Parker.

## Branch Prefixes

Branch prefix follows agent identity, not lane subject. Lesa's commits on her own lane use `oc-lesa-mini/`. CC's commits on Lesa's lane (e.g. lane revisions, review-driven cleanup) use `cc-mini/`. The lane scope is a property of the work; the prefix is a property of the author.

Reference: `~/.ldm/shared/dev-guide-wipcomputerinc.md` and the repo's CLAUDE.md `Conventions` section.

## Release Discipline

For code changes spawned from a Lesa spec:

**WIP-owned packages** (memory-crystal, wip-ldm-os, all `@wipcomputer/*` npm packages, plugins). Alpha is dogfood-track and may be installed for validation without a fresh explicit install gate from Parker. Beta and stable still require Parker's explicit go.

**Third-party software** (OpenClaw itself, npm dependencies, etc.). Keep the stricter upgrade/canary path documented in `repos/ldm-os/devops/open-claw-upgrade-private/UPGRADE-RUNBOOK.md`. No dogfood-without-approval here.

Merge is not deploy. Deploy is not install. After stable publish on a WIP-owned package, stop unless Parker explicitly asks to install or promote.

For docs-only planning changes in this private repo (this lane), merge the PR and pull private `main`. No public release is implied.

## Archive

Once a spec is fully implemented and verified, `git mv` it to `plans-prds/archive/`. Never delete planning artifacts. The archive preserves history and lets future work cite prior decisions.
