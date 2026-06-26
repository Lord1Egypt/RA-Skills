# Reolink Remote Backup Troubleshooting

## Symptoms and fixes

## 1) `vsftpd` fails to start (`status=2/INVALIDARGUMENT`)

- Run parser directly:
  - `/usr/sbin/vsftpd /etc/vsftpd.conf`
- Remove unsupported config keys reported by OOPS message.
- Restart: `systemctl restart vsftpd`

## 2) Camera FTP test shows `451 login failed`

- Re-enter username/password in app.
- Reset server password: `passwd reolinkftp`.
- Ensure user in allow list:
  - `echo reolinkftp >/etc/vsftpd.userlist`
- Check logs:
  - `tail -n 120 /var/log/vsftpd.log`
  - `tail -n 120 /var/log/auth.log`

## 3) Camera FTP test shows `455` failure

Usually write/path/passive/TLS mismatch.

- Confirm writable ingest path:
  - `mkdir -p /srv/reolink/incoming`
  - `chown -R reolinkftp:reolinkftp /srv/reolink`
  - `chmod 775 /srv/reolink/incoming`
- Confirm passive ports open (21 + 50000-50100/TCP).
- Temporarily disable forced TLS for debugging only:
  - `force_local_logins_ssl=NO`
  - `force_local_data_ssl=NO`

## 4) Connect appears in logs, but no USER/PASS lines

Likely protocol mismatch or early TLS negotiation failure.

- Enable protocol logging in vsftpd config:
  - `log_ftp_protocol=YES`
  - `dual_log_enable=YES`
- Re-test and inspect `/var/log/vsftpd.log`.

## 5) Local pull script says mount missing

- Verify mount:
  - `findmnt <mountpoint>`
  - `mount | grep <name>`
- Check duplicate/conflicting `/etc/fstab` entries.
- Run:
  - `sudo systemctl daemon-reload`
  - `sudo mount -a`

## 6) Nothing arrives while camera is remote and idle

- Trigger uploads may require motion/events.
- Use camera app/web test button if available.
- Historical microSD archives may need explicit download through Reolink web/app tools.

## 7) rsync fails with `change_dir "/srv/reolink/incoming" failed`

The generated pull script uses a relative source path (`incoming/`) because the
`reolinkftp` user's home is `/srv/reolink`. If an older script has the absolute
path, patch it:

```bash
sed -i "s|VPS_SRC=/srv/reolink/incoming/|VPS_SRC=incoming/|" ~/bin/reolink_pull.sh
```

Also ensure `/srv/reolink/incoming` exists on the VPS:

```bash
mkdir -p /srv/reolink/incoming
chown reolinkftp:reolinkftp /srv/reolink/incoming
chmod 775 /srv/reolink/incoming
```

## 8) rsync fails with `protocol version mismatch -- is your shell clean?`

This happens when a **forced rsync command** is set in `authorized_keys` and the
flags in that command don't match what the client negotiates. Do **not** use a
forced rsync command for this setup. Instead, use restriction flags only:

```
no-pty,no-agent-forwarding,no-port-forwarding,no-X11-forwarding ssh-ed25519 AAAA...
```

Remove a forced command with:

```bash
sed -i 's|command="rsync[^"]*",||' /srv/reolink/.ssh/authorized_keys
```

The `reolinkftp` user is already restricted (no sudo, home-dir only) so the
forced command provides little extra security while breaking rsync negotiation.

## 9) VPS fills up

- Confirm local pull timer active:
  - `systemctl --user list-timers | grep reolink-pull`
- Confirm local script ran and logs are fresh.
- Keep VPS retention prune enabled.
