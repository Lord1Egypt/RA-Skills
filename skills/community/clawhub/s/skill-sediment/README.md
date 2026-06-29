# skill-sediment

> One-shot installer and operator for the **OpenClaw skill-sediment plugin extension** —
> automatically distill successful conversation workflows into `SKILL.md` files, then
> promote them into `skills/`.

## Features

- **Auto-sediment** — a background review sub-Agent listens to your conversations
  and writes successful non-trivial workflows out as `SKILL.md` files
- **Convention-dir loading** — drops the plugin into `<workspace>/.openclaw/extensions/skill-sediment/`,
  zero `openclaw.json` change required in the common case
- **PVC-aware** — survives container restart and PVC volume swap; `recover` re-deploys
  when the volume is wiped
- **Self-repair (`heal`)** — detects whitelist loss / file loss / missing
  `validAgentId` and fixes them, then optionally restarts the gateway
- **Managed-env detection** — auto-detects Lobi / Apollo style remote-config
  overrides and warns the user about pod-rebuild implications
- **Version guard** — `install` refuses to deploy on OpenClaw versions below
  the verified baseline (override with `--force-version`)
- **Interactive agent picker** — `install` reads the local agent list and lets
  you pick which agents enable sediment
- **Offline-first** — plugin source bundle (≈91KB tarball) is embedded in
  `assets/`; CDN fallback is optional and unused in normal installs

## Quick Start

```bash
# Install via clawhub
clawhub install skill-sediment

# Or clone directly
git clone https://github.com/Songhonglei/build-better-skills.git
cd build-better-skills/skills/skill-sediment

# Run the installer
python3 scripts/manage.py install

# After the prompted gateway restart
python3 scripts/manage.py doctor
```

## Subcommands

| Command | Purpose |
|---------|---------|
| `install` | Full install (deploy + agent pick + whitelist append + restart prompt) |
| `config` | Print current `plugins.allow` state and recommended action |
| `doctor` | Diagnose plugin files / config / version / sediment dir |
| `recover` | Restore plugin after pod restart (redeploys if PVC volume was swapped) |
| `status` | Show sediment pool: pending incubations vs. activated promotions |
| `heal` | Self-repair: whitelist / files / `validAgentId`, then restart gateway |
| `uninstall` | Remove config entries (`--purge` to also delete the plugin dir; never deletes existing sediments) |

Full design, troubleshooting and tunable parameters: see [SKILL.md](./SKILL.md)
and [references/sediment-internals.md](./references/sediment-internals.md).

## Install in your AI agent

| Agent | Install |
|-------|---------|
| OpenClaw (clawhub.com) | `clawhub install skill-sediment` |
| OpenClaw (GitHub source) | `git clone` then copy `skill-sediment/` into `~/.openclaw/workspace/skills/` |
| Claude Code | Copy to `~/.claude/skills/skill-sediment/` (the OpenClaw plugin layer only loads on OpenClaw — but the management scripts still work as a learning reference) |

## Environment Variables

| Env | Default | Purpose |
|-----|---------|---------|
| `OPENCLAW_WORKSPACE` | `~/.openclaw/workspace` | Workspace root (plugin lives here) |
| `OPENCLAW_CONFIG` | `~/.openclaw/openclaw.json` | Config file (only when allow non-empty) |
| `SKILL_SEDIMENT_AGENTS` | `main` | Default `validAgentId` |
| `SKILL_SEDIMENT_CDN` | (empty) | Optional fallback URL for the plugin tarball |
| `SKILL_SEDIMENT_SHA256` | (empty) | Optional sha256 checksum for the downloaded bundle |
| `SKILL_SEDIMENT_TZ` | `Asia/Shanghai` | Timezone for diagnostics formatting |

## Differences from the internal build

This open-source release intentionally omits the **`cron-setup` subcommand**
and the auto-installed self-healing Cron Job from the internal build. Unattended
scheduling assumes platform-specific orchestration. To get periodic self-repair,
wire `python3 scripts/manage.py heal` into your own scheduler:

- cron: `30 8,13,18 * * * /usr/bin/python3 /path/to/scripts/manage.py heal --valid-agent-id main`
- systemd timer
- Kubernetes CronJob

The `heal` subcommand itself is preserved — it works fine as a manual operation.

## License

[MIT](./LICENSE) — also see the note in SKILL.md about clawhub.com publishing
this skill as MIT-0 (their platform policy); the GitHub source tree remains true MIT.

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)

## Changelog

### v1.0.0 (2026-06-22)

- Initial open-source release
- Forked from internal v0.2.0
- Translated to English (UI / docstrings / comments)
- Removed `cron-setup` subcommand (internal-only; not generic)
- Removed install-time auto Cron Job creation
- Replaced hard-coded `/home/node` with `$HOME` + `Path.home()` fallback
- Added `SKILL_SEDIMENT_TZ` env var (defaults to `Asia/Shanghai`)
- Added LICENSE, README, .gitignore, attribution lines in SKILL.md
