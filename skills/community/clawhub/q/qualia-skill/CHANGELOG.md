# Changelog

## 2.1.1 (2026-06-29)

Install and setup documentation hardening.

- Documented the working OpenClaw install command: `openclaw skills install qualia-skill`
- Added warnings that owner-qualified slugs such as `@fabbe1999/qualia-skill` or `fabbe1999/qualia-skill` may fail on current installers
- Added explicit OpenClaw config example for `skills.entries.qualia.env.QUALIA_API_KEY`
- Clarified that the ClawHub slug is `qualia-skill` but the loaded skill name/config key is `qualia`
- Added post-install verification and troubleshooting steps so a silent inactive install is easier to diagnose

## 2.1.0 (2026-06-10)

Agent-native release. Built for AI agents driving the CLI programmatically.

- Global `--json` flag on all commands: exactly one JSON object/array on stdout, errors as `{"error": {"code", "message", "details"}}` with matching exit code
- Stable exit-code contract: 0 ok, 1 generic, 2 usage, 3 auth, 4 insufficient credits, 5 validation, 6 not found, 7 connection
- New `doctor` command: self-test for API key, auth/connectivity, and models endpoint
- Keyword-rich skill description for agent search (VLA, pi0, pi0.5, GR00T N1.5, ACT, SmolVLA, SARM, LeRobot)
- SKILL.md sections added: Verify your install, Machine-readable output, Exit codes
- Changelog introduced

## 1.x

Initial releases: pure-stdlib Python CLI wrapping the Qualia API (models, instances, credits, projects, dataset-keys, hyperparams, finetune, status, cancel), SKILL.md instructions for ClawHub/OpenClaw agents, human-readable output only.
