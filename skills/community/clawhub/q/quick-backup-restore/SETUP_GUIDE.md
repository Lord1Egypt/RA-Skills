# Time Clawshine — Setup Guide

This guide is for the OpenClaw agent to read and walk the user through an interactive setup.
Follow each section in order. Ask the user each question, apply their choice to `config.yaml`, then move on.

---

## Step 0: Upgrade from v2 (skip on fresh install)

If the user already has v2.x installed, `setup.sh` will auto-detect legacy artifacts and offer to migrate.

Tell the user:
> "I detected a v2.x installation. Running setup again will automatically migrate your system files to v3 (renamed cron, logrotate, marker files). Your repository, password, and snapshots are preserved."

Then proceed with Step 7 (Run Setup) directly — setup.sh handles the migration.

---

## Step 1: Telegram Notifications

Ask the user:
> "Want to receive Telegram alerts when a backup fails? This sends minimal operational metadata to Telegram, a third-party service. I can also send a daily summary with stats."

**If yes:**
1. Ask for the **bot token** (from @BotFather on Telegram)
2. Ask for the **chat ID** (from @userinfobot on Telegram)
3. Ask if they want a **daily digest** (daily summary with snapshot count, repo size, disk free)
4. Tell the user not to paste the token into public logs, issues, screenshots, or shared transcripts.
5. Set in `config.yaml`:
```yaml
privacy:
  local_only: false
  send_error_details: false
  include_hostname: false

notifications:
  telegram:
    enabled: true
    bot_token: "<their token>"
    chat_id: "<their chat id>"
    daily_digest: true  # or false
```

**If no:** leave defaults (`privacy.local_only: true`, `enabled: false`). Failures will only be logged locally.

---

## Step 1b: External Healthcheck (recommended for production)

Ask the user:
> "Telegram only pings you when a backup *runs and fails*. If the scheduler
> itself breaks (cron disabled, systemd timer not loaded, container
> restart), Telegram stays quiet. Want to add a healthcheck.io / hc ping
> so you get alerted when backups *stop running*?"

**If yes:**
1. Ask for the **healthcheck URL** (e.g. `https://hc-ping.com/<uuid>` from
   healthchecks.io, or a self-hosted instance like `https://hc.example.com/ping/<uuid>`).
2. Require `https://` unless the URL points to loopback localhost.
3. Configure the check at the provider to expect a ping every hour
   (matching `schedule.cron`) plus some grace.
4. Set in `config.yaml`:
```yaml
privacy:
  local_only: false

notifications:
  healthcheck:
    enabled: true
    url: "<their healthcheck url>"
    ping_start: true   # adds /start ping so duration is tracked
```

**If no:** leave defaults (`privacy.local_only: true`, `enabled: false`). No pings will be sent.

---

## Step 2: Backup Frequency

Ask the user:
> "How often should I back up? Default is every hour at :05. Options:"
> - **Every hour** (recommended — 72 snapshots = 3 days of history)
> - **Every 2 hours** (good balance for quieter agents)
> - **Every 30 minutes** (more granular, uses more disk)
> - **Once a day at midnight** (minimal disk usage, less granularity)
> - **Custom** (let them type a cron expression)

Set `schedule.cron` accordingly:
| Choice | Cron |
|--------|------|
| Every hour | `5 * * * *` |
| Every 2 hours | `0 */2 * * *` |
| Every 30 min | `*/30 * * * *` |
| Daily at midnight | `0 0 * * *` |
| Custom | whatever they provide |

---

## Step 3: Retention

Ask the user:
> "How many snapshots should I keep? More = more history but more disk usage."
> - **72** (3 days at hourly — default, recommended)
> - **168** (7 days at hourly)
> - **24** (1 day at hourly — minimal)
> - **Custom number**

Set `retention.keep_last` to their choice.

---

## Step 4: Extra Paths

Ask the user:
> "By default I back up OpenClaw's workspace, sessions, config, and cron jobs. Want to add any extra paths?"
> 
> Common additions:
> - `~/.config` — app configs
> - Custom scripts or data directories
>
> Avoid adding credential stores such as `~/.ssh` and `~/.gnupg` unless you explicitly want encrypted backup copies of private keys and have strong controls around the repository and password file.

If they add paths, append to `backup.extra_paths` in `config.yaml`:
```yaml
backup:
  extra_paths:
    - /root/.config
```

Or suggest running `sudo bin/customize.sh` after setup for an automated scan.

---

## Step 5: Disk Safety

Ask the user:
> "I can abort backups if your disk gets too full. What's the minimum free space I should require?"
> - **500 MB** (default — safe for most setups)
> - **1000 MB** (1 GB — recommended if backup paths are large)
> - **0** (disable — I'll run even if disk is almost full)

Set `safety.min_disk_mb` accordingly.

---

## Step 6: Repository Location

Ask the user:
> "Where should I store the backup repository? Default is `/var/backups/time-clawshine`."
> - **Default** (local, fast)
> - **Custom local path** (e.g. external drive)
> - *Note: restic also supports S3, SFTP, and other remote backends — see restic docs*

Set `repository.path` if they want a custom location.

---

## Step 7: Run Setup

After configuring everything, confirm with the user:
> "Here's your configuration:"
> (show the key values: schedule, retention, privacy.local_only, Telegram/healthcheck/update on/off, paths, disk guard)
>
> "Ready to install? This will:"
> - Install dependencies (restic, yq, curl, jq)
> - Generate an AES-256 encryption password
> - Initialize the backup repository
> - Register the configured scheduler (systemd timer or cron)
> - Restrict config.yaml permissions because it may contain notification tokens
>
> "Shall I proceed?"

Preview first:
```bash
bash {baseDir}/bin/setup.sh --dry-run
```

If yes, run:
```bash
sudo bash {baseDir}/bin/setup.sh
```

After setup completes, remind the user:
> "⚠ **Back up your password file** (the path shown in `config.yaml` → `repository.password_file`) separately. Without it, your snapshots are unrecoverable — even if the repository is intact."

---

## Step 8: Verify

Run the status dashboard to confirm everything is working:
```bash
sudo bash {baseDir}/bin/status.sh
```

Show the output to the user and confirm the setup is complete.

---

## Step 9: Uninstall (if ever needed)

If the user asks to remove Time Clawshine:

```bash
sudo bash {baseDir}/bin/uninstall.sh
```

This removes all system artifacts (timer, cron, logrotate, binary) but **preserves** the backup repository and password file.

To also delete all backup data (irreversible):
```bash
sudo bash {baseDir}/bin/uninstall.sh --purge
```
