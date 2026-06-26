# Execute Reference

Use this reference when the user wants to deploy a ToxTunnel setup, install the
binary, start processes, or configure service persistence.

## Step 0: Environment Detection

Run these checks before writing files or starting anything:

### 1. Is `toxtunnel` installed?

```bash
which toxtunnel 2>/dev/null || where toxtunnel 2>nul
```

If not found, prefer package installation over source builds.

#### One-line install (recommended)

The repo ships installer scripts that auto-detect arch, download the matching
native package from GitHub Releases, install it, and seed `config.yaml`
based on `--mode`. Client mode writes a config scaffold and leaves the system
service idled (exit 0) until the user fills in `client.server_id` and sets
`service.allow_client_daemon: true`.

```bash
# macOS / Linux (DEB / RPM / .pkg auto-detected)
curl -fsSL https://raw.githubusercontent.com/anonymoussoft/tox-tcp-tunnel/master/scripts/install.sh | sudo sh                       # server
curl -fsSL https://raw.githubusercontent.com/anonymoussoft/tox-tcp-tunnel/master/scripts/install.sh | sudo sh -s -- --mode client   # client scaffold
```

```powershell
# Windows (Administrator PowerShell)
irm https://raw.githubusercontent.com/anonymoussoft/tox-tcp-tunnel/master/scripts/install.ps1 | iex                                       # server
$env:TOXTUNNEL_MODE='client'; irm https://raw.githubusercontent.com/anonymoussoft/tox-tcp-tunnel/master/scripts/install.ps1 | iex         # client scaffold
```

Env vars / flags: `TOXTUNNEL_MODE`, `TOXTUNNEL_VERSION`, `TOXTUNNEL_REPO`. The
installer is idempotent on the same mode and refuses to overwrite a
user-customized config (only rewrites the freshly seeded server template
when switching to client).

#### Manual install per platform

Each release also publishes both versioned assets
(`toxtunnel-<VERSION>-<System>-<arch>.<ext>`) and a stable `-latest` alias
(`toxtunnel-<System>-<arch>-latest.<ext>`). Use the alias URLs below for the
newest release.

#### Linux (DEB - Ubuntu/Debian)

```bash
ARCH=x86_64      # or aarch64
wget "https://github.com/anonymoussoft/tox-tcp-tunnel/releases/latest/download/toxtunnel-Linux-${ARCH}-latest.deb"
sudo dpkg -i "toxtunnel-Linux-${ARCH}-latest.deb"
```

#### Linux (RPM - Fedora/RHEL/CentOS)

```bash
ARCH=x86_64      # or aarch64
wget "https://github.com/anonymoussoft/tox-tcp-tunnel/releases/latest/download/toxtunnel-Linux-${ARCH}-latest.rpm"
sudo rpm -i "toxtunnel-Linux-${ARCH}-latest.rpm"
```

#### macOS

```bash
ARCH=arm64       # or x86_64
wget "https://github.com/anonymoussoft/tox-tcp-tunnel/releases/latest/download/toxtunnel-Darwin-${ARCH}-latest.pkg"
sudo installer -pkg "toxtunnel-Darwin-${ARCH}-latest.pkg" -target /
```

#### Windows

Download the MSI from
`https://github.com/anonymoussoft/tox-tcp-tunnel/releases/latest/download/toxtunnel-Windows-AMD64-latest.msi`
(use `toxtunnel-Windows-ARM64-latest.msi` for ARM) and run it as Administrator.

#### Build from source (only if no package fits)

- macOS: `brew install libsodium && cd <project> && cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(sysctl -n hw.ncpu) && sudo cp build/toxtunnel /usr/local/bin/`
- Linux (Debian/Ubuntu): `sudo apt install libsodium-dev build-essential cmake && cd <project> && cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc) && sudo cp build/toxtunnel /usr/local/bin/`
- Linux (Fedora/RHEL): `sudo dnf install libsodium-devel cmake gcc-c++ && ...`
- Windows: build with MSVC + vcpkg or MSYS2 (see `BUILDING.md`)

### 2. Is libsodium available?

```bash
pkg-config --exists libsodium && echo "OK" || echo "MISSING"
# or: ldconfig -p | grep libsodium   (Linux)
# or: brew list libsodium            (macOS)
```

### 3. Are target ports available?

```bash
lsof -i :PORT -sTCP:LISTEN    # macOS/Linux
netstat -an | findstr :PORT   # Windows
```

### 4. Detect OS for path and service defaults

- macOS (from `.pkg`): `binary: /usr/local/bin/toxtunnel`, example config at `/usr/local/share/toxtunnel/config.yaml.example`. The pkg postinstall automatically seeds `/usr/local/etc/toxtunnel/config.yaml` (from the example), installs `com.toxtunnel.daemon.plist` into `/Library/LaunchDaemons/`, and runs `launchctl bootstrap`.
- macOS (manual/source build): `data_dir: ~/Library/Application Support/toxtunnel/` or `~/.config/toxtunnel/`, service: launchd user agent
- Linux (from DEB/RPM): `binary: /usr/bin/toxtunnel`, `config: /etc/toxtunnel/config.yaml`, `data_dir: /var/lib/toxtunnel`, service: `toxtunnel.service` (Type=notify, `RemainAfterExit=yes`, enabled and started by postinst).
- Linux (manual): `data_dir: ~/.config/toxtunnel/`, service: custom systemd unit
- Windows (from MSI): `binary: C:\Program Files\ToxTunnel\bin\toxtunnel.exe`. **In v0.2.0 the MSI does NOT auto-register the SCM service** — the WiX patch is shelved (`cmake/Packaging.cmake` has the rationale). The user creates `C:\ProgramData\ToxTunnel\config.yaml`, then runs `& 'C:\Program Files\ToxTunnel\bin\toxtunnel.exe' install-windows-service -c 'C:\ProgramData\ToxTunnel\config.yaml'` from an Administrator PowerShell, then `sc start ToxTunnel`. The bundled `scripts/install.ps1` one-liner does all of this automatically.
- Windows (manual): `data_dir: %APPDATA%\toxtunnel\`, service: NSSM or Task Scheduler

## Step 1: Write Config Files

Generate and write:

- `server.yaml`
- `client.yaml`
- `rules.yaml` when access control is needed

Use the templates under `templates/` and enforce the minimum-privilege rules from
the main skill.

## Step 2: Startup Commands

```bash
# Server side
toxtunnel -m server -c /path/to/server.yaml

# Client side
toxtunnel -m client -c /path/to/client.yaml
```

If running on the current machine, only start processes after explicit user request.

## Step 3: Service Persistence

Only do this when the user explicitly asks for persistent service management.

### Linux DEB/RPM

Postinst creates the `toxtunnel` system user, seeds `/etc/toxtunnel/config.yaml`
from the example if missing, registers `toxtunnel.service`, and runs
`systemctl enable --now`. The unit is `Type=notify` with `RemainAfterExit=yes`,
so a daemon that gates itself off (client mode without `allow_client_daemon`,
or missing config under `--service`) shows as `active (exited)` rather than
`inactive (dead)`.

```bash
sudo vim /etc/toxtunnel/config.yaml      # already seeded; edit in place
sudo systemctl restart toxtunnel         # apply changes
sudo systemctl status toxtunnel
```

### macOS `.pkg`

The pkg postinstall (`packaging/macos/postinstall.sh`) seeds
`/usr/local/etc/toxtunnel/config.yaml` from the example if missing, installs
`com.toxtunnel.daemon.plist` into `/Library/LaunchDaemons/`, and runs
`launchctl bootstrap system`. The plist's `KeepAlive { SuccessfulExit: false }`
means a config-gated exit-0 daemon stays stopped (won't loop). On newer macOS
versions, `launchctl bootstrap` may require user approval in System Settings →
Privacy & Security; the postinstall treats that failure as non-fatal.

```bash
sudo vim /usr/local/etc/toxtunnel/config.yaml          # already seeded; edit in place
sudo launchctl kickstart -k system/com.toxtunnel.daemon  # apply changes
sudo launchctl print system/com.toxtunnel.daemon | head
```

### Windows MSI

**In v0.2.0 the MSI does NOT auto-register the SCM service** (the WiX patch is
shelved — see `cmake/Packaging.cmake` for context). Workflow: install MSI →
create config → register the service with the bundled subcommand → start it.

```powershell
mkdir 'C:\ProgramData\ToxTunnel' -Force
notepad 'C:\ProgramData\ToxTunnel\config.yaml'

# Register the service (run as Administrator):
& 'C:\Program Files\ToxTunnel\bin\toxtunnel.exe' install-windows-service `
    -c 'C:\ProgramData\ToxTunnel\config.yaml'

sc start ToxTunnel
sc query ToxTunnel
sc stop ToxTunnel
```

> The one-line installer `scripts/install.ps1` automates all of the above. Use
> it unless the user explicitly needs the manual flow. Remove the service with
> `& 'C:\Program Files\ToxTunnel\bin\toxtunnel.exe' uninstall-windows-service`.

### Manual source-build service templates

#### Linux systemd

```ini
[Unit]
Description=ToxTunnel %i
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/local/bin/toxtunnel -m %i -c /etc/toxtunnel/%i.yaml --service
Restart=on-failure
RestartSec=5
User=toxtunnel
WorkingDirectory=/etc/toxtunnel

[Install]
WantedBy=multi-user.target
```

Install with:
`sudo cp toxtunnel@.service /etc/systemd/system/ && sudo systemctl enable --now toxtunnel@server`

#### macOS launchd

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.toxtunnel.MODE</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/toxtunnel</string>
        <string>-m</string>
        <string>MODE</string>
        <string>-c</string>
        <string>/usr/local/etc/toxtunnel/MODE.yaml</string>
        <string>--service</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/usr/local/var/log/toxtunnel-MODE.log</string>
    <key>StandardErrorPath</key>
    <string>/usr/local/var/log/toxtunnel-MODE.log</string>
</dict>
</plist>
```

Install with:
`cp com.toxtunnel.MODE.plist ~/Library/LaunchAgents/ && launchctl load ~/Library/LaunchAgents/com.toxtunnel.MODE.plist`

#### Windows `sc.exe` (raw)

```cmd
sc create ToxTunnel binPath= "\"C:\path\to\toxtunnel.exe\" -c \"C:\path\to\config.yaml\" --service" start= auto
sc start ToxTunnel
```

Or use the bundled subcommand (same effect, fewer footguns around quoting):

```cmd
"C:\path\to\toxtunnel.exe" install-windows-service -c "C:\path\to\config.yaml"
sc start ToxTunnel
```

#### Windows NSSM

```cmd
nssm install ToxTunnel-MODE "C:\path\to\toxtunnel.exe" -m MODE -c "C:\path\to\MODE.yaml"
nssm set ToxTunnel-MODE AppStdout "C:\path\to\logs\MODE.log"
nssm set ToxTunnel-MODE AppStderr "C:\path\to\logs\MODE.log"
nssm start ToxTunnel-MODE
```

## Step 4: Lifecycle Operations

### Start / Stop / Restart

```bash
# Direct process
toxtunnel -m server -c server.yaml &
kill $(pgrep -f "toxtunnel.*server")

# systemd
sudo systemctl start toxtunnel
sudo systemctl stop toxtunnel
sudo systemctl restart toxtunnel
sudo systemctl start toxtunnel@server
sudo systemctl stop toxtunnel@server

# launchd
sudo launchctl bootstrap system /Library/LaunchDaemons/com.toxtunnel.daemon.plist
sudo launchctl bootout system /Library/LaunchDaemons/com.toxtunnel.daemon.plist
launchctl start com.toxtunnel.server
launchctl stop com.toxtunnel.server

# Windows SCM
sc start ToxTunnel
sc stop ToxTunnel

# Windows NSSM
nssm start ToxTunnel-server
nssm stop ToxTunnel-server
```

### View logs

```bash
tail -f /var/log/toxtunnel/server.log
journalctl -u toxtunnel@server -f
tail -f /usr/local/var/log/toxtunnel-server.log
toxtunnel -m server -c server.yaml -l debug
```

## Step 4.4: v0.3.0 Feature Recipes

### Enable Prometheus `/metrics`

Add to **either** `server.yaml` **or** `client.yaml` (or both — they expose
different label sets):

```yaml
metrics:
  enabled: true
  listen: 127.0.0.1:9100   # KEEP loopback unless the scraper is on a trusted network
  path: /metrics
```

Restart the daemon (metrics listen is NOT a hot-reloadable field), then smoke-test:

```bash
curl -s http://127.0.0.1:9100/metrics | grep '^toxtunnel_' | head -20
```

Expected metric families:
`toxtunnel_build_info`, `toxtunnel_tunnels_active{role=...}`,
`toxtunnel_tunnels_opened_total{result="ok|denied|failed"}`,
`toxtunnel_tunnels_closed_total{reason="local|remote|timeout|error"}`,
`toxtunnel_bytes_in_total`, `toxtunnel_bytes_out_total`,
`toxtunnel_friends_online`, `toxtunnel_tox_iterate_lag_milliseconds_{count,sum,max}`.

Minimal Prometheus scrape config:

```yaml
scrape_configs:
  - job_name: toxtunnel
    static_configs:
      - targets: ['127.0.0.1:9100']
    scrape_interval: 15s
```

### Enable SOCKS5 / HTTP CONNECT listener (client side)

CLI flag form (no YAML edit, ephemeral):

```bash
toxtunnel -m client --server-id homelab --socks5 127.0.0.1:1080
```

YAML form:

```yaml
client:
  server_id: homelab
  socks5:
    enabled: true
    listen: 127.0.0.1:1080     # config validator REJECTS non-loopback binds
```

Use it from a browser / curl / pip:

```bash
# curl over SOCKS5 (DNS resolved on the server side via socks5-hostname / socks5h)
curl --socks5-hostname 127.0.0.1:1080 http://internal.example.lan/

# HTTP CONNECT (same listener auto-detects)
https_proxy=http://127.0.0.1:1080 curl https://internal.example.lan/

# Firefox / Chrome: SOCKS host 127.0.0.1, port 1080, "Proxy DNS when using SOCKS v5"
```

**The server-side `rules.yaml` still gates which destinations succeed** — a
SOCKS5 CONNECT to a host/port that isn't in the friend's allow list returns a
SOCKS5 "connection not allowed by ruleset" reply. SOCKS5 and `client.pipe`
cannot be enabled at the same time (validator error).

### Multi-server failover (production HA)

YAML list form for `server_id`:

```yaml
client:
  server_id:
    - homelab-primary       # entry 0 = preferred primary
    - hetzner-fallback
    - <full-76-char-tox-id> # raw IDs and aliases mix freely
  failover:
    timeout_seconds: 60               # primary offline this long -> promote next online candidate
    prefer_primary_grace_seconds: 30  # primary must be online this long before we switch back
  forwards:
    - { local_port: 2222, remote_host: 127.0.0.1, remote_port: 22 }
```

CLI flag form (one primary + repeated fallback):

```bash
toxtunnel -m client \
  --server-id homelab-primary \
  --server-id-fallback hetzner-fallback aws-fallback \
  -c client.yaml
```

Verify failover behavior:

```bash
# Watch active server transitions in the log
journalctl -u toxtunnel -f | grep -E 'Failover|active server'

# Or query the running daemon directly
toxtunnel inspect status --json | jq '.active_server, .friends'
```

### Live inspection (`toxtunnel inspect`)

The daemon serves a local IPC channel — Unix socket on POSIX
(`<data_dir>/toxtunnel.sock`), named pipe on Windows
(`\\.\pipe\toxtunnel-inspect-<pid>`). Inspection is read-only and
strictly local — never network-exposed.

```bash
# Table of currently open tunnels (id, role, friend, target, bytes, age)
toxtunnel inspect tunnels

# Process / version / friend / metrics snapshot
toxtunnel inspect status

# Pipe JSON into jq for dashboards or scripting
toxtunnel inspect tunnels --json | jq '.tunnels[] | select(.bytes_in > 1000000)'

# Point at a non-default data_dir (e.g. service install paths)
toxtunnel inspect status -c /etc/toxtunnel/server.yaml
toxtunnel inspect tunnels -d /var/lib/toxtunnel
```

`inspect.enabled` is **default-on**; set `inspect.enabled: false` to disable.

### Hot-reload (no restart)

Reloadable subset only: **`server.rules_file` contents, `client.forwards`,
`logging.level`**. Tox identity, listen ports, mode, and `data_dir` still
require a full restart.

```bash
# POSIX (Linux/macOS): SIGHUP, either form works
toxtunnel reload                            # cross-platform, finds pid via data_dir
toxtunnel reload -c /etc/toxtunnel/server.yaml
kill -HUP $(cat /var/lib/toxtunnel/toxtunnel.pid)
kill -HUP $(pgrep -f 'toxtunnel.*server')
```

```powershell
# Windows: writes RELOAD\n to \\.\pipe\toxtunnel-reload-<pid>
toxtunnel.exe reload -c 'C:\ProgramData\ToxTunnel\config.yaml'
```

Confirm the reload landed by tailing the log for one of:

```
config reloaded (rules: N rules)
config reloaded (forwards: +A -B)
```

If the new config has a parse error or validation failure, the daemon
**rejects the reload, keeps running the old config, and logs**
`reload failed: <reason>` / `reload rejected: <reason>` — no downtime, no
partial state.

### Idle tunnel reaper

Set a non-zero `tunnel.idle_timeout_seconds` to close tunnels that have
seen no data in that many seconds. Default `0` disables it.

```yaml
tunnel:
  idle_timeout_seconds: 900   # 15 minutes
  reaper_tick_seconds: 10     # how often the reaper wakes up
```

Closed-by-reaper events show up as `toxtunnel_tunnels_closed_total{reason="timeout"}`
in the metrics endpoint.

## Step 4.5: Known-Servers Registry (client side)

After a successful client→server connection, the client persists an entry in
`<data_dir>/known_servers.yaml`. Manage it from the CLI:

```bash
toxtunnel servers list                       # compact list of saved servers
toxtunnel servers list --full                # show full 76-char Tox IDs
toxtunnel servers show <alias_or_tox_id>     # full record incl. info disclosed by server
toxtunnel servers add  <alias> <tox_id>      # name a Tox ID
toxtunnel servers remove <alias_or_tox_id>   # forget
```

After `servers add homelab DE47F2...`, both `--server-id homelab` and
`client.server_id: homelab` resolve from the registry at startup.

For server-side info disclosure (defaults to nothing), uncomment the relevant
fields under `server.disclose:` in `server.yaml`:

```yaml
server:
  rules_file: rules.yaml
  disclose:
    hostname: true
    os: true
    arch: true
```

The disclosed snapshot is sent via `INFO_REPLY` (frame 0x07) when the client
sends an `INFO_REQUEST` (frame 0x06) on first reaching online state.

## Step 5: Post-Deploy Verification

```bash
bash scripts/verify.sh <local_port> <service_type>
```

## Output Format

```text
## Environment Check
- toxtunnel: [installed at /usr/local/bin/toxtunnel | NOT FOUND]
- libsodium: [OK | MISSING]
- Port XXXX: [available | in use by PROCESS]
- OS: [macOS / Linux / Windows]

## Generated Files
- server.yaml -> /path/to/server.yaml
- client.yaml -> /path/to/client.yaml
- rules.yaml  -> /path/to/rules.yaml  (if applicable)

## Startup Commands
[OS-specific commands]

## Service Persistence
[Only if requested: systemd/launchd/NSSM config]

## Lifecycle Commands
[start / stop / restart / logs]

## Verification
[Test command and expected output]
```

## v0.4 Optional Config Blocks

Operators with extra capacity / hardening needs can opt into the new
v0.4 blocks. Defaults preserve v0.3.0 behaviour byte-for-byte.

### Watchdog (on by default)

```yaml
watchdog:
  enabled: true                # default
  deadline_seconds: 30         # min 5; raise on flaky-network deployments
  systemd_notify: true         # ignored outside Linux
```

### Adaptive coalescing (opt-in)

```yaml
tunnel:
  coalesce_mode: adaptive      # default fixed (v0.3.0); flip to adaptive
                                # only after one release of soak
```

### BDP flow control (opt-in)

```yaml
flow_control:
  mode: bdp                    # default fixed; bdp scales window from RTT × bps
  send_window_min_bytes: 65536
  send_window_max_bytes: 4194304
  safety_factor_x100: 150
  fixed_window_bytes: 262144
```

### Per-friend rate limiting (opt-in)

In `rules.yaml`:

```yaml
rate_limit_defaults:
  mode: report                 # start shadow; flip to enforce once tuned
  open_per_sec: 10
  open_burst: 50
  bytes_per_sec: 10485760
  bytes_burst: 33554432
  max_concurrent_tunnels: 100

rules:
  - friend: "...64hex..."
    rate_limit:
      bytes_per_sec: 104857600
      max_concurrent_tunnels: 200
    allow:
      - host: "127.0.0.1"
        ports: [22]
```

### Tunnel resume (opt-in, live in v0.4.x)

```yaml
tunnel:
  resume:
    enabled: false             # opt-in; default off. Live in v0.4.x: opcodes
                                # 0x08 / 0x09 are wire-active only when enabled.
    max_age_seconds: 300
    on_gap: passthrough
```

