# Changelog

All notable changes to Time Clawshine are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [3.2.3] — 2026-06-01

### Fixed

- Preserve custom backup cadence when installing on systemd hosts. `setup.sh`
  now converts simple cron expressions such as `0 */2 * * *` to equivalent
  `OnCalendar` values instead of falling back to hourly.
- Fall back to `/etc/cron.d/time-clawshine` for cron expressions that cannot be
  converted safely, preserving the user's configured `schedule.cron` exactly.

### Documentation

- Document the OpenClaw install command with the slug-only format:
  `openclaw skills install quick-backup-restore`.
- Add "every 2 hours" as a first-class setup-guide frequency option.

---

## [3.2.2] — 2026-06-01

### Fixed

- Rename `skill-card.md` to `MARKETPLACE.md` because ClawHub generates `skill-card.md` internally and rejects direct publishes containing that file.

---

## [3.2.1] — 2026-06-01

### Changed

- Refresh ClawHub positioning around the public name
  `Time Clawshine — OpenClaw Time Machine`.
- Rewrite the first-line description for discovery around restic, encrypted
  snapshots, time/snapshot/file restore, local-only privacy defaults, integrity,
  retention, and optional alerts.
- Split discovery tags into focused tags: backup, restore, restic, snapshots,
  time-machine, encrypted-backup, local-backup, openclaw, disaster-recovery, and
  privacy.
- Add `skill-card.md` with concise marketplace copy highlighting the difference
  between restic snapshots and plain tarball backups.

---

## [3.2.0] — 2026-06-01

### Security

- Respond to the ClawHub security audit by making sensitive capabilities explicit
  in `skill.json`, `SKILL.md`, `README.md`, `SECURITY.md`, and `PRIVACY.md`.
  The docs now call out root setup, package installation, scheduler persistence,
  backup of sensitive OpenClaw memory/session/config data, restore overwrite
  risk, retention/prune deletion, purge behavior, and optional network egress.
- Add `privacy.local_only: true` as the default hard egress gate. While enabled,
  Telegram, healthcheck, and ClawHub update checks are blocked even if their
  individual config blocks are edited.
- Change `updates.check` default to `false`; update checks now require explicit
  opt-in by setting `privacy.local_only: false` and `updates.check: true`.
- Minimize external notifications by default: no hostname and no raw error
  output. `privacy.send_error_details: true` enables only a short sanitized error
  excerpt.
- Require healthcheck URLs to use `https://` unless they point to loopback
  localhost.
- Remove the Telegram notification from `uninstall.sh`; uninstall no longer
  reports host identity, timing, or removal state to an external service.
- Stop auto-suggesting `~/.ssh` and `~/.gnupg` in `customize.sh`; credential
  stores now require manual opt-in with explicit warnings.

### Added

- `setup.sh --dry-run` previews dependencies, repository/password/log paths,
  backup paths, privacy settings, and planned system files without requiring
  root or changing the machine.
- Stronger restore confirmation for target `/`: users must type
  `RESTORE TO /` after the dry-run preview.
- Extra tests for privacy defaults, local-only gating, healthcheck URL
  validation, and default notification redaction.

### Changed

- `setup.sh` now refuses to install `yq` when the release checksum cannot be
  fetched, and downloads to a temporary file before replacing `/usr/local/bin/yq`.

---

## [3.1.4] — 2026-05-25

### Documentation

- Clarify intent of the restic password generation line in `setup.sh`. The
  ClawHub static-analysis scanner flagged
  `( set -C; openssl rand -base64 48 > "$PASS_FILE" )` as a potential
  exfiltration ("shell base64-encodes a local file and sends it over the
  network"). False positive: `openssl rand -base64 48` is *generating* 48
  bytes of entropy and base64-encoding them so the password is printable
  ASCII; the `>` redirect target is `$PASS_FILE` on local disk (the
  restic encryption key file at `/etc/time-clawshine.pass`). No network
  call, no file-to-base64 step. Added an inline comment explaining the
  CSPRNG → ASCII encoding → local write sequence and the role of
  `set -C` (race-condition guard against the outer `[[ -f ]]` check).
  No behavior change.

---

## [3.1.3] — 2026-05-25

### Fixed

- **Missing backup paths now warn-and-skip instead of failing the entire backup.**
  `tc_validate_paths` used to abort (and fire a Telegram alert) on the first
  missing path, then `restic` never ran. On clean OpenClaw installs the default
  `config.yaml` lists optional dirs like `/root/.openclaw/cron` that only
  materialize once the user creates a cron job, so the very first validation
  backup after setup would fail with `Paths not found: /root/.openclaw/cron`
  even though everything else was healthy. New behavior: missing paths log a
  single `WARN` line and drop out of the backup set; `restic` still runs on the
  remaining paths. We only fail loudly (and alert via Telegram) if *every*
  configured path is missing — the genuine "nothing to back up" case.

- **`setup.sh` no longer hides what it accomplished when the validation backup
  fails.** Before: a failing first backup `exit 1`'d before the summary box,
  leaving the user with `Initial backup FAILED — check config.yaml and retry`
  and no idea whether the repo was initialized, the systemd timer wired up,
  logrotate configured, etc. After: the summary box prints unconditionally with
  a new `Validation` line showing `success`, `skipped (--skip-backup)`, or
  `FAILED (exit N)`; the script still exits non-zero on validation failure, but
  prints a short follow-up block pointing at the log and the retry command
  first. The field label `Cron` was renamed to `Scheduler` so it makes sense
  whether systemd timer or cron actually got installed.

- **Robust systemd detection + cleanup of the loser scheduler.** The
  systemd-presence check used `systemctl is-system-running`, which returns
  non-zero whenever the system reports `degraded` (any unrelated unit failed).
  On otherwise-healthy hosts with one degraded unit, setup would incorrectly
  fall back to cron — and the cron path did *not* remove a pre-existing systemd
  timer, so you could end up with BOTH cron and the legacy timer firing the
  same backup back-to-back. Replaced with the canonical
  `[ -d /run/systemd/system ]` check (present iff PID 1 is systemd, regardless
  of other units' state), and the cron fallback path now disables and removes
  any prior `/etc/systemd/system/time-clawshine.{timer,service}` before
  installing the cron file.

- **`apt-get update` no longer runs when no apt-managed dep is missing.** Setup
  unconditionally called `apt-get update -qq` even when `restic`, `curl`, and
  `jq` were all present. On hosts with flaky third-party repos (docker,
  nodesource, tailscale, …) every re-run spammed a dozen `W: Failed to fetch`
  warnings even though no install was going to happen. The apt index is now
  refreshed only when at least one apt-managed dep is actually missing;
  otherwise setup prints `Skipping apt-get update (all apt-managed deps
  already present)` and finishes the dep-check section in a fraction of a
  second.

- **Update check surfaces *why* it failed instead of going silent.** Both
  `backup.sh` (daily) and `status.sh` did the same blind `curl … | jq …` pipe
  against the ClawHub API. On any failure (DNS, TLS, HTTP 5xx, missing
  `.version` field, JSON shape change, …) `status.sh` just printed
  `Update : could not reach ClawHub` and `backup.sh` said nothing at all —
  operators had no signal whether the problem was network, the host, or the
  API. Extracted a shared `tc_check_update` helper in `lib.sh` that captures
  the curl exit code, the HTTP status, and the parsed `.version` separately
  and sets `TC_UPDATE_STATE` (`uptodate` / `newer` / `error`) plus
  `TC_UPDATE_ERROR` with a short reason. `status.sh` now renders e.g.
  `Update : could not check — HTTP 307 from ClawHub`, and `backup.sh` logs
  `WARN Update check skipped: network error (curl exit 6): …` once per day.
  Failures stay non-blocking — never abort a backup, never spam Telegram.

- **Summary box stays aligned.** The setup summary used `printf '%-Ns'` with
  field values that could contain multi-byte UTF-8 (`✓`, em dash, long systemd
  unit name) — `printf` pads bytes, not visual columns, so the right border
  drifted and `Scheduler : systemd: time-clawshine.timer (*-*-* *:05:00)`
  overflowed entirely. Replaced the box-internal special chars with ASCII
  (`[OK]`, `--`), shortened the systemd label to `systemd timer @ <calendar>`
  (full unit name is still discoverable via `systemctl status`), and added a
  `_field_fit` helper that truncates oversized values to
  `<first 33 chars>...` — keeps the right border vertical on any path length.

---

## [3.1.2] — 2026-05-14

### Changed
- Display name on ClawHub: `Quick Backup Restore` (slug auto-title) →
  `OpenClaw Time Machine (restic quick backup and restore)`. Internal
  brand name (`⏱🦞 Time Clawshine`) is kept in SKILL.md and the log.

---

## [3.1.1] — 2026-05-14

### Security
- Redact a real-looking chat_id (a 10-digit number that was the
  maintainer's own Telegram chat_id) from the `config.yaml` example
  comment. Replaced with the obviously-placeholder `123456789`. No
  behavior change — the comment was always documentation, never read
  by the script.

---

## [3.1.0] — 2026-05-14

### Added
- **Healthcheck.io / hc-style ping support** (`notifications.healthcheck`). Pings
  `<url>/start` at backup start, `<url>` on success, `<url>/fail` on any failure.
  Compatible with healthchecks.io and self-hosted hc instances. Disabled by
  default; opt-in via `enabled: true` + `url: "<your-uuid-url>"`.
- `hc_send()` helper in `lib.sh` — short timeout (10s), 2 retries, non-blocking
  (a ping failure logs a warning but never aborts the backup).
- Config validation: `notifications.healthcheck.url` is required when
  `healthcheck.enabled: true`.

### Fixed
- **Log lines duplicated 2×.** Systemd unit captured stdout via
  `StandardOutput=append:LOG_FILE` while `log()` also writes to `LOG_FILE`
  through `tee(1)`. Setup now writes `StandardOutput=journal` —
  `tee` keeps writing to the log file once, and systemd captures any
  unexpected stderr/stdout to the journal (`journalctl -u time-clawshine`).
- **Retention policy double-counted snapshots after a paths change.**
  `restic forget --keep-last N` groups by `(host, paths)` by default. If the
  list of backup paths ever changed, two groups existed and each kept N
  snapshots — silently retaining 2N. Now uses `--group-by host` so retention
  is global per host. Existing repos with stale path-set groups are pruned
  automatically on the next backup.

---

## [3.0.0] — 2026-04-12

### Added
- `bin/uninstall.sh`: clean removal of all system artifacts with `--yes` and `--purge` flags. Sends Telegram notification. Preserves backup data by default
- `--help` / `-h` flag on all scripts (exits before config load so it works without a valid config)
- GitHub Actions CI: runs `shellcheck` + test suite on `ubuntu-22.04` and `ubuntu-24.04` with yq checksum verification
- v2→v3 migration engine `_migrate_v2()` in `setup.sh`: auto-detects legacy v2.x system files (cron, logrotate, lock, markers), prompts to migrate, cleans old and renames markers
- `SETUP_GUIDE.md`: Step 0 (upgrade from v2) and Step 9 (uninstall) sections
- Password file existence check in `tc_load_config` — clear error instead of cryptic restic failure
- Signal trap (`SIGTERM`/`SIGINT`) in `backup.sh` — sends Telegram on unexpected termination
- `openssl` added to `tc_check_deps` (was required by setup but not validated)
- ARM64 and ARMv7 support for yq download in `setup.sh` (auto-detects `uname -m`)

### Changed
- **BREAKING**: System file paths renamed from `quick-backup-restore` to `time-clawshine`:
  - `/etc/cron.d/quick-backup-restore` → `/etc/cron.d/time-clawshine`
  - `/etc/logrotate.d/quick-backup-restore` → `/etc/logrotate.d/time-clawshine`
  - `/var/lock/quick-backup-restore.lock` → `/var/lock/time-clawshine.lock`
  - `/var/tmp/quick-backup-restore-*` → `/var/tmp/time-clawshine-*`
- **BREAKING**: Default config paths now use `time-clawshine` name (new installs only; existing configs are preserved)
- `backup.sh`: split `forget` (every backup) from `prune` (daily) — avoids hourly I/O storms on large repos
- `restore.sh`: now checks `restic restore` exit code — no longer shows "✓" on failure
- `customize.sh`: added missing `set -e` — prevents silent config corruption on errors
- `status.sh`: detects systemd timer (not just cron) and caches `restic snapshots --json` (single call instead of two)
- `backup.sh`: ensures log directory exists (`mkdir -p`) before first write
- `setup.sh`: fixed password warning box alignment, yq checksum now uses `checksums-bsd` format
- `setup.sh`: binary now installs as `/usr/local/bin/time-clawshine` with backward-compat symlink
- `prune.sh`: fixed SIGPIPE (exit 141) when capturing large restic output with `set -euo pipefail` — now uses temp files
- All UI headers, log messages, error prefixes, and Telegram notifications now show "Time Clawshine"
- `SKILL.md` technical reference uses config-based paths instead of hardcoded defaults
- `README.md` updated with CI badge, uninstall section, expanded flags table
- Binary symlink `/usr/local/bin/quick-backup-restore` → `time-clawshine` preserved for backward compatibility
- Test suite expanded to 25 tests (--help checks, uninstall.sh syntax, prune dry-run, permissions)

### Removed
- `CHANGES-PLAN.md` and `quick-backup-restore-changes.md` (stale planning files)

---

## [2.0.2] — 2026-04-09

### Fixed
- Telegram notifications (`tg_failure`, `tg_digest`) now show "Time Clawshine" instead of legacy "Quick Backup and Restore" name

---

## [2.0.1] — 2026-04-09

### Fixed
- `setup.sh`: yq checksum verification failed (404) — yq publishes a bulk `checksums` file, not individual `.sha256` per binary. Now downloads the correct file and greps for the matching hash
- `setup.sh`: scripts missing execute permission on some platforms — added `chmod +x` for all `bin/*.sh` and `lib.sh` at startup
- `test.sh`: roundtrip hash comparison used absolute paths causing false mismatch — switched to relative paths via `cd`

---

## [2.0.0] — 2026-04-09

### Added
- `bin/prune.sh`: manual repository cleanup with `--keep-last`, `--older-than`, `--dry-run`, `--yes` flags. Shows before/after size and sends Telegram notification
- `bin/test.sh`: self-test suite — validates deps, config, shell syntax on all scripts, and runs a full backup→restore→verify roundtrip in a temp directory
- `SETUP_GUIDE.md`: interactive setup guide for the OpenClaw agent — walks the user through Telegram, frequency, retention, paths, disk safety, and repo location before running setup.sh
- Config validation (`tc_validate_config`): validates types, ranges, cron syntax, required Telegram fields, and backup paths on every config load
- `backup.sh --dry-run`: validates backup without writing (uses `restic backup --dry-run`)
- `restore.sh` time-based restore: `"2h ago"`, `"1d ago"`, `"yesterday"` — resolves to closest snapshot automatically
- `restore.sh` Telegram notification on successful restore
- Systemd timer support: `setup.sh` auto-detects systemd and prefers `time-clawshine.timer` over cron. Falls back to cron if systemd is unavailable

### Changed
- SKILL.md: complete hero copy rewrite with marketing-grade intro, problem/solution table, and feature highlights
- SKILL.md: added sections for prune, dry-run, test, guided setup, and time-based restore
- README.md: added prune, self-test, dry-run, and time-based restore documentation
- Title unified to "Time Clawshine" across all files

---

## [1.3.0] — 2026-04-09

### Changed
- SKILL.md: complete rewrite of hero copy — marketing-grade intro with problem/solution table, feature highlights, and technical reference below
- Title unified to "Time Clawshine" across all docs

---

## [1.2.4] — 2026-04-09

### Changed
- SKILL.md description rewritten to lead with the name and purpose (visible as summary on ClawHub)

---

## [1.2.3] — 2026-04-09

### Changed
- Description: emphasize restic's incremental deduplication (near-instant backups, tiny storage)

---

## [1.2.2] — 2026-04-09

### Changed
- Display name unified to "Time Clawshine" across skill.json and ClawHub
- Description rewritten to explain the name and purpose

---

## [1.2.1] — 2026-04-09

### Fixed
- SKILL.md: removed false claim that `credentials/` are backed up by default — only paths listed in `config.yaml` are covered

---

## [1.2.0] — 2026-04-09

### Added
- `bin/status.sh`: health check showing version, snapshots, repo size, disk space, cron, password file warning, integrity counter, update check, and last log lines
- Disk space guard (`safety.min_disk_mb`): aborts backup and sends Telegram alert if free disk is below threshold
- Periodic integrity check (`integrity.check_every`): runs `restic check` every N backups (default 24 = daily with hourly cron)
- Daily digest via Telegram (`notifications.telegram.daily_digest`): summary with snapshot count, repo size, and disk free — sent on first backup after midnight
- Update version check (`updates.check`): daily non-blocking check against ClawHub API, logs a warning if a newer version is available
- Logrotate configuration: `setup.sh` now creates `/etc/logrotate.d/quick-backup-restore` for weekly log rotation (4 weeks, compressed)

### Fixed
- `config.yaml` comment on line 59 claimed logrotate was already set up — now it actually is

---

## [1.1.1] — 2026-04-09

### Fixed
- SKILL.md metadata: declared full dependency list (`bash`, `openssl`, `curl`, `jq` + auto_install `restic`, `yq`) — was previously only `bash` and `openssl`

---

## [1.1.0] — 2026-04-09

### Changed
- `bin/customize.sh`: replaced `openclaw agent ask` with pure bash analysis — no data leaves the machine
- `bin/setup.sh`: added `--no-system-install` flag for repo-only setup without root modifications
- `bin/setup.sh`: added dependency install confirmation prompt (override with `--assume-yes` / `-y`)

### Removed
- Deleted `prompts/whitelist.txt` and `prompts/blacklist.txt` (no longer needed)

### Security
- Eliminates workspace listing exfiltration risk flagged by ClawHub security scan
- Users can now set up backup repo without modifying system files

---

## [1.0.0] — 2026-03-04

Initial release.

### Added

**Core backup engine**
- `bin/backup.sh` — hourly restic backup; silent on success; Telegram notification on failure; validates paths before running
- `bin/restore.sh` — interactive restore with mandatory dry-run preview; `--file` and `--target` flags for surgical restores
- `bin/setup.sh` — self-installing setup: installs `restic`, `yq v4`, `curl`, `jq`; initializes AES-256 encrypted repo; registers cron from config
- `lib.sh` — shared layer for all scripts: YAML parsing, structured logging, Telegram wrapper, restic wrapper, path/dep validation

**AI-assisted customization**
- `bin/customize.sh` — analyzes actual workspace, runs AI prompts via the OpenClaw agent, shows whitelist/blacklist suggestions, applies to `config.yaml` only after explicit user confirmation; saves `config.yaml.bak` before any change
- `prompts/whitelist.txt` — template asking the agent to identify extra paths worth backing up
- `prompts/blacklist.txt` — template asking the agent to identify patterns that should be excluded

**Configuration**
- `config.yaml` as single source of truth — zero hardcoded values in any script
- Full standard OpenClaw path coverage by default: `workspace/`, `sessions/`, `openclaw.json`, `cron/`, `credentials/`
- `backup.extra_paths` and `backup.extra_excludes` as clean extension points for custom additions

**OpenClaw skill**
- `SKILL.md` with ClaWHub-compatible frontmatter (single-line metadata, correct `metadata.openclaw` namespace)
- Agent instruction body covering: setup, manual backup, status check, restore, integrity check, config changes, and customization

**Other**
- `CHANGELOG.md` in Keep a Changelog format
- `.gitignore` pre-configured: excludes `.pass`, `.env`, `secrets.*`, `.bak`, backup directories
- 72-snapshot retention (3 days at 1/hour), configurable via `retention.keep_last`

---

[1.0.0]: https://github.com/marzliak/quick-backup-restore/releases/tag/v1.0.0
