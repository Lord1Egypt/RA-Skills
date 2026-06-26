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
  rules_file: rules.yaml
```

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
      remote_host: 127.0.0.1
      remote_port: 3000             # adjust to your web app's port
```

## Rules

```yaml
rules:
  - friend: "AABBCCDD...your-64-char-hex-public-key...EEFF"
    allow:
      - host: "127.0.0.1"
        ports: [3000]
```

## Multiple Web Services

Forward several services at once:

```yaml
client:
  server_id: <PASTE_SERVER_TOX_ID_HERE>
  forwards:
    - local_port: 8080
      remote_host: 127.0.0.1
      remote_port: 3000             # Main app (e.g., Next.js)
    - local_port: 8081
      remote_host: 127.0.0.1
      remote_port: 3001             # API server
    - local_port: 3030
      remote_host: 127.0.0.1
      remote_port: 3100             # Grafana (custom port)
    - local_port: 9090
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
bash verify.sh 8080 http
```
