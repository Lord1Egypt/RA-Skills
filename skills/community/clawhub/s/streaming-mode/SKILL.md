---
name: streaming-mode
description: Install, verify, update, or roll back the bundled Streaming Mode Control UI for OpenClaw 2026.9.6 on Linux, macOS, or Windows.
metadata:
  openclaw:
    requires:
      bins:
        - node
        - openclaw
    envVars:
      - name: OPENCLAW_INSTALL_ROOT
        required: false
        description: Optional path to the OpenClaw package directory when automatic discovery cannot locate it.
      - name: OPENCLAW_STATE_DIR
        required: false
        description: Optional OpenClaw state directory; defaults to ~/.openclaw.
    os:
      - linux
      - darwin
      - win32
    emoji: "📺"
    homepage: https://github.com/svetlyoh/web-wallet/tree/master/openclaw/skills/streaming-mode
---

# OpenClaw Streaming Mode

Use this skill when the user asks to install, update, check, troubleshoot, or roll back Streaming Mode. It replaces only the installed OpenClaw 2026.9.6 Control UI directory and keeps the first original UI as a rollback backup.

Streaming Mode expands the transcript and composer across almost the full browser width, leaving only a small responsive edge gutter. It uses a responsive 24–32 px size for model prose and tables; a 20–24 px size with 1.4 line spacing for fenced code and receipts; 22–24 px composer text; and larger top and bottom command controls for OBS streams viewed on phones.

## Safety and compatibility

- Run on Linux, macOS, or native Windows with OpenClaw 2026.9.6. The installer refuses every other host version before changing files. For a Gateway in Windows WSL2, run installation inside that same WSL distribution.
- Run commands from this skill directory so `scripts/install.mjs` can find the bundled payload.
- Run as the account that owns the Gateway installation. Do not use `sudo` or an elevated Windows terminal, weaken file permissions, disable checksum verification, or download a replacement payload.
- The bundle requires no credentials and makes no network requests during installation.
- The installer uses only Node.js filesystem, crypto, and gzip APIs. It does not start shell commands or subprocesses.
- Existing native Control UI plugins remain enabled. Streaming Mode keeps the `session-header` accessory host mounted, so the Gear Engine widget remains visible and responsive while Streaming Mode is active.
- The installer verifies the bundled archive against `payload/manifest.json`, stages the new UI, and swaps directories atomically.
- The installer verifies that the installed Gateway, payload manifest, and extracted Control UI all carry the same official build identity. Stop on any mismatch; do not bypass this check.
- The payload is built from the OpenClaw source commit recorded in the manifest. Its upstream MIT license and third-party notices are included under `licenses/`.
- State and the first backup are stored under `OPENCLAW_STATE_DIR`, or the current user's `.openclaw` home folder (`~/.openclaw` on Linux/macOS and `$HOME\.openclaw` in Windows PowerShell). Preserve them until the user no longer needs rollback.
- If automatic discovery cannot locate OpenClaw, set `OPENCLAW_INSTALL_ROOT` only to the package directory whose `package.json` name is `openclaw`.

## Check status

Run:

```sh
node scripts/install.mjs status
```

Report the detected OpenClaw version and whether Streaming Mode is active.

## Install or update

When the user asks to install or update, run:

```sh
node scripts/install.mjs install
```

The backup and copy step can take a couple of minutes. Do not interrupt it. On success, tell the user to hard-refresh the Control UI. The Gateway does not need a restart.

The same Node commands work in Linux/macOS terminals and Windows PowerShell. Install on the machine running the Gateway; a Mac or Windows browser viewing a remote Linux Gateway does not need a local patch. This updates the browser Control UI, not a separately bundled native companion app.

For a skill installed from a local directory, refresh the skill itself by rerunning `openclaw skills install /path/to/streaming-mode --as streaming-mode --global --force`; `openclaw skills update` refreshes ClawHub-tracked installs only. The repository's local transfer bundle runs the payload installer before this registration step so it can repair a broken Control UI.

## Roll back

When the user asks to remove or roll back Streaming Mode, run:

```sh
node scripts/install.mjs rollback
```

Rollback refuses to overwrite a Control UI that no longer carries the Streaming Mode marker. On success, tell the user to hard-refresh the browser tab.

Always roll back before uninstalling this skill. Uninstalling a skill does not restore OpenClaw application files. If the skill was already removed, reinstall the skill and run rollback, or use the recovery command documented in the GitHub README.

## Troubleshooting

- A version error means this bundle does not support the installed OpenClaw release. Leave the installation unchanged.
- A checksum error means the bundled payload is incomplete or altered. Reinstall the skill from ClawHub; do not bypass the check.
- A build identity error means the payload is not the exact artifact for the installed Gateway build. Leave the installation unchanged and obtain a compatible Streaming Mode release.
- A discovery error means the OpenClaw package could not be found from the `openclaw` entry on `PATH`, `NODE_PATH`, or standard global Node.js locations. Set `OPENCLAW_INSTALL_ROOT` to the verified package directory and retry.
- If rollback reports no tracked backup, do not copy files manually. Report the state path shown by the installer.
