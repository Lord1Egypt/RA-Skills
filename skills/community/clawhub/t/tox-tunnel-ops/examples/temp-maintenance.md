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
data_dir: /var/lib/toxtunnel        # mutable state — NOT under /etc
logging:
  level: info
  file: /var/log/toxtunnel/server.log    # audit trail
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
      local_address: 127.0.0.1
      remote_host: 127.0.0.1
      remote_port: 22
```

> ### ⚠️ `local_port: 2222` binds `0.0.0.0` without `local_address` (pre-v0.5.0) on the contractor's machine
>
> Before v0.5.0, without `local_address` the listener binds every IPv4
> interface. Anyone on the contractor's network can reach your sshd through their
> machine. On **v0.4.13+** set `local_address: 127.0.0.1` (the config above does); on v0.4.12 and older no such key exists — firewall it instead. Make firewalling the port to loopback
> part of the onboarding instructions.

## Onboarding Steps

1. Ask contractor to install toxtunnel
2. Contractor generates their identity and prints their Tox ID:

   ```bash
   toxtunnel print-id -c client.yaml
   ```

   `print-id` creates and persists `tox_save.dat` if it does not exist (it
   announces `No existing Tox identity at …; creating a new one.` on stderr) and
   prints the 76-char Tox ID.

   **Do not tell them to "start the client once to generate the identity".** With
   `server_id` still the placeholder, the daemon exits *before* it ever
   initialises Tox: server-ID/alias resolution and config validation both run
   ahead of client initialisation, so it prints
   `Unknown server alias '<PASTE_SERVER_TOX_ID_HERE>' …` (or a Tox-ID checksum
   error) and returns 1 with an **empty data directory**. Verified on v0.4.12.
3. Contractor shares that Tox ID. You need the **first 64 hex characters** of it
   as the `friend:` key — not the whole 76-char ID.
4. You add their key to `rules.yaml`, then **hot-reload** the server
   (`toxtunnel reload -c /etc/toxtunnel/server.yaml`) — a restart is not needed
   for a rules change and would drop everyone else's tunnels
5. Share your server Tox ID with the contractor
6. Contractor pastes it into `server_id` and starts the client
7. Verify: contractor runs `ssh -p 2222 user@127.0.0.1`

## Revocation Checklist

**Decide first which of these you actually need — they are not the same thing:**

| Goal | Mechanism | Effect on the contractor's live session |
|------|-----------|------------------------------------------|
| Stop them opening anything **new** | Edit `rules.yaml` + `toxtunnel reload` | **None — it keeps working** |
| End their access **right now** | Revoke at the service, and/or restart the server | Session dies |

A hot-reload denies future `TUNNEL_OPEN` frames only. If the contractor has an
`ssh` session open when you reload, that session keeps flowing until they
disconnect. If "revoke immediately" is the requirement, steps 1–2 are not
sufficient on their own — do step 3 as well.

When maintenance is complete:

1. **Remove the contractor's rule** from `rules.yaml`
2. **Hot-reload the server — blocks NEW sessions only (no restart needed in v0.3.0+):**
   - POSIX: `toxtunnel reload -c /etc/toxtunnel/server.yaml` (or
     `kill -HUP $(cat <data_dir>/toxtunnel.pid)` — the pid file lives in the
     daemon's `data_dir`, not next to the config)
   - Windows (Administrator): `toxtunnel.exe reload -c 'C:\ProgramData\ToxTunnel\config.yaml'`
   - Verify the reload landed: grep the server log for `config reloaded (rules: N rules)`
   - Existing tunnels keep flowing; new TUNNEL_OPEN frames from the revoked friend are denied immediately
   - Fallback path if reload isn't available: `sudo systemctl restart toxtunnel` (drops all open tunnels)
3. **To terminate access that is live right now** (only if required — steps 1–2
   do not do this):
   - Revoke at the service, which is the surgical option and affects nobody else:
     - SSH: lock the account (`usermod -L contractor` / `passwd -l`), remove their
       key from `authorized_keys`, then kill their sessions
       (`pkill -u contractor sshd`)
     - PostgreSQL: `ALTER ROLE contractor_readonly NOLOGIN;` then
       `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE usename = 'contractor_readonly';`
     - MySQL: `ALTER USER 'contractor'@'%' ACCOUNT LOCK;` then `KILL <id>;` per connection
   - Or restart the toxtunnel server: `sudo systemctl restart toxtunnel`. This
     drops **every** tunnel for **every** friend, so it is a blunt instrument —
     use it when the contractor is the only user, or when you cannot revoke at
     the service
4. **Drop the DB user** if applicable: `DROP USER contractor_readonly;`
5. **Review logs**: `grep "contractor-key-prefix" /var/log/toxtunnel/server.log`.
   Note this shows tunnel-level events only — which tunnels opened, to what
   target, how many bytes. It does not record what the contractor *did* inside
   the session; for that you need the service's own audit trail
6. **Confirm via inspect**: `toxtunnel inspect tunnels` — if any of the
   contractor's tunnels are still listed after a reload, that is expected
   behaviour, not a failed revocation. They disappear when the client
   disconnects or when you do step 3
7. **Optional**: remove the contractor as a Tox friend (requires tox_save.dat
   editing or a fresh identity). Rarely worth it — the rules engine
   default-denies an unlisted key, so a leftover friend entry grants nothing,
   and deleting it can deadlock a future re-grant

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
bash scripts/verify.sh 2222 ssh client.yaml
```

Run this from the skill root (the script lives at `scripts/verify.sh`).
Passing the client config lets it read `friends_online` from the running
daemon instead of guessing from a local TCP accept.

**Judge it by the exit code:** `0` = the remote service answered through the
tunnel, `2` = local checks passed but end-to-end was **not** proven (do not
report this as working), `1` = a check failed.
