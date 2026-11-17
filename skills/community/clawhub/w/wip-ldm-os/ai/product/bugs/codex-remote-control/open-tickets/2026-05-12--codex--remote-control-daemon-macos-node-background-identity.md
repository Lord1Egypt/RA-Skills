---
title: "Codex Remote Control daemon shows as generic Node in macOS background and privacy prompts"
status: open
priority: P1
owner: Remote Control Installer Cody
repo: wip-codex-remote-control-private
created: 2026-05-12
surface: codex-daemon macOS lifecycle
---

# Codex Remote Control Daemon Shows As Generic Node In macOS Background And Privacy Prompts

## Problem

After upgrading Node, Parker is repeatedly seeing macOS permission prompts for `node` while running Codex Remote Control on a headless machine.

Observed local state during diagnosis:

- `codex-daemon 0.0.4-alpha.13` was running as pid `7307`.
- It was paired to the relay.
- It was listening on `127.0.0.1:7777`.
- The long-lived background process was:

```text
/opt/homebrew/Cellar/node/25.9.0_3/bin/node /opt/homebrew/bin/codex-daemon start --foreground
```

This is not random Node noise. It is Codex Remote Control running as a detached Node process.

The current daemon start path in `wip-codex-remote-control-private/src/cli.ts` daemonizes by spawning:

```ts
spawn(process.execPath, [process.argv[1], "start", "--foreground"], ...)
```

Because `process.execPath` is Homebrew Node, macOS attributes the long-lived background process and protected-data prompts to generic `node`, not to WIP, Codex Remote Control, or a named local service.

This blocks headless dogfood operation. Parker cannot be required to click `Allow` every time a background Remote Control process trips a macOS prompt.

## Immediate workaround

```bash
codex-daemon stop
```

This removes the prompt source for now, but disables Remote Control until the daemon is started again. It is not a product fix.

## Existing LDM OS machinery to reuse

Do not invent a new service system before checking the LDM OS service path.

LDM OS already has a managed LaunchAgent pattern:

- Templates live in `wip-ldm-os-private/shared/launchagents/`.
- `ldm install` deploys templates to `~/Library/LaunchAgents/`.
- `ldm install` replaces placeholders like `{{HOME}}`.
- `ldm install` unloads and reloads changed plists.
- `ldm status` checks the managed LaunchAgents.

Existing managed examples:

- `ai.openclaw.gateway.plist`
- `ai.openclaw.healthcheck.plist`
- `ai.openclaw.ldm-backup.plist`

There is also an LDM Dev Tools app-wrapper concept in the DevOps toolbox:

- `LDMDevTools.app` is documented as a macOS `.app` wrapper for automation that needs Full Disk Access.
- It is meant to give macOS one app identity instead of granting broad permissions to shell scripts.
- Current LDM OS code also documents old `LDMDevTools.app` cron usage as broken and cleans stale cron entries that reference it.

So the implementation should not blindly route the daemon through `LDMDevTools.app`. Treat it as an option to evaluate if LaunchAgent alone does not fix the macOS identity or TCC prompt problem.

Important distinction: LaunchAgent management and macOS process identity are related but not the same problem. A LaunchAgent that still runs `/opt/homebrew/bin/node /opt/homebrew/bin/codex-daemon ...` may improve lifecycle, login restoration, crash restart, and `launchctl` visibility while macOS still attributes privacy or background prompts to the interpreter. Treat prompt naming as an early acceptance check, not a polish item at the end.

macOS also has multiple prompt and management surfaces:

- Background-process notification, such as "`X` is running in the background": LaunchAgent management can help because the daemon becomes a managed service, but the visible name may still come from the executable identity.
- TCC/privacy prompts, such as Full Disk Access or protected folder access: these are identity-based and may require a signed `.app` bundle, native wrapper, or equivalent WIP identity instead of the Homebrew Node interpreter.
- Login Items and background-item management: LaunchAgent deployment is the right first path and should make this surface cleaner.

## Desired product behavior

Codex Remote Control should have a headless-clean macOS daemon lifecycle:

- `codex-daemon start` should not create repeated generic `node` prompts.
- Reboot or login should restore the daemon through a managed service path.
- The process should be inspectable as a named WIP/Codex Remote Control service.
- Logs should continue to land under `~/.codex-daemon/` or another documented WIP-owned log path.
- `codex-daemon status` should report service state clearly.
- `codex-daemon stop` should stop the managed service cleanly.

## Preferred fix shape

Start with the lowest-risk LDM-native path:

1. Add a Codex Remote Control LaunchAgent template, probably under the package or LDM-managed service inventory.
2. Give it a stable label, for example `ai.wip.codex-remote-control.daemon` or `com.wipcomputer.codex-daemon`.
3. Have install/update deploy it through the same LDM OS LaunchAgent machinery used for gateway, healthcheck, and backup.
4. Stop self-daemonizing through `spawn(process.execPath, ...)` for the normal managed path.
5. Keep `codex-daemon start --foreground` for debugging.
6. Make `codex-daemon start`, `stop`, and `status` aware of the service path on macOS.
7. Immediately test macOS prompt naming after this slice ships. If prompts still say generic `node`, escalate to a packaged `.app` or native wrapper path instead of spending more time on LaunchAgent tweaks.

If macOS still attributes protected-data prompts to generic Node because the LaunchAgent runs the Homebrew `node` interpreter, then evaluate the durable packaged path:

- a small native or packaged `WIP Codex Remote Control Daemon.app`,
- or a native wrapper binary,
- or a reusable app-wrapper pattern based on the LDM Dev Tools approach, after confirming the current LDMDevTools PID/cron issue is not inherited.

## Acceptance

- On macOS, starting Remote Control uses the managed service path instead of self-spawning generic `node` for normal background mode.
- `codex-daemon start` returns promptly and starts the managed daemon.
- `codex-daemon stop` stops the managed daemon.
- `codex-daemon status` reports the managed daemon status, pid, paired state, and log path.
- After reboot or login, the daemon can come back without Parker manually running a terminal process.
- The daemon remains paired across restart and does not require `codex-daemon link` unless credentials are actually missing or invalid.
- macOS does not repeatedly prompt for generic `node` in normal headless operation.
- If macOS prompts at all, the prompt names a WIP/Codex Remote Control identity, not generic `node`.
- Local dogfood verifies: no repeated popup while the daemon is running, Remote Control still pairs, browser to TUI works, TUI to browser works.

## Tests

- Add a unit or source-shape test proving normal `codex-daemon start` no longer routes through `spawn(process.execPath, ["start", "--foreground"])` on macOS.
- Add a lifecycle test or scripted smoke for service install, start, status, and stop where feasible.
- Keep existing daemon tests green.
- Keep the Remote Control regression contract green.

## Non-goals

- Do not weaken daemon pairing, E2EE key persistence, thread authority binding, or relay auth.
- Do not require Parker to grant permissions to generic Node, Terminal, or shell as the durable fix.
- Do not route production daemon lifecycle through the old broken `LDMDevTools.app` cron path without first proving that path is fixed.
- Do not change hosted relay behavior for this ticket unless a service lifecycle change requires installer metadata updates.

## Handoff

This belongs with Remote Control installer/daemon lifecycle work, not hosted relay hardening.

The key implementation question is whether LDM OS LaunchAgent management is sufficient to fix the user-visible macOS identity problem. If not, the ticket should escalate to a packaged app/native wrapper so macOS has a named WIP identity for the background process.
