# Changelog

All notable changes to Skill Doctor are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/); this project adheres to semantic versioning.

## [1.0.0] - 2026-05-23

Initial release.

### Added
- `audit` command: full health report covering conflicts, security flags, and versions.
- `conflicts` command: detects skills whose triggers overlap, via shared explicit trigger phrases and keyword Jaccard overlap (default threshold 0.20).
- `security` command: inline red-flag scan with severity ratings — remote code execution, credential exfiltration, hard-coded secrets, SSH/credential file access, reverse shells, destructive commands, `shell=True`, and `eval`/`exec`.
- `stale` command: compares installed versions against the latest ClawHub release using the `clawhub` CLI when available.
- `which "<prompt>"` command: predicts which installed skill will fire for a prompt and warns when the choice is ambiguous.
- Auto-detection of the installed-skills directory across common OpenClaw and Claude layouts, with `--skills-dir` override.
- Zero required dependencies: pure Python standard library, with optional PyYAML for the most robust frontmatter parsing.
