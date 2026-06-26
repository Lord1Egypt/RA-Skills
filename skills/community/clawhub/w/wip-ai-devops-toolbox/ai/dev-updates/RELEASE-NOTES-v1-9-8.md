# Release Notes: AI DevOps Toolbox v1.9.8

## wip-install Delegates to ldm install

When `ldm` CLI is on PATH, `wip-install` now delegates immediately instead of cloning and detecting on its own. Passes through all flags (--dry-run, --json, etc.).

Falls back to standalone installer if ldm is not found or if ldm install fails. The standalone path is fully preserved.

Prints "Tip: Install LDM OS for more components" when ldm is not available.

## deploy-public.sh Safety Guards

Three new checks prevent deploying sanitized code back to the source repo:
- Source match check (compares origin URL against target)
- Name check (rejects targets containing "-private")
- Redirect detection (catches GitHub's silent URL redirects)

Auto-creates public repo if it doesn't exist. Handles empty repos.
