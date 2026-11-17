---
title: Bin manifest layer 2 — cross-package CI conflict gate
date: 2026-04-29
status: open (parked follow-up from 2026-04-28 thread)
severity: P2
component: ldm-installer
parent-ticket: archive/2026-04-28--cc-mini--ldm-bin-overwrite-wipes-crystal-capture.md
parent-design: ../../plans-prds/archive/2026-04-28--cc-mini--ldm-bin-ownership-manifest-design.md
related-prs: wipcomputer/wip-ldm-os-private#717 (design), #718 (impl, layers 1+3)
---

# Layer 2 cross-package CI conflict gate

## Context

The bin ownership manifest (PR #717 design, #718 implementation) defined three enforcement layers for duplicate-name detection:

- **Layer 1** (per-package validator at `prepublishOnly`) — landed in #718 for the LDM CLI and in `memory-crystal-private` PR #124. Stops a *single* package from publishing a broken declaration.
- **Layer 3** (runtime enforcement at `ldm install`) — landed in #718. Aborts pre-write if the live aggregate has a conflict.
- **Layer 2** (cross-package CI gate) — **not yet built. This ticket.**

Layer 2 catches conflicts that layers 1 and 3 cannot: when MC and the LDM CLI both declare the same `name`, layer 1 only validates each in isolation, and layer 3 only catches it after at least one of the two packages has shipped to npm. By that time, an operator's machine could be in a borderline state.

## What needs to exist

A GitHub Actions workflow on `wip-ldm-os-private` that, on every release-PR or scheduled run:

1. Reads the LDM CLI's own `wipLdmOs.binFiles` from this repo.
2. Fetches the latest published `openclaw.plugin.json` for each known extension. Sources:
   - npm: `npm view @wipcomputer/<name> --json` includes the published manifest.
   - GitHub: clone the public repo's tagged release.
3. Aggregates using `lib/bin-manifest.mjs#aggregateBinManifest()` (or a static-analysis equivalent that doesn't need a live `~/.ldm/` layout).
4. Fails the workflow if `aggregateBinManifest` returns any `conflicts`.

## Dependencies

- **Known-extensions registry.** The workflow needs a list of which extensions to fetch. Today the only declarer besides the LDM CLI is `memory-crystal`. Hardcoding it is acceptable for v1; longer-term move it to `catalog.json` or a dedicated registry file.

## Out of scope

- Validating extensions outside the WIP namespace.
- Validating the LDM CLI's declarations against a hypothetical "global" registry. Layers 1 + 3 already cover this surface.

## Acceptance criteria

- [ ] `.github/workflows/bin-manifest-cross-package.yml` (or similar) runs on PR + push to main.
- [ ] Workflow reads LDM CLI manifest + every entry in the known-extensions registry.
- [ ] Workflow fails with a clear message naming both declarers and both source paths if any name is doubly-claimed.
- [ ] Workflow passes on the current main of both `wip-ldm-os-private` and `memory-crystal-private`.
- [ ] Test case: introduce a duplicate declaration on a feature branch; confirm the workflow blocks the PR.

## Why P2

Layer 1 covers the realistic single-package failure mode; layer 3 catches anything that slips past layer 1 on the operator's machine. Layer 2 is hardening for the cross-package case that has never actually fired (the `ldm-backup.sh` near-collision was caught and resolved at the design pass). It's worth building, but it's not blocking the 2026-04-28 outage class.
