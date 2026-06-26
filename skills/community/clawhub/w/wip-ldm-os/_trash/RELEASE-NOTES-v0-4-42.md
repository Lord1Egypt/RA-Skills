Single Source of Truth: the first cut.

For 49 days, our instruction files grew by accretion. Every bad output got a new rule. Every incident got a patch. CLAUDE.md hit 367 lines. The same rule ("never run tools from repo clones") appeared in 7 places. Branch prefixes had 3 different naming schemes fighting each other. TOOLS.md showed `--squash` in a code example while every other file said never squash.

This release starts the cleanup. It doesn't rewrite CLAUDE.md yet (that comes next, after dogfooding confirms nothing breaks). What it does:

**Shared rules get on-demand pointers.** Instead of stuffing all dev conventions into rules that load every session, each rule now points to the full operational doc in `settings/docs/`. Agents read the detailed workflow when they need it, not on boot. `git-conventions.md` points to `how-worktrees-work.md`. `release-pipeline.md` points to `how-releases-work.md`. `workspace-boundaries.md` points to `system-directories.md`. This is why Lesa got the worktree workflow wrong three times... the thin rule said "use worktrees" but never told her where to find the actual commands.

**workspace-boundaries.md fixed.** `staff/` renamed to `team/` to match the Mar 24 migration. Every session since then loaded a stale rule.

**boot-config.json fixed and tracked.** The journal path still pointed to the old iCloud location (`~/Documents/wipcomputer--mac-mini-01/staff/...`). Updated to `~/wipcomputerinc/team/cc-mini/documents/journals`. Now tracked in the repo so future installs deploy the fix.

**Level 1 CLAUDE.md template created.** The thin global instructions (~30 lines) that `ldm install` will deploy to `~/.claude/CLAUDE.md`. Writing style, co-authors, 1Password, shared file protection, memory-first, and the pointer to `settings/docs/`. This replaces the current 367-line duplicate that drifts from the project CLAUDE.md.

Closes #183 (audit phase). Partial progress on #157, #158.
