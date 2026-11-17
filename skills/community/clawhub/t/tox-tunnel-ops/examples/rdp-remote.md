# Remote Desktop (RDP/VNC) via ToxTunnel

## Scenario

You want to access a Windows machine via RDP or a Linux desktop via VNC from anywhere, without exposing desktop ports to the internet.

## Topology (RDP)

```
Your Laptop (client)                  Windows Machine (server)
───────────────────                   ──────────────────────────
RDP client → 127.0.0.1:13389         RDP on :3389
        ↓                                    ↑
  toxtunnel client                    toxtunnel server
        ↓                                    ↑
        └──── Tox P2P encrypted tunnel ──────┘
```

## Server Config (on the Windows machine or a Linux gateway)

```yaml
mode: server
data_dir: ~/.config/toxtunnel/server    # or %APPDATA%\toxtunnel\server on Windows
logging:
  level: info
tox:
  udp_enabled: true
  bootstrap_mode: auto
server:
  rules_file: ~/.config/toxtunnel/server/rules.yaml
```

> **`rules_file` must be an absolute path.** ToxTunnel expands `~` and nothing
> else, then hands the string to the rules loader, so a relative path resolves
> against the **daemon's working directory** — not this config's directory.
> Starting the daemon from anywhere else dies with
> `Failed to load rules file: Rules file not found: rules.yaml`. Verified on
> v0.4.12.


## Client Config

**RDP (Windows Remote Desktop):**
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
    - local_port: 13389
      local_address: 127.0.0.1
      remote_host: 127.0.0.1
      remote_port: 3389
```

**VNC (Linux Desktop):**
```yaml
client:
  server_id: <PASTE_SERVER_TOX_ID_HERE>
  forwards:
    - local_port: 15900
      local_address: 127.0.0.1
      remote_host: 127.0.0.1
      remote_port: 5900            # VNC default
```

> ### ⚠️ `local_port: 13389` binds `0.0.0.0` without `local_address` (pre-v0.5.0)
>
> Before v0.5.0, without `local_address` a forward has no bind restriction — the listener binds the IPv4
> wildcard, so every host on your network can reach the remote desktop through
> this port, with only RDP's own authentication in front of it. On **v0.4.13+**
> set `local_address: 127.0.0.1` (the config above does). On v0.4.12 and older
> no bind key exists.
>
> Firewall it to loopback (`ufw deny in to any port 13389`, an nftables/pf rule,
> or `New-NetFirewallRule … -Action Block`) before leaving the tunnel up on an
> untrusted network.

## Rules

```yaml
rules:
  - friend: "AABBCCDD...your-64-char-hex-public-key...EEFF"
    allow:
      - host: "127.0.0.1"
        ports: [3389]              # or [5900] for VNC
```

> The `friend` value is the **first 64 hex characters** of that peer's 76-char Tox ID
> (from its `Client Tox ID: …` startup log line, or `toxtunnel print-id -c client.yaml`),
> not the whole ID. A wrong length is rejected when the rules file loads
> (`Invalid public key length: expected 64`).

## Steps

1. Ensure RDP is enabled on the Windows machine (Settings → System → Remote Desktop)
2. Start server: `toxtunnel -m server -c server.yaml`
3. Copy Tox ID → paste into client config
4. Start client: `toxtunnel -m client -c client.yaml`
5. Connect with RDP client to `127.0.0.1:13389`

## Connection Commands

**macOS:**
```bash
open "rdp://full%20address=s:127.0.0.1:13389"
# or use Microsoft Remote Desktop app
```

**Linux:**
```bash
xfreerdp /v:127.0.0.1:13389 /u:USERNAME
# or: rdesktop 127.0.0.1:13389
```

**Windows:**
```cmd
mstsc /v:127.0.0.1:13389
```

**VNC (cross-platform):**
```bash
# TigerVNC
vncviewer 127.0.0.1:15900
# or open in browser if using noVNC on the server
```

## Performance Notes

- RDP and VNC are bandwidth-heavy protocols. Performance depends on:
  - Whether Tox establishes a **direct UDP connection** (best) or uses a **TCP relay** (slower)
  - Network latency between the two machines
- Confirm which path you got with `toxtunnel servers list` (or
  `last_connection_type` in `known_servers.yaml`): `udp` = direct, `tcp` = Tox
  relay. RDP over a relay (~5–10 KB/s) is effectively unusable for a desktop
  session — expect to need direct UDP.
- For better performance over slow links:
  - RDP: reduce color depth, disable visual effects, enable compression
  - VNC: use Tight or ZRLE encoding, reduce resolution

## Verification

```bash
bash scripts/verify.sh 13389 rdp client.yaml
```

Run this from the skill root (the script lives at `scripts/verify.sh`).
Passing the client config lets it read `friends_online` from the running
daemon instead of guessing from a local TCP accept.

**Judge it by the exit code:** `0` = the remote service answered through the
tunnel, `2` = local checks passed but end-to-end was **not** proven (do not
report this as working), `1` = a check failed.
