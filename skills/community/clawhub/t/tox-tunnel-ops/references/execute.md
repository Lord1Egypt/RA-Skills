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

#### Preferred: version-pinned native package

The canonical, always-current install instructions are the "Installation"
section of the repo's [`README.md`](https://github.com/agentx-icu/tox-tcp-tunnel#installation);
if this file and the README ever disagree, the README wins. The newest release
at the time of writing is **v0.5.1** — check the Releases page for the current
one rather than trusting this number.

**When you are installing on an operator's machine, do not pipe a script from a
mutable branch into `sudo sh`.** You have already detected OS and architecture,
so you can do the installer's actual job — pick the right asset, hand it to the
package manager — from a version-pinned URL. This avoids piping a mutable remote
script into a root shell. It is **not** "no remote code as root": installing a
DEB/RPM/PKG/MSI still runs that package's maintainer scripts with privileges.
What changes is that the code executed is the released package, pinned to a
version you chose, rather than whatever `master` holds at that moment:

```bash
VER=0.5.1; ARCH=x86_64           # or aarch64
BASE="https://github.com/agentx-icu/tox-tcp-tunnel/releases/download/v${VER}"

# Linux (DEB - Ubuntu/Debian)
curl -fsSL -o "/tmp/toxtunnel-${VER}.deb" "${BASE}/toxtunnel-${VER}-Linux-${ARCH}.deb"
sudo apt-get install -y "/tmp/toxtunnel-${VER}.deb"

# Linux (RPM - Fedora/RHEL/CentOS)
curl -fsSL -o "/tmp/toxtunnel-${VER}.rpm" "${BASE}/toxtunnel-${VER}-Linux-${ARCH}.rpm"
sudo rpm -i "/tmp/toxtunnel-${VER}.rpm"

# macOS (ARCH=arm64 or x86_64)
curl -fsSL -o "/tmp/toxtunnel-${VER}.pkg" "${BASE}/toxtunnel-${VER}-Darwin-${ARCH}.pkg"
sudo installer -pkg "/tmp/toxtunnel-${VER}.pkg" -target /
```

```powershell
# Windows (Administrator PowerShell); ARM: toxtunnel-$VER-Windows-ARM64.msi
$VER='0.5.1'
irm "https://github.com/agentx-icu/tox-tcp-tunnel/releases/download/v$VER/toxtunnel-$VER-Windows-AMD64.msi" -OutFile "$env:TEMP\toxtunnel.msi"
msiexec /i "$env:TEMP\toxtunnel.msi" /qn
```

**Integrity, stated accurately.** No `.sha256` or signature assets are
published — the release carries the packages and their `-latest` aliases. But
GitHub exposes a SHA-256 digest for every release asset regardless, so there IS
something to verify against: compare the downloaded file's digest with the one
GitHub reports for that asset. What is missing is independent
signature/provenance — the digest and the file come from the same party, so it
detects corruption and truncation, not a compromised release. Note also that a
release URL is only immutable if the repository enabled immutable releases;
otherwise the tag is a convention, not a guarantee. Say exactly this if the
operator asks about integrity, rather than implying either more or less
assurance than exists.

Each release also publishes stable `-latest` aliases
(`toxtunnel-<System>-<arch>-latest.<ext>`). They are convenient but unpinned, and
what they resolve to changes under you — prefer the versioned asset when the
install needs to be reproducible.

#### The one-line installer (only when the user asks for it)

The repo ships installer scripts that auto-detect arch, download the matching
native package from GitHub Releases, install it, and seed `config.yaml`
based on the mode (`--mode` for `install.sh`, `-Mode` or `TOXTUNNEL_MODE` for
`install.ps1`). Client mode writes a config scaffold and leaves the system
service idled (exit 0) until the user fills in `client.server_id` and sets
`service.allow_client_daemon: true`.

If the user explicitly wants this path, **pin it to a release tag, download it,
let them read it, and only then run it.** `master` is mutable: the `| sudo sh`
form executes whatever landed on that branch today, as root, unreviewed.

```bash
# Download a pinned copy (tag URLs resolve; verified for v0.5.1)
curl -fsSL -o /tmp/toxtunnel-install.sh \
  https://raw.githubusercontent.com/agentx-icu/tox-tcp-tunnel/v0.5.1/scripts/install.sh
less /tmp/toxtunnel-install.sh            # <- show the operator what will run as root
sudo sh /tmp/toxtunnel-install.sh                        # server
sudo sh /tmp/toxtunnel-install.sh --mode client          # client scaffold
```

```powershell
# Windows (Administrator PowerShell)
irm https://raw.githubusercontent.com/agentx-icu/tox-tcp-tunnel/v0.5.1/scripts/install.ps1 -OutFile "$env:TEMP\install.ps1"
Get-Content "$env:TEMP\install.ps1" | more     # review first
$env:TOXTUNNEL_MODE='client'; & "$env:TEMP\install.ps1"
```

Env vars / flags: `TOXTUNNEL_MODE`, `TOXTUNNEL_VERSION`, `TOXTUNNEL_REPO`. The
installer is idempotent on the same mode and refuses to overwrite a
user-customized config (only rewrites the freshly seeded server template
when switching to client).

Do not run the `curl … | sudo sh` or `irm … | iex` form on the user's behalf.

#### Unpinned `-latest` aliases (convenience only)

If reproducibility does not matter, the `-latest` aliases save looking up a
version number:

```bash
ARCH=x86_64      # or aarch64 (Darwin: arm64 / x86_64)
BASE=https://github.com/agentx-icu/tox-tcp-tunnel/releases/latest/download
wget "$BASE/toxtunnel-Linux-${ARCH}-latest.deb"  && sudo dpkg -i "toxtunnel-Linux-${ARCH}-latest.deb"
wget "$BASE/toxtunnel-Linux-${ARCH}-latest.rpm"  && sudo rpm -i  "toxtunnel-Linux-${ARCH}-latest.rpm"
wget "$BASE/toxtunnel-Darwin-${ARCH}-latest.pkg" && sudo installer -pkg "toxtunnel-Darwin-${ARCH}-latest.pkg" -target /
# Windows: $BASE/toxtunnel-Windows-AMD64-latest.msi (ARM64 variant available), run as Administrator
```

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
- Windows (from MSI): `binary: C:\Program Files\ToxTunnel\bin\toxtunnel.exe`. **The MSI does NOT auto-register the SCM service** — the WiX patch is shelved (`cmake/Packaging.cmake` has the rationale). The user creates `C:\ProgramData\ToxTunnel\config.yaml`, then runs `& 'C:\Program Files\ToxTunnel\bin\toxtunnel.exe' install-windows-service -c 'C:\ProgramData\ToxTunnel\config.yaml'` from an Administrator PowerShell, then `sc start ToxTunnel`. The repo's own `scripts/install.ps1` (in the tox-tcp-tunnel repository, not this skill's `scripts/`) does all of this automatically — download and review it first.
- Windows (manual): `data_dir: %APPDATA%\toxtunnel\`, service: NSSM or Task Scheduler

## Step 1: Write Config Files

Generate and write:

- `server.yaml`
- `client.yaml`
- `rules.yaml` when access control is needed

Use the templates under `templates/` and enforce the minimum-privilege rules from
the main skill. Three things to get right at write time:

1. **`server.rules_file` must be absolute.** A relative path resolves against the
   daemon's working directory, not the config's directory, so a service unit
   fails to start with `Rules file not found`.
2. **`data_dir` must be absolute, writable by the service account, and not under
   `/etc`** — it holds mutable state (identity, pid, lock, inspect socket). Use
   `/var/lib/toxtunnel` on Linux.
3. **Always write `local_address` explicitly.** An absent key binds
   `127.0.0.1` on v0.5.0+ but `0.0.0.0` on every version before it, so an
   implicit bind changes meaning across the upgrade. On **v0.4.13+** set
   `local_address: 127.0.0.1` unless it must serve other machines (then
   `0.0.0.0`); on v0.4.12 and older there is no such key and the bind is
   always wide, so emit the exposure warning with the config and give the
   operator either a host firewall rule for that port or a loopback-only SOCKS5
   listener instead.

Then validate before starting anything:

```bash
toxtunnel config check -c server.yaml --strict
toxtunnel config check -c client.yaml --strict
bash scripts/diagnose.sh server.yaml    # covers rules.yaml semantics (config check opens
                                        # the file only on v0.5.0+, and syntax-only there)
```

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

**The MSI does NOT auto-register the SCM service** (the WiX patch is
shelved — see `cmake/Packaging.cmake` for context). Workflow: install MSI →
create config → register the service with the bundled subcommand → start it.
An in-place upgrade (`msiexec /i toxtunnel-<new>.msi /qn /norestart`) keeps
`config.yaml`, `data\` and the registered service; `Stop-Service ToxTunnel`
before and `Start-Service ToxTunnel` after.

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

> The repo's one-line installer (`scripts/install.ps1` in the tox-tcp-tunnel
> repository, not this skill's `scripts/`) automates all of the above. Use
> it unless the user explicitly needs the manual flow. Remove the service with
> `& 'C:\Program Files\ToxTunnel\bin\toxtunnel.exe' uninstall-windows-service`.
>
> `install-windows-service` also configures SCM recovery actions (restart after
> 10 s / 30 s / 60 s, with `fFailureActionsOnNonCrashFailures` set so a clean
> exit reporting an error counts). That is what makes Windows retry a startup
> that failed for a transient reason — e.g. a restart racing the previous
> instance for the data-directory lock — the way systemd's `Restart=on-failure`
> and launchd's `KeepAlive` already do. Check it with `sc qfailure ToxTunnel`.
>
> From v0.5.0 the command is safe to re-run after an upgrade: an existing
> registration is updated in place (binary path, auto-start, recovery policy)
> instead of failing, and the daemon re-applies a missing recovery policy at
> every service start, so a service registered by an older release repairs
> itself.

### Manual source-build service templates

#### Linux systemd

Model it on the packaged unit (`packaging/linux/toxtunnel.service`), which runs
as a dedicated account with systemd-managed state — never as root:

```ini
[Unit]
Description=ToxTunnel %i
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/local/bin/toxtunnel -m %i -c /etc/toxtunnel/%i.yaml --service
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5
RemainAfterExit=yes
# Never run this as root. StateDirectory creates and chowns
# /var/lib/toxtunnel to the service account; point data_dir there.
User=toxtunnel
Group=toxtunnel
StateDirectory=toxtunnel
StateDirectoryMode=0750
WorkingDirectory=/etc/toxtunnel

[Install]
WantedBy=multi-user.target
```

`WorkingDirectory` is set here only as a belt-and-braces measure — do **not**
rely on it to resolve a relative `server.rules_file`. Write that path absolute
(`/etc/toxtunnel/rules.yaml`); the daemon does no config-relative resolution and
any change to the unit's working directory would break startup.

The packaged unit carries no sandboxing directives. If you are writing a unit
from scratch for an exposed host, consider adding `NoNewPrivileges=yes`,
`ProtectSystem=strict`, `ProtectHome=yes`, `PrivateTmp=yes`,
`RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX` and
`CapabilityBoundingSet=` — but test them, they are not what ships.

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
    <!-- Match the packaged plist: restart on failure, but NOT after a clean
         exit. An unconditional <true/> here respawn-loops a daemon that has
         gated itself off on purpose (client mode without allow_client_daemon,
         or a missing config under --service), because those exit 0. -->
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
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
kill "$(cat <data_dir>/toxtunnel.pid)"      # pid file written by the daemon (v0.4.11+)
# or: pkill -x toxtunnel   — never `pkill -f toxtunnel…`: -f also matches the
#     shell / CI step / SSH wrapper whose command line mentions toxtunnel

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

**Server-side policy still gates which destinations succeed** — a SOCKS5
CONNECT the friend's `rules.yaml` does not allow returns reply `0x02`
("connection not allowed by ruleset"), and so do the other policy rejections,
the rate limiter and the concurrent-tunnel cap; the same denial over HTTP
CONNECT returns `403 Forbidden`. Everything else the open can fail with maps
elsewhere — SOCKS5 `0x04` (host unreachable), `0x05` (connection refused),
`0x01` (general failure), and `502 Bad Gateway` for all three over HTTP CONNECT
— so the code tells you whether the **server** refused the request or simply
could not reach the target. SOCKS5 and `client.pipe` cannot be enabled at the
same time (validator error).

**Reading a rate-limit / tunnel-cap denial depends on BOTH versions.** Before
v0.4.12 the server sent `TUNNEL_ERROR` code 3 for those denials; from v0.4.12 it
sends code 1. Independently, a v0.4.12+ client carries a compatibility shim that
re-classifies code 3 as a denial when the description is exactly
`"Rate limit exceeded"` or `"Tunnel limit exceeded"`. So:

| Server | Client | Rate-limit / cap denial surfaces as |
|--------|--------|-------------------------------------|
| ≥ v0.4.12 | ≥ v0.4.12 | `0x02` / `403` — correct |
| ≥ v0.4.12 | ≤ v0.4.11 | `0x02` / `403` — correct (the server already sends code 1) |
| ≤ v0.4.11 | ≥ v0.4.12 | `0x02` / `403` — correct, via the client-side shim |
| ≤ v0.4.11 | ≤ v0.4.11 | **`0x04` / `502`** — looks like an unreachable host |

Only the last row is misleading, and it needs *both* ends to be old. The shim
matches those two strings exactly, so a server that reworded them would fall
back to `0x04` as well. When you are on that last row, check
`toxtunnel_rate_limit_open_rejected_total` on the server before blaming the
target.

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
    - { local_port: 2222, local_address: 127.0.0.1, remote_host: 127.0.0.1, remote_port: 22 }
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
toxtunnel inspect status --json | jq '.friends_online, .dht_connected, .peer_online_seconds'
# (there is no .active_server field — the active server appears only in the
#  `Failover: switching active server …` log line)
```

### Live inspection (`toxtunnel inspect`)

The daemon serves a local IPC channel — Unix socket on POSIX
(`<data_dir>/toxtunnel.sock`), named pipe on Windows
(`\\.\pipe\toxtunnel-<pid>`, with the pid published in
`<data_dir>\toxtunnel.pid`). Inspection is read-only and strictly local —
never network-exposed.

```bash
# Table of currently open tunnels: ID TARGET STATE BYTES_IN BYTES_OUT IDLE_S PEER
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
The switch is only honoured from **v0.4.11** — earlier daemons parsed the key
and started the listener regardless, so on an older build the only way to keep
the IPC channel closed is not to run that build.

### Hot-reload (no restart)

Reloadable subset only: **`server.rules_file` contents, `client.forwards`,
`logging.level`**. Tox identity, listen ports, mode, and `data_dir` still
require a full restart.

```bash
# POSIX (Linux/macOS): SIGHUP, either form works
toxtunnel reload -c /etc/toxtunnel/server.yaml   # reads <data_dir>/toxtunnel.pid, sends SIGHUP
kill -HUP $(cat /var/lib/toxtunnel/toxtunnel.pid)
sudo systemctl reload toxtunnel                  # packaged install
```

```powershell
# Windows: writes RELOAD\n to \\.\pipe\toxtunnel-reload-<pid>
# (pid from <data_dir>\toxtunnel.pid; use an elevated prompt for the service)
toxtunnel.exe reload -c 'C:\ProgramData\ToxTunnel\config.yaml'
```

Daemons older than v0.4.11 wrote no pid file: set `TOXTUNNEL_RELOAD_PID=<pid>`
(the pid is in the startup log line `Inspect IPC listening at ...toxtunnel-<pid>`).

Confirm the reload landed by tailing the log for one of:

```
config reloaded (rules: N rules)
config reloaded (forwards: +A -B)
```

If the new config has a parse error or validation failure, the daemon
**rejects the reload, keeps running the old config, and logs**
`reload failed: <reason>` / `reload rejected: <reason>` — no downtime, no
partial state.

### Tunnel reapers — two distinct policies

```yaml
tunnel:
  half_close_timeout_seconds: 120   # DEFAULT-ON. Disconnecting tunnels only.
  idle_timeout_seconds: 0           # opt-in. ANY non-Connecting tunnel.
  reaper_tick_seconds: 10           # shared wake-up interval
```

- **`half_close_timeout_seconds` (default 120, on)** reaps only tunnels in state
  `Disconnecting` — a one-sided TCP close whose peer never sent the reciprocal
  `TUNNEL_CLOSE`, which would otherwise pin a half-open fd forever. This is the
  policy that already handles "zombie" tunnels. If half-closed tunnels linger,
  **lower this**; do not enable the idle reaper for them.
- **`idle_timeout_seconds` (default 0, off)** reaps *any* tunnel that is not in
  `Connecting`, purely on time since the last `TUNNEL_DATA` in either direction.
  That includes healthy `Connected` tunnels, so it will kill a quiet SSH session
  or an idle connection pool. Enable it only after confirming with
  `toxtunnel inspect tunnels` that the accumulating tunnels really are
  `Connected` and genuinely abandoned, and pick a timeout longer than the
  longest legitimate silence in your workload.

Both book `toxtunnel_tunnels_closed_total{reason="timeout"}`, so that counter
does not tell you which one fired — check the tunnel states instead.

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
  rules_file: /etc/toxtunnel/rules.yaml   # absolute — see Step 1
  disclose:
    hostname: true
    os: true
    arch: true
```

The disclosed snapshot is sent via `INFO_REPLY` (frame 0x07) when the client
sends an `INFO_REQUEST` (frame 0x06) on first reaching online state.

## Step 5: Post-Deploy Verification

```bash
bash scripts/verify.sh <local_port> <service_type> <client.yaml>
```

`service_type` is one of `ssh | http | postgres | mysql | redis | mongo | rdp |
tcp`; an unrecognised value is rejected rather than silently treated as generic
TCP. Passing the client config lets the script read `friends_online` from the
running daemon instead of inferring liveness from a local TCP accept.

**Judge it by the exit code, not the text:**

| Exit | Meaning | What to report |
|------|---------|----------------|
| `0` | The remote service replied through the tunnel | Working |
| `2` | Local checks passed, end-to-end **NOT** proven (no probe tool installed, or `tcp` has no protocol probe) | **Not** working-confirmed. Say what is still unverified |
| `1` | A check failed | Broken; the output names the layer |

A successful TCP connect to `127.0.0.1:<port>` is **not** evidence the tunnel
works: the client binds and accepts the local port before any `TUNNEL_OPEN` is
attempted, so the port answers even with the Tox link down and the rules denying
everything. Only a reply from the real remote service proves the path.

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
v0.4 blocks. Defaults preserve v0.3.0 behaviour, with two deliberate
exceptions: `flow_control.mode` is `bdp` (since v0.4.1), and `watchdog`
is on. v0.5.0 adds two default-on client timings, `open_timeout_seconds`
and `offline_open_wait_seconds` (see "v0.5.0 additions" below).

### Watchdog (on by default)

```yaml
watchdog:
  enabled: true                # default
  deadline_seconds: 30         # min 5 (validator-enforced)
  systemd_notify: true         # ignored outside Linux
```

The watchdog measures **one thing**: how long since the Tox thread last returned
from `tox_iterate()`. It knows nothing about network reachability, so "the
network is flaky" is not a reason to raise `deadline_seconds` — a peer being
unreachable does not stall `tox_iterate`. Raise it only when the *host* is slow
enough that a legitimate iterate can exceed the deadline: heavy CPU oversubscription,
a frozen or swapping VM, a stalled disk. Otherwise leave it at 30.

Monitoring it — mind the two similarly named metrics:

- **`toxtunnel_tox_iterate_lag_ms`** — gauge, milliseconds since the last
  successful `tox_iterate()` return. **This is the wedge signal.** Alert when it
  approaches `deadline_seconds` (e.g. `> 5000`).
- **`toxtunnel_tox_iterate_lag_milliseconds_max`** (plus `_count` / `_sum`) —
  the maximum *completed* call duration since process start. It latches on one
  historical slow call and can never move while a call is actually hung, so it
  is a trend indicator, not an alarm.
- **`toxtunnel_watchdog_aborts_total`** — **resets to 0 at every process start.**
  It is not seeded from `<data_dir>/abort_count`; that file is the durable
  count, written only at abort time. Alert on `increase(...)` over a window, and
  read the file for history.

The fatal line is logged at **critical** level and reads:

```text
tox_thread wedge detected: lag_ms=<N> deadline_ms=<N> heartbeat_count=<N> phase=<phase> (confirmed over 5 consecutive checks); aborting so the service manager restarts the daemon
```

Since v0.5.0 the abort is **confirmed**: the heartbeat counter must stay
unchanged for 5 consecutive over-deadline checks, and a check that finds the
observer itself was stalled past the deadline (host sleep, a paused VM) is
discarded. Before that, every laptop lid-close or VM pause longer than the
deadline aborted a perfectly healthy daemon on resume. The warnings leading up
to it read `tox_thread heartbeat stale for <N> ms (deadline <N> ms,
phase=<phase>); confirming wedge (<k>/5)`; `phase` (`idle`, `tox_iterate`,
`posted tasks`, `application callbacks`, `maintenance`) says where the Tox
thread is stuck. On v0.4.x the line
has no `phase=` and a single over-deadline check aborts.

### Adaptive coalescing (opt-in)

```yaml
tunnel:
  coalesce_mode: adaptive      # default fixed (v0.3.0); flip to adaptive
                                # only after one release of soak
```

### BDP flow control (default since v0.4.1)

```yaml
flow_control:
  mode: bdp                    # default; `fixed` locks the v0.3.0 256 KiB window
  send_window_min_bytes: 32768 # v0.5.0 default; never below 32 KiB (65536 before)
  send_window_max_bytes: 4194304
  safety_factor_x100: 150
  fixed_window_bytes: 262144
```

From v0.5.0 each tunnel starts at `fixed_window_bytes` and sizes its window as
`bandwidth × (min RTT + 50 ms) × safety_factor_x100 / 100`, clamped to
`[min, max]`. RTT is measured per byte range (DATA handed to toxcore until the
peer's ACK covers it) and the window uses the minimum of the last ~10 s, taken
only from samples sent with little in flight. Bandwidth (since v0.5.1) is a
BBR-style delivery rate: bytes delivered since a sample was sent, over the time
since the delivery before it, so bunched ACKs cannot read as a rate above what was
really delivered. A send that starts with nothing in flight begins a fresh
measurement (an idle gap is not counted as slow delivery), and a sample sent while
the application had nothing queued and the window still had room for another full
frame may only raise the estimate; with the window full, a quiet application's
samples still count normally. Consequences worth telling an operator:

- The seed is no longer a floor: on a slow or relayed path the window shrinks
  toward 32 KiB, so a bulk transfer stops parking tens of seconds of data in
  toxcore's per-friend queue ahead of every other tunnel and control frame.
  The queue it can build is about min RTT / 2 + 75 ms of data, or the 32 KiB
  floor's worth on paths slower than ~440 KB/s.
- `send_window_min_bytes` is clamped up to 32 KiB (the receiver ACKs every
  16 KiB, so a smaller window would stall). A pre-v0.5.0 config that set 65536
  explicitly still works; it just keeps a 64 KiB floor.
- A sustained transfer dips to the floor for a round trip or two about every
  10 s to re-measure the path (like BBR's ProbeRTT). That periodic dip in
  `toxtunnel_tunnel_send_window_bytes` is expected, not a fault.

### Per-friend rate limiting (opt-in)

In `rules.yaml`:

```yaml
rate_limit_defaults:
  mode: report                 # start shadow; flip to enforce once tuned
  open_per_sec: 10
  open_burst: 50
  max_concurrent_tunnels: 100
  bytes_per_sec: 1048576       # inbound TUNNEL_DATA payload, bytes/sec
  bytes_burst: 4194304         # BOTH byte keys must be non-zero to engage

rules:
  - friend: "...64hex..."
    rate_limit:
      # A per-friend block OVERRIDES ONLY the fields it names; everything else
      # is inherited from rate_limit_defaults above (including `mode`). An
      # explicit 0 means "no limit for this friend on that field".
      max_concurrent_tunnels: 200
      bytes_per_sec: 262144
      bytes_burst: 1048576
    allow:
      - host: "127.0.0.1"
        ports: [22]
```

#### Byte budgets: what `bytes_per_sec` / `bytes_burst` actually do

Implemented since **v0.4.11**. Earlier v0.4.x releases parsed these keys and
never consulted them, so a rules file carried over from one of those will start
shaping traffic on the first restart after upgrading — check the value is one
you want before rolling it out.

- **Direction.** It meters the payload of **inbound `TUNNEL_DATA` frames from
  that friend**, per friend, summed across all of that friend's tunnels. Same
  direction `open_per_sec` guards: a server's `rules.yaml` describes what a peer
  may do *to it*. Traffic the server sends back is **not** metered by this key.
  If the operator wants to cap what this host *transmits*, say so plainly and
  point at an OS-level shaper (`tc` on Linux, `pf`/`dnctl` on macOS) — nothing
  in `rules.yaml` does that.
- **`report`** accounts and increments
  `toxtunnel_rate_limit_bytes_throttled_total` while nothing is delayed. This is
  the "measure before you enforce" mode; size the budget here first. A limit
  that never moves the counter is not binding; one that moves it constantly is
  tighter than the link.
- **`enforce`** does not drop and does not close the tunnel. Dropping a
  `TUNNEL_DATA` frame would punch a hole in a lossless byte stream that neither
  end can detect. Instead the server **defers** the frame into a per-friend FIFO
  and replays it, in arrival order, as the bucket refills. Every byte arrives —
  just later.
- **Why the queue does not grow without bound.** A deferred frame never reaches
  its tunnel, so no `TUNNEL_ACK` is emitted for it, so the peer's send window
  fills and the peer stops sending. The throttle propagates back to the origin
  TCP socket instead of being absorbed by local memory.
- **Ordering.** Total for tunnel-lifecycle frames (`TUNNEL_OPEN`, `DATA`,
  `CLOSE`, `ERROR`, resume opcodes) — a `TUNNEL_CLOSE` that overtook deferred
  data would strand it. `PING` / `PONG` (keepalive, or a healthy peer gets
  declared dead), `TUNNEL_ACK` (window credit for the *other* direction) and
  `INFO_REQUEST` / `INFO_REPLY` deliberately bypass the queue.
- **The limitation to state up front.** A receiver-side deferral cannot hold an
  average rate against a peer that ignores flow control; against such a peer it
  degrades to bursts capped by a 32 MiB per-friend memory rail. Both that rail
  and a per-frame release deadline (derived from the reaper timeouts, ≤ 60 s)
  fail **open**: the backlog is released early, in order, with a `warn` line —
  the budget is briefly exceeded, nothing is lost. So this is a bandwidth budget
  for cooperative peers, not a defence against a hostile one.
  `max_concurrent_tunnels` and `open_per_sec` are the anti-DoS knobs.
- **Engaging it.** Both keys must be non-zero — a refill rate with no capacity
  holds no tokens. `bytes_burst: 0` is the way to exempt a friend; a non-zero
  value below 65535 is raised to 65535, and both fields are clamped to 1 GB/s.
  The daemon enforces the clamped values, not the numbers in the file, and it
  does not echo them anywhere — `toxtunnel inspect` carries no rate-limit
  state at all, so do the arithmetic yourself rather than expecting the daemon
  to confirm it. (`docs/CONFIGURATION.md` claims `inspect` reports the clamped
  budget; as of v0.4.11 it does not.)

Log lines worth knowing:

```
Inbound byte throttle engaged for friend <N> (rate_limit.bytes_per_sec)
Inbound byte throttle engaged|disengaged for friend <N>        # after a reload
Friend <N> reached the inbound throttle backlog rail (<B> bytes deferred); ...
Friend <N>: a deferred frame reached its release deadline ...
```

### Tunnel resume (opt-in, live in v0.4.x)

```yaml
tunnel:
  resume:
    enabled: false             # opt-in; default off. Live in v0.4.x: opcodes
                                # 0x08 / 0x09 are wire-active only when enabled.
    max_age_seconds: 300        # in-memory hold window (see below)
    on_gap: passthrough
```

**What `max_age_seconds` actually governs:** when a friend disconnects, the
server keeps that friend's `TunnelManager` — its tunnels *and* their live target
TCP connections — parked in memory behind a timer of this length, logged as
`Holding tunnel manager for friend N for resume (up to Ns)`. If the friend
reconnects inside the window, `TUNNEL_RESUME_REQUEST` reattaches to those live
objects. If the timer expires first, the manager is dropped and every held
tunnel closed. It is **not** a pruning window over persisted entries.

**Nothing about resume is written to disk.** There is no on-disk resume state,
which is exactly why the feature cannot survive a process restart on either side
— a restart destroys the held sockets along with the process. Live-reconnect
only. If a user wants an SSH session to survive a server restart, no ToxTunnel
setting delivers that; point them at `tmux`/`screen` or `mosh` instead.

## v0.5.0 additions

### Hosts whose only egress is a proxy (`tox.proxy`)

```yaml
tox:
  udp_enabled: false           # optional: toxcore turns UDP off for a proxy anyway
  proxy:
    type: socks5               # none (default) | http | socks5
    host: 127.0.0.1            # IP or DNS name (resolved locally)
    port: 7890
  bootstrap_nodes:             # pin them by IP (see below)
    - address: 144.172.88.203
      port: 33445
      public_key: "2016A0F2797EE3A8B004BA623F11AAFC8146F1B8F45107232A1A1AECCE856674"
```

- The startup log confirms it: `Tox traffic goes through SOCKS5 proxy
  127.0.0.1:7890 (TCP relays only; toxcore disables UDP for a proxied node)`.
- **No UDP.** toxcore cannot proxy UDP, so a proxied node reaches peers only
  through TCP relays: expect relay throughput (SSH / DB grade, not bulk).
- **Pin `bootstrap_nodes` by IP.** The public node-list fetch in `bootstrap_mode:
  auto` runs `curl` without the proxy, and node addresses resolve locally.
- `bootstrap_mode: lan` with a proxy is rejected at startup. Not reloadable.

### Bootstrapping from another ToxTunnel daemon (private networks)

When one side cannot reach the public DHT but can reach another daemon directly
(VPN, overlay, LAN segment — or a proxied node that can reach one), pin that
daemon as a bootstrap node. Read its DHT identity:

```bash
toxtunnel inspect status --json -c <its config> | jq '{dht_public_key, udp_port, tcp_relay_port}'
# udp_port / tcp_relay_port are omitted when zero (jq shows null): a proxied node
# has no UDP port, and a client normally runs no TCP relay.
# or its startup line:
#   DHT node key: 6F2C…E1A0 (UDP port 34510, TCP relay port 34511; changes on every restart)
```

```yaml
tox:
  bootstrap_nodes:
    - {address: 10.0.0.5, port: 34510, public_key: "6F2C…E1A0"}   # UDP DHT
    - {address: 10.0.0.5, port: 34511, public_key: "6F2C…E1A0"}   # TCP relay (servers)
```

- `dht_public_key` is **not** the Tox ID, and it **changes every time that
  daemon restarts** — after a restart, regenerate the pinned entries. Keep at
  least one public node in the list as well.
- Pin that daemon's ports with `tox.udp_port` (new in v0.5.0; `0` = toxcore's
  33445..33545 walk) and `tox.tcp_port`, so only the key moves.

### Client open timing: `open_timeout_seconds` and `offline_open_wait_seconds`

```yaml
tunnel:
  open_timeout_seconds: 30         # default; 0 = wait forever (pre-v0.5.0)
  offline_open_wait_seconds: 10    # default; 0 = close at once (pre-v0.5.0)
```

- **`open_timeout_seconds`** closes a tunnel whose TUNNEL_OPEN got no OPEN_ACK in
  time (`Tunnel N open timed out after 30s with no OPEN_ACK from the peer;
  closing`), booked as `tunnels_opened_total{result="failed"}`. Before v0.5.0
  the application hung in `Connecting` indefinitely.
- **`offline_open_wait_seconds`** holds a forward connection accepted while the
  server is offline (start-up, a brief link drop) — unread, at most 64 — and
  opens it when the server comes back (`TCP connection accepted on port P while the server is offline; holding it
  for up to 10s (N held)` → `Server online; opening N held connection(s)`, or `Held
  connection on port P timed out after 10s waiting for the server; closing`).
  Forward rules only; SOCKS5 / HTTP CONNECT still fail at once. The default is
  shorter than `failover.timeout_seconds` (60): with failover configured, raise
  it past that if a connection made while the primary is down should wait for
  the fallback.

### Behaviour changes to know when upgrading to v0.5.0

- **Abnormal ends are resets.** When the target resets the connection after the
  tunnel is up, the client resets its local socket too (the application sees
  ECONNRESET, not a clean EOF), and the client logs `Tunnel N received
  TUNNEL_ERROR: code=4, desc='target connection ended abnormally: …'` (the
  server: `Tunnel N sent error: code=4, …`). A declined resume ends the
  tunnel the same way.
- **Keepalive is less trigger-happy and recovers by itself.** With
  `keepalive_interval_seconds` set, any inbound frame now counts as life (not
  only a PONG, which can queue behind bulk data), probing continues after a dead
  verdict, and the first sign of life restores the server. Before v0.5.0 a slow
  link could get a peer declared dead mid-transfer, and a verdict over a link
  that never dropped stayed permanent.
- **Bootstrap retries.** While not DHT-connected the daemon re-contacts its node
  list on a 10 s–5 min backoff (`Bootstrap retry N: contacted X/Y node(s)`) and
  re-fetches the public list when it has none. `inspect status` reports
  `dht_connected`; `/metrics` exports `toxtunnel_dht_connected`.
- **`--version` on a source build** reports `git describe` (e.g.
  `0.5.1-3-gabc1234`); packages report the plain release number.
