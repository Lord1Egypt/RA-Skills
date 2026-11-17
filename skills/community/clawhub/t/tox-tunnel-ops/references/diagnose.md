# Diagnose Reference

Use this reference when an existing tunnel does not work and you need a layered,
evidence-driven troubleshooting flow.

## Diagnostic Layers

Run through these layers in order. Stop at the first failure and propose a fix.

### Layer 1: Process & Binary

- Is `toxtunnel` installed? (`which toxtunnel`)
- Is it running? (`ps aux | grep toxtunnel` / `Get-Process toxtunnel`)
- Which config file is it using? What mode?
- What version? (≥ v0.3.0 unlocks the inspect/reload/metrics short-circuits below)

**Prefer `inspect` over log tailing for live state.** If the daemon is up
and v0.3.0+, this single command answers Layers 1, 4, and 5 in one shot:

```bash
toxtunnel inspect status --json | jq .
toxtunnel inspect tunnels
```

Look for: `mode`, `version`, `friends_online`, `peer_online_seconds` (client),
`tunnels_active`, `bytes_in`, `bytes_out` — that is the complete field set.
`friends_online: 0` points at Layer 4; friends online with no tunnels points at
Layer 5. (There is no `active_server`, `pid` or `uptime` field, and `inspect`
takes only `tunnels` / `status`.)

### Layer 2: Configuration Static Check

**Start here, always:**

```bash
toxtunnel config check -c /path/to/config.yaml --strict
```

This is the daemon's own validator (v0.4.11+). Exit `0` = usable, `1` =
unloadable / invalid / (with `--strict`) carrying keys the daemon would silently
ignore. Anything it reports is authoritative — fix it before investigating
anything else, and do not hand-audit YAML that it has not seen.

Blind spots you must cover by hand (verified against v0.4.12; the alias one is
closed from v0.4.13):

1. **On v0.4.13 and older it never opens `server.rules_file`.** A server
   config pointing at a nonexistent or malformed rules file still prints
   `is valid`; rules problems surface only when the daemon loads them
   (Layer 3). **v0.5.0+ loads and parses the rules file**, so existence and
   syntax are covered there — the widening semantic leniencies (unknown keys
   ignored, missing `ports` = all ports, duplicate friends) still are not,
   on any version.
2. **On v0.4.12 and older it does not resolve known-servers aliases.** There an
   alias-form `client.server_id` fails with
   `Server ID must be 76 characters, got N`, even when the alias is registered
   and the daemon runs fine — confirm with `toxtunnel servers list -c <config>`
   before treating that one message as an error. **v0.4.13+ resolves aliases**
   at startup, on reload and in `config check`, so this gap does not apply
   there.

`bash scripts/diagnose.sh <config>` runs the validator and then covers whichever
of these gaps apply to the daemon in front of you.

Then check by hand:

- Is `mode` set correctly?
- Does `data_dir` exist and is it writable?
- Does `tox_save.dat` exist? (first run creates it)
- Client-specific:
  - Is `server_id` set?
  - Is `server_id` not the placeholder `<PASTE_SERVER_TOX_ID_HERE>`?
  - If `server_id` is exactly 76 hex characters → treat as literal Tox ID.
  - If `server_id` is shorter → treat as an alias and check that
    `<data_dir>/known_servers.yaml` exists and contains an entry whose `alias:`
    matches. (`toxtunnel servers list -d <data_dir>` resolves this quickly.)
    A non-76-char `server_id` with no matching alias is a misconfiguration —
    the daemon will fail validation at startup.
  - Are `forwards` entries present with valid port numbers?
- Server-specific:
  - Is `rules_file` an **absolute** path? ToxTunnel expands `~` and nothing else,
    then hands the string to the rules loader, so a relative path resolves
    against the **daemon's working directory** — not the config's directory.
    Verified on v0.4.12: the same config loads from one cwd and dies with
    `Failed to load rules file: Rules file not found: rules.yaml` from another.
    Do **not** test existence by rebasing the path against the config directory;
    that reports "the file exists" while the daemon cannot open it.
  - Does the file exist at the path the *daemon* will resolve?
  - Is the rules YAML valid? (Nothing checks this until the daemon loads it.)

### Layer 3: Rules Risk Analysis

The rules loader has **no unknown-key detection** — unlike the main config, which
`config check --strict` scans. Parse `rules.yaml` yourself and check for:

**Silent-widening bugs (these are the dangerous ones):**

- **Unrecognised keys inside an allow/deny entry.** Only `host` and `ports` are
  read; anything else is ignored with no warning.
- **A missing `ports` key**, which the engine reads as **all ports**. Together
  with the previous item, a `port: 22` typo (singular) parses as "allow every
  port on that host". Confirmed on v0.4.12: the daemon logs `Loaded access rules`
  and nothing else.
- **Duplicate `friend:` entries.** Lookup is a linear first-match, so the second
  and later blocks for one key are dead config and their allows never apply —
  which can read as "I allowed it and it is still denied".
- `friend_public_key` as a key name — not recognised (use `friend` / `friend_pk`).

**Scope:**

- Overly broad allow rules: host `*`, or `ports: []`
- Host patterns with more than one `*` (e.g. `192.168.*.*`): the matcher handles
  one prefix and one suffix only, so these never match anything
- Friend key format: exactly 64 hex characters (the first 64 of the 76-char Tox ID)
- Port `0` or out-of-range ports

**Not a risk:** a friend rule with `allow:` and no `deny:`. The engine is
default-deny, so anything not explicitly allowed is already refused; an empty
`deny` list adds nothing. Do not report missing deny coverage as a finding.

Report risk level: LOW / MEDIUM / HIGH.

### Layer 4: Network & Tox Connection

- **ICMP is not a test of Tox reachability.** `ping -c 1 -W 2 1.1.1.1` is a weak
  hint at best: Tox bootstraps over UDP and falls back to TCP relays, and plenty
  of networks drop ICMP while passing both (and vice versa — ICMP can succeed
  through a captive portal or a proxy that blocks everything Tox needs). Never
  conclude "the network is down" from a failed ping, or "the network is fine"
  from a successful one. The signals that mean something:
  - `Connected to Tox DHT` / `Self connection status: connected (UDP|TCP)` in the log
  - `toxtunnel inspect status --json | jq '.friends_online, .dht_connected'`
    (`dht_connected` is v0.5.0+; so is `toxtunnel_dht_connected` in `/metrics`)
  - `Bootstrap contacted 0 of N node(s): this daemon has NO DHT connectivity …`
    (v0.5.0+, error level) — no node answered at all. The daemon then retries on a
    10 s–5 min backoff (`Bootstrap retry N: contacted X/Y node(s)`). A host whose
    only egress is an HTTP/SOCKS proxy never gets past this on its own: set
    `tox.proxy` (v0.5.0+) and pin `bootstrap_nodes` by IP
  - `last_connection_type` in `known_servers.yaml` for the actual peer path
  - If `bootstrap_mode: lan`, no internet is required at all, but both machines
    must be on the same subnet and the network must pass multicast
  - If `bootstrap_mode: auto`, reachability to the public DHT nodes is required
    — which is about UDP/TCP to those nodes, not about ICMP to a resolver
- Is UDP blocked?
- Is `tox.tcp_port` (default `33445`) available?
- Check logs for (exact strings the daemon emits):
  - `Connected to Tox DHT` / `Self connection status: connected (UDP|TCP)`
  - client: `Server friend N is now online` (and `Still trying to reach server …; offline for Ns` while it is not)
  - server: `Friend N (pk=…) connected`, `Accepted friend request from …`, or
    `Refused friend request from …: no rule entry` when the client's PK is missing from rules
  - server (startup **and** every reload): `Pre-seeded friend <PK> from rules
    (friend_number=N)` / `Friend pre-seed: added X of Y missing key(s)`. Every PK in
    `rules.yaml` is pushed into the Tox friend list directly, so a client whose key was
    added *after* it first tried to connect no longer needs a friend request it can never
    re-send — see "client can never connect after being refused once" below

### Layer 5: Port & Tunnel Connectivity

- Is the local listening port open? (`lsof -nP -i TCP:PORT -sTCP:LISTEN`).
  Expect whatever `local_address` says: `127.0.0.1:PORT` for a v0.4.13+ config
  that sets it. When the key is absent the answer is version-dependent —
  `127.0.0.1:PORT` on v0.5.0+, `0.0.0.0:PORT` on anything older (including
  every v0.4.12-and-older daemon, which predates the key entirely).
  If the operator believed it was loopback-only and it is not, that is
  a finding in itself: the service is reachable from the whole subnet. The
  inverse on v0.5.0+ — "other machines could reach it before the upgrade and
  now cannot" — means the config needs an explicit `local_address: 0.0.0.0`.
- Can TCP connect to it? (`nc -z -w 5 127.0.0.1 PORT`) — **but this proves almost
  nothing.** The client binds and accepts the forward port before it attempts any
  `TUNNEL_OPEN`, so the connect succeeds with the Tox link down, the friend
  offline, and the rules denying everything. Never treat a successful `nc -z` as
  evidence the tunnel works; it only rules out "the listener is missing".
  Use a service-level probe (`scripts/verify.sh <port> <service> <config>`) or
  `toxtunnel inspect tunnels` for real evidence.
- Is the target service reachable from the server? (`nc -zv target_host target_port`)
- Check logs for `TUNNEL_OPEN`, `TUNNEL_ERROR`, `TUNNEL_CLOSE`
- `toxtunnel inspect tunnels` shows live tunnels with their target host:port, bytes in/out, and age — if your tunnel never shows up here, the open was denied or never reached the server
- If metrics are enabled, watch `toxtunnel_tunnels_opened_total{result="denied"}` (rules blocked it) vs `result="failed"` (target unreachable from server) vs `result="ok"` (succeeded)

### Layer 6: v0.3.0 Subsystem Diagnostics

These layers only apply when the corresponding feature is enabled.

**Hot-reload didn't apply:**
- Grep the daemon log for `config reloaded` (success) or `reload failed:` / `reload rejected:` (parse / validation error)
- If neither appears, the SIGHUP / pipe message never reached the daemon — check pid resolution (`<data_dir>/toxtunnel.pid` exists?), permissions (can the caller signal the process?), and on Windows that the named pipe `\\.\pipe\toxtunnel-reload-<pid>` exists
- Remember the reloadable set is small: `server.rules_file` contents, `client.forwards`, `logging.level`. Anything else (Tox identity, listen ports, mode, `data_dir`, `client.socks5`, `client.failover`, `metrics.*`, `tunnel.*`, `flow_control.*`, `watchdog.*`) makes the daemon **reject the whole reload** — it is not silently ignored: `reload rejected: config reload rejected: field '<name>' requires a restart (not in the reloadable subset)`, with the previous config left running

**SOCKS5 listener didn't bind:**
- Check startup log for `Invalid client.socks5.listen value` or `must bind to a loopback address` — the validator rejects non-loopback binds (`0.0.0.0`, LAN IPs)
- Verify the listener is actually enabled: `socks5.enabled: true` in YAML, OR `--socks5 host:port` on the CLI
- SOCKS5 and `client.pipe` are mutually exclusive; the validator emits `socks5.enabled and client.pipe cannot be used together`
- If listener bound but CONNECTs are refused with SOCKS5 reply 0x02 ("connection not allowed") — or `403 Forbidden` when the client spoke HTTP CONNECT — the request was denied by **server policy**: `rules.yaml`, the rate limiter, or the concurrent-tunnel cap. Widen the allow list or the limits on the server, not the client. A `0x04` / `0x05` / `0x01` reply (all `502 Bad Gateway` over HTTP CONNECT) means policy allowed the request and the *target* was unreachable, refused, or the open failed — a different problem entirely
- Reading the reply byte back to a cause (v0.4.12+): `0x02` = policy denial (`TUNNEL_ERROR` code 1) · `0x05` = the target actively refused the connection (code 3) · `0x04` = every other open failure — DNS, connect timeout, target lost mid-open (code 2). Before v0.4.12 the server sent code 3 for policy denials too, so a rate-limited OPEN arrived as `0x04` "host unreachable", indistinguishable from a dead target. But a v0.4.12+ **client** carries a shim that re-maps that older server's `"Rate limit exceeded"` / `"Tunnel limit exceeded"` back to `0x02`, so you only actually see the misleading `0x04` when **both** ends predate v0.4.12 — see the version matrix under "a friend is denied with Rate limit exceeded" below. On that combination, check `toxtunnel_rate_limit_open_rejected_total` on the server before chasing the target

**Multi-server failover not switching:**
- Tail the log for `Failover: switching active server X... -> Y... (friend N)` — absence means no switch decision has fired
- Check `client.failover.timeout_seconds` (default 60) — if set too high, the client waits longer than expected before promoting a fallback
- Make sure the fallback servers are in the list (`server_id` must be a YAML sequence, or use `--server-id-fallback` repeated); a single-string `server_id` ignores the failover block
- After fallback promotion, the client waits `prefer_primary_grace_seconds` (default 30) of *continuous* primary uptime before switching back — brief primary flaps reset the grace timer
- The active server is **not** in `inspect status` — grep the log for
  `Failover: switching active server <A>... -> <B>... (friend N)`; the most
  recent such line names the current one

**Metrics endpoint missing / wrong values:**
- `curl -s localhost:9100/metrics | head` — if connection refused, `metrics.enabled: false` (the default) or the daemon didn't pick up the config (restart, since metrics listen isn't hot-reloadable)
- Wrong listen address? Check `metrics.listen` matches what Prometheus is scraping
- Path is `/metrics` by default; if a custom path was set, the default URL 404s
- `toxtunnel_friends_online` stuck at 0 → friend connectivity broken (back to Layer 4)
- `toxtunnel_tunnels_opened_total{result="denied"}` climbing → rules.yaml is rejecting opens; cross-reference with `inspect tunnels` to see what's actually getting through

**A reaper closed a tunnel unexpectedly:**
- Look for a `toxtunnel_tunnels_closed_total{reason="timeout"}` increment — but
  note **both** reapers book that same label, so identify which one fired from
  the tunnel's state before it went
- `tunnel.idle_timeout_seconds: 0` (the default) disables the general reaper;
  a non-zero value reaps any non-`Connecting` tunnel idle that long, healthy
  `Connected` ones included
- `tunnel.half_close_timeout_seconds: 120` is **on by default** and reaps only
  `Disconnecting` tunnels. A tunnel that vanished ~2 minutes after one side
  closed was almost certainly this, not the idle reaper
- If a long-lived but quiet protocol (an SSH session with no traffic, a
  connection pool) is being reaped, raise `idle_timeout_seconds` or set it to `0`
- Set `tunnel.keepalive_interval_seconds` if you want application-level traffic
  to keep otherwise-silent tunnels marked live

### Layer 6: Application Layer Smoke Test

- SSH: check SSH banner via `nc`
- HTTP: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:PORT/`
- DB: use service-native ping or query commands

## Common Errors Explained

| Error / Symptom | Meaning | Fix |
|-----------------|---------|-----|
| `Connection refused` on local port | Client not running, wrong `local_port`, or port conflict | Check process, config, and `lsof -i :PORT` |
| Friend stays `Offline` | Wrong `server_id`, DHT not connected, or UDP blocked | Verify 76-char Tox ID, wait 30-60s, check internet, try `bootstrap_mode: lan` on same LAN |
| Friend online but tunnel fails | Rules block the target or target service is down | Check `rules.yaml` and test target with `nc -zv host port` |
| `Invalid public key length` | Wrong friend key format in `rules.yaml` | Friend public key must be exactly 64 hex chars, not the full 76-char Tox ID |
| `Rules file not found` | Bad `server.rules_file` path | Use an absolute path and verify permissions |
| Slow transfer speed (≈5–10 KB/s; a tiny request takes seconds while a bulk transfer runs) | Tox **TCP relay** instead of direct UDP — `toxtunnel servers list` / `known_servers.yaml` shows `last_connection_type: tcp`. toxcore's congestion control over relays tops out at a few packets/s; interactive SSH / DB queries are fine, bulk copies are not | Get the peers onto direct UDP: same LAN → `bootstrap_mode: lan` (that is what turns on toxcore local discovery — there is no separate `local_discovery_enabled` YAML key); otherwise make sure UDP 33445+ is reachable on at least one side. On a relay-only path keep payloads small (compress) and avoid concurrent bulk flows — every tunnel to one friend shares a single toxcore send queue, so one bulk copy starves the others (v0.5.0+ bounds the queue a bulk copy builds to about min RTT / 2 + 75 ms of data, or the 32 KiB floor's worth on paths slower than ~440 KB/s; before, on a relay path, it was tens of seconds) |
| Periodic disconnects | Unstable Tox friend connectivity | Raise log level and check network stability |
| `Tunnel N open timed out after 30s with no OPEN_ACK from the peer; closing` (v0.5.0+) | The server never answered the open: it went offline mid-handshake, or (pre-v0.5.0 server on a slow path) the OPEN_ACK sat behind a bulk transfer in the friend's queue. Booked as `tunnels_opened_total{result="failed"}` | Check the server is online and not saturated by a bulk flow to the same client; upgrade both ends to v0.5.1+ (the window shrinks on slow paths since v0.5.0, and since v0.5.1 bunched ACKs no longer inflate it). `tunnel.open_timeout_seconds` tunes the limit (0 = the old wait-forever) |
| `TCP connection accepted on port P while the server is offline; holding it for up to 10s (N held)` then `Held connection on port P timed out after 10s waiting for the server; closing` (v0.5.0+) | The client's server was offline when the app connected; the connection was held but the server did not come back in time | Normal at start-up or across a brief link drop. If it times out, find out why the server is offline (layer 4). Raise `tunnel.offline_open_wait_seconds` to ride out longer gaps, e.g. past `failover.timeout_seconds` when a fallback should take over |
| App sees `Connection reset by peer`; client log `Tunnel N received TUNNEL_ERROR: code=4, desc='target connection ended abnormally: …'` (server: `Tunnel N sent error: code=4, …`) | The **target** service reset or broke its connection after the tunnel was up; v0.5.0+ passes that through as a local reset (older releases turned it into a clean EOF, so truncated replies looked complete) | Investigate the target service (its logs, limits, crashes); the tunnel did its job |
| Crashes on startup with `std::bad_alloc` (huge `mmap`) | A non-regular file — usually a **directory** — sits at `<data_dir>/tox_save.dat` (or it is corrupt), so the loader read a garbage size. The v0.4.8 Linux packaging bug created the directory case | **Do not `rm -rf` it — that destroys the Tox identity, which cannot be recovered.** Stop the daemon, then: if it is an **empty directory**, `rmdir` it (v0.4.9+ self-heals this on the next write anyway). If it is a **file**, move it aside rather than deleting: `mv <data_dir>/tox_save.dat <data_dir>/tox_save.dat.bak-$(date +%s)`. Only then restart, which mints a **new identity with a new public key** — so every server's `rules.yaml` needs the new key, and the peer's `known_servers.yaml` entry is stale. Get the user's explicit agreement to that before doing it. Hardened to fail gracefully in builds after v0.4.7 |
| Both peers reach DHT but `friends_online` stays 0 **across different machines** | Tox friend-discovery (onion) blocked by the network — a local HTTP/SOCKS proxy or VPN in TUN mode (e.g. Clash) degrades onion routing; a corporate switch usually filters the multicast that `bootstrap_mode: lan` needs | Same LAN allowing multicast → `lan`. Else the path must pass Tox UDP/onion (don't let a TUN-mode VPN capture the daemon's traffic), or pin a mutually-reachable bootstrap node — on v0.5.0+ another daemon can be that node (`dht_public_key` / `tcp_relay_port` from its `inspect status`), and a proxy-only host can go through `tox.proxy` to that daemon's TCP relay. Same-host loopback (`lan`) always works |
| `TcpListener: failed to bind <addr>:<port>: Address already in use` (Windows: `Only one usage of each socket address … is normally permitted`) | Local forward port taken (often a second toxtunnel) | At startup the client refuses to run: `Failed to initialize client: cannot listen on configured forward port(s): …` and exits 1. On reload it is per-forward: `Reload: not forwarding <addr>:<port> -> …` plus `reload applied with warnings: …`, everything else stays live. v0.4.13+ reports the bind address alongside the port; older builds print the port alone. Free the port (`ss -tlnp \| grep :N`) or pick another |
| `failed to create Tox instance: could not bind Tox TCP relay port <N>` | Another toxtunnel (or anything else) holds that port. The Tox **UDP** port auto-walks to the next free one; the **TCP relay** port does not, and server mode will not accept `tcp_port: 0` | Give this daemon its own `tox.tcp_port` |
| `data directory <dir> is already in use by toxtunnel pid <N>` | A second daemon tried to take a `data_dir` another one owns. Sharing it would mean sharing the Tox identity, the inspect socket and `known_servers.yaml`, so startup refuses with exit 1 — including under `--service`, so `Restart=on-failure` retries once the holder exits | Stop the other instance, or give this one its own `data_dir` |
| `Could not claim the data directory: … Refusing to start without it` | The lock could not be taken for a reason other than a live holder (unwritable dir, filesystem without working locks) | Fix the permissions/filesystem. If the data_dir genuinely cannot host a lock, `TOXTUNNEL_ALLOW_UNLOCKED_DATA_DIR=1` starts anyway — at the cost of nothing preventing a second daemon |
| `config: ignoring unknown key '<path>'` | The config contains a key no version of the parser reads — a typo, or a plausible-but-nonexistent setting | Fix or delete the key. `toxtunnel config check -c <file>` lists them all; `--strict` makes it exit non-zero for CI |
| `Permission denied` on `data_dir` | Wrong ownership or permissions | `chmod 700 data_dir` and fix owner |
| Config parse error | YAML syntax problem | Fix indentation and validate with `python3 -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" config.yaml` |
| `client.socks5.listen must bind to a loopback address` | SOCKS5 listener set to non-loopback bind | Change to `127.0.0.1:<port>`, `::1`, or `localhost`; for remote consumers use SSH local-forward over loopback |
| `socks5.enabled and client.pipe cannot be used together` | Both dynamic-destination modes enabled | Pick one — SOCKS5 for dynamic, `pipe` for SSH ProxyCommand |
| `Invalid metrics.listen value` / `metrics.path must start with '/'` | Bad metrics config | Use `host:port` for listen and a path starting with `/` |
| `reload rejected: <reason>` in logs | New config failed parse/validation | Daemon kept old config; fix the YAML and re-trigger reload |
| `reload: no pid file at ...` | Daemon not running, different `data_dir`, a pre-v0.4.11 daemon (never wrote the file), **or a corrupt pid file** — parsing is strict, so anything other than one positive integer (`123abc`, `12.5`, empty) reads as absent rather than being partially parsed into a signal for an unrelated process | Verify daemon is up; pass `-d` or `-c` so reload looks in the right place; check the file really holds just a number; or set `TOXTUNNEL_RELOAD_PID` |
| `reload: pid N is no longer a toxtunnel process (stale toxtunnel.pid?)` | Daemon crashed / was killed and the pid was reused | Start the daemon again (it overwrites the pid file) |
| SOCKS5 CONNECT returns reply 0x02 (HTTP CONNECT: `403 Forbidden`) | Server **policy** denied the open: rules.yaml, rate limiter, or tunnel cap | Add the host/port to the friend's allow list on the **server** (not client), or loosen its `rate_limit`. Reply `0x04`/`0x05`/`0x01` (HTTP `502`) is *not* a policy denial — the target was unreachable/refused |
| One friend's throughput plateaus while others are fine; `toxtunnel_rate_limit_bytes_throttled_total` climbing | Its `rate_limit.bytes_per_sec` budget is binding — inbound TUNNEL_DATA is being deferred and replayed, not dropped (implemented in v0.4.11; the keys were inert before) | Working as configured. Raise `bytes_per_sec` / `bytes_burst`, or set `bytes_burst: 0` to exempt the friend, then reload |
| `Friend N reached the inbound throttle backlog rail (… bytes deferred)` | 32 MiB of that friend's inbound frames are parked. The backlog is released early, in order — nothing is lost, but the budget is exceeded for the burst | Either `bytes_per_sec` is far below what the peer offers, or the peer is not honouring flow control. Raise the budget, or use `max_concurrent_tunnels` / `open_per_sec` if the peer is the problem |
| Tunnel reaped while still in use | `tunnel.idle_timeout_seconds` too aggressive for the protocol | Raise the timeout or set `0` (disabled) |

## Output Format

```text
## Diagnosis Result

### Layer [N]: [Layer Name]

### Problem Identified
[Clear description of what's wrong]

### Evidence
[Log lines, command output, or config snippets that confirm the issue]

### Risk Assessment (for rules issues)
[LOW / MEDIUM / HIGH with explanation]

### Fix
[Exact steps to resolve, including commands]

### Verification
[Command to confirm the fix worked]
```

## Helper Scripts

```bash
# Full diagnostic. Runs `toxtunnel config check --strict` first, then covers
# what that misses: rules.yaml structure, alias resolution, forward exposure,
# per-server transport. Exit 1 if any issue was found.
bash scripts/diagnose.sh /path/to/config.yaml

# Verify a specific port end to end.
bash scripts/verify.sh <local_port> [ssh|http|postgres|mysql|redis|mongo|rdp|tcp] [client.yaml]
```

Read both scripts by exit code:

- `diagnose.sh`: `0` = clean, `1` = at least one WARN/FAIL. A `[SKIP]` line means
  the check **could not run** (missing PyYAML, missing binary) — it is not a pass,
  and it must not be summarised as one.
- `verify.sh`: `0` = the remote service answered (end-to-end proven), `2` = local
  checks passed but end-to-end was **not** proven, `1` = failed. Never report a
  `2` as a working tunnel; say what remains unverified and why.

## v0.4 Stability + Performance Diagnostics

### Symptom: daemon went silent without exiting

Tox-thread watchdog fires when `tox_iterate` stalls past
`watchdog.deadline_seconds`. Check:

1. `journalctl -u toxtunnel | grep "tox_thread wedge"` — logged at **critical**
   level, verbatim:
   v0.4.x: `tox_thread wedge detected: lag_ms=<N> deadline_ms=<N> heartbeat_count=<N>`;
   v0.5.0+: `tox_thread wedge detected: lag_ms=<N> deadline_ms=<N>
   heartbeat_count=<N> phase=<phase> (confirmed over 5 consecutive checks);
   aborting so the service manager restarts the daemon`. `phase` names where
   the Tox thread is stuck: `idle`, `tox_iterate`, `posted tasks`,
   `application callbacks` or `maintenance`. There are no `delta_ms` or `last_heartbeat_counter`
   fields. On v0.5.0+ it is preceded by warnings `tox_thread heartbeat stale for
   <N> ms (deadline <N> ms, phase=…); confirming wedge (k/5)`.
   **An abort right after the host woke from sleep, or after a VM pause, on
   v0.4.x is that pause, not a wedge** — v0.4.x aborts on one stale check;
   v0.5.0 requires 5 consecutive ones and discards checks taken across a process
   suspend. Correlate with the host's sleep/wake log before chasing toxcore.
2. `cat <data_dir>/abort_count` — **the only durable count.** Written at abort
   time; nothing reads it back at startup.
3. `curl 127.0.0.1:9100/metrics | grep watchdog_aborts` —
   `toxtunnel_watchdog_aborts_total` is the **in-process** view and **resets to
   0 on every restart**, so after the abort-and-restart it reads 0 while the file
   reads N. They agree only within a single process lifetime. Alert on
   `increase(...)`, and reconcile history against the file.
4. `toxtunnel_tox_iterate_lag_ms` — the gauge that actually tracks a wedge:
   milliseconds since the last `tox_iterate()` **returned**. It climbs toward
   `deadline_seconds` while the thread is stuck.
5. `toxtunnel_tox_iterate_lag_milliseconds_max` — the maximum *completed* call
   duration since process start. Useful as a slow-toxcore trend, useless as a
   wedge alarm: it latches on one old slow call and, because a hung call has not
   completed, it cannot move during the wedge you are chasing. The summary is
   also exposed as `_count` / `_sum` for rate-style queries.

The watchdog calls `std::abort()` precisely because in-process recovery
of a wedged toxcore is unsafe. systemd / launchd / Windows SCM
brings the daemon back.

### Symptom: a friend is denied with "Rate limit exceeded"

Rate limiter rejected the TUNNEL_OPEN. Check:

1. `curl 127.0.0.1:9100/metrics | grep rate_limit_open_rejected_total`
   — global counter.
2. The structured WARN log line carries the friend public key prefix.
3. `toxtunnel inspect status --json` does **not** expose per-friend bucket
   levels — the WARN log line and the counter above are the only signals.

On the client side this surfaces as `TUNNEL_ERROR` code 1 and a SOCKS5
`0x02` / HTTP `403` — a denial, not an unreachable host.

Seeing `0x04` instead takes **both** ends being old, not just the server:

| Server | Client | Rate-limit / cap denial surfaces as |
|--------|--------|-------------------------------------|
| ≥ v0.4.12 | ≥ v0.4.12 | `0x02` / `403` |
| ≥ v0.4.12 | ≤ v0.4.11 | `0x02` / `403` (server already sends code 1) |
| ≤ v0.4.11 | ≥ v0.4.12 | `0x02` / `403` (client-side compatibility shim) |
| ≤ v0.4.11 | ≤ v0.4.11 | **`0x04` / `502`** — looks like an unreachable host |

The v0.4.12+ client shim re-maps code 3 to a denial when the description matches
`"Rate limit exceeded"` or `"Tunnel limit exceeded"` **exactly**. So check both
versions before concluding, and on the last row read
`toxtunnel_rate_limit_open_rejected_total` on the server rather than chasing the
target.

Loosen `rate_limit_defaults` or add a per-friend override block in
`rules.yaml` and `kill -HUP` to reload.

### Symptom: one friend's transfers are slow but nothing is erroring

No `TUNNEL_ERROR`, no closed tunnels, no rules denial — that friend's bytes
just arrive slower than the link allows. Check whether its byte budget is
binding (`rate_limit.bytes_per_sec` / `bytes_burst`, live since v0.4.11 —
in earlier v0.4.x releases these keys parsed and did nothing, so a config
carried across the upgrade can start shaping traffic that never was before):

1. `curl 127.0.0.1:9100/metrics | grep rate_limit_bytes_throttled_total`
   — a climbing counter means frames are finding the bucket short. In
   `enforce` that is the throttle working; in `report` nothing is being
   delayed and the counter is pure measurement.
2. Server log at startup / after reload:
   `Inbound byte throttle engaged for friend <N> (rate_limit.bytes_per_sec)`,
   or `Inbound byte throttle engaged|disengaged for friend <N>`.
3. `toxtunnel inspect status --json` does **not** expose bucket levels;
   the counter and the log lines are the only signals.

Remember what this key does and does not cover before concluding anything:
it meters **inbound TUNNEL_DATA from that friend** only. If the slow
direction is server → client, the byte budget is not the cause — look at
transport (UDP vs TCP relay) and flow control instead. Enforcement defers
and replays in order; it never drops bytes and never closes a tunnel, so a
throttled tunnel is slow, not broken. Two rails release the backlog early
rather than growing it (32 MiB per friend, and a per-frame deadline of at
most 60 s derived from the reaper timeouts) — both log at `warn` and both
mean the configured rate was briefly exceeded, not that data was lost.

Fix: raise `bytes_per_sec` / `bytes_burst`, switch the friend to
`mode: report` to confirm the budget is the cause, or set `bytes_burst: 0`
to exempt it — then reload. A reload refills every bucket, so give it a
moment before re-measuring.

### Symptom: adaptive coalescing is making bad decisions

The `toxtunnel_coalesce_policy_transitions_total` counter ticks on
every state-machine move. If it climbs fast under steady traffic, the
EWMA is flapping. Workarounds:

1. Pin the mode: `tunnel.coalesce_mode: fixed` to lock to the v0.3.0 cadence.
   This is the right answer for a flapping EWMA in almost every case.
2. For bulk-only workloads pin `bypass`; for trickle-only, where you want every
   small write batched, pin `drain`.

The **only** valid values for `tunnel.coalesce_mode` are `fixed`, `adaptive`,
`bypass`, `drain`. `batch` is an internal state the adaptive machine selects at
runtime (and a metric label) — it is **not** a config value, and setting it makes
the daemon refuse to start:
`Invalid tunnel.coalesce_mode 'batch': must be one of 'fixed', 'adaptive', 'bypass', 'drain'`.
`toxtunnel config check -c <file>` catches it before you find out the hard way.

### Symptom: high BDP link still capped at 256 KiB

`flow_control.mode` defaults to `bdp` since v0.4.1 — check the config has
not pinned `mode: fixed`. In `bdp` mode the per-tunnel `BdpFlowControl`
scales the window between `send_window_min_bytes` and
`send_window_max_bytes`: bandwidth × (minimum RTT of the last ~10 s + 50 ms) ×
`safety_factor_x100`/100 on v0.5.0+ (an RTT × bandwidth EWMA before). Inspect via
the `toxtunnel_tunnel_send_window_bytes` summary. On v0.5.0+ a dip to the 32 KiB
floor about every 10 s during a long transfer is the periodic RTT re-measure,
not a fault. If the link is a TCP relay
the window is not the limiter — see "Slow transfer speed" above.

### Symptom: tunnels die across server restart

Tunnel resume (`tunnel.resume.enabled: true`) holds a disconnected
friend's tunnels for `resume.max_age_seconds` and reattaches them on
reconnect — but only while **both processes stay up** (live reconnect).
A process restart loses the local TCP sockets, so tunnels always die
across a restart; that is by design, not a bug. With the default
`enabled: false` the opcodes are wire-inactive.

### Symptom (macOS 15+): every LAN target fails with "No route to host"

`TCP connect failed: No route to host` for **other devices on the LAN**, while
`127.0.0.1` targets and the Mac's *own* LAN addresses work, and `nc`/`curl` from
a shell on the same Mac reach the target fine. This is macOS **Local Network
privacy**, not a tunnel fault: the check is per responsible process, and a
daemon left running by `nohup … &` from an SSH session (re-parented to launchd)
gets denied with no prompt and no log entry.

Reproduce without toxtunnel: run any small TCP-connect binary the same detached
way — it fails identically. Fix: run the server as an approved launchd
daemon/agent (System Settings → Privacy & Security → Local Network), or keep
its targets on loopback.

### Symptom (Windows): daemon started from an SSH session dies silently

A daemon launched with `Start-Process` inside an `ssh host "..."` command
logs `Client started` / `Server started` and then nothing: when the SSH
command returns, Win32-OpenSSH tears down the session's job object and
the process is killed with no log line and no Event Log entry. Run it as
the service (`install-windows-service`), as a Scheduled Task, or via
`Invoke-CimMethod -ClassName Win32_Process -MethodName Create`.

### Symptom (Windows): `inspect` / `reload` say "no pid file" or "cannot connect"

- Daemons before v0.4.11 never wrote `toxtunnel.pid`; set
  `TOXTUNNEL_INSPECT_PID` / `TOXTUNNEL_RELOAD_PID` to the pid printed in
  `Inspect IPC listening at \\.\pipe\toxtunnel-<pid>`.
- `cannot connect … (error 5: access denied)` against the service:
  the pipe only admits SYSTEM and Administrators — use an elevated prompt.
- `error 2: no such pipe`: the pid is stale (daemon restarted) — re-read
  the pid file / log.

### Symptom: tunnels stuck in `Connecting` or `Disconnecting` after a burst

`toxtunnel inspect tunnels` on the client shows N tunnels frozen in
`Connecting`, while the server side shows the same IDs as `Connected`
(or `Disconnecting`). Cause: a control frame (`TUNNEL_OPEN_ACK`,
`TUNNEL_CLOSE`, `PING`, `PONG`) hit toxcore's lossless SENDQ while it
was full and got silently dropped. Fixed in v0.4.5+ (and since v0.5.0
`tunnel.open_timeout_seconds`, default 30, closes any client tunnel still in
`Connecting` after that long instead of letting it hang):

- Control frames routed via `TunnelManager::send_frame` are parked in a
  bounded FIFO retry queue (cap 4096) and re-emitted every 20 ms until
  SENDQ drains. (v0.4.11 took the handshake frames back out of that
  queue — see below.)
- Control frames sent via the per-tunnel `on_send_to_tox` callback
  (`TUNNEL_CLOSE`, `PING`/`PONG`, `INFO`, resume opcodes) inspect the
  frame type at offset 0 and, on failure, hand off to the same retry
  queue. `TUNNEL_DATA` frames keep using the per-tunnel coalesce-buffer
  retry-on-timer path instead — routing them through the manager queue
  would double-send. Without the per-tunnel-path fix, a `TUNNEL_CLOSE`
  lost to SENDQ-full would leave the peer's tunnel hung in
  `Disconnecting` (the bidirectional bulk-transfer close-handshake hang
  seen in the v0.4.5 1 MB-echo soak).

v0.4.11 closed the remaining hole on the handshake frames themselves:

- The client's `TUNNEL_OPEN` and the server's OPEN_ACK (`TUNNEL_ACK`) are
  no longer parked in the shared queue at all — the queue holds bare wire
  bytes with no tunnel identity, so a parked handshake frame could be
  delivered later against whatever tunnel had recycled that id. They now
  report backpressure to their own driver, which retains and re-sends
  them. A `TUNNEL_OPEN` refused by a full SENDQ is retried, not dropped;
  `create_tunnel()` releases the id and reports failure rather than
  handing back an id the peer never heard of.
- Those two frame types also consult the outbound queue before being
  handed to toxcore, so neither can overtake something already parked.
  `TUNNEL_DATA` is covered transitively — it only flows once the OPEN or
  the OPEN_ACK has gone out — so DATA can no longer arrive ahead of a
  backpressured OPEN_ACK. The still-parked control frames (CLOSE, ERROR,
  PING/PONG, INFO, resume) keep the older, weaker ordering; that is a
  known and documented residual, not a bug to chase.

If you see a wedge anyway:

1. Grep `journalctl -u toxtunnel | grep 'pending queue at cap'` — the
   only path that drops a control frame today is overflow at the cap.
2. The queue depth is not exposed anywhere; use `toxtunnel inspect tunnels`
   and watch each tunnel's `BYTES_IN` / `BYTES_OUT` rather than just state —
   a tunnel whose counters advance is not actually wedged.
3. Pair with `toxtunnel_tox_iterate_lag_milliseconds_max`: a sustained
   spike there usually precedes a backpressure pulse.

Operational hardening — **check the tunnel state before choosing a knob**:

- Tunnels stuck in **`Disconnecting`** are already covered by
  `tunnel.half_close_timeout_seconds`, which is **on by default at 120 s** and
  force-closes exactly this case. If they are still lingering, lower that value.
  It is not true that the defaults leave stale tunnels around forever; that was
  only so before the half-close cap existed.
- Tunnels stuck in **`Connected`** but genuinely abandoned are what the opt-in
  `tunnel.idle_timeout_seconds` (default `0`) is for. Enable it deliberately:
  it reaps any non-`Connecting` tunnel purely on inactivity, so an idle-but-alive
  SSH session or DB pool is killed just as readily as an abandoned one. Pick a
  timeout longer than the longest legitimate silence in the workload.

Both fire from the same `reaper_tick_seconds` timer and book
`tunnels_closed_total{reason="timeout"}`, so the counter alone will not tell you
which one acted — look at `toxtunnel inspect tunnels`. Under
sustained *bidirectional* bulk transfer the close handshake can still
be slow because TUNNEL_DATA frames continuously fill the same shared
toxcore SENDQ that control frames need; bytes flow correctly but
close-completion latency grows. Confirm via `inspect tunnels`: an
idle counter that resets means the tunnel is alive but slow, not
wedged.


### Symptom: a client can never connect after being refused once

The server logged `Refused friend request from <PK>: no rule entry for this Tox
ID`, the operator added `<PK>` to `rules.yaml`, and the client *still* never comes
online — reloading the server, restarting the server, and restarting the client
all change nothing. Waiting does not help either; measured at 3.5+ minutes with a
full client restart in between.

Cause (fixed; on releases before this fix the only escape is destructive). The
client persists the server in its own `tox_save.dat` the moment it first adds it,
so toxcore considers the friendship already requested and **never re-sends the
friend request**. On the server, `on_friend_request` used to be the one and only
path into the friend list, and it refuses any key not yet in `rules.yaml`. Adding
the rule afterwards therefore fixes the access check for a friend request that
will never arrive again. The two sides deadlock permanently.

- On a fixed build: nothing to do. The server pre-seeds every `rules.yaml` public
  key into its Tox friend list at startup and after every reload, so `kill -HUP`
  (or `toxtunnel reload`) is enough. Confirm with `Pre-seeded friend <PK> from
  rules` in the server log; the client comes online within ~50 s.
- On an affected older build the escape is destructive, so **upgrade instead if
  you possibly can** — the pre-seed fix removes the need entirely. If you cannot:
  the client's Tox identity has to be replaced. **Quarantine, never delete**, and
  only with the user's explicit agreement, having told them it mints a **new
  public key**:

  ```bash
  # 1. Stop the client. 2. Move the whole data dir aside — do not rm -rf it.
  mv <client data_dir> <client data_dir>.bak-$(date +%s)
  # 3. Start the client once to mint the new identity, note the new PK.
  # 4. Replace the OLD PK with the NEW one in the server's rules.yaml.
  # 5. Reload the server BEFORE starting the client again.
  ```

  Order matters on those builds: the client's PK must be in `rules.yaml` and the
  server reloaded *before* the client's first connection attempt, or you
  reproduce the same deadlock. The backup directory also preserves
  `known_servers.yaml` and any aliases, which you will want to copy back.
  Note that discarding the identity invalidates **every** server's `rules.yaml`
  entry for this client, not just the one you are fixing.

Note the pre-seed is deliberately one-way: removing a key from `rules.yaml` does
**not** delete the friend. The rules engine default-denies every `TUNNEL_OPEN`
from an unlisted key, so a leftover friend entry grants no access — while deleting
it would invalidate the peer's saved friendship and recreate exactly this deadlock
if the rule is ever restored. To actually drop a friend, stop the daemon and
remove it explicitly.

### Symptom: resume declines with "no held tunnel" after a long outage

Client log shows `TUNNEL_RESUME_REQUEST` answered with a decline; server log has
`RESUME_REQUEST from friend N (tunnel M): no held tunnel; declined (re-open)`,
and there is **no** preceding `Holding tunnel manager for friend N for resume`.

Cause (fixed): toxcore does not guarantee a `disconnected` callback before the
matching `connected` one — after a long outage it can report the friend back
online with no disconnect in between. The resume hold only ever ran from the
`disconnected` path, while the `connected` path unconditionally installed a fresh
`TunnelManager`, silently destroying the live one along with every open tunnel and
its target TCP connection. Measured failure rate before the fix: 2 of 3
long-disconnect trials.

The fixed server keeps the live manager and logs
`Friend N reported connected while its tunnel manager is still live (no matching
disconnected event); keeping the existing manager and its tunnels` at **warn**.
Seeing that line is normal and benign — the tunnels survive and the follow-up
`RESUME_REQUEST` resolves against them. What it *does* tell you is that the peer
was away for a while without the server noticing, so:

- Some of those tunnels may be reaped shortly afterwards if
  `tunnel.idle_timeout_seconds` or `tunnel.half_close_timeout_seconds` elapsed
  during the invisible outage. That is the reaper working as configured, not a
  resume failure.
- Repeated warns for the same friend point at a flapping Tox path (check
  `last_connection_type` — relay-only links flap far more than direct UDP), not at
  a server bug. Enabling `tunnel.keepalive_interval_seconds` makes the server
  notice these outages itself and take the proper hold-for-resume path.
