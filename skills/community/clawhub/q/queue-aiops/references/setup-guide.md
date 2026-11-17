# queue-aiops — setup guide

## 1. Install

```bash
uv tool install queue-aiops     # or: pipx install queue-aiops / pip install queue-aiops
```

Python >= 3.11.

## 2. Prepare the brokers

### redis

Any reachable redis 5.x–7.x instance works. Auth is optional:

- **No password (lab)**: nothing to prepare — the wizard accepts an empty
  password and connects without `AUTH`.
- **Password**: the value of `requirepass` (or an ACL user's password). TLS
  deployments (`rediss://`) are supported via the wizard's TLS prompt.

The tool only ever issues a typed allow-list of commands (INFO, SLOWLOG,
CLIENT, CONFIG, MEMORY, SCAN, DBSIZE, PING) — reads are safe on production,
and key sampling is SCAN-budgeted, never `KEYS *`.

### rabbitmq

Enable the management plugin and create (or reuse) a user with at least the
`monitoring` tag (reads) — the `management`/`policymaker` tag is needed for
policy writes, and queue purge/delete needs configure permission on the vhost:

```bash
rabbitmq-plugins enable rabbitmq_management
rabbitmqctl add_user queueops 'a-strong-password'
rabbitmqctl set_user_tags queueops monitoring
rabbitmqctl set_permissions -p / queueops "" "" ".*"   # read-only example
```

The management API listens on 15672 (HTTP) / 15671 (HTTPS) by default.

## 3. Onboard

```bash
queue-aiops init
```

The wizard asks for:

1. **Master password** — encrypts `~/.queue-aiops/secrets.enc` (Fernet +
   scrypt). Export `QUEUE_AIOPS_MASTER_PASSWORD` for non-interactive/MCP use.
2. **Targets** — name, platform (`redis`/`rabbitmq`), host, port (defaults
   6379/15672), redis db index, TLS (verify defaults to **true**; answer No
   for self-signed lab certs), rabbitmq management user, and the secret
   (hidden prompt; empty = auth-less redis).
3. It offers to run `doctor` to confirm connectivity right away.

Config lands in `~/.queue-aiops/config.yaml`:

```yaml
targets:
  - name: cache1
    platform: redis
    host: 10.0.0.10
    port: 6379
    username: ""
    db: 0
    use_tls: false
    verify_ssl: true
  - name: broker1
    platform: rabbitmq
    host: 10.0.0.20
    port: 15672
    username: queueops
    db: 0
    use_tls: false
    verify_ssl: true
```

## 4. Verify

```bash
queue-aiops doctor
```

Checks config, the encrypted store (and its 600 permissions), per-target
secrets (a missing redis secret is a *warning* — auth-less lab mode), and live
connectivity: `PING` for redis, `GET /api/overview` for rabbitmq. Exit code 0
= healthy.

## 5. Wire up MCP

```json
{
  "mcpServers": {
    "queue-aiops": {
      "command": "uvx",
      "args": ["--from", "queue-aiops", "queue-aiops-mcp"],
      "env": {
        "QUEUE_AIOPS_MASTER_PASSWORD": "your-master-password"
      }
    }
  }
}
```

MCP clients start the server with a minimal environment — put everything it
needs (`QUEUE_AIOPS_MASTER_PASSWORD`, a relocated `QUEUE_AIOPS_HOME`, and any
optional `QUEUE_AUDIT_APPROVED_BY`/`QUEUE_AUDIT_RATIONALE` audit annotations) in
that `env` block.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `No secret for target 'x'` | `queue-aiops secret set x` or re-run `init` (redis targets may legitimately have none) |
| Redis `AUTH` errors | The stored password is wrong — `queue-aiops secret set <target>` |
| 401/403 from the management API | Wrong user/password, or the user lacks the `monitoring`/`management` tag or vhost access |
| 404 on a queue/policy | Stale name, or the vhost is wrong — remember the default vhost is `/` |
| Write rejected by the broker | The connecting user lacks configure/write permission (or the Redis ACL forbids the command) — grant it, or connect a user that has it |
| Master-password prompt in MCP | Export `QUEUE_AIOPS_MASTER_PASSWORD` in the MCP `env` block |
