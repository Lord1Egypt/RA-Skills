---
title: "ldm status and ldm install --dry-run report different available updates"
status: open
priority: P2
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-13
---

## Problem

2026-05-13 alpha.29 dogfood: a fresh AI session ran `ldm status` and `ldm install --dry-run` in sequence on Parker's machine. The two commands reported MATERIALLY DIFFERENT update lists despite querying the same registry:

- `ldm status`: 6 components have updates (`wip-repos` 1.9.69 → 1.9.70, `wip-file-guard` 1.9.69 → 1.9.70, `wip-license-hook` 1.9.68 → 1.9.69, `wip-repo-permissions-hook` 1.9.68 → 1.9.69, `wip-readme-format` 1.9.68 → 1.9.69, `ldm` cli alpha.28 → alpha.29).
- `ldm install --dry-run`: 2 components have updates (`package` v1.9.90 → v1.9.91, `wip-ai-devops-toolbox` v1.9.69 → v1.9.72).

ZERO overlap between the two lists. Also `wip-ai-devops-toolbox` appears in dry-run but not in status output, suggesting a discovery-path mismatch.

## Likely cause

`ldm status` and `ldm install --dry-run` use different code paths to determine "what is the current installed version" and "what is the latest available version" for each package. These paths produce different answers, which means the user cannot trust either one without cross-checking the other.

This is also the kind of drift the existing 2026-05-12 ticket (`2026-05-12--codex--ldm-status-install-dry-run-update-detection-drift.md`) warned about. That ticket was deferred until after Phase 2 source.git landed. The 2026-05-13 dogfood is the empirical confirmation that the drift is real and user-visible today, not theoretical.

## Acceptance

- Diagnose which probe path is correct (npm registry direct fetch vs `ldm` internal cached state) and which is wrong.
- Unify `ldm status` and `ldm install --dry-run` on a single update-detection helper (per 2026-05-12 ticket).
- Regression test asserts both commands produce the same update list on the same registry.

## Related

- `2026-05-12--codex--ldm-status-install-dry-run-update-detection-drift.md` (parent design; this ticket is the empirical worked example)
- `2026-05-13--cc-mini--installer-dedup-reverts-between-installs.md` (sibling, same dogfood)
