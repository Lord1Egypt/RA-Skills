# SOCKS5 / HTTP CONNECT Browser Proxy via ToxTunnel

## Scenario

You have a homelab / corporate network behind a server running ToxTunnel and
want to **browse arbitrary internal hosts** from your laptop — internal HTTP
admin UIs, multiple Grafana / Prometheus / GitLab instances, ad-hoc curl to
private services — **without enumerating every destination** in
`client.forwards`. SOCKS5 makes the client a dynamic egress; the server-side
`rules.yaml` is still the only thing that decides what's reachable.

## Topology

```
Your Laptop (client)                      Homelab Server (server)
─────────────────────────                 ─────────────────────────
Browser/curl → 127.0.0.1:1080  ─────┐
(SOCKS5 / HTTP CONNECT)             │
                                    ▼
                            toxtunnel client
                                    │
                                    │ (Tox P2P encrypted)
                                    ▼
                            toxtunnel server
                                    │
                                    ▼
                   internal.lan, grafana.lan, gitlab.lan, ...
```

## Key Principles

- **Loopback bind only.** `socks5.listen` MUST be `127.0.0.1:<port>`,
  `[::1]:<port>`, or `localhost:<port>`. The config validator rejects anything
  else, including `0.0.0.0` and LAN IPs. SOCKS5 has no auth — binding off
  loopback would hand any LAN host the same access as the local user.
- **Server is the trust boundary.** The client doesn't decide what's
  reachable; `rules.yaml` on the server does. Keep the allow list scoped.
- **DNS resolution.** Use `socks5h://` / `--socks5-hostname` so DNS happens on
  the server side; otherwise the client tries to resolve internal names
  locally and fails.
- **Mutually exclusive with `pipe`.** Don't enable both; the validator errors.

## Server Config

```yaml
mode: server
data_dir: /etc/toxtunnel/server
logging:
  level: info
  file: /var/log/toxtunnel/server.log
tox:
  udp_enabled: true
  bootstrap_mode: auto
server:
  rules_file: /etc/toxtunnel/rules.yaml
```

## Server Rules (the actual trust boundary)

```yaml
rules:
  # You (the laptop) — explicit internal destinations only
  - friend: "AABBCCDD...your-laptop-64-char-hex-public-key...EEFF"
    allow:
      - host: "grafana.internal.lan"
        ports: [3000]
      - host: "gitlab.internal.lan"
        ports: [80, 443]
      - host: "prometheus.internal.lan"
        ports: [9090]
      - host: "10.20.30.40"
        ports: [22, 80, 443]
```

Even though the *client* can dial any host:port via SOCKS5, the server denies
anything not in this list and the SOCKS5 listener returns reply code 0x02
("connection not allowed by ruleset").

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
  server_id: <PASTE_SERVER_TOX_ID_HERE>     # or a known-servers alias
  socks5:
    enabled: true
    listen: 127.0.0.1:1080                  # loopback only
  # `forwards` and `pipe` are not needed when only SOCKS5 is in use.
```

CLI-flag alternative (no YAML edit):

```bash
toxtunnel -m client --server-id homelab --socks5 127.0.0.1:1080
```

## Steps

1. Start server: `sudo systemctl start toxtunnel` (or `toxtunnel -m server -c server.yaml`)
2. Note the server's Tox ID (`toxtunnel print-id --data-dir /etc/toxtunnel/server` on the server, or the ID printed at startup)
3. Paste into client config, start client: `toxtunnel -m client -c client.yaml`
4. Wait for `Friend connection status: Connected` in the client log
5. Point your tool at `127.0.0.1:1080`

## Using It

```bash
# curl over SOCKS5 with server-side DNS resolution
curl --socks5-hostname 127.0.0.1:1080 http://grafana.internal.lan:3000/

# Env vars for any HTTP client that respects them
export ALL_PROXY=socks5h://127.0.0.1:1080
export HTTPS_PROXY=socks5h://127.0.0.1:1080
git clone http://gitlab.internal.lan/repo.git

# HTTP CONNECT (same listener auto-detects the protocol)
https_proxy=http://127.0.0.1:1080 curl https://gitlab.internal.lan/

# Firefox: Settings -> Network Settings -> Manual proxy configuration
#   SOCKS Host: 127.0.0.1   Port: 1080   SOCKS v5
#   Check "Proxy DNS when using SOCKS v5"

# Chrome / Chromium (per-profile flag)
chromium --proxy-server="socks5://127.0.0.1:1080"
```

## Verification

```bash
# 1. SOCKS5 listener is up?
nc -z -w 2 127.0.0.1 1080 && echo "listener up"

# 2. Friend connectivity?
toxtunnel inspect status --json | jq '.friends_online'

# 3. End-to-end against an allowed destination
curl --socks5-hostname 127.0.0.1:1080 -sI http://grafana.internal.lan:3000/ | head -1

# 4. Confirm a *denied* destination fails as expected (SOCKS5 reply 0x02)
curl --socks5-hostname 127.0.0.1:1080 -v http://not-in-rules.lan/ 2>&1 | grep -i 'refused\|not allowed'
```

## Diagnostics

- Listener didn't bind → check log for `Invalid client.socks5.listen value` or
  `must bind to a loopback address`
- SOCKS5 CONNECT succeeds locally but fails immediately → server-side rules
  denied it (expected); add the host/port to `rules.yaml` and
  `toxtunnel reload` on the server
- DNS errors for internal hostnames → using `socks5://` instead of
  `socks5h://`; force server-side DNS

## Adding / Removing Allowed Destinations Live

The server's `rules.yaml` is hot-reloadable:

```bash
# On the server, after editing rules.yaml:
toxtunnel reload                                  # or kill -HUP $(pidof toxtunnel)
journalctl -u toxtunnel -n 5 | grep 'config reloaded'
```

No client restart needed — the next SOCKS5 CONNECT picks up the new rules.

## Cleanup

```bash
# Stop the listener
sudo systemctl stop toxtunnel               # service install
# or: kill $(pgrep -f 'toxtunnel.*client')  # direct process
```

Or simply set `client.socks5.enabled: false` and reload — but reloading
listen-address changes requires a restart, so flipping `enabled` cleanly is
restart-only.
