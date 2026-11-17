# queue-aiops — CLI reference

All read commands print JSON. All write commands support `--dry-run` and
double-confirm before executing through the governed MCP twins (audited).
`--target/-t <name>` selects a target from config; omitted = the first target.

## Top level

```bash
queue-aiops init                 # onboarding wizard (targets + encrypted secrets)
queue-aiops doctor [--skip-auth] # config/secret/connectivity check (PING / /api/overview)
queue-aiops overview [-t T]      # one-shot health summary (platform-dispatched)
queue-aiops mcp                  # run the MCP server (stdio)
```

## Secrets

```bash
queue-aiops secret set <target>    # add/update an encrypted secret
queue-aiops secret list            # names only — values are never printed
queue-aiops secret rm <target>
queue-aiops secret migrate         # legacy .env / env vars → encrypted store
queue-aiops secret rotate-password
```

## redis

```bash
queue-aiops redis info                      # version, role, clients, ops/sec, hit rate
queue-aiops redis memory                    # used vs maxmemory, policy, fragmentation
queue-aiops redis clients                   # clients grouped by source
queue-aiops redis slowlog [-n 128]          # slowest entries first
queue-aiops redis config-get "maxmemory*"   # CONFIG GET glob
queue-aiops redis keyspace                  # per-db keys + expiry coverage
queue-aiops redis bigkeys [--top 20]        # SCAN-budgeted big-key sample

# writes (dry-run + double-confirm; audited via the governed twins)
queue-aiops redis config-set maxmemory-policy allkeys-lru [--dry-run]
queue-aiops redis kill-client --id 77 [--dry-run]
queue-aiops redis kill-client --addr 10.0.0.5:5000 [--dry-run]
```

## rabbitmq

```bash
queue-aiops rabbitmq overview                    # totals + rates + churn
queue-aiops rabbitmq queues [--vhost /]          # deepest backlog first
queue-aiops rabbitmq queue <name> [--vhost /]    # one queue's detail
queue-aiops rabbitmq connections                 # grouped by peer host
queue-aiops rabbitmq channels                    # most unacked first
queue-aiops rabbitmq policies [--vhost /]
queue-aiops rabbitmq nodes                       # memory/disk/fd + alarms

# writes (dry-run + double-confirm; audited via the governed twins)
queue-aiops rabbitmq declare-queue <name> [--vhost /] [--durable/--transient] [--auto-delete]
queue-aiops rabbitmq purge <name> [--vhost /] [--dry-run]          # HIGH risk
queue-aiops rabbitmq delete-queue <name> [--vhost /] [--dry-run]   # HIGH risk
queue-aiops rabbitmq set-policy <name> '<pattern>' '{"max-length": 100000}' \
    [--vhost /] [--priority 0] [--apply-to queues] [--dry-run]
queue-aiops rabbitmq delete-policy <name> [--vhost /] [--dry-run]
```

`QUEUE_AUDIT_APPROVED_BY` / `QUEUE_AUDIT_RATIONALE` are optional — set them to
record who ran a write and why on the audit row (never required, never block):

```bash
export QUEUE_AUDIT_APPROVED_BY="alice"
export QUEUE_AUDIT_RATIONALE="INC-1234: drain the poison-message queue"
```

## analyze (flagship RCAs)

```bash
queue-aiops analyze memory  [--used-pct 85]   # redis memory-pressure RCA
queue-aiops analyze latency [--slow-us 10000] # redis latency/slowlog RCA
queue-aiops analyze backlog [--vhost /] [--top 20]  # rabbitmq queue-backlog RCA
queue-aiops analyze churn                     # connection churn (both platforms)
```
