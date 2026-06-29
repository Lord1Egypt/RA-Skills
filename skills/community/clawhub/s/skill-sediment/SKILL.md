---
name: skill-sediment
description: >
  Install and operate the OpenClaw skill-sediment plugin extension (turns successful
  conversations into auto-generated SKILL.md files, then promotes them to skills/).
  Covers: install (with interactive agent selection), heal (self-repair: detect and fix
  whitelist/file loss, supplement missing validAgentId, auto-restart gateway), doctor
  (diagnostics), recover (restore after pod restart), status (sediment pool stats),
  config (current state), uninstall. Triggers on: sediment / auto-skill-sediment /
  install/port/clone sediment / sediment not working / sediment pool / uninstall
  sediment. Note: unrelated to the same-named Rust semantic-memory MCP (store/recall);
  does not cover OpenClaw installation itself nor publishing to Skill Hubs.
---

> - **Author**: Evan Song <Songhonglei@users.noreply.github.com>
> - **Repository**: https://github.com/Songhonglei/build-better-skills
> - **License**: MIT — see [LICENSE](./LICENSE)
> - **Version**: 1.0.0

# skill-sediment

One-shot installer for the **OpenClaw skill-sediment plugin extension** — auto-distill
successful conversation workflows into `SKILL.md` files, then promote them to `skills/`.

## Core Facts

- **What is being ported**: an OpenClaw plugin extension (not an MCP, not a standalone
  service) that listens to conversations and writes successful workflows as SKILL.md.
- The plugin is ≈340KB of pure TypeScript source (9 files), depending only on
  OpenClaw core's built-in `plugin-sdk` + `typebox`.
- **No embedding model required** — sediment uses LLM semantic judgement, not vector retrieval.
- The plugin source is **already embedded in `assets/plugin-source/`** (flat directory
  of 9 TypeScript files + `package.json` + `openclaw.plugin.json`) — offline install
  works out of the box. A legacy `.tar.gz` fallback path is also supported for
  backward compatibility.

## Quick Install

```bash
cd <this skill directory>
python3 scripts/manage.py install
# Then follow the prompt to manually restart: openclaw gateway restart
# Verify after restart: python3 scripts/manage.py doctor
```

In most cases `plugins.allow` is empty, so the plugin loads automatically from the
convention directory — **no config change required**, just restart.

`--valid-agent-id` is only needed when restricting which agents get sediment enabled
(comma-separated, e.g. `main,debp`; defaults to `main`).

## Subcommands

| Command | Purpose |
|---------|---------|
| `install` | Full install: env check → deploy plugin to convention dir → interactive agent selection → allow-empty auto-load / allow-nonempty whitelist append → restart prompt |
| `config` | Print current allow state and recommended actions (helpful for managed pods) |
| `doctor` | Diagnose: version / plugin-sdk / plugin files / allow whitelist / validAgentId / sediment_skills dir |
| `recover` | Restore after pod restart (plugin present → OK; PVC volume swapped → redeploy) |
| `status` | Inspect sediment pool: pending incubations (sediment_skills/) and activated promotions (skills/) |
| `heal` | Self-repair: detect and fix whitelist/file loss, supplement missing validAgentId, auto-restart gateway |
| `uninstall` | Remove allow/entries config entries (add `--purge` to also remove plugin dir; **never deletes already-sedimented SKILL.md**) |

> **Note**: this open-source version intentionally omits the `cron-setup` subcommand
> from the internal build, since unattended scheduling assumes platform-specific
> orchestration. Use `heal` manually, or wire it into your own scheduler (cron, systemd
> timer, K8s CronJob, etc.) by invoking `python3 scripts/manage.py heal`.

## openclaw.json Changes

| Scenario | Change |
|----------|--------|
| `plugins.allow` empty | **No openclaw.json change**, convention dir auto-loads ✨ |
| `plugins.allow` non-empty without this plugin | Idempotently append `"skill-sediment"` to allow |
| `plugins.entries` | Optionally append validAgentId config (can be added manually any time) |

Convention-dir loading **no longer requires `plugins.load.paths`**; `install` does
not touch it.

## Key Constraints (must obey)

### 1. Plugin directory uses the workspace convention path
OpenClaw auto-discovers plugins under:
```
<workspace>/.openclaw/extensions/<plugin-name>/
```
The plugin is deployed here (mounted on PVC, survives container restart/volume swap).
**Do not put it under `/app/extensions`** (container layer is restored on restart).

When `plugins.allow` is empty, all plugins in this dir **auto-load — no whitelist
needed**. When non-empty, the plugin must be explicitly listed in allow.

### 2. Managed environments (Lobi / Apollo)
If `plugins.allow` is non-empty and requires a whitelist append, you'll be writing
openclaw.json. Managed pods face an override risk:
- **Pre-detect**: `LOBI_SYNC_ENABLED` / `APPID=clawbot*` / Apollo signals → skip
  local write, redirect to remote console config
- The plugin file itself (convention dir) lands locally regardless, unaffected by
  managed-config sync

If `plugins.allow` is empty (most cases), managed and unmanaged pods behave
**identically** — zero config change.

### 3. Gateway restart is not automatic by default
By default `install` only **prompts for manual restart**. Pass `--auto-restart` to
have it restart the gateway automatically.

### 4. Version compatibility
Verified OpenClaw baseline: `2026.3.8`. `install` auto-compares the target version:
- `= 2026.3.8` → green light
- `> baseline` → warn and continue (the plugin API surface is narrow; rely on
  post-install smoke test)
- `< baseline` → refuse (missing-API risk); pass `--force-version` to override

## Verify the plugin actually loaded

`doctor` checks files/config, but **hook mount status only shows in gateway logs**.
In K8s containers logs go to stdout (usually no systemd/journalctl), pick by env:

```bash
# Inside container: tail PID 1 stdout
grep -r "\[skill-sediment\]" /proc/1/fd/1 2>/dev/null | tail
# Or OpenClaw's own logs
grep "\[skill-sediment\]" ~/.openclaw/logs/*.log 2>/dev/null | tail
# Or K8s from outside
kubectl logs <pod> | grep "\[skill-sediment\]"
```

Final confirmation that sediment actually works: after a normal conversation accumulates
~15 tool calls, `status` should show pending sediments under `sediment_skills/`.
`doctor` also prints these two steps at the end.

## Path Environment Variables (multi-pod / non-standard environments)

| env | Default | Description |
|-----|---------|-------------|
| `OPENCLAW_WORKSPACE` | `~/.openclaw/workspace` | Workspace root (plugin dir lives here) |
| `OPENCLAW_CONFIG` | `~/.openclaw/openclaw.json` | Config file (only needed when allow non-empty) |
| `SKILL_SEDIMENT_AGENTS` | `main` | Default validAgentId |
| `SKILL_SEDIMENT_CDN` | (empty) | Fallback URL for the plugin tarball (only used if the bundled `assets/` copy is missing; typical installs never use this) |
| `SKILL_SEDIMENT_SHA256` | (empty) | Optional sha256 checksum for the downloaded bundle |
| `SKILL_SEDIMENT_TZ` | `Asia/Shanghai` | Timezone for any local time formatting in diagnostics |

Convention plugin path (auto-computed, no manual config needed):
```
<OPENCLAW_WORKSPACE>/.openclaw/extensions/skill-sediment/
```

## Sediment Mechanism (FAQ after install)

- **Trigger**: every ~15 tool calls, a background review sub-Agent is kicked off (`nudgeInterval` is tunable)
- **Output**: `sediment_skills/*.md` (pending) → after a second hit, promoted to `skills/*.md` (activated)
- **Second-hit logic**: a different parent session hits again, OR the sediment is ≥1 day old and the same session hits again
- **Eviction**: untouched for 10 days → auto-evict / max 20 per agent / 3-day grace for new ones
- Full architecture (6 Gates / lifecycle / promote guards) is in `references/sediment-internals.md`

## License

MIT — see [LICENSE](./LICENSE) for the full text.

When publishing to clawhub.com the platform re-licenses uploads as MIT-0 (No
Attribution); the GitHub source tree remains true MIT. See clawhub docs for details.

## Dependencies

Runtime:

- **Python 3.8+** (uses `pathlib`, `argparse`, `subprocess`, `urllib`, `json` — all stdlib, no `pip install` needed)
- **OpenClaw runtime** with the `plugin-sdk` module — the verified baseline is `2026.3.8`;
  `install` will warn or refuse on older versions
- **`openclaw` CLI** available on `PATH` (used for `gateway restart` and optional
  `agents list` discovery)

No third-party Python packages are required.

## Environment Variables (read by `scripts/manage.py`)

The script reads the following environment variables. They are all optional with
sensible defaults; this list is provided for audit transparency.

| Env | Purpose |
|-----|---------|
| `OPENCLAW_WORKSPACE` | Workspace root (default `~/.openclaw/workspace`) |
| `OPENCLAW_CONFIG` | Path to openclaw.json (default `~/.openclaw/openclaw.json`) |
| `OPENCLAW_CORE_PKG` | OpenClaw core package.json (default `/app/package.json`) |
| `OPENCLAW_PLUGIN_SDK` | plugin-sdk directory (default `/app/dist/plugin-sdk`) |
| `SKILL_SEDIMENT_AGENTS` | Default `validAgentId` (default `main`) |
| `SKILL_SEDIMENT_CDN` | Optional fallback URL for the plugin tarball (default empty) |
| `SKILL_SEDIMENT_SHA256` | Optional sha256 for the downloaded bundle (default empty) |
| `SKILL_SEDIMENT_DETECT_WAIT` | Read-back detection window in seconds (default 20) |
| `SKILL_SEDIMENT_TZ` | Timezone for diagnostics formatting (default `Asia/Shanghai`) |
| `HOME` | Standard POSIX home dir; used to resolve workspace/config defaults |
| `LOBI_SYNC_ENABLED`, `APPID`, `APOLLO_META`, `APOLLO_APP_ID` | Managed-env signals (read-only detection; never written) |

