# Web Service Forwarding via ToxTunnel

## Scenario

You have an internal web application (admin panel, Grafana dashboard, development server, etc.) running on a remote machine and want to access it from your local browser — without exposing it to the internet.

## Topology

```
Your Laptop (client)                  Remote Server (server)
───────────────────                   ───────────────────────
Browser → 127.0.0.1:8080             Web app on :80 or :3000
        ↓                                    ↑
  toxtunnel client                    toxtunnel server
        ↓                                    ↑
        └──── Tox P2P encrypted tunnel ──────┘
```

## Server Config

```yaml
mode: server
data_dir: ~/.config/toxtunnel/server
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
      remote_host: 127.0.0.1
      remote_port: 3000             # adjust to your web app's port
```

> ### ⚠️ `local_port: 8080` binds `0.0.0.0` without `local_address` (pre-v0.5.0)
>
> Before v0.5.0, without `local_address` a forward has no bind restriction: the client calls
> `TcpListener(io, 8080)`, which binds the IPv4 wildcard. Anyone on the same
> network reaches the internal web app through this port — and an admin panel or
> Grafana instance usually assumes it is behind something. On **v0.4.13+** set `local_address: 127.0.0.1` (the config above
> does). On v0.4.12 and older there is **no** such key — firewall it instead.
>
> Firewall the port to loopback (`ufw deny in to any port 8080`,
> `nft add rule inet filter input tcp dport 8080 iif != lo drop`, a pf `block in`
> rule, or `New-NetFirewallRule … -Action Block`), or use a loopback-only SOCKS5
> listener instead of a static forward.

## Rules

```yaml
rules:
  - friend: "AABBCCDD...your-64-char-hex-public-key...EEFF"
    allow:
      - host: "127.0.0.1"
        ports: [3000]
```

> The `friend` value is the **first 64 hex characters** of that peer's 76-char Tox ID
> (from its `Client Tox ID: …` startup log line, or `toxtunnel print-id -c client.yaml`),
> not the whole ID. A wrong length is rejected when the rules file loads
> (`Invalid public key length: expected 64`).

## Multiple Web Services

Forward several services at once:

```yaml
client:
  server_id: <PASTE_SERVER_TOX_ID_HERE>
  forwards:
    - local_port: 8080
      local_address: 127.0.0.1
      remote_host: 127.0.0.1
      remote_port: 3000             # Main app (e.g., Next.js)
    - local_port: 8081
      local_address: 127.0.0.1
      remote_host: 127.0.0.1
      remote_port: 3001             # API server
    - local_port: 3030
      local_address: 127.0.0.1
      remote_host: 127.0.0.1
      remote_port: 3100             # Grafana (custom port)
    - local_port: 9090
      local_address: 127.0.0.1
      remote_host: 127.0.0.1
      remote_port: 9090             # Prometheus
```

Update rules to match all ports:

```yaml
rules:
  - friend: "AABBCCDD...your-64-char-hex-public-key...EEFF"
    allow:
      - host: "127.0.0.1"
        ports: [3000, 3001, 3100, 9090]
```

## Steps

1. Start server: `toxtunnel -m server -c server.yaml`
2. Copy Tox ID → paste into client config
3. Start client: `toxtunnel -m client -c client.yaml`
4. Open browser: `http://127.0.0.1:8080`

## HTTPS Considerations

- **The tunnel is transparent to TLS.** If the backend serves HTTPS, forward the HTTPS port and access via `https://127.0.0.1:LOCAL_PORT`.
- **Certificate warnings** are expected since the certificate won't match `127.0.0.1`. Options:
  - Add `127.0.0.1 your-app.example.com` to `/etc/hosts` and access via the hostname
  - Use a self-signed cert that includes `127.0.0.1` as a SAN
  - Accept the warning for internal tools

## Common Web Applications

| Application | Default Port | Notes |
|-------------|-------------|-------|
| Grafana | 3000 | Dashboard access |
| Prometheus | 9090 | Metrics |
| Pi-hole | 80 | Admin at `/admin` |
| Home Assistant | 8123 | Smart home |
| Portainer | 9443 (HTTPS) | Container management |
| Webmin | 10000 | System admin |
| Jenkins | 8080 | CI/CD |
| GitLab | 80/443 | Source code |

## Verification

```bash
bash scripts/verify.sh 8080 http client.yaml
```

Run this from the skill root (the script lives at `scripts/verify.sh`).
Passing the client config lets it read `friends_online` from the running
daemon instead of guessing from a local TCP accept.

**Judge it by the exit code:** `0` = the remote service answered through the
tunnel, `2` = local checks passed but end-to-end was **not** proven (do not
report this as working), `1` = a check failed.
