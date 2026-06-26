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
      remote_host: 127.0.0.1
      remote_port: 5432
```

## Rules (locked down — contractor's friend key only)

```yaml
rules:
  - friend: "AABBCCDD...contractor-64-char-hex-public-key...EEFF"
    allow:
      - host: "127.0.0.1"
        ports: [5432]
```

The `friend` value must be the contractor's 64-character hex public key. They can find it in their toxtunnel startup log.

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
3. The contractor's NEW tunnel attempts will be denied immediately.

Also consider:
- Drop the temporary database user
- Review audit logs for any unexpected queries

## Other Databases

**MySQL:**
```yaml
forwards:
  - local_port: 13306
    remote_host: 127.0.0.1
    remote_port: 3306
```
Rules ports: `[3306]`
Test: `mysql -h 127.0.0.1 -P 13306 -u db_user -p`

**Redis:**
```yaml
forwards:
  - local_port: 16379
    remote_host: 127.0.0.1
    remote_port: 6379
```
Rules ports: `[6379]`
Test: `redis-cli -h 127.0.0.1 -p 16379 ping`

**MongoDB:**
```yaml
forwards:
  - local_port: 17017
    remote_host: 127.0.0.1
    remote_port: 27017
```
Rules ports: `[27017]`
Test: `mongosh --host 127.0.0.1 --port 17017`

## Security Best Practices

- **Use a specific friend key** in rules — never leave rules_file unset for temporary access
- **Create a read-only database user** for the contractor when possible
- **Set a time window** — agree on when access ends and schedule rule removal
- **Enable logging** on the server to audit tunnel usage
- **Revoke promptly** — remove the rule as soon as the maintenance is done
- Back up `tox_save.dat` on both sides — it's the identity

## Verification

```bash
bash verify.sh 15432 postgres
```
