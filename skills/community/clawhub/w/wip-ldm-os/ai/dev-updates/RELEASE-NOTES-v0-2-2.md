# Release Notes: LDM OS v0.2.2

## Registry Auto-Detection

`ldm install` and `ldm doctor` now scan `~/.ldm/extensions/` for extensions that were installed outside of `ldm install` (via `crystal init`, `wip-install`, or manual setup). These get auto-registered so the catalog status is accurate.

Previously, Memory Crystal and other extensions showed as "available but not installed" even when they were deployed and running. Now they show up correctly.

## deploy-public.sh Safety Guards

Three new checks prevent the deploy script from ever targeting the wrong repo:
- Compares private repo origin against the target. Refuses if they match.
- Rejects any target containing "-private".
- Detects GitHub URL redirects (resolved name != requested name).

Also auto-creates the public repo if it doesn't exist, and handles empty repos by pushing directly to main.

## SKILL.md Updated

Full 9-skill catalog table (was 3). All skill repos listed in "Part of LDM OS" section. Added note about re-registering skills installed before LDM OS.

## ai/ Directory Reorganized

Parker's reorg: dev-updates, feedback, plans-prds/current, _sort, _trash. Three AI model reviews (Grok, GPT, Claude web) saved with combined recommendations.
