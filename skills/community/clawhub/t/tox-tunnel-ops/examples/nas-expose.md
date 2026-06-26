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

If the NAS cannot run toxtunnel directly (e.g., ARM NAS without a compatible binary), run the server on another machine on the same LAN and point `remote_host` to the NAS IP (e.g., `192.168.1.100`).

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
      remote_host: 127.0.0.1       # or NAS IP like 192.168.1.100
      remote_port: 5000             # Synology DSM default
    - local_port: 2222
      remote_host: 127.0.0.1
      remote_port: 22
    - local_port: 4450
      remote_host: 127.0.0.1
      remote_port: 445
```

## Rules (scoped to your own friend key)

```yaml
rules:
  - friend: "AABBCCDD...your-64-char-hex-public-key...EEFF"
    allow:
      - host: "127.0.0.1"
        ports: [5000, 22, 445]
```

Note: Replace with your actual 64-character hex public key from the client's toxtunnel startup log.

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

```ini
[Unit]
Description=ToxTunnel Server
After=network-online.target

[Service]
ExecStart=/usr/local/bin/toxtunnel -m server -c /etc/toxtunnel/server.yaml
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## Verification

```bash
bash verify.sh 8080 http
bash verify.sh 2222 ssh
```
