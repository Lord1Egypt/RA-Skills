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
data_dir: /var/lib/toxtunnel        # mutable state — NOT under /etc
logging:
  level: info
  file: /var/log/toxtunnel/server.log
tox:
  udp_enabled: true
  bootstrap_mode: auto
server:
  rules_file: /etc/toxtunnel/rules.yaml
```

> **`data_dir` holds mutable state, so keep it out of `/etc`.** That directory
> carries the Tox identity (`tox_save.dat`), the pid file, the data-directory
> lock and the inspect socket — all written at runtime. `/var/lib/toxtunnel` is
> what the packaged Linux unit uses (`StateDirectory=toxtunnel`,
> `StateDirectoryMode=0750`), owned by the dedicated `toxtunnel` user; macOS
> equivalent is `/usr/local/var/toxtunnel`. Keep `/etc/toxtunnel` for
> `server.yaml` and `rules.yaml` only.
>
> **Run the daemon as that unprivileged account, not as root.** Nothing here
> needs root once the package is installed: the Tox port is 33445 and the targets
> are ordinary services. The packaged unit already does this; a hand-written one
> must set `User=`, `Group=` and `StateDirectory=` itself.


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

> The `friend` value is the **first 64 hex characters** of that peer's 76-char Tox ID
> (from its `Client Tox ID: …` startup log line, or `toxtunnel print-id -c client.yaml`),
> not the whole ID. A wrong length is rejected when the rules file loads
> (`Invalid public key length: expected 64`).

Even though the *client* can dial any host:port via SOCKS5, the server denies
anything not in this list and the SOCKS5 listener returns reply code 0x02
("connection not allowed by ruleset") — or `403 Forbidden` if the client came
in over HTTP CONNECT. The same 0x02 covers the other server-side policy
rejections, the rate limiter and the concurrent-tunnel cap. A target that was
*allowed* but unreachable answers differently (`0x04` / `0x05` / `0x01`, all
`502 Bad Gateway` over HTTP CONNECT), so the reply distinguishes "the server
said no" from "the server couldn't get there".

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
2. Note the server's Tox ID (`toxtunnel print-id -c /etc/toxtunnel/server.yaml` on
   the server, which resolves the same `data_dir` the daemon uses, or read the ID
   printed at startup)
3. Paste into client config, start client: `toxtunnel -m client -c client.yaml`
4. Wait for `Server friend 0 is now online` in the client log (on a Tox relay
   path this can take minutes, not seconds)
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
# On the server, after editing rules.yaml. Pass -c (or -d) so reload finds the
# right daemon: bare `toxtunnel reload` looks in the DEFAULT data_dir
# (~/.config/toxtunnel), which is not where this server keeps its pid file.
toxtunnel reload -c /etc/toxtunnel/server.yaml
# Equivalent, explicit:
kill -HUP "$(cat /var/lib/toxtunnel/toxtunnel.pid)"

journalctl -u toxtunnel -n 5 | grep 'config reloaded'
```

**Do not use `kill -HUP $(pidof toxtunnel)`.** `pidof` returns *every* toxtunnel
process on the host, so on a machine also running a client you would signal both.
The pid file names exactly one daemon.

No client restart needed — the next SOCKS5 CONNECT picks up the new rules.

## Cleanup

```bash
# Stop the listener
sudo systemctl stop toxtunnel               # service install
# or: kill "$(cat <client data_dir>/toxtunnel.pid)"   # direct process
# (avoid `pkill -f toxtunnel…` — it also matches the shell that runs it)
```

Turning the listener off is **restart-only**: `client.socks5` is outside the
reloadable subset, so editing it and sending SIGHUP makes the daemon reject the
whole reload (`field 'client.socks5' requires a restart`) and keep serving the
old config. Set `client.socks5.enabled: false` and restart the client.
