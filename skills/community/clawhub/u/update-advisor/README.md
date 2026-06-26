# update-advisor

An [OpenClaw](https://openclaw.ai) skill for safely checking and applying OpenClaw updates — with changelog analysis, risk rating, and a Gateway-independent recovery watchdog for Execute mode on macOS and Linux/systemd.

## Why this skill?

`openclaw update` restarts the Gateway, which disconnects the active chat session. Without a skill to handle this gracefully, you'd have no way to confirm whether the update succeeded. This skill solves that by:

1. Analyzing the changelog *before* updating (risk rating, relevance to your setup, new features)
2. Launching a pre-update recovery watchdog that can run `openclaw gateway install` if Gateway does not recover
3. Detecting installation ownership issues that would cause duplicate installations in multi-user environments

## Features

- **Check mode**: Fetch latest version, parse changelog delta, flag high-risk items, assess relevance to your config
- **Execute mode (v2)**: Requires explicit confirmation for a watchdog-assisted flow that starts recovery monitoring before `openclaw update`
- **Gateway-independent recovery**: `scripts/recovery-watchdog.sh` checks `openclaw gateway status` after a grace window and runs bounded `openclaw gateway install` retries when needed
- **macOS/Linux arming helper**: `scripts/arm-recovery-watchdog.sh` resolves `OPENCLAW_BIN`, then arms and verifies either a macOS LaunchAgent (`launchctl print`) or a Linux systemd user unit (`systemctl --user show`), and cleans up state/log artifacts; the plist template remains inert documentation
- **Multi-user safety**: Detects when OpenClaw is owned by a different OS user and stops before creating a duplicate installation
- **Dynamic changelog path**: Uses `openclaw update status --json` when available, with npm-global / binary-path / pnpm fallbacks

## Usage

Just talk to your agent naturally:

| Intent | Example phrases |
|--------|----------------|
| Check for updates | "Check for OpenClaw updates" / "Any new version?" |
| Execute update | "Confirm update" / "Execute update" / "Upgrade OpenClaw" |

## Installation

```bash
clawhub install lzyling/update-advisor
```

Or copy the skill directory into `~/.openclaw/workspace/skills/update-advisor/`.

## Requirements

- OpenClaw with skills support
- `npm` available in PATH (fallback for checking the latest version when OpenClaw update metadata is unavailable)
- `python3` available in PATH (used for changelog parsing and path/XML escaping)
- Execute recovery arming requires either macOS `launchctl` + `plutil`, or Linux `systemd-run` + `systemctl --user`

## Security boundaries

- Check mode is read/report only and does not modify OpenClaw state.
- The only routine network lookup is `npm view openclaw version` when OpenClaw update metadata is unavailable.
- Personalized relevance analysis may optionally use `MEMORY.md`, but only as read-only context and only after explicit user consent; Check mode never writes to memory files.
- Execute mode requires explicit user confirmation before any persistent side effect. It can run `openclaw update` and temporarily arm a user-level launchd/systemd recovery job.
- The watchdog writes bounded temporary state/log files and cleans them up after recovery. It does not read secrets or send data to third-party endpoints.

## How it works

```
check-update.sh
  ├── Gets current + latest version via npm view
  ├── Parses local CHANGELOG.md for delta between versions
  ├── Runs openclaw doctor
  └── Outputs structured JSON

arm-recovery-watchdog.sh — arm/verify/cleanup temporary launchd/systemd recovery job
recovery-watchdog.sh     — bounded Gateway status/install recovery loop
parse_changelog.py       — extracts and flags risky changelog entries
assemble_result.py       — assembles final JSON for the agent
```

The agent reads the JSON, performs analysis, and either reports findings (check mode) or proceeds with the safe update flow (execute mode).

Execute mode v2 now uses an external watchdog path designed to survive Gateway restarts. Before `openclaw update`, the agent must ask for explicit confirmation, pass ownership/dry-run checks, arm the watchdog with `scripts/arm-recovery-watchdog.sh` while passing the resolved OpenClaw binary path, verify the external job (`launchctl print` on macOS, `systemctl --user show` on Linux/systemd), and only then start the update. If arming verification fails or the OS/backend is unsupported, the update must not run. After recovery, the same helper performs cleanup from the saved state file.

## Compatibility

| Platform | Check mode | Execute recovery mode | Notes |
|---|---:|---:|---|
| macOS | ✅ | ✅ | Uses launchd LaunchAgent via `launchctl` + `plutil`. |
| Linux with systemd user manager | ✅ | ✅ | Uses `systemd-run --user` and verifies with `systemctl --user show`. |
| Linux without systemd user manager | ✅ | ❌ | The skill must stop before `openclaw update`; no protected arming backend is available yet. |
| Windows native | ❌ | ❌ | Not supported; use WSL/Linux-like shell only for check-mode experimentation. |

## Multi-user note

If OpenClaw was installed by a different OS user (e.g. via Homebrew under another account), running `openclaw update` as the current user may silently install a second copy instead of updating the original. This skill detects that scenario and stops with clear instructions before anything breaks.

## License

MIT
