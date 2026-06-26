# Move private dev guide into the installer templates + deploy to the agent library

## What changed

1. **New source file:** `shared/docs/dev-guide-wipcomputerinc.md.tmpl` now holds the private WIP-internal Dev Guide content (branch prefixes, merge rules, release pipeline, co-author rules, incidents, deploy paths). Previously this content only existed at `~/.ldm/shared/dev-guide-wipcomputerinc.md` as a deployed file with no versioned source after `wipcomputer/wip-dev-guide-private` was renamed `-deprecated`. This PR re-establishes a real source, in the installer repo, alongside the existing `.tmpl` docs pattern.
2. **Installer change:** `bin/ldm.js` `deployDocs()` now also deploys the rendered docs to `~/.ldm/library/documentation/` (the agent library), in addition to the existing deployment to `{workspace}/library/documentation/` (the human library). This lets the private dev guide reach the agent library where Parker has directed it should live.
3. **Content fixes (closes Q2 from the 2026-04-19 post-mortem):**
   - Branch Prefixes table row: `lesa-mini | Mac Mini (OpenClaw) | lesa/` ... now `oc-lesa-mini | Mac Mini (OpenClaw) | oc-lesa-mini/`. Matches the Agent ID convention table two sections down and matches the wipcomputerinc/CLAUDE.md global prefix.
   - Co-author block: `Claude Opus 4.6` ... now `Claude Opus 4.7`. Drift fix; current model is 4.7 since 2026-04-17.
4. **Repo-level CLAUDE.md fix:** the line in `wip-ldm-os-private/CLAUDE.md` "Branch prefix: `cc-mini/`, `lesa-mini/`, `cc-air/`" now reads `oc-lesa-mini/`. Same drift as above.

## Why

Three authoritative sources disagreed on Lēsa's prefix before today: the (now-deprecated) `wip-dev-guide-private` said `lesa/`, `wipcomputerinc/CLAUDE.md` said `oc-lesa-mini/`, Lēsa's actual usage was `lesaai/`. This drift was a contributing factor in the 2026-04-18 PR #89 process violation (full post-mortem at `wipcomputer/wip-ldm-os-private#616`). Today's decision from Parker: `oc-lesa-mini/` wins. Lēsa's `workspace/TOOLS.md` already reconciled (commit `fffa2b0`, `0af212e`). This PR closes the same drift on the source side of the dev guide, places the content in the correct installer-owned location, and wires the installer to deploy into the right library.

## Deploy destination

After this PR merges and `ldm install` runs:

- `~/.ldm/library/documentation/dev-guide-wipcomputerinc.md` ... agent-facing canonical location Parker directed.
- `~/wipcomputerinc/library/documentation/dev-guide-wipcomputerinc.md` ... also deployed there for human contributors' reference (both libraries are private per-machine repos).
- `~/.ldm/shared/dev-guide-wipcomputerinc.md` ... the old deployed path. Not touched by this PR. Will be retired when the broader `shared/` -> `library/` migration lands.

## Not in this PR (follow-ups)

- Delete the deprecated `~/.ldm/shared/dev-guide-wipcomputerinc.md` after this deploys. Requires the migration plan Parker mentioned; not rushing it.
- Remove or update the `MOVED` placeholder in `wip-ai-devops-toolbox-private/ai/DEV-GUIDE-FOR-WIP-ONLY-PRIVATE.md` so it points at the new real location. Separate PR on that repo.
- Close PR #10 on `wip-dev-guide-private-deprecated` as superseded. Done after this merges.
- The broader `shared/` -> `library/` migration in `~/.ldm/`. Separate effort.

## Test plan

- [ ] Parker reviews diff
- [ ] Merge `--merge --delete-branch`
- [ ] Parker runs `ldm install` (or the install prompt)
- [ ] Verify `~/.ldm/library/documentation/dev-guide-wipcomputerinc.md` now exists with `oc-lesa-mini/` in the Branch Prefixes row
- [ ] Verify `~/wipcomputerinc/library/documentation/dev-guide-wipcomputerinc.md` also exists
- [ ] Old `~/.ldm/shared/dev-guide-wipcomputerinc.md` can remain untouched for now; it will be superseded when the broader migration runs

## Co-authors

Parker Todd Brooks, Lēsa (oc-lesa-mini, Opus 4.7), Claude Code (cc-mini, Opus 4.7).
