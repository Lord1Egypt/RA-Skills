# Installer: install-spec URL publish pipeline

**Date:** 2026-04-28
**Owner:** unassigned
**Status:** open
**Master plan:** [2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md](2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md)

## What

The canonical install pattern is:

```
Read https://wip.computer/install/<slug>.txt
```

Today only two of these files exist on the VPS:

- `wip.computer/install/wip-ldm-os.txt`
- `wip.computer/install/wip-codex-remote-control.txt`

Both were hand-authored. There is no pipeline that takes a product's `SKILL.md` (or sibling source) and publishes it to that URL on release.

## Why this matters

The Install Spec section in `docs/universal-installer/SPEC.md` says: *"the contract is the URL and the behavior, not the file origin. Can be generated from, mirrored from, or live alongside SKILL.md."* That's true in spec but unsupported in practice. Every new product currently means a hand-edited file synced to the VPS.

## Decision needed

Pick one (or both):

**A. Auto-derive from SKILL.md.** A release-time hook reads `SKILL.md`, applies a transform (strip frontmatter, add an install header, append the canonical install prompt template), and uploads to `wip.computer/install/<slug>.txt`.

**B. Hand-author per product.** Keep an `install-spec.txt` file in the repo root. Release pipeline scp's it to the VPS. No transform, no surprises.

**Recommendation:** B for now (predictable, auditable). Add A later as a convention if the pattern stabilizes and SKILL.md content reliably maps to install spec content.

## Pipeline shape (assuming B)

1. `wip-release` notices `install-spec.txt` at the repo root.
2. After publishing the npm package and the GitHub release, scp the file to `wip-vps:/var/www/wip.computer/app/install/<slug>.txt`.
3. Verify with `curl -sI https://wip.computer/install/<slug>.txt` returns 200.
4. Print the install URL in the release output so the user can paste it into an AI immediately.

## Acceptance

- `wip-release` (or a sibling script) publishes `install-spec.txt` to `wip.computer/install/<slug>.txt` as part of a release.
- A new product that adds `install-spec.txt` and runs `wip-release` ends up with a live install URL.
- The two existing hand-authored files (`wip-ldm-os.txt`, `wip-codex-remote-control.txt`) are migrated into their source repos as `install-spec.txt` and republished via the new pipeline. No drift between repo and VPS.

## Open questions

- Is the VPS path correct? Confirm against `~/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-release/` how scp is currently shaped.
- Does `wip-release` already publish anything to the VPS, or is this a new transport for it?
