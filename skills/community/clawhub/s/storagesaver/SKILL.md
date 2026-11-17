---
name: storagesaver-watcher
description: >
  Watch and explain Mac disk usage. Use when the user asks about Mac
  storage/disk space ("what's eating my disk?", "disk full", "free up
  space"), wants a visual map of what's on the disk, or wants scheduled
  storage watching with alerts. Read-only by design: it recommends
  copy-paste commands, it never deletes anything itself.
---

# StorageSaver watcher

StorageSaver is a read-only Mac disk scanner that produces an interactive
HTML map (sunburst + tree) with plain-English explanations and safety
badges (safe / review / never-touch), plus this watcher script for
scheduled checks.

## Install / one-off scan

```bash
npx storagesaver            # scan → storagesaver.html in cwd → opens in browser
npx storagesaver --quick    # home-folder-only fast pass
```

For a scheduled setup, clone or install the package once so `watcher.js`
and the CLI are on disk:

```bash
npm install -g storagesaver
# watcher lives at <install>/skill/watcher.js
```

## Answering "what's eating my disk?"

1. Run `npx storagesaver scan --no-open --out /tmp/storagesaver.html`
   (45–90s for a full disk walk).
2. Open or attach the HTML. The severity summary and top easy wins are in
   the map; green ⧉ buttons carry copy-paste reclaim commands.
3. Never run the reclaim commands yourself unless the user explicitly
   asks; present them for the user to run.

## Scheduled watching (weekly cron)

The watcher gathers, classifies, and only speaks when it matters:

- **Severity tiers** (% used on the data volume): `<70%` silent,
  `70–84%` heads-up, `85–94%` getting tight, `>=95%` urgent.
- **Debounce**: same severity bucket within 6 days of the last alert →
  stays quiet (no weekly nagging about the same state). `--force` overrides.

Plain cron example:

```cron
0 10 * * 1 NOTIFY_CMD='mail -s "Mac storage" you@example.com' node /path/to/skill/watcher.js
```

OpenClaw agent example — schedule it as a command cron so the agent
delivers the result rather than re-planning the work:

```bash
openclaw cron add --name storage-watch --schedule "0 10 * * 1" \
  --command "node /path/to/StorageSaver/skill/watcher.js" \
  --deliver
```

### Notification channel

`NOTIFY_CMD` is any shell command: the alert message is piped to stdin
and the freshly generated `storagesaver.html` path is passed as `$1`.
**Attach that HTML to whatever channel you notify on** (email attachment,
chat upload, etc.) — the one-line alert says what to do first; the map is
where the user digs. Without `NOTIFY_CMD` the message goes to stdout.

State, logs, and JSON reports live under `~/.config/storagesaver/`.

## Verify-before-flagging-apps playbook

Never tell the user an app is "unused" from file timestamps alone.
Background utilities (window managers, launchers, clipboard managers)
rarely rewrite their prefs while running 24/7. Before flagging any app:

1. **Is it running right now?** Match by executable path, not name:
   ```bash
   pgrep -f "/Applications/<App>.app/Contents/MacOS"
   ```
2. **Is it a login item?** The user explicitly wants those auto-started:
   ```bash
   osascript -e 'tell application "System Events" to get the name of every login item'
   ```
3. **Last-used signals, best first**: Spotlight's
   `mdls -name kMDItemLastUsedDate -raw <App>.app` beats prefs-plist
   mtime when present (it records actual opens); fall back to
   `~/Library/Preferences/<bundleId>.plist` mtime, the app's
   `~/Library/Containers/<bundleId>` mtime, and Saved Application State.
   Take the MOST RECENT signal — the generous estimate.
4. Helper-style apps launched by other tools (diff viewers via
   `git difftool`, etc.) leave almost no signals — always phrase these as
   "confirm before deleting", never as certain.

The watcher already implements all of this; the playbook is for when you
investigate manually or the user questions a finding.

## Safety rules the recommendations follow

- Docker's `Docker.raw` is a grow-only sparse VM disk: `docker system
  prune` will NOT shrink it — purge via Docker Desktop.
- With Messages in iCloud ON, lowering "Keep messages" deletes history
  from iCloud on ALL devices — only the render cache is safe to clear.
- `~/Library/CloudStorage` is live cloud data: a local `rm` there is a
  cloud delete. Reclaim Google Drive space by reconnecting in Stream
  mode, never by deleting files.
- Photos libraries are managed by Photos.app — never touch in Finder.
- Users can add their own rules in `~/.config/storagesaver/rules.json`
  (see the project README).
