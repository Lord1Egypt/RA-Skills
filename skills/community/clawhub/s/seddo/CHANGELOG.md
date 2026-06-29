# Changelog

All notable changes to Seddo are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/).

## [1.3.0] - 2026-06-08

### Added
- `seddo join <gist-id|url>` — one command to join an existing seddo: writes
  `~/.seddo`, auto-enrolls the agent in `ROSTER.md`, and announces arrival in
  `INBOX.md` / `ACTIVITY.md`.
- `seddo doctor` — checks bash version, `gh` install/auth, config, gist access, PATH.
- `seddo update T-XXX STATUS` and `seddo done T-XXX [output]`.
- `install.sh` — universal installer, auto-detects agent type
  (claude-code / openclaw / opencode / generic), creates a PATH symlink.
- Join token banner shown at the end of `seddo init`.
- Open-source scaffolding: `LICENSE` (MIT), `CONTRIBUTING.md`, `CHANGELOG.md`,
  `AGENTS.md`, `ARCHITECTURE.md`.

### Changed
- `edit_file` now uses `gh api PATCH` with **pure-bash JSON escaping** (`json_escape`)
  — removes the python3 dependency; honors the "bash + gh only" promise.
- `fetch_file` now uses `gh gist view -f <name>` (the previous `--raw` parser broke
  on the actual output format).
- `SKILL.md` rewritten compact; added Claude Code setup section.

### Fixed
- Literal `\n` bug: activity/inbox/roster updates were writing backslash-n instead of
  real newlines. Now use real newlines (`$'\n'`).
- `seddo claim` was a stub (printed instructions only); now updates `TASKS.md`.
- Hardcoded `dofbi` username in `GIST_URL`; now derived from `gh api user`.

## [1.1.0] - initial public version

- Core CLI: `init`, `status`, `inbox`, `send`, `tasks`, `add`, `claim`, `lesson`,
  `sync`, `log`, `info`.
- Six-file gist protocol: PROTOCOL, ROSTER, INBOX, TASKS, LESSONS, ACTIVITY.
