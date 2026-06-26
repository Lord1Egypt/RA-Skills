# Privacy

Time Clawshine is local-only by default. With the default `config.yaml`, backups
run locally and external integrations are blocked by `privacy.local_only: true`.

## Data Stored Locally

The tool stores encrypted restic snapshots for the configured backup paths. The
default paths include OpenClaw workspace data, session history, configuration,
and cron jobs. These files may contain memory, prompts, private operational
context, credentials, or other sensitive information.

The restic password file is stored at `repository.password_file` and is required
to restore snapshots. If it is lost, the repository cannot be recovered. If it is
exposed together with the repository, encrypted backup contents may be readable.

## External Data Flows

External integrations are optional:
- Telegram sends failure notifications only when explicitly enabled.
- Healthcheck sends start/success/failure pings only when explicitly enabled.
- Update checks contact ClawHub only when `updates.check: true`.

All of the above are blocked while `privacy.local_only: true`.

By default, external notifications do not include hostname or raw error details.
If `privacy.send_error_details: true` is enabled, failure messages may include a
short sanitized excerpt of the local error output. Keep it false unless you have
reviewed the environment and destination.

## Secret Handling

Do not paste Telegram bot tokens, chat IDs, restic passwords, or private keys into
public logs, issues, screenshots, or chat transcripts. `setup.sh` restricts
`config.yaml` to mode `600` after system setup because it may contain notification
tokens.

Avoid adding credential directories such as `~/.ssh` and `~/.gnupg` unless you
intend to create encrypted backup copies of those credentials and have a separate
plan for protecting the repository and password file.
