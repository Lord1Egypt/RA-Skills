---
name: openclaw-windows-sentinel
description: "Keep the OpenClaw gateway alive 24/7 on Windows — install a hidden auto-restart watchdog, cure the SQLite snapshot cleanup failure, kill zombie port listeners, survive logon-only persistence, and diagnose slow starts."
---

# OpenClaw Windows Sentinel

Battle-tested operational kit for running the OpenClaw gateway as an
unattended Windows service. Every rule below comes from a real production
incident; follow them in order when the gateway misbehaves.

## When to use

- Gateway dies when a console window is closed or Ctrl+C is pressed
- Startup fails with "SQLite read-only worker snapshot cleanup failed"
- Gateway process runs but port never listens (looks hung, is just slow)
- Restart leaves an invisible "zombie" listener owning the port
- You need the gateway to survive reboots without a visible window

## The five failure modes and their cures

### 1. Console-window death (whole tree dies together)

Never launch the gateway from a visible console or `start "" /min cmd`.
Closing that window kills gateway + daemon + watchdog in the same instant.

**Cure:** launch through a hidden WScript shim (`scripts/install-autostart.ps1`
writes `gateway-autostart.vbs` into the user's Startup folder). The VBS runs
the watchdog with window style 0, so there is no console to close.

### 2. SQLite read-only snapshot pile-up

OpenClaw opens its shared-state DB through temporary read-only snapshot
copies under `%LOCALAPPDATA%\openclaw`. Bulk-deleting leftovers fail-closes
on locked dirs; once they pile up the next start dies with
"SQLite read-only worker snapshot cleanup failed".

**Cure:** before each start, MOVE (never delete) stale
`openclaw-sqlite-readonly-v2-*` directories to a quarantine folder:

```powershell
scripts/quarantine-snapshots.ps1   # moves stale snapshots, prints count
```

### 3. Zombie port listener after crash-restart

A crashed gateway can leave its old node process LISTENING on the port while
runtime state says stopped. New starts then silently fail to bind.

**Cure:** after every gateway exit, find and force-kill any LISTENING pid on
the gateway port before restarting. The watchdog (`scripts/gateway-daemon.cmd`)
does this automatically.

### 4. Slow start mistaken for a hang

A normal boot takes **2-3 minutes** (agent-DB integrity gates, six worker
threads, plugin init). The HTTP server logs "http server listening (...; Ns)"
with N typically 120-180. Do not kill and retry at 60s — you will loop
forever, and a second instance will refuse with
"Another gateway (pid N) already owns this state directory".

**Cure:** wait at least 4 minutes before declaring a start failed. Probe with
`openclaw gateway status`, not a bare HTTP GET (the ws listener may answer
before plain HTTP does).

### 5. Stopping and force-stopping

`openclaw gateway stop` refuses while it considers the instance unmanaged;
use `openclaw gateway stop --force` only when the port actually has a
listener. If stop cannot find one but a node process still holds the state
directory, kill that pid directly, then remove stale state locks.

## Install the watchdog (3 steps)

```powershell
# 1. quarantine helper + watchdog live in this skill's scripts/ dir
# 2. point the watchdog at your gateway home (default C:\OpenClaw)
scripts/install-autostart.ps1 -GatewayDir "C:\OpenClaw" -Port 18789

# 3. verify
Get-Content "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\OpenClawGateway.vbs"
netstat -ano | findstr ":18789"
```

The watchdog loop: strip host-injected env pollution (NODE_OPTIONS,
PYTHONPATH, BASH_ENV, CODEBUDDY_*), set heap headroom
(`--max-old-space-size=3072`), quarantine snapshots, run the gateway,
on exit kill zombie listeners, wait 30s, repeat. A `gateway-daemon.stop`
flag file ends the loop cleanly.

## Host-environment rules that bite on Windows

- **Job-object reaping:** processes spawned by automation shells are killed
  with the whole tree when the tool call returns. Long-running services must
  run either (a) inside a still-active foreground task, or (b) from
  logon autostart. `Start-Process` + hidden window is NOT enough.
- **Env pollution:** injected `NODE_OPTIONS` / `CODEBUDDY_SAFE_DELETE_*` /
  `GENIE_TRASH_DIR` vars make node's fs operations route through foreign
  helpers and time out. The watchdog strips them; never import them into
  the gateway environment.
- **Launcher pairs:** venv `python.exe`-style launchers appear as two PIDs
  (parent launcher + real interpreter). Count process TREES, not PIDs,
  before deciding something is duplicated.

## Diagnostics cheat sheet

```bash
openclaw gateway status          # runtime + probe + config paths
tail gateway-daemon.log          # boot log: plugin list, listening line
netstat -ano | findstr :18789    # who owns the port
scripts/quarantine-snapshots.ps1 # snapshot hygiene
```

Log locations: `gateway-daemon.log` (watchdog boot log, next to the
watchdog), `%LOCALAPPDATA%\Temp\openclaw\openclaw-<date>.log` (runtime).
