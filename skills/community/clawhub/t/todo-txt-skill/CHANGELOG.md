# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Bundled `scripts/install_todo_cli.sh` installer for `todo.sh` (macOS via Homebrew, Linux from source).

### Changed
- The agent no longer checks whether `todo.sh` is installed on every run; it just runs the requested command and falls back to `scripts/install_todo_cli.sh` (then the manual steps) only if that command fails.

## [1.0.0] - 2026-06-11

### Added
- Initial release of the todo.txt Claude skill (`SKILL.md`).
- Installation guidance for `todo.sh` on macOS (Homebrew) and Linux (from source).
- Command reference covering add, list/filter, complete, prioritize, edit, delete, and maintenance actions.
- todo.txt format cheatsheet (priorities, dates, projects, contexts, metadata).
- Behavior guidelines so the agent re-lists tasks after changes and suggests `+project`/`@context` tags.
- Open-source project files: README, LICENSE (MIT), CONTRIBUTING guide, and GitHub issue/PR templates.

[Unreleased]: https://github.com/aguilera-ee/todo.txt-skill/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/aguilera-ee/todo.txt-skill/releases/tag/v1.0.0
