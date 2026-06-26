# Add root SKILL.md + ldm install as primary path

Added SKILL.md to repo root (source of truth for wip-release website publishing). `ldm install wipcomputer/memory-crystal` is now the recommended install path. `crystal init` stays for MC-specific setup (database, cron, role, pairing).

Also added `.publish-skill.json` so wip-release publishes SKILL.md to wip.computer/install/.

Closes wipcomputer/wip-ldm-os#97. Convergence tracked in wipcomputer/wip-ldm-os#99.
