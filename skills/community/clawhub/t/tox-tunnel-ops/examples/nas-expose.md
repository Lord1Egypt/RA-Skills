# NAS / HomeLab Exposure via ToxTunnel

## Scenario

You have a NAS (Synology, QNAP, TrueNAS, or DIY) or HomeLab server on your home network and want to access its web UI, SSH, and file sharing from outside — without opening ports on your router.

## Topology

```
Your Laptop (client)                  Home NAS (server)
───────────────────                   ─────────────────
Browser → 127.0.0.1:8080             Web UI on :5000
SSH    → 127.0.0.1:2222              SSH on :22
SMB    → 127.0.0.1:4450              SMB on :445
        ↓                                    ↑
  toxtunnel client                    toxtunnel server
        ↓                                    ↑
        └──── Tox P2P encrypted tunnel ──────┘
```

## Server Config (on the NAS or a LAN companion machine)

```yaml
mode: server
data_dir: /volume1/toxtunnel/data    # Synology example path
logging:
  level: info
tox:
  udp_enabled: true
  bootstrap_mode: auto
server:
  rules_file: /volume1/toxtunnel/rules.yaml
```

### Two topologies — pick one and be consistent

**(A) Server runs ON the NAS.** `remote_host: 127.0.0.1` throughout, and the
rules allow `127.0.0.1`. This is the configuration shown below.

**(B) Server runs on a LAN companion machine** (an ARM NAS with no compatible
binary, a Raspberry Pi, etc.). Then `127.0.0.1` on the server side means *the
companion*, not the NAS — so **every** target must change, not just one:

- **All three `remote_host` values** in the client config become the NAS IP
  (e.g. `192.168.1.100`), not just the web UI. Leaving SSH and SMB on
  `127.0.0.1` silently forwards them to the companion's own sshd and SMB (or
  nothing at all), which looks like a broken tunnel but is a misdirected one.
- **The rules `host:` must change too.** `host: "127.0.0.1"` does not match a
  target of `192.168.1.100`, so every open is denied by default-deny. Use
  `host: "192.168.1.100"` with the same explicit port list.

Concretely, for topology (B) the client forwards become
`remote_host: 192.168.1.100` on all three entries, and the rule becomes:

```yaml
rules:
  - friend: "AABBCCDD...your-64-char-hex-public-key...EEFF"
    allow:
      - host: "192.168.1.100"      # the NAS, as seen from the companion
        ports: [5000, 22, 445]
```

Do not widen this to `192.168.*` to make it work — that grants the peer every
host on your home LAN. Name the NAS.

## Client Config (on your laptop)

```yaml
mode: client
data_dir: ~/.config/toxtunnel/client
logging:
  level: info
tox:
  udp_enabled: true
  bootstrap_mode: auto
client:
  server_id: <PASTE_SERVER_TOX_ID_HERE>
  forwards:
    - local_port: 8080
      local_address: 127.0.0.1
      remote_host: 127.0.0.1       # or NAS IP like 192.168.1.100
      remote_port: 5000             # Synology DSM default
    - local_port: 2222
      local_address: 127.0.0.1
      remote_host: 127.0.0.1
      remote_port: 22
    - local_port: 4450
      local_address: 127.0.0.1
      remote_host: 127.0.0.1
      remote_port: 445
```

> ### ⚠️ Every forward here binds `0.0.0.0` without `local_address` (pre-v0.5.0)
>
> Before v0.5.0, without `local_address` a forward has no bind restriction — Ports 8080, 2222 and 4450 all
> bind every IPv4 interface on the laptop, so any host on the network the laptop
> happens to be on reaches your NAS web UI, SSH and SMB. On v0.4.13+ the
> `local_address: 127.0.0.1` lines above prevent that; on v0.4.12 and older
> firewall all three to loopback, especially on public Wi-Fi.

## Rules (scoped to your own friend key)

```yaml
rules:
  - friend: "AABBCCDD...your-64-char-hex-public-key...EEFF"
    allow:
      - host: "127.0.0.1"
        ports: [5000, 22, 445]
```

Note: The `friend` value is the **first 64 hex characters** of the peer's 76-char Tox ID — not the whole ID. They get it from their own daemon's startup log line `Client Tox ID: <76 hex>`, or from `toxtunnel print-id -c client.yaml`. A wrong length is rejected when the rules file loads (`Invalid public key length: expected 64`), so the server refuses to start or hot-reload rather than silently denying.

## Steps

1. Install toxtunnel on the NAS (or a LAN companion machine)
2. Start server: `toxtunnel -m server -c server.yaml`
3. Copy Tox ID → paste into client config
4. Start client: `toxtunnel -m client -c client.yaml`
5. Access:
   - Web UI: open `http://127.0.0.1:8080` in browser
   - SSH: `ssh -p 2222 admin@127.0.0.1`
   - SMB: see notes below

## Platform Notes

- **HTTPS**: If the NAS serves HTTPS on port 5001, forward that port instead. The tunnel is transparent to TLS.
- **macOS SMB**: macOS may not connect to SMB on non-standard ports easily. Alternative: use SSHFS: `sshfs -p 2222 admin@127.0.0.1:/volume1 ~/nas-mount`
- **Windows SMB**: Windows UNC paths (`\\host\share`) don't support non-standard ports. Workaround: use `netsh interface portproxy add v4tov4 listenport=445 listenaddress=127.0.0.2 connectport=4450 connectaddress=127.0.0.1` then access `\\127.0.0.2\share`
- **Persistence**: Set up toxtunnel as a systemd service (Linux NAS), Synology Task Scheduler, or launchd plist (macOS) for auto-start.

## Auto-Start (systemd example for Linux NAS)

A unit with no `User=` runs **as root** — which for an internet-reachable
gateway daemon is exactly what you do not want. Nothing here needs root: the Tox
port is 33445 and the targets are ordinary services. Create a dedicated account
and let systemd own the state directory:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin toxtunnel
```

```ini
[Unit]
Description=ToxTunnel Server
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/local/bin/toxtunnel -m server -c /etc/toxtunnel/server.yaml --service
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5
RemainAfterExit=yes

# Do not run as root. StateDirectory creates and chowns /var/lib/toxtunnel to
# this account — point `data_dir` there, and keep /etc/toxtunnel config-only.
User=toxtunnel
Group=toxtunnel
StateDirectory=toxtunnel
StateDirectoryMode=0750

[Install]
WantedBy=multi-user.target
```

Then set `data_dir: /var/lib/toxtunnel` in `server.yaml`, and make sure
`rules_file` is an **absolute** path — a relative one resolves against the
daemon's working directory, which under systemd is not the config's directory,
and startup fails with `Rules file not found`.

On a Synology this maps to a Task Scheduler entry rather than a systemd unit;
the same rule applies — run it as a non-root user that owns `data_dir`.

## Verification

```bash
bash scripts/verify.sh 8080 http client.yaml
bash scripts/verify.sh 2222 ssh  client.yaml
```

Run this from the skill root (the script lives at `scripts/verify.sh`).
Passing the client config lets it read `friends_online` from the running
daemon instead of guessing from a local TCP accept.

**Judge it by the exit code:** `0` = the remote service answered through the
tunnel, `2` = local checks passed but end-to-end was **not** proven (do not
report this as working), `1` = a check failed.
