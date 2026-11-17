# Lesa Bug Tickets and Incidents

This folder is Lesa's private bug lane for issues she discovers or is asked to investigate when the issue is tied to **her operating context**: identity continuity, boot path, memory retrieval, agent-to-agent workflow, or her personal pages/blog.

## Lane Scope

`bugs/lesa/` is for **agent-operating** bugs.

**Component bugs** (memory-crystal, openclaw, bridge, installer, guard, etc.) go in their existing component lane regardless of who discovered them. Example: a memory-crystal SQL bug Lesa surfaces lives in `bugs/memory-crystal/`, not here. A bug in OpenClaw's runtime that affects Lesa's session goes in `bugs/openclaw/`.

The discoverer doesn't change the component. If you cannot decide whether a bug is agent-operating or component, default to the component lane. The lane question should not block the ticket.

## Required Workflow

1. Create one dated bug or incident ticket in `bugs/lesa/` with the format `YYYY-MM-DD--<author-id>--<short-slug>.md`.
2. Capture observed behavior, expected behavior, impact, evidence, suspected root cause, fix plan, tests, smoke test, release path, rollback, and CC review questions.
3. Use a worktree under `.worktrees/wip-ldm-os-private--<branch-name>` rooted on the appropriate branch.
4. Commit the ticket on the appropriate branch (see Branch Prefixes below), open a private PR, merge normally with `--merge --delete-branch`, and fast-forward private `main`.
5. Send the merged private-main ticket to CC for review.
6. Incorporate CC feedback in a follow-up private PR.
7. Send the updated ticket back to CC.
8. Only after Status reaches `ready` does fix implementation begin, unless the bug is a live P0 (see P0 Exception below).

## Ticket Template

Each ticket should include:

- `Severity`: P0, P1, P2, or P3.
- `Status`: one of `investigating | ticketed | CC review | ready | fixing | fixed | verified | archived`. **Fix implementation begins only when Status is `ready` or later.** This is the gate. A linked CC comment is not a substitute.
- `Co-authors`: Parker, Lesa, Claude (all three required on every commit).
- `Observed`: what happened.
- `Expected`: what should have happened.
- `Impact`: user, agent, deploy, data, privacy, or continuity impact.
- `Evidence`: commands, logs, URLs, screenshots, memory hits, or git commits.
- `Root cause`: confirmed or suspected.
- `Fix plan`: ordered steps.
- `Test plan`: automated and manual checks.
- `Smoke test`: smallest live proof.
- `CC review request`: exact questions for CC.
- `Release path`: alpha first for package/runtime code (see `plans-prds/current/lesa/README.md` for the WIP-owned vs third-party distinction).
- `Rollback`: how to disable or revert safely.

## CC Partnership

CC is Lesa's standing bug partner.

**Default reviewer:** `cc-mini:lesa-work-02`. Parker may reassign at any time. Lesa picks ONE cc-mini instance per ticket and stays with that instance through the review loop.

Lesa should send tickets to CC after the private artifact is merged, then update from CC feedback before implementation unless the issue is an active P0.

CC's role: check root cause, missing evidence, process discipline, test coverage, release path, and rollback safety.

Lesa's role: own the ticket, land the updates, and carry the fix through verification.

### CC Review SLA

- **Normal/non-blocking bugs:** 24h response window.
- **Immediate review (no SLA, jump-the-queue):** P0/P1, or anything blocking live stability, release, install, memory capture, or OpenClaw upgrade.

If CC cannot meet SLA, Lesa proceeds based on best judgment and surfaces the gap to Parker.

## Branch Prefixes

Branch prefix follows agent identity, not lane subject. Lesa's commits on her own lane use `oc-lesa-mini/`. CC's commits on Lesa's lane (e.g. lane revisions, review-driven cleanup) use `cc-mini/`. The lane scope is a property of the work; the prefix is a property of the author.

Reference: `~/.ldm/shared/dev-guide-wipcomputerinc.md` and the repo's CLAUDE.md `Conventions` section.

## P0 Exception

For live P0 incidents, restoration may happen before the full ticket if waiting would worsen damage. The ticket must still be created immediately after stabilization, and it must include the exact recovery actions already taken. Status starts at `fixed` or `verified` in this case rather than passing through `ready`, with a clear note that the live recovery preceded the ticket.

## Archive

Once a bug is `verified` and stable, `git mv` it to `bugs/archive/`. Never delete bug tickets; the archive preserves the failure pattern for future investigators.
