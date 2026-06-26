---
name: install-vt-sentinel
description: >-
  Install or upgrade VT Sentinel security plugin. Use when the user asks to install,
  set up, enable, update, or upgrade VT Sentinel, VirusTotal scanning, malware protection,
  or file security scanning. Handles fresh installs and upgrades from any previous version.
user-invocable: true
metadata:
  openclaw:
    emoji: "\U0001F6E1\uFE0F"
    requires:
      anyBins:
        - openclaw
---

# Install / Upgrade VT Sentinel Plugin

This skill delegates everything to the official `openclaw` CLI. It does **not**
delete files, edit `openclaw.json` manually, download tarballs from external
URLs, or touch system services directly. All filesystem and config changes are
performed by `openclaw plugins` subcommands.

## What this skill will do

Before proceeding, tell the user the exact actions that will run, so they can
approve:

1. Query installed plugins (`openclaw plugins list`) — read-only.
2. If not installed → `openclaw plugins install clawhub:openclaw-plugin-vt-sentinel`
   (downloads the verified ClawHub package into `~/.openclaw/extensions/`).
3. If installed → `openclaw plugins update openclaw-plugin-vt-sentinel`
   (in-place upgrade handled by the OpenClaw CLI).
4. `openclaw gateway restart` — restart the user-scope gateway so the plugin loads.
5. Verify the plugin is active.

User data (`vt-sentinel-agent.json`, `vt-sentinel-state.json`,
`vt-sentinel-audit/`) lives in `<OPENCLAW_STATE_DIR>` (outside the plugin
directory) and is preserved across install/upgrade.

## Source & provenance

- ClawHub package: `openclaw-plugin-vt-sentinel` (verified / LLM-reviewed clean).
- npm package: `openclaw-plugin-vt-sentinel` (public, MIT licensed).
- Source repository: `https://github.com/king-tero/VT-sentinel`.

If the user is uncertain about provenance, suggest inspecting the package first
with `openclaw plugins inspect clawhub:openclaw-plugin-vt-sentinel`.

## Step 1: Check current state

```
exec { "command": "openclaw plugins list" }
```

Look for `openclaw-plugin-vt-sentinel` in the output.

- **Not present** → go to Step 2 (fresh install).
- **Present** → go to Step 3 (upgrade in place).

## Step 2: Fresh install

```
exec { "command": "openclaw plugins install clawhub:openclaw-plugin-vt-sentinel" }
```

This downloads the ClawHub package, registers the plugin, and loads skills and
hooks automatically. No manual configuration needed. Go to Step 4.

## Step 3: Upgrade in place

```
exec { "command": "openclaw plugins update openclaw-plugin-vt-sentinel" }
```

The OpenClaw CLI handles the upgrade atomically: it fetches the latest version,
replaces the extension directory, and updates `plugins.installs` metadata. User
config in `plugins.entries` and state files under `<OPENCLAW_STATE_DIR>` are
preserved.

If the CLI reports "already at latest version", tell the user VT Sentinel is
up to date and skip to Step 5 (verify only).

If the update is blocked (for example by a corrupted install), fall back to a
clean reinstall using only official subcommands:

```
exec { "command": "openclaw plugins uninstall openclaw-plugin-vt-sentinel --force" }
exec { "command": "openclaw plugins install clawhub:openclaw-plugin-vt-sentinel" }
```

`uninstall` removes the extension directory and cleans `plugins.installs` in a
single supported operation — do not edit `openclaw.json` manually.

## Step 4: Restart the gateway

The plugin will not become active until the gateway restarts. The OpenClaw CLI
provides a cross-platform wrapper that handles the underlying service manager
(launchd on macOS, systemd user unit on Linux, schtasks on Windows):

```
exec { "command": "openclaw gateway restart" }
```

## Step 5: Verify

```
exec { "command": "openclaw plugins list" }
```

Confirm `openclaw-plugin-vt-sentinel` appears as loaded. A healthy install
registers **9 tools** and **2 hooks**.

## Step 6: Inform the user

1. VT Sentinel is installed and active (mention whether this was a fresh
   install or an upgrade, and from which version if known).
2. **No API key needed** — the plugin auto-registers with VirusTotal's AI API
   (VTAI) on first scan. Zero configuration required.
3. Optionally, the user can add their own VirusTotal API key for higher rate
   limits:
   ```
   openclaw config set plugins.entries.openclaw-plugin-vt-sentinel.config.apiKey "vt_xxxxxxxx"
   ```
   Since v0.11.0 the `VIRUSTOTAL_API_KEY` environment variable fallback was
   retired — only the plugin config value or VTAI auto-registration are
   supported.

### What VT Sentinel provides

Tools exposed after install:

- `vt_scan_file` — Full file scan (AV + AI Code Insight)
- `vt_check_hash` — Quick hash lookup
- `vt_upload_consent` — Consent flow for sensitive file uploads
- `vt_sentinel_status` — View current config, watched dirs, protection status
- `vt_sentinel_configure` — Change settings at runtime (presets, notify level, block mode)
- `vt_sentinel_reset_policy` — Reset to defaults
- `vt_sentinel_help` — Quick-start guide and privacy info
- `vt_sentinel_update` — Check for updates and get upgrade instructions
- `vt_sentinel_re_register` — Re-register agent identity with VTAI

Behavior:

- Automatic scanning of downloaded and created files (AV + AI Code Insight)
- Active blocking of known-malicious file execution and dangerous command patterns
- Rotating audit logs under `<OPENCLAW_STATE_DIR>/vt-sentinel-audit/`

## Troubleshooting

If any step fails:

- Check connectivity to ClawHub and the OpenClaw gateway: `openclaw gateway status`.
- Re-run the failing command with verbose output: append `--verbose` to the
  `openclaw plugins ...` command.
- Inspect plugin load errors: `openclaw plugins doctor`.
- Inspect the package before install: `openclaw plugins inspect clawhub:openclaw-plugin-vt-sentinel`.

## Constraints

- Do **not** modify `~/.openclaw/openclaw.json` manually — `openclaw plugins
  install/update/uninstall` handle configuration atomically.
- Do **not** run `rm -rf` on `~/.openclaw/extensions/...` — use
  `openclaw plugins uninstall` instead.
- If the user reports the plugin is blocked, check `plugins.deny` in their
  `openclaw.json` (read-only inspection is fine; the user edits it themselves).
