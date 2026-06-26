# Temporary Maintenance Channel via ToxTunnel

## Scenario

A contractor or external team member needs short-term access to a specific service (SSH, database, web admin) for maintenance work. You want to grant access quickly, keep it scoped, and revoke it cleanly when done.

## Key Principles

- **Scoped access**: only the specific service port, only the contractor's friend key
- **Time-limited**: agree on a window, revoke promptly after
- **Auditable**: enable logging on the server
- **Least privilege**: read-only DB accounts when possible

## Server Config

```yaml
mode: server
data_dir: /etc/toxtunnel/server
logging:
  level: info
  file: /var/log/toxtunnel/server.log    # audit trail
tox:
  udp_enabled: true
  bootstrap_mode: auto
server:
  rules_file: /etc/toxtunnel/rules.yaml
```

## Rules (contractor-scoped)

```yaml
rules:
  # Contractor: Jane Doe — SSH access only — valid until 2026-04-01
  - friend: "AABBCCDD...contractor-64-char-hex-public-key...EEFF"
    allow:
      - host: "127.0.0.1"
        ports: [22]
```

The comment with the date is for your reference — toxtunnel does not enforce time limits. You must manually revoke.

## Client Config (provided to contractor)

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
    - local_port: 2222
      remote_host: 127.0.0.1
      remote_port: 22
```

## Onboarding Steps

1. Ask contractor to install toxtunnel
2. Contractor starts their client once to generate identity: `toxtunnel -m client -c client.yaml` (will fail to connect but creates `tox_save.dat`)
3. Contractor shares their public key (from startup log)
4. You add their key to `rules.yaml` and restart server
5. Share your server Tox ID with the contractor
6. Contractor updates `server_id` and restarts client
7. Verify: contractor runs `ssh -p 2222 user@127.0.0.1`

## Revocation Checklist

When maintenance is complete:

1. **Remove the contractor's rule** from `rules.yaml`
2. **Hot-reload the server (no restart needed in v0.3.0+):**
   - POSIX: `toxtunnel reload` or `kill -HUP $(cat /etc/toxtunnel/toxtunnel.pid)`
   - Windows (Administrator): `toxtunnel.exe reload -c 'C:\ProgramData\ToxTunnel\config.yaml'`
   - Verify the reload landed: grep the log for `config reloaded (rules: N rules)`
   - Existing tunnels keep flowing; new TUNNEL_OPEN frames from the revoked friend are denied immediately
   - Fallback path if reload isn't available: `sudo systemctl restart toxtunnel` (drops all open tunnels)
3. **Revoke DB access** if applicable: `DROP USER contractor_readonly;`
4. **Review logs**: `grep "contractor-key-prefix" /var/log/toxtunnel/server.log`
5. **Confirm via inspect**: `toxtunnel inspect tunnels` — the contractor should no longer appear as a friend with open tunnels
6. **Optional**: remove the contractor as a Tox friend (requires tox_save.dat editing or fresh identity)

## Multiple Contractors

Add one rule per contractor, each with their own friend key:

```yaml
rules:
  # Contractor A — SSH only — valid until 2026-04-01
  - friend: "AAAA...64hex..."
    allow:
      - host: "127.0.0.1"
        ports: [22]

  # Contractor B — PostgreSQL only — valid until 2026-04-15
  - friend: "BBBB...64hex..."
    allow:
      - host: "127.0.0.1"
        ports: [5432]
```

## Verification

```bash
bash verify.sh 2222 ssh
```
