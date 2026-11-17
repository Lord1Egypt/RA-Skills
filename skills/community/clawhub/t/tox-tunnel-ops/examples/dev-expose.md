# Dev/Test Server Exposure via ToxTunnel

## Scenario

You're running a development server locally (Next.js, Django, Flask, Rails, etc.) and want a teammate or tester to access it from their machine — without deploying to a staging server.

## Topology

```
Tester's Machine (client)             Your Dev Machine (server)
─────────────────────────             ──────────────────────────
Browser → 127.0.0.1:8080             dev server on :3000
        ↓                                    ↑
  toxtunnel client                    toxtunnel server
        ↓                                    ↑
        └──── Tox P2P encrypted tunnel ──────┘
```

## Security Warning

Development servers typically:
- Have no authentication
- Expose debug endpoints, stack traces, and source maps
- May have hot-reload websocket endpoints
- Run with elevated permissions

**Recommendations:**
- Use a specific friend key in rules (not wide open)
- Only keep the tunnel running during the testing session
- Don't expose `.env` or admin routes
- Consider adding basic auth (e.g., nginx proxy) in front of the dev server

## Server Config (your dev machine)

```yaml
mode: server
data_dir: ~/.config/toxtunnel/dev-expose
logging:
  level: info
tox:
  udp_enabled: true
  bootstrap_mode: auto    # or lan if both are in the same office
server:
  rules_file: ~/.config/toxtunnel/dev-expose/rules.yaml
```

> **`rules_file` must be an absolute path.** ToxTunnel expands `~` and nothing
> else, then hands the string to the rules loader, so a relative path resolves
> against the **daemon's working directory** — not this config's directory.
> Starting the daemon from anywhere else dies with
> `Failed to load rules file: Rules file not found: rules.yaml`. Verified on
> v0.4.12.


## Client Config (tester's machine)

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
      remote_port: 3000
```

> ### ⚠️ `local_port: 8080` binds `0.0.0.0` without `local_address` (pre-v0.5.0) on the tester's machine
>
> Before v0.5.0, without `local_address` the listener binds every IPv4
> interface. Combined with the warning above — dev servers have no auth and
> expose debug endpoints — this means anyone on the tester's network reaches your
> dev server, not just the tester. On **v0.4.13+** set `local_address: 127.0.0.1` (the config above does); on v0.4.12 and older no such key exists — firewall it instead.
>
> Have the tester firewall the port to loopback, or use the SOCKS5 alternative
> below, whose listener is validated loopback-only.

## Rules (tester's friend key only)

```yaml
rules:
  - friend: "AABBCCDD...tester-64-char-hex-public-key...EEFF"
    allow:
      - host: "127.0.0.1"
        ports: [3000]
```

> The `friend` value is the **first 64 hex characters** of that peer's 76-char Tox ID
> (from its `Client Tox ID: …` startup log line, or `toxtunnel print-id -c client.yaml`),
> not the whole ID. A wrong length is rejected when the rules file loads
> (`Invalid public key length: expected 64`).

## Steps

1. Start your dev server as usual: `npm run dev` (or equivalent)
2. Start toxtunnel server: `toxtunnel -m server -c server.yaml`
3. Share your Tox ID with the tester
4. Tester starts client and accesses `http://127.0.0.1:8080`

## LAN Shortcut

If both developers are in the same office:

```yaml
tox:
  bootstrap_mode: lan    # no internet needed, faster connection
```

## Alternative: SOCKS5 listener for a moving target

If you're not exposing one dev server but a *set* of internal endpoints that
keeps changing (multiple services, ad-hoc curl, debugger probes), skip the
per-port `forwards` and enable a loopback SOCKS5 listener on the tester's
client instead. The server's `rules.yaml` still gates which destinations
succeed, so the trust boundary doesn't move:

```yaml
# tester's client.yaml
client:
  server_id: <PASTE_SERVER_TOX_ID_HERE>
  socks5:
    enabled: true
    listen: 127.0.0.1:1080     # MUST be loopback; validator rejects 0.0.0.0
```

```bash
# Tester uses it from any tool that speaks SOCKS5 / HTTP CONNECT:
curl --socks5-hostname 127.0.0.1:1080 http://internal.lan:3000/
ALL_PROXY=socks5h://127.0.0.1:1080 npm test
# Firefox: SOCKS host 127.0.0.1, port 1080, "Proxy DNS when using SOCKS v5"
```

Server-side `rules.yaml` must still allow every host:port the tester needs to
reach — keep the allowlist scoped to the tester's friend key.

## Cleanup

When testing is done:

1. Stop the toxtunnel server. In order of preference:

   ```bash
   # Best: the daemon publishes its own pid (v0.4.11+)
   kill "$(cat ~/.config/toxtunnel/dev-expose/toxtunnel.pid)"

   # Or Ctrl+C in the terminal running it.

   # Acceptable when you know it is the only instance:
   pkill -x toxtunnel
   ```

   **Never `pkill -f "toxtunnel.*server"`.** `-f` matches the whole command line,
   so it also matches the shell, CI step or SSH wrapper whose command line
   happens to mention toxtunnel — including the very command you typed — and it
   will kill unrelated toxtunnel instances (your long-lived client, another
   project's server) alongside the one you meant.

2. Optionally delete the config files. **Think before deleting the data
   directory**: it holds `tox_save.dat`, so removing it discards this server's
   Tox identity, and every tester's `client.yaml` and `known_servers.yaml` entry
   becomes stale. Keep it if you expect to run this again.
3. No persistent service to clean up (unless you set one up)

## Multiple Testers

Add each tester as a separate friend rule:

```yaml
rules:
  - friend: "AAAA...64hex..."    # Tester 1
    allow:
      - host: "127.0.0.1"
        ports: [3000]
  - friend: "BBBB...64hex..."    # Tester 2
    allow:
      - host: "127.0.0.1"
        ports: [3000]
```

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
