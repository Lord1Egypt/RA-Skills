# Local Loopback Test — validate a full server↔client setup on one machine

## Scenario

Before deploying ToxTunnel across two machines, validate the **entire** server +
client + rules + forward chain on a **single host** over loopback. This catches
config mistakes (wrong `server_id`, friend PK typo, rule that denies the target)
without depending on the internet or a second box.

This is the exact recipe used to validate the v0.4.7 release on macOS arm64
(SSH, web, Postgres, Redis, SOCKS5/HTTP-CONNECT, pipe mode, hot-reload — all green).

## The one critical knob: `bootstrap_mode: lan`

Two daemons on the **same machine** will *not* reliably become friends in the
default `bootstrap_mode: auto`: DHT returns each peer's NAT-translated public IP
and the loopback peer-to-peer connect fails on home routers without NAT hairpin
(`friends_online` stays 0 for 10+ minutes). Use LAN mode on **both** peers:

```yaml
tox:
  udp_enabled: true
  bootstrap_mode: lan
  bootstrap_nodes: []
```

Pure local discovery, no internet, friend online in **~10 s**. LAN mode is a
**testing/same-subnet** shortcut — real cross-internet deployments keep the
default `auto`.

## Layout

```
host client  --127.0.0.1:<fwd>-->  toxtunnel client --Tox(lan)--> toxtunnel server --127.0.0.1:<target>--> service
```

- One server, one client, distinct `data_dir`s (each daemon has its own Tox
  identity). Distinct is **required**, not merely tidy: since v0.4.11 a daemon
  takes an exclusive lock on its data directory, so a shared one makes the second
  process exit 1 with `data directory <dir> is already in use by toxtunnel pid <N>`.
- The forwards below set `local_address: 127.0.0.1`, so on **v0.4.13+** they
  bind loopback only. On v0.4.12 and older that key does not exist and these
  ports bind **`0.0.0.0`** — on a laptop on a
  shared network this test briefly exposes the local sshd, web server and
  databases to the whole subnet. Run it on an isolated machine, or firewall
  those ports first.
- `client.server_id` = the **server's** 76-char Tox ID.
- `rules.yaml` `friend:` = the **first 64 hex chars** of the **client's** 76-char Tox ID.
  Get IDs without starting the daemon: `toxtunnel print-id --data-dir <data_dir>`.

## Configs

> **If another toxtunnel server already runs on this host, set `tox.tcp_port`
> explicitly on the new one.** The Tox **UDP** port walks to the next free port
> automatically; the Tox **TCP relay** port does not, and server mode rejects
> `tcp_port: 0`. Without it startup dies with
> `failed to create Tox instance: could not bind Tox TCP relay port 33445 …`.

`server.yaml`:
```yaml
mode: server
data_dir: /tmp/tt-server
logging: { level: info, file: /tmp/tt-server.log }
tox: { udp_enabled: true, bootstrap_mode: lan, bootstrap_nodes: [], tcp_port: 33500 }
server: { rules_file: /tmp/tt-rules.yaml }
inspect: { enabled: true }
```

`client.yaml` (one forward per service under test):
```yaml
mode: client
data_dir: /tmp/tt-client
logging: { level: info, file: /tmp/tt-client.log }
tox: { udp_enabled: true, bootstrap_mode: lan, bootstrap_nodes: [] }
client:
  server_id: "<PASTE server's 76-char Tox ID>"
  forwards:
    - { local_port: 13022, local_address: 127.0.0.1, remote_host: 127.0.0.1, remote_port: 2222 }   # ssh
    - { local_port: 13080, local_address: 127.0.0.1, remote_host: 127.0.0.1, remote_port: 8080 }   # web
    - { local_port: 13432, local_address: 127.0.0.1, remote_host: 127.0.0.1, remote_port: 5432 }   # postgres
    - { local_port: 13379, local_address: 127.0.0.1, remote_host: 127.0.0.1, remote_port: 6379 }   # redis
inspect: { enabled: true }
```

`rules.yaml` (loopback all-ports is fine for a local test; tighten for real use):
```yaml
rules:
  - friend: "<first 64 hex chars of the CLIENT's Tox ID>"
    allow:
      - { host: "127.0.0.1", ports: [] }   # [] = all loopback ports
```

## Bring up targets, then the tunnel

```bash
# Targets bound to loopback (use whatever you have; docker is handy for DBs):
python3 -m http.server 8080 --bind 127.0.0.1 --directory ./webroot &        # web
/usr/sbin/sshd -D -f ./sshd_config -E ./sshd.log &                          # ssh on :2222
docker run -d --name pg    -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD=x postgres:16-alpine
docker run -d --name redis -p 127.0.0.1:6379:6379 redis:7-alpine

# Tunnel (capture each Tox ID, fill server_id + rules friend, then start both).
# print-id CREATES and persists the identity if the data dir is empty — that is
# the supported way to learn a key before the daemon has ever run. Starting the
# daemon with a placeholder server_id does NOT work: it exits 1 during ID
# resolution, before Tox is initialised, leaving an empty data dir.
toxtunnel print-id --data-dir /tmp/tt-server
toxtunnel print-id --data-dir /tmp/tt-client

# Validate both configs before starting (catches typo keys the daemon ignores):
toxtunnel config check -c server.yaml --strict
toxtunnel config check -c client.yaml --strict

toxtunnel -m server -c server.yaml &
toxtunnel -m client -c client.yaml &
# Wait for "Server friend 0 is now online" in the client log (~10 s).
```

## Verify each scenario through the forwarded port

```bash
# SSH (remote exec + key auth):
ssh -p 13022 -i id_test -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
    user@127.0.0.1 'whoami; uname -s'

# Web (status + large-file integrity):
curl --noproxy '*' -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:13080/
curl --noproxy '*' -s http://127.0.0.1:13080/big.bin | shasum -a 256   # compare to source

# Postgres (real query):
PGPASSWORD=x psql -h 127.0.0.1 -p 13432 -U postgres -c 'SELECT 1;'

# Redis (small + LARGE value):
redis-cli -h 127.0.0.1 -p 13379 ping
redis-cli -h 127.0.0.1 -p 13379 set k small
redis-cli -h 127.0.0.1 -p 13379 -x set k:big < big_value.txt   # see ARG_MAX note below
```

## Health check after the run (catches leaks / truncation)

```bash
toxtunnel inspect status   -c server.yaml --json   # friends_online=1, tunnels_active=0
toxtunnel inspect status   -c client.yaml --json   # friends_online=1, tunnels_active=0
# Truncation check: compare the two JSON snapshots — server bytes_out should equal client bytes_in
# (and vice versa, minus a few framing bytes). Each `status` only reports its OWN daemon's counters.
toxtunnel inspect tunnels  -c server.yaml          # should be empty once flows close (no stuck-Disconnecting)
cat /tmp/tt-server/abort_count 2>/dev/null         # file is ABSENT until a watchdog abort; absent/0 = healthy
```

## Gotchas (each one looks like a tunnel bug but isn't)

- **Proxy hijack of loopback curl.** A system HTTP/SOCKS proxy (e.g. Clash/mihomo in
  TUN mode) can intercept `curl http://127.0.0.1:<fwd>` and return `502`. Always pass
  `curl --noproxy '*'` (or `unset http_proxy https_proxy all_proxy`) for forward ports.
  For SOCKS5 forwards, route explicitly with `--socks5-hostname 127.0.0.1:<port>`.
- **Redis large value via argv.** `redis-cli set key <1MB+ value>` as a command-line
  argument hits the shell's `ARG_MAX` (~1 MB on macOS) → `Argument list too long`; the
  SET never runs and a later GET returns `(nil)`. This is a shell limit, **not** a tunnel
  truncation. Pass the value on **stdin**: `redis-cli -x set key < file`.
- **Default `auto` mode same-host.** If `friends_online` stays 0, you almost certainly
  forgot `bootstrap_mode: lan` on one of the two configs.
- **friend PK ≠ Tox ID.** `rules.yaml` wants the **64-char** public key (first 64 of the
  76-char ID), not the full Tox ID. A wrong-length `friend:` is **rejected when the rules file
  loads** (`Invalid public key length: expected 64`) — the server refuses to start / hot-reload,
  so you'll see it immediately rather than as a silent deny.

## What this does NOT cover

Loopback + LAN mode deliberately skips the public DHT/relay bootstrap path, NAT, MTU,
loss, and cross-machine routing. A green local run proves your **config and the
application data path** are correct; it does not substitute for a real two-machine
smoke on `bootstrap_mode: auto`. Run one of these locally first, then deploy.
