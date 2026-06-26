# MOVED

The private dev guide source now lives in the LDM OS installer repo:

- **Source (edit here):** `wipcomputer/wip-ldm-os-private` → `shared/docs/dev-guide-wipcomputerinc.md.tmpl`
- **Deployed (don't edit directly):**
  - `~/.ldm/library/documentation/dev-guide-wipcomputerinc.md` ← agent library, canonical read path
  - `~/wipcomputerinc/library/documentation/dev-guide-wipcomputerinc.md` ← human library

Deploy path: `ldm install` invokes `deployDocs()` in `wip-ldm-os-private/bin/ldm.js`, which renders the `.tmpl` and writes to both libraries.

## History

- Originally shared space between this repo (public dev guide half) and `wipcomputer/wip-dev-guide-private` (private dev guide half).
- `wip-dev-guide-private` was renamed `-deprecated` but the intended move path (`~/wipcomputerinc/settings/templates/dev-guide-private.md`) never actually existed. The placeholder pointed at a path no repo had.
- 2026-04-19: re-established a real versioned source in `wip-ldm-os-private/shared/docs/` via `wip-ldm-os-private#618`, released as `@wipcomputer/wip-ldm-os@0.4.75-alpha.1`, deployed via `ldm install`.
- 2026-04-20: this placeholder updated to point at the actual location.

The public dev guide (`DEV-GUIDE-GENERAL-PUBLIC.md` at this repo's root) is unchanged. Only the private supplement moved.
