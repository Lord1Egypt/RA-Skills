---
name: teleport-tbot-bootstrap
description: Bootstrap a persistent Teleport Machine ID (tbot) setup on macOS using LaunchAgent and tbot configure identity. Trigger when asked to set up, automate, or validate local Teleport bot identity refresh, including proxy/token/join-method inputs, LaunchAgent persistence, and first-run verification with tsh. Complements the teleport-tsh-ssh skill for day-to-day SSH/command/scp usage with the refreshed identity.
---

# teleport-tbot-bootstrap

Set up a local, persistent Machine ID bot on macOS for OpenClaw/agent SSH access.

Pair this with `teleport-tsh-ssh` for operational host access once identity refresh is in place.

## Compatibility

Tested against Teleport/tbot **18.7.0**.

## Inputs to collect

- Teleport proxy address (for example `teleport.example.com:443`)
- Bot onboarding secret (token and/or registration secret depending on cluster setup)
- Bot role(s) / bot name context from Teleport setup
- Optional output directory (default: `~/.openclaw/workspace/tbot`)

## LaunchAgent behavior (macOS)

Use LaunchAgent for user-session persistence.

- Starts automatically at user login.
- Starts immediately when loaded with `launchctl bootstrap gui/<uid> ...`.
- Restarts automatically when `KeepAlive` is true.
- Does **not** require root when installed under `~/Library/LaunchAgents`.

Use LaunchDaemon only when system-wide root context is explicitly required.

## Workflow

1. Ensure prerequisites: `tbot`, `tsh`, writable output dir.
2. Create output + state dirs (default `~/.openclaw/workspace/tbot` and `~/.openclaw/workspace/tbot/state`).
3. Generate config via `tbot configure identity` (do not hand-write config):
   - destination should point to output dir (`file://.../tbot`)
   - storage should point to state dir (`file://.../tbot/state`)
   - set proxy and join method (`bound_keypair` preferred)
   - write config file to `~/.openclaw/workspace/tbot/tbot.yaml`
4. Create LaunchAgent plist to run `tbot start -c <config>` with `RunAtLoad` + `KeepAlive`.
5. Load/start LaunchAgent.
6. Verify identity output exists and is fresh (`.../tbot/identity`).
7. Verify access path with `tsh -i <identity> --proxy=<proxy> ls`.
8. Report status and next steps.

## Bound keypair guidance

Prefer `bound_keypair` join method for recoverability after interruptions (sleep/reboot).
Use high recovery limits for resilient rejoin flows when appropriate.

Use a fresh bot/state directory for first-time setup. Reusing state from a different bot/token can cause key lookup mismatches.

Use Teleport-side preregistration first (Bot + role + join config). Keep access label-scoped (for example `openclaw-allowed: "true"`) so access is opt-in per node.
See:

- `references/teleport-prereq-examples.yaml`
- https://goteleport.com/docs/reference/cli/tbot/

## Security notes

- Never commit onboarding tokens or registration secrets to git.
- Treat `tbot.yaml`, bot state, and identity outputs as sensitive material.
- Prefer secure secret delivery (interactive input, secret manager, env injection) over plaintext chat logs.

## Known limitations (v1.0.0)

- Focuses on SSH identity output workflows (not Teleport app/db/kubernetes outputs).
- Uses LaunchAgent user context; does not provide full LaunchDaemon/root automation.

## Commands (reference)

- Generate config:
  - `tbot configure identity --output ~/.openclaw/workspace/tbot/tbot.yaml ...`
- Start once (foreground test):
  - `tbot start -c ~/.openclaw/workspace/tbot/tbot.yaml`
- LaunchAgent load:
  - `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.openclaw.tbot.plist`
- LaunchAgent restart:
  - `launchctl kickstart -k gui/$(id -u)/com.openclaw.tbot`

## Clawhub listing copy

### Clawhub short description

Bootstrap a persistent Teleport Machine ID (`tbot`) identity on macOS using LaunchAgent and `tbot configure identity`.

### Companion skill

Use with `teleport-tsh-ssh` for day-to-day SSH/command/scp operations using the refreshed identity.

### Clawhub long description

Set up a local, persistent Machine ID bot for automation hosts.
Generate config using `tbot configure identity`, install a user LaunchAgent (`com.openclaw.tbot`), and validate identity output with a `tsh` smoke test.

Includes LaunchAgent persistence (no root), bound keypair onboarding support, Teleport prereq examples (Role/Bot/Token), label-scoped node access patterns, registration-secret retrieval guidance, and first-run fresh-state guidance.

## Resources

- Setup script: `scripts/bootstrap_tbot_launchagent.sh`
- Teleport YAML examples: `references/teleport-prereq-examples.yaml`
- LaunchAgent template notes: `references/launchagent-notes.md`

## Uninstall / cleanup

- `launchctl bootout gui/$(id -u)/com.openclaw.tbot`
- `rm -f ~/Library/LaunchAgents/com.openclaw.tbot.plist`
- Remove bot files if desired: `rm -rf ~/.openclaw/workspace/tbot`
