# Security Policy

Time Clawshine is a privileged backup and restore tool for OpenClaw. Treat it as
system administration software: review `config.yaml`, run `setup.sh --dry-run`
before installation, and keep the restic password file outside the repository.

## Capability Summary

Filesystem:
- Reads only the paths configured under `backup.paths` and `backup.extra_paths`.
- Writes encrypted snapshot data to `repository.path`.
- Restores snapshots to the chosen target; restoring to `/` can overwrite current files.
- Applies retention with `restic forget` and `restic prune`, which can remove old recovery points.
- `uninstall.sh --purge` can delete the repository, password file, and logs.

System:
- Normal setup requires root.
- Setup may install `restic`, `curl`, `jq`, and `yq`.
- Setup may write `/usr/local/bin/time-clawshine`, a backward-compatible symlink,
  systemd units or a cron file, a logrotate file, and lock/marker files.
- `setup.sh --no-system-install` limits setup to repository/password initialization
  and skips package installation, scheduler registration, and `/usr/local/bin`.

Network:
- Telegram notifications are disabled by default.
- Healthcheck pings are disabled by default.
- ClawHub update checks are disabled by default.
- `privacy.local_only: true` blocks all external integrations.

## Sensitive Data

OpenClaw memory, session JSONL, configuration files, and custom backup paths may
contain secrets, credentials, prompts, private user data, or operational details.
Credential stores such as `~/.ssh` and `~/.gnupg` are not auto-suggested by the
customizer. Add them only when the backup repository and password file are
protected with controls appropriate for private keys.

## Reporting Vulnerabilities

Please report vulnerabilities through GitHub Issues unless the report contains
private exploit details or secrets. For sensitive reports, contact the maintainer
directly via the GitHub profile listed in `skill.json`.

Do not include Telegram tokens, restic passwords, private keys, or live backup
repository contents in public reports.
