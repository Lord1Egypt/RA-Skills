# Changelog

## 1.2.0 + Oracle review

- Fixes runtime dispatch so `--mode cursor` checks and runs `cursor-agent` instead of looking for a `cursor` binary.
- `geordi run --mode codex --model MODEL_ID` now forwards the model to Codex instead of silently ignoring it.
- Tightens flag handling: required flags (`--goal`, `--accept`) now produce a clear `ERROR: --flag is required` message, while optional flags (`--mode`, `--model`, `--scope`) are silently treated as absent when missing or empty (so a trailing `--model` no longer aborts a run).
- Removes the unused `json_escape` helper.
- Loads optional project defaults from `.geordi.env`.
- Sanitizes public install examples and the streamed installer tarball path; streamed installs now require `GEORDI_TARBALL_URL`.
- Documents Cursor credential-store failures and Windows installer expectations.

## 1.2.0

- Adds **Cursor** and **Claude Code** runtimes alongside Codex and Droid. Geordi now supports four modes: `codex`, `droid`, `cursor`, `claude`.
- New environment overrides: `GEORDI_CURSOR_ARGS` (default `-p --trust --output-format text`) and `GEORDI_CLAUDE_ARGS` (default `-p --dangerously-skip-permissions --output-format text`).
- `geordi doctor` now validates `cursor-agent` and `claude` on `PATH` when those modes are requested.
- `geordi run --model` is honored by Codex, Droid, Cursor, and Claude Code runtimes.
- Adds `examples/cursor-goal.md` and `examples/claude-goal.md`.
- Updates build-loop and agent-identity references to document the four runtimes.

## 1.1.1

- Requires global `AGENTS.md` context by default before Geordi mission prompts.
- Adds `GEORDI_AGENTS_FILE` and `GEORDI_REQUIRE_AGENTS` controls for portable installs.
- Updates Codex/Droid examples and build-loop reference to document the global context step.

## 1.1.0

- Renames the public bundle and command to `geordi`.
- Merges the reusable geordi build-pipeline discipline into the installable mission runner.
- Adds sanitized references for the build loop and Geordi builder identity.
- Keeps Codex and Droid modes, goal/mission state, acceptance checks, receipts, and resumable logs.

## 1.0.0

- Initial public installable mission-runner bundle.
- Adds install script, CLI, Codex mode, Droid mode, goal/mission state, acceptance checks, and examples.
- Sanitized for public reuse: no private hostnames, private IPs, operator names, account-specific model IDs, or secrets.
