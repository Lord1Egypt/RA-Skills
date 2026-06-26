# Changelog

## [0.1.0] — 2026-04-07

### Added — Phase 1: Upstream Watcher + Analysis Pipeline

**`ustack import <github-url> [--name <id>]`**
- Clones or pulls upstream repo
- Detects key files: control docs, config, skills, tooling
- Detects structure: skill count, format, host conventions, category
- Writes manifest.json with current HEAD sha
- Preserves previous sha for change detection
- Saves README snapshot for fast inspection

**`ustack analyze <upstream-id>`**
- Compares HEAD to previous sha via git diff
- Extracts commit log and changed file list
- Classifies impact by 8 areas: skills, install, browser, workflow, safety, tooling, docs, config
- Assesses portability: portable / needs-adaptation / host-specific
- Produces structured JSON artifact + human-readable markdown analysis

**`ustack publish <upstream-id>`**
- Reads latest analysis run
- Generates website-ready markdown page with YAML frontmatter
- Includes: summary, impact table, portability breakdown, commit list, usage instructions, trust note
- Writes to both run directory and `.ustack/site/updates/<id>/`
- Designed to drop directly into AGI.security blog/update feed

**`ustack update <upstream-id>`**
- Combines import → analyze → publish in one command
- Only proceeds with analyze+publish if upstream actually changed
- The canonical cron-friendly command

**`ustack doctor`**
- Shows configured upstreams with health status
- Shows last import date, last analysis date, skill count, host conventions
- Flags upstreams with unanalyzed changes pending
- Lists recent run artifacts
