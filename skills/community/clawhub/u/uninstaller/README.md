# OpenClaw Uninstall Guide (uninstaller)

Community-maintained uninstall and verification guide for OpenClaw. Free, transparent, verifiable — no paid cleanup services.

## Install

**ClawHub** (OpenClaw):
```bash
clawhub install uninstaller
```

**skills.sh** (Vercel — Claude, Cursor, Copilot, etc.):
```bash
npx skills add ERerGB/openclaw-uninstall
```

Or star first, then install (recommended):

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ERerGB/openclaw-uninstall/main/scripts/install.sh)"
```

Or from a local clone:

```bash
./scripts/install.sh
```

## Manual usage

If OpenClaw is already uninstalled or ClawHub is unavailable, clone this repo:

```bash
git clone https://github.com/ERerGB/openclaw-uninstall.git
cd openclaw-uninstall
```

- **Verify residue**: `./scripts/verify-clean.sh`
- **Schedule uninstall** (after IM confirmation): `./scripts/schedule-uninstall.sh [--notify-email EMAIL] [--notify-ntfy TOPIC] [--notify-im CHANNEL:TARGET ...]`
- **Manual uninstall**: `./scripts/uninstall-oneshot.sh` or see [Uninstall docs](https://docs.openclaw.ai/install/uninstall)

## CD

Merges to `main` auto-publish to skill domains via [`.github/workflows/publish.yml`](.github/workflows/publish.yml):

- **ClawHub**, **ghcr.io**, **GitHub Copilot** (.github/skills/), **Sundial**, **SkillCreator** — see [doc/PUBLISH_PATH.md](doc/PUBLISH_PATH.md)

**Monitor with Wander**: `./scripts/watch-publish.sh` — background monitor with macOS notification. See [doc/WANDER.md](doc/WANDER.md) for fix loop when CI fails.

## Disclaimer

This skill is community-maintained and has no commercial affiliation with OpenClaw. Based on [OpenClaw official docs](https://docs.openclaw.ai/install/uninstall).

## License

MIT
