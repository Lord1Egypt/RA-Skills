# Database Migration Window via ToxTunnel

## Scenario

A DBA needs a secure tunnel to a production or staging database for a migration, data transfer, or bulk operation. The tunnel should be strictly time-limited with full audit capability.

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
data_dir: /etc/toxtunnel/server
logging:
  level: debug                       # verbose for audit
  file: /var/log/toxtunnel/migration.log
tox:
  udp_enabled: true
  bootstrap_mode: auto
server:
  rules_file: /etc/toxtunnel/rules.yaml
```

## Rules (DBA's friend key, DB port only)

```yaml
rules:
  # DBA: migration window — remove after completion
  - friend: "AABBCCDD...dba-64-char-hex-public-key...EEFF"
    allow:
      - host: "127.0.0.1"
        ports: [5432]
```

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
      remote_host: 127.0.0.1
      remote_port: 5432
```

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
  - Tox may use TCP relay if direct UDP is not established — check logs for `Direct UDP connection`
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
bash verify.sh 15432 postgres
```
