# Changelog

All notable changes to this skill will be documented in this file.

## [1.0.0] - 2026-03-19

### Added

- **SKILL.md** — Complete skill definition with Pipeline + Tool Wrapper design patterns
- **Standard Directory Structure** — Dual workspace architecture:
  - `Workspace_Human/` — Human-facing files (input, output, backup, temp)
  - `Workspace_Agent/` — Agent-only files (memory, skills, subagents, shared_context, artifacts, cache, logs, skills_custom, prompts, kb)
- **Pipeline Orchestrator** (`scripts/pipeline.sh`) — Master script that runs all 5 steps in sequence: Audit → Organize → Clean → Archive → Sync
  - Supports `--all` (full pipeline), `--dry-run` (preview only), and step selection (e.g., `audit organize`)
  - Optional sync step gracefully skipped if gog CLI is not configured
- **Health Check** (`scripts/health-check.sh`) — Workspace entropy audit with 0-100 health score:
  - Broken symlinks detection
  - Empty directory detection
  - Large file detection (>10MB)
  - Malformed filename detection
  - Disk usage by directory
  - Recent activity summary
- **Standardize** (`scripts/standardize.sh`) — Ensures all standard directories exist and detects misplaced files in root
- **Organize** (`scripts/organize.sh`) — Auto-classifies files from `Workspace_Agent/artifacts/` into `Workspace_Human/output/` subdirectories by file type
- **Cleanup** (`scripts/cleanup.py`) — Safe Python-based cleanup with dry-run default:
  - Moves files to system trash (recoverable via `trash-put`)
  - Configurable patterns via `config/patterns.json`
  - Age and size filters
  - JSON output for automation
- **Archive** (`scripts/archive.sh`) — Interactive archiver that moves files older than N days into `archive/YYYY-MM/` structure
- **Sync** (`scripts/sync.sh`) — Optional Google Drive sync via `gog` CLI:
  - Syncs `Workspace_Human/` → `AI_Workspace/`
  - Syncs `Workspace_Agent/` → `AI_Workspace/` (opt-in)
  - Backs up core config files → `AI_Workspace_Backup/`
  - Gracefully skipped if gog is not installed/authenticated
- **Config Files**:
  - `config/patterns.json` — Customizable cleanup patterns and protected paths
  - `config/sync-config.json` — Sync toggle switches and folder names

### Design Patterns

- **Pipeline** — Strict 5-step workflow with checkpoint gating
- **Tool Wrapper** — File system operations encapsulated in reusable scripts

### Security Features

- Never uses `rm` — all deletions go through `trash-put` (recoverable)
- Default dry-run on all destructive operations
- Protected paths whitelist (core config files, .git, memory/, skills/, Workspace_Human/)
- 24-hour recent-file protection

### Recommended Usage

```bash
# Full pipeline (recommended for weekly maintenance)
bash {{SKILL_DIR}}/scripts/pipeline.sh --all

# Quick session cleanup
bash {{SKILL_DIR}}/scripts/pipeline.sh audit organize

# Preview what would be cleaned
python3 {{SKILL_DIR}}/scripts/cleanup.py
```
