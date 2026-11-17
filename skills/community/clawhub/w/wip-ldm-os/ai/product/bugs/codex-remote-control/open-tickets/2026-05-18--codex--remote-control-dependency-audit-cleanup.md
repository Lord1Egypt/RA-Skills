---
title: "Remote Control dependency audit cleanup before broader launch"
status: open
priority: P1
owner: Hardening Cody
repo: wip-codex-remote-control-private / wip-ldm-os-private / kaleidoscope-private
created: 2026-05-18
source_review: 2026-05-18 security triage of private Remote Control architecture
master_plan_item: 39
---

# Remote Control Dependency Audit Cleanup Before Broader Launch

## Problem

The 2026-05-18 security triage still saw dependency advisories in the Remote Control and hosted MCP dependency trees, including a high-severity `fast-uri` advisory path.

This does not mean the vulnerability is reachable through Remote Control. It does mean the broader launch story is not production-clean until we can explain or clear the advisories.

## Risk

P1 launch hygiene and supply-chain risk.

Dependency advisories are common in alpha work. For invite-list or public launch, they need an explicit disposition:

- fixed by version bump;
- unreachable and documented;
- transitive advisory waiting on upstream with mitigation;
- removed by replacing the dependency.

## Scope

Audit the packages that participate in Remote Control:

- `wip-codex-remote-control-private`;
- `wip-ldm-os-private` hosted MCP relay paths;
- `kaleidoscope-private` browser Remote Control app, if still the browser surface;
- any shared packages pulled into those paths.

## Fix shape

- Run the repo-native audit commands for each involved package.
- Identify direct and transitive advisory paths.
- Upgrade direct dependencies where safe.
- For transitive advisories, prefer supported dependency upgrades over overrides.
- Use overrides only with a written reason and test evidence.
- If an advisory is unreachable, document why with the exact import path and runtime boundary.
- Keep package lockfiles consistent.

## Acceptance

- Dependency audit output is captured in the PR or linked ticket notes.
- High advisories in Remote Control runtime paths are either fixed or have an explicit unreachable/accepted-risk note.
- The `fast-uri` advisory path is specifically addressed.
- Existing Remote Control daemon tests pass.
- Hosted MCP Remote Control relay tests pass.
- Browser Remote Control tests pass if the browser package is touched.
- No dependency upgrade changes Remote Control auth, E2EE, routing, or pairing behavior without separate review.

## Non-goals

- Do not do a repo-wide dependency modernization sweep.
- Do not upgrade unrelated UI or dev-only dependencies unless they block audit clarity.
- Do not accept an advisory silently because the product is still alpha.
