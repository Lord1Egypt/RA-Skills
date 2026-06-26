# Dev Update: Unified Backup System + Workspace Migration

**Date:** 2026-03-24
**Author:** cc-mini (with Parker)
**Session:** Full day (8+ hours)

## What Shipped

### Unified Backup System (#119)

Three competing backup systems replaced by one script.

**Before:** Lesa's daily-backup.sh (broken, pointed to deleted iCloud path), ldm-backup.sh (only covered ~/.ldm/), verify-backup.sh (checking wrong path). 527 GB of redundant old backups across three locations.

**After:** `~/.ldm/bin/ldm-backup.sh` ... one script, backs up everything, tars to iCloud for offsite. Deployed by `ldm install`.

What it backs up:
- `~/.ldm/` ... crystal.db (sqlite3 .backup), agents, state, config
- `~/.openclaw/` ... main.sqlite, context-embeddings.sqlite, workspace, sessions
- `~/.claude/` ... CLAUDE.md, settings.json, projects (auto-memory + transcripts)
- `~/wipcomputerinc/` ... entire workspace (excludes node_modules, .git/objects, old backups, _trash)

iCloud offsite: compressed tar at `wipcomputerinc-icloud/backups/`. One file per backup. Rotates to 7 days.

Restore script: `~/.ldm/bin/ldm-restore.sh` ... restore from local or iCloud, partial restore with `--only`, dry-run preview.

Tested: 28 GB local backup, 12 GB compressed iCloud tar. All sqlite databases use sqlite3 .backup (handles WAL mode correctly).

### Workspace Migration (iCloud -> ~/wipcomputerinc/)

Moved everything out of iCloud (`~/Documents/wipcomputer--mac-mini-01/`) to local workspace.

- **Repos:** `~/wipcomputerinc/repos/` (was `iCloud/.../Claude Code - Mini/repos/`)
- **Lesa's workspace:** `~/wipcomputerinc/staff/Lēsa/` (was `iCloud/staff/Lēsa/`)
- **Org rename:** `wipcomputer` -> `wipcomputerinc` (local install name, GitHub org stays `wipcomputer`)
- **Git repo naming convention:** `wipcomputer-ldmos-{orgname}-home-private` and `wipcomputer-ldmos-{orgname}-system-private`

All config files updated: both CLAUDE.md files, TOOLS.md, SHARED-CONTEXT.md, WHERE-TO-WRITE.md, HEARTBEAT.md, healthcheck config, repo-locations memory, workspace docs.

### New Repo: wipcomputer/wipcomputer-ldmos-wipcomputerinc-home-private

The workspace (`~/wipcomputerinc/`) is now a git repo. Contains settings/config.json, 13 operational docs (Amazon method), templates, acknowledgements, config-dependencies.json.

### .ldm/ as Source of Truth, .claude/ as Deployment Target

Adopted from the "Anatomy of the .claude/ folder" article. Rules, commands, skills authored in `~/.ldm/shared/`, deployed to `~/.claude/rules/`, `~/.claude/commands/`, etc. by `ldm install`. OpenClaw gets the same content deployed to workspace/TOOLS.md.

Plan committed. Not implemented yet.

### Branch Guard: Workspace Files Allowlist (#185)

TOOLS.md, MEMORY.md, IDENTITY.md, SOUL.md, WHERE-TO-WRITE.md, HEARTBEAT.md added to the branch guard's shared state allowlist. Both agents can now write to workspace files on main.

### Crystal Relay Tickets (#163-#166)

Architecture for hosted MCP server (iOS/cloud Claude Code). Per-agent auth tokens, async embedding queue, CLAUDE.md fallback instruction. Tickets filed, not started.

### Memory Crystal Augmentation Plan (MC #59-#62)

OpenViking-inspired: structured memory categories, dedup before storing, tiered content loading, virtual hierarchy. All additive to Dream Weaver + Crystal. Heavy caveats on each. Plan committed, not started.

### Web Skills for claude.ai (#168)

Plan for deploying LDM OS skills to the Claude web app as a third harness deployment target. Same source (.ldm/), three outputs (CLI, OpenClaw, web).

### Local-First Principle Doc

"OSS means you can run the whole system yourself." Every LDM OS tool must work fully local. The Crystal relay is optional (exists because of iOS platform constraints, not by design choice). Documented the distinction between open core (not OSS) and local-first (what we do).

### Acknowledgements System

12 entries tracking external ideas we draw from. Format: what, where we use it, link, license, date. License guard integration planned (#167). Entries include: QMD (Tobi Lutke), OpenViking (Volcengine), Supermemory (with open core critique), Akshay Pachaar, Gary Tan, m13v, Hruthik Kommuru, @cyrilXBT, @louislva, @mvanhorn, @internetvin, Ole Lehmann.

### Parker's Plane Session (merged)

7 commits: Obsidian as LDMOS UI layer, Supermemory critique, claude-peers-mcp vs Bridge comparison, @mvanhorn workflow takeaways, Bridge docs update (CC-to-CC, session discovery). 9 issues moved from private to public repo.

### Audit-Rules Plan (#183)

`ldm audit-rules` ... detect dead weight in instruction files. 5-check framework: default behavior, conflicts, duplicates, one-off fixes, vague rules. Inspired by Ole Lehmann. Plan committed, not started.

## Tickets Filed This Session

**wip-ldm-os (public):**
- #163 Crystal relay for iOS/cloud
- #164 Per-agent auth tokens
- #165 Async embedding queue
- #166 CLAUDE.md fallback instruction
- #167 License guard checks acknowledgements
- #168 Web skills for claude.ai
- #169 Enforce local-first in CI
- #170 Crystal relay self-hostable
- #171 Bridge session status broadcast
- #172 Bridge evaluate claude/channel push
- #173 Bridge auto-summarize on register
- #174-#182 (moved from private: Obsidian, session status, claude/channel, plan-first, voice, /last30days, Granola, acknowledgements, Supermemory reconcile)
- #183 Audit-rules
- #184 Audit tool paths (run from .ldm not repos)
- #185 Branch guard workspace allowlist (fixed)
- #186 Installer verification for guard fix
- #187 Branch guard worktree warning retry bug

**memory-crystal (public):**
- #59 Structured memory categories
- #60 Dedup before storing
- #61 Tiered content loading
- #62 Virtual hierarchy in search

## Plans Committed

- `current/2026-03-22--cc-mini--workspace-migration.md` (updated with backup + .claude/ deployment sections)
- `current/2026-03-24--cc-mini--org-rename-git-convention.md`
- `current/2026-03-24--cc-mini--comprehensive-backup-fix.md`
- `upcoming/2026-03-23--cc-mini--memory-crystal-augmentations.md`
- `upcoming/2026-03-23--obsidian-as-ldmos-ui-layer.md`
- `upcoming/2026-03-23--claude-peers-mcp-comparison.md`
- `upcoming/2026-03-23--mvanhorn-workflow-takeaways.md`
- `upcoming/2026-03-24--cc-mini--audit-rules.md`

## What's Next

1. Delete old backup dirs (527 GB) once unified backup is proven over a few days
2. Worktree convention update (moving from _worktrees/ to .claude/worktrees)
3. Fix branch guard worktree warning retry bug (#187)
4. Rules/ split of CLAUDE.md (run audit-rules first, cut, then split)
5. Crystal relay (#163) when ready for iOS
