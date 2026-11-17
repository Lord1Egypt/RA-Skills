# Database Migration Window via ToxTunnel

## Scenario

A DBA needs a secure tunnel to a production or staging database for a migration,
data transfer, or bulk operation. The tunnel should be strictly time-limited and
logged.

> **What "audited" means here.** ToxTunnel logs *tunnel* activity: which friend
> opened a tunnel, to which `host:port`, when it closed, and how many bytes
> flowed. Even at `level: debug` it never sees inside the stream — the payload is
> an opaque TCP byte stream to it, so **no SQL statement, table name, row count
> or transaction is ever recorded**. If the migration needs statement-level
> accountability, turn on the database's own auditing (`pgaudit` or
> `log_statement = 'all'` for PostgreSQL, the audit plugin / general query log
> for MySQL) — that is the only place query-level evidence exists. Say this to
> anyone who asks for "an audit trail of the migration".

## Topology

```
DBA Workstation (client)              DB Server (server)
────────────────────────              ──────────────────
pg_dump / migration tool              PostgreSQL on :5432
  → 127.0.0.1:15432                          ↑
        ↓                                    ↑
  toxtunnel client                    toxtunnel server
        ↓                                    ↑
        └──── Tox P2P encrypted tunnel ──────┘
```

## Pre-Migration Checklist

- [ ] Create a **temporary database user** with minimum required permissions
  - Read-only for verification: `CREATE USER migration_ro WITH PASSWORD '...' LOGIN; GRANT SELECT ON ALL TABLES IN SCHEMA public TO migration_ro;`
  - Read-write for migration: `CREATE USER migration_rw WITH PASSWORD '...' LOGIN; GRANT ALL ON ALL TABLES IN SCHEMA public TO migration_rw;`
- [ ] Back up the database before starting
- [ ] Agree on a maintenance window with stakeholders
- [ ] Test the migration on a staging copy first

## Server Config

```yaml
mode: server
data_dir: /var/lib/toxtunnel        # mutable state — NOT under /etc
logging:
  level: debug                       # verbose TUNNEL-level record; not SQL
  file: /var/log/toxtunnel/migration.log
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


## Rules (DBA's friend key, DB port only)

```yaml
rules:
  # DBA: migration window — remove after completion
  - friend: "AABBCCDD...dba-64-char-hex-public-key...EEFF"
    allow:
      - host: "127.0.0.1"
        ports: [5432]
```

> The `friend` value is the **first 64 hex characters** of that peer's 76-char Tox ID
> (from its `Client Tox ID: …` startup log line, or `toxtunnel print-id -c client.yaml`),
> not the whole ID. A wrong length is rejected when the rules file loads
> (`Invalid public key length: expected 64`).

## Client Config (DBA's workstation)

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

> ### ⚠️ `local_port: 15432` binds `0.0.0.0` without `local_address` (pre-v0.5.0) on the DBA workstation
>
> Before v0.5.0, without `local_address` a forward has no bind restriction — the listener binds every IPv4
> interface, so anyone on the DBA's network can reach the production database
> through that port. On **v0.4.13+** set `local_address: 127.0.0.1` (the config above does); on v0.4.12 and older no such key exists — firewall it instead. Firewall it to loopback for
> the duration of the migration window.

## Migration Workflow

### Phase 1: Verify Connectivity (read-only user)
```bash
psql -h 127.0.0.1 -p 15432 -U migration_ro -d mydb -c "SELECT count(*) FROM important_table;"
```

### Phase 2: Run Migration (read-write user)
```bash
# Example: run migration script
psql -h 127.0.0.1 -p 15432 -U migration_rw -d mydb -f migration.sql

# Example: pg_dump / pg_restore
pg_dump -h 127.0.0.1 -p 15432 -U migration_rw -d old_db | psql -h 127.0.0.1 -p 15432 -U migration_rw -d new_db
```

### Phase 3: Verify Results (read-only user)
```bash
psql -h 127.0.0.1 -p 15432 -U migration_ro -d mydb -c "SELECT count(*) FROM migrated_table;"
```

## Bandwidth Considerations

- Tox tunnels have limited throughput compared to direct network connections
- For large data transfers (>1 GB), consider:
  - Tox may use a TCP relay if direct UDP is not established. Check which one you
    got: `last_connection_type` in `<data_dir>/known_servers.yaml` (or
    `toxtunnel servers list`) — `udp` is direct, `tcp` is a relay and caps bulk
    throughput at roughly 5–10 KB/s. The log line
    `Self connection status: connected (UDP|TCP)` describes this daemon's DHT
    link, not the per-friend path.
  - Compress data before transfer: `pg_dump ... | gzip | ...`
  - Run during off-peak hours to minimize contention
  - For very large migrations, consider a VPN or direct connection instead

## Post-Migration Cleanup

1. **Verify migration results** using the read-only user
2. **Remove the DBA's rule** from `rules.yaml`
3. **Reload the server** (preserves existing tunnels): `sudo systemctl reload toxtunnel` — only restart if a non-reloadable field changed.
4. **Drop temporary users**:
   ```sql
   DROP USER migration_ro;
   DROP USER migration_rw;
   ```
5. **Archive the migration log**: `cp /var/log/toxtunnel/migration.log /var/log/toxtunnel/migration-$(date +%Y%m%d).log`
6. **Verify application connectivity** — ensure the app still works after migration

## Rollback

If the migration fails:
1. Stop the migration immediately
2. Restore from the pre-migration backup
3. Keep the tunnel open for debugging if needed
4. After investigation, close the tunnel and revoke access

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
