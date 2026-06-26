---
name: reolink-remote-backup
version: 0.3.0
description: Set up reliable off-site Reolink camera backup when cameras are remote (4G/5G/LTE) and home inbound networking is constrained (CGNAT/locked routers). Use for architecture decisions, VPS relay setup, FTP/FTPS ingest, local/NAS pull sync, retention, and troubleshooting upload/auth/path failures.
---

# Reolink Remote Backup

Implement resilient backup using:

1. Reolink camera FTP/FTPS upload -> VPS relay
2. Local machine pull from VPS -> NAS/local archive
3. Retention + health checks

Use this flow when direct camera->home ingest is impractical.

## Inputs to collect

- Camera model + hardware version
- Whether FTP/FTPS options are visible in app/client
- VPS host/IP and SSH access method
- Local destination path (NAS mountpoint)
- Desired pull interval (default 10 min)
- Desired VPS retention window (default 30 days)

## Workflow

### 1) Validate architecture constraints

- If home inbound routing is locked/CGNAT, prefer VPS relay.
- Keep NAS off public internet.
- Use local pull from VPS (never rely on VPS pushing into home NAT).

### 2) Configure VPS ingest

Run `scripts/setup_vps_vsftpd.sh` on VPS as root. It:

- installs vsftpd + ufw
- creates `reolinkftp` ingest user
- sets up `/srv/reolink/incoming`
- opens SSH + FTP passive ports

Then set camera FTP/FTPS target to VPS.

### 3) Configure local pull

Run `scripts/setup_local_pull.sh` on local machine. It writes:

- `/home/$USER/bin/reolink_pull.sh`
- systemd user service + timer with `Persistent=true`

This ensures catch-up after downtime.

### 4) Set retention safety

Run `scripts/setup_vps_retention.sh` on VPS to prune old files if local sync is offline for prolonged periods.

### 5) Verify

- Trigger camera upload or run camera FTP test.
- Confirm files appear on VPS: `/srv/reolink/incoming`
- Run local pull script once manually.
- Confirm files appear on destination path.
- Confirm timer active: `systemctl --user list-timers | grep reolink-pull`

## Troubleshooting

Read `references/troubleshooting.md` for response-code and log-driven fixes.

Fast checks:

- VPS service status: `systemctl status vsftpd`
- VPS logs: `journalctl -u vsftpd -n 120 --no-pager`
- FTP logs: `tail -n 120 /var/log/vsftpd.log`
- Mount status (local): `mountpoint -q <mountpath>`

## Security baseline

- Use SSH keys for VPS admin access.
- Keep FTP user isolated from admin users.
- Prefer FTPS after initial debugging.
- Enforce retention so VPS disk cannot fill.
- Rotate any credential exposed in chat/logs.
