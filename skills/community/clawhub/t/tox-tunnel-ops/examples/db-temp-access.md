# Temporary Database Access via ToxTunnel

## Scenario

You need to give a contractor or team member temporary access to a PostgreSQL (or MySQL/Redis/MongoDB) database on an internal server — without VPN setup, without opening firewall ports, and with the ability to revoke access easily.

## Topology

```
Contractor Laptop (client)            Internal DB Server (server)
──────────────────────────            ──────────────────────────
psql -h 127.0.0.1 -p 15432           PostgreSQL on :5432
        ↓                                    ↑
  toxtunnel client                    toxtunnel server
        ↓                                    ↑
        └──── Tox P2P encrypted tunnel ──────┘
```

## Server Config (on machine with DB access)

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


## Client Config (sent to contractor)

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
    - local_port: 15432
      local_address: 127.0.0.1
      remote_host: 127.0.0.1
      remote_port: 5432
```

> ### ⚠️ `local_port: 15432` binds `0.0.0.0` without `local_address` (pre-v0.5.0) on the contractor's laptop
>
> Before v0.5.0, without `local_address` the listener binds every IPv4
> interface, so every host on whatever network the contractor is using can reach
> your database through their machine, with only the DB's own authentication in
> front of it. On **v0.4.13+** set `local_address: 127.0.0.1` (the config above does); on v0.4.12 and older no such key exists — firewall it instead.
>
> Require the contractor to firewall the port to loopback
> (`sudo ufw deny in to any port 15432`, an nftables/pf rule, or
> `New-NetFirewallRule … -Action Block`) as a condition of access, and keep the
> DB credentials scoped and short-lived regardless.

## Rules (locked down — contractor's friend key only)

```yaml
rules:
  - friend: "AABBCCDD...contractor-64-char-hex-public-key...EEFF"
    allow:
      - host: "127.0.0.1"
        ports: [5432]
```

The `friend` value is the **first 64 hex characters** of the peer's 76-char Tox ID — not the whole ID. They get it from their own daemon's startup log line `Client Tox ID: <76 hex>`, or from `toxtunnel print-id -c client.yaml`. A wrong length is rejected when the rules file loads (`Invalid public key length: expected 64`), so the server refuses to start or hot-reload rather than silently denying.

## Steps

1. Start server with rules
2. Share the server Tox ID with the contractor (via secure channel)
3. Contractor installs toxtunnel and starts client. Optionally, the contractor
   registers an alias once so subsequent runs only need the short name:
   `toxtunnel servers add client-db <SERVER_TOX_ID>`
4. Wait for friend connection
5. Contractor connects: `psql -h 127.0.0.1 -p 15432 -U db_user -d mydb`

## Revocation

**To revoke access:**
1. Remove the contractor's entry from `rules.yaml`
2. **Reload** the server so existing tunnels survive but the next
   TUNNEL_OPEN from the revoked friend is denied:
   `sudo systemctl reload toxtunnel` (POSIX, sends SIGHUP) or
   `toxtunnel reload` (cross-platform; uses the local IPC).
   Use `sudo systemctl restart toxtunnel` only if the change touched a
   non-reloadable field.
3. The contractor's NEW tunnel attempts are denied immediately — but a reload
   does **not** cut sessions that are already open. A `psql` connection the
   contractor established before the reload keeps working until they
   disconnect. If you need to end live access this second, restart the server
   (`sudo systemctl restart toxtunnel`), which drops every tunnel, or revoke at
   the database (`ALTER ROLE … NOLOGIN` + terminate their backends).

Also consider:
- Drop the temporary database user
- Review audit logs for any unexpected queries

## Other Databases

**MySQL:**
```yaml
forwards:
  - local_port: 13306
    local_address: 127.0.0.1
    remote_host: 127.0.0.1
    remote_port: 3306
```
Rules ports: `[3306]`
Test: `mysql -h 127.0.0.1 -P 13306 -u db_user -p`

**Redis:**
```yaml
forwards:
  - local_port: 16379
    local_address: 127.0.0.1
    remote_host: 127.0.0.1
    remote_port: 6379
```
Rules ports: `[6379]`
Test: `redis-cli -h 127.0.0.1 -p 16379 ping`

**MongoDB:**
```yaml
forwards:
  - local_port: 17017
    local_address: 127.0.0.1
    remote_host: 127.0.0.1
    remote_port: 27017
```
Rules ports: `[27017]`
Test: `mongosh --host 127.0.0.1 --port 17017`

## Security Best Practices

- **Use a specific friend key** in rules — never leave rules_file unset for temporary access
- **Create a read-only database user** for the contractor when possible
- **Set a time window** — agree on when access ends and schedule rule removal
- **Enable logging** on the server to record tunnel usage — but know its limits.
  The toxtunnel log shows *that* the contractor opened a tunnel to
  `127.0.0.1:5432`, when, and how many bytes moved. It never shows what they
  queried: the payload is an opaque byte stream to the tunnel, at any log level.
  For query-level accountability enable the database's own auditing (`pgaudit` /
  `log_statement`, MySQL's audit plugin or general query log). Do not tell a
  stakeholder the tunnel gives you a record of what was run.
- **Revoke promptly** — remove the rule as soon as the maintenance is done, and
  remember a reload blocks only *new* opens (see Revocation above)
- Back up `tox_save.dat` on both sides — it is the private identity, and the one
  file here that genuinely is a secret. The Tox IDs and friend public keys are
  public identifiers; they belong in the configs and are safe to exchange

## Verification

```bash
bash scripts/verify.sh 15432 postgres client.yaml
```

Run this from the skill root (the script lives at `scripts/verify.sh`).
Passing the client config lets it read `friends_online` from the running
daemon instead of guessing from a local TCP accept.

**Judge it by the exit code:** `0` = the remote service answered through the
tunnel, `2` = local checks passed but end-to-end was **not** proven (do not
report this as working), `1` = a check failed.
