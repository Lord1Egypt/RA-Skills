# Troubleshooting and scheduling

Run `smfa doctor` first. Its output is sanitized and reports OpenAI-compatible variables as presence booleans only. Use `smfa status --json` for local aggregate state and `smfa report --json` for the latest run; neither command emits private cursors, raw errors, request headers, or provider responses.

## Stable command outcomes

- Exit `0`: the requested local operation completed.
- Exit `1`: an operational failure needs inspection or a safe retry.
- Exit `2`: command usage or configuration is invalid.
- Exit `3`: login, QR, captcha, or device confirmation requires the user.
- Exit `130`: the run was interrupted at a safe checkpoint.

`smfa sync` reports enumeration/skeleton progress separately from durable heavy-queue progress. `--metadata-only` leaves heavy jobs queued. `--foreground` consumes them in the invoking process. `--limit` is for representative validation and always disables removal reconciliation for that incomplete run. `--dry-run` discovers the selected collections without creating the vault or state database.

If a sync is cancelled, already completed skeletons and jobs remain durable, no active foreground lease is left behind, and the incomplete run cannot mark missing favorites as removed. Restart the same command; enumeration may restart from the collection root, while idempotent identities prevent duplicate notes.

## Browser and platform recovery

The CLI attaches only to the configured dedicated Chrome CDP session. It does not copy a normal Chrome profile or accept cookies on the command line.

1. Run `smfa doctor` and resolve the browser/CDP warning.
2. Run `smfa login <platform>`.
3. Complete the platform's own QR, captcha, or device-confirmation UI when requested. Do not attempt to bypass it.
4. Re-run `smfa login <platform>`, then `smfa collections <platform>`.
5. Resume with `smfa sync <platform>` or requeue local failures with `smfa retry failed`.

A layout-change diagnostic pauses the affected adapter rather than declaring a partial list complete. Update the adapter against authorized, sanitized structural evidence before retrying. A media failure should normally be retried after re-enumeration because page-exposed URLs may be ephemeral.

## Cleanup

`smfa cleanup` is a preview. `smfa cleanup --apply` deletes only exact item-owned files that already have a verified cleanup job and matching local hash. A missing derivative, path-containment failure, symlink, or hash mismatch retains the file and exits with an operational error.

## Optional scheduling

Scheduling is opt-in. First complete one manual `doctor`, login, collection listing, sync, and report. Scheduled runs reuse the existing dedicated browser session; they cannot answer QR, captcha, or device-confirmation prompts.

The examples intentionally contain no key, Cookie, token, authorization header, or optional enrichment environment variable. Replace the executable and config paths with absolute, user-owned paths. Keep secrets in the user's existing secure environment rather than copying them into a service definition.

### macOS LaunchAgent

Save as `~/Library/LaunchAgents/dev.smfa.sync.plist`, then load it with `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/dev.smfa.sync.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>dev.smfa.sync</string>
  <key>ProgramArguments</key>
  <array>
    <string>/absolute/path/to/smfa</string>
    <string>sync</string>
    <string>all</string>
    <string>--metadata-only</string>
    <string>--config</string>
    <string>/absolute/path/to/config.yml</string>
  </array>
  <key>StartInterval</key><integer>21600</integer>
  <key>ProcessType</key><string>Background</string>
</dict>
</plist>
```

### Linux systemd user timer

Save this as `~/.config/systemd/user/smfa-sync.service`:

```ini
[Unit]
Description=Social Media Favorites Archiver sync

[Service]
Type=oneshot
ExecStart=/absolute/path/to/smfa sync all --metadata-only --config /absolute/path/to/config.yml
```

Save this as `~/.config/systemd/user/smfa-sync.timer`:

```ini
[Unit]
Description=Run Social Media Favorites Archiver every six hours

[Timer]
OnBootSec=10m
OnUnitActiveSec=6h
Persistent=true

[Install]
WantedBy=timers.target
```

Enable it with `systemctl --user daemon-reload && systemctl --user enable --now smfa-sync.timer`. Inspect only sanitized application reports with `smfa status --json` and `smfa report --json`.
