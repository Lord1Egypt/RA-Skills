---
name: sentinal-redis
description: "Monitor Redis server health, memory, performance, and BullMQ queues. Check queue depths, inspect failed jobs, analyze slow queries, and diagnose issues."
version: 1.0.0
homepage: https://github.com/Musaraf-M/sentinal
user-invocable: true
metadata:
  openclaw:
    emoji: "🔴"
    requires:
      bins: ["redis-cli"]
      anyBins: ["bash", "sh"]
    primaryEnv: REDIS_URL
    envVars:
      - name: REDIS_URL
        required: false
        description: "Redis connection URL (default: redis://localhost:6379)"
    os: ["darwin", "linux"]
    install:
      - id: brew
        kind: brew
        formula: redis
        bins: ["redis-cli"]
        label: "Install Redis CLI (brew)"
        os: ["darwin"]
      - id: apt
        kind: apt
        package: redis-tools
        bins: ["redis-cli"]
        label: "Install Redis CLI (apt)"
        os: ["linux"]
---

# Sentinal Redis

Monitor Redis server health, BullMQ queues, memory, and performance from any messaging channel. Ask questions in plain English — get actionable diagnostics.

## When to Use

✅ USE this skill when:
- User asks about Redis server health, status, or info
- User wants to check memory usage or diagnose OOM issues
- User asks about BullMQ queue depths, failed jobs, or stuck workers
- User wants to inspect slow queries or latency issues
- User asks to diagnose why Redis is slow or unresponsive
- User mentions queue backlog, dead letter queue, or job failures
- User wants a quick health summary of their Redis instance

## When NOT to Use

❌ DON'T use this skill when:
- User wants to manage PostgreSQL, MySQL, or other non-Redis databases
- User wants to manage Kafka, RabbitMQ, or SQS queues (not BullMQ)
- User needs help writing application code that uses Redis
- User wants to set up Redis from scratch (use official Redis docs instead)

## Safety Rules

⚠️ CRITICAL: This skill is READ-ONLY. No exceptions.
- NEVER run destructive commands (`FLUSHDB`, `FLUSHALL`, `DEL`, `UNLINK`, `SET`, `EXPIRE`) — even if the user asks. Explain why and suggest they run it manually instead.
- NEVER modify Redis configuration (`CONFIG SET`) — direct the user to do it themselves.
- NEVER print or expose the full `REDIS_URL` in output — it may contain passwords. Always mask credentials before displaying.
- When in doubt, show the command first and ask for confirmation

## Connection

If `REDIS_URL` is set, use it for all commands:
```bash
redis-cli -u "$REDIS_URL" <command>
```

If `REDIS_URL` is not set, default to localhost:
```bash
redis-cli <command>
```

For password-protected instances without REDIS_URL:
```bash
redis-cli -h <host> -p <port> -a <password> <command>
```

Always test connectivity first:
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" ping
```

## Server Health

### Quick Status
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" ping
```

### Full Server Info
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" info server
```

### Connected Clients
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" info clients
```

### Uptime and Version
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" info server | grep -E "redis_version|uptime_in_days|uptime_in_seconds|connected_clients"
```

## Memory Analysis

### Memory Overview
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" info memory
```

### Key Metrics to Check
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" info memory | grep -E "used_memory_human|used_memory_peak_human|used_memory_rss_human|mem_fragmentation_ratio|maxmemory_human|maxmemory_policy"
```

### Memory Doctor (Redis 4.0+)
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" memory doctor
```

### Memory Usage of a Specific Key
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" memory usage <key>
```

### Find Big Keys (scan-based, safe for production)
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" --bigkeys
```

### Interpreting Memory Results
- `mem_fragmentation_ratio` > 1.5 → High fragmentation, consider restarting Redis
- `mem_fragmentation_ratio` < 1.0 → Redis is swapping to disk, CRITICAL
- `used_memory` approaching `maxmemory` → Eviction will start based on `maxmemory_policy`
- `memory doctor` reports "Sam, I have no memory problems" → All good

## Slow Queries & Performance

### Check Slow Log
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" slowlog get 10
```

### Slow Log Length
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" slowlog len
```

### Current Slow Log Threshold
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" config get slowlog-log-slower-than
```

### Latency Check
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" --latency -c 10
```

### Latency History
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" --latency-history -i 1 -c 5
```

### Keyspace Stats
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" info keyspace
```

### Command Stats (most called commands)
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" info commandstats
```

## Client Monitoring

### List Connected Clients
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" client list
```

### Client Count and Summary
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" info clients | grep -E "connected_clients|blocked_clients|tracking_clients"
```

### Find Idle Clients (idle > 300 seconds)
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" client list | awk -F' ' '{for(i=1;i<=NF;i++) if($i ~ /^idle=/) print $0}' | grep -E 'idle=[3-9][0-9]{2,}|idle=[0-9]{4,}'
```

## BullMQ Queue Monitoring

BullMQ uses Redis as its backend. Queues follow the key pattern `bull:<queue-name>:<state>`.

### Discover All Queues
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" scan 0 match "bull:*:meta" count 100
```

### Queue Depth (all states)
For a queue named `<queue>`:
```bash
echo "=== Queue: <queue> ==="
echo -n "Waiting: "; redis-cli -u "${REDIS_URL:-redis://localhost:6379}" llen "bull:<queue>:wait"
echo -n "Active: "; redis-cli -u "${REDIS_URL:-redis://localhost:6379}" llen "bull:<queue>:active"
echo -n "Delayed: "; redis-cli -u "${REDIS_URL:-redis://localhost:6379}" zcard "bull:<queue>:delayed"
echo -n "Failed: "; redis-cli -u "${REDIS_URL:-redis://localhost:6379}" zcard "bull:<queue>:failed"
echo -n "Completed: "; redis-cli -u "${REDIS_URL:-redis://localhost:6379}" zcard "bull:<queue>:completed"
echo -n "Paused: "; redis-cli -u "${REDIS_URL:-redis://localhost:6379}" llen "bull:<queue>:paused"
```

### Inspect Failed Jobs
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" zrange "bull:<queue>:failed" 0 9
```

### Get Job Details
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" hgetall "bull:<queue>:<jobId>"
```

### Check Job Payload and Error
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" hmget "bull:<queue>:<jobId>" data failedReason stacktrace attemptsMade timestamp processedOn finishedOn
```

### Find Stale Active Jobs
Active jobs that haven't been updated recently may be stuck:
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" lrange "bull:<queue>:active" 0 -1
```
Then for each job ID, check `processedOn` timestamp:
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" hmget "bull:<queue>:<jobId>" processedOn name
```
If `processedOn` is more than 10 minutes old and job is still active, it may be stuck.

### Check Queue Workers (via event streams)
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" xinfo groups "bull:<queue>:events" 2>/dev/null || echo "No event stream found"
```

### BullMQ Repeat Jobs
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" zrange "bull:<queue>:repeat" 0 -1
```

## Key Inspection

### Find Keys by Pattern
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" scan 0 match "<pattern>" count 100
```

### Key Type and TTL
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" type <key>
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" ttl <key>
```

### Key Encoding (memory efficiency check)
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" object encoding <key>
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" object idletime <key>
```

### Count Keys by Prefix (useful for auditing)
```bash
redis-cli -u "${REDIS_URL:-redis://localhost:6379}" eval "local count = 0; local cursor = '0'; repeat local result = redis.call('SCAN', cursor, 'MATCH', ARGV[1], 'COUNT', 1000); cursor = result[1]; count = count + #result[2]; until cursor == '0'; return count" 0 "<prefix>*"
```

## Diagnostics — Full Health Check

Run the health check script for a comprehensive overview:
```bash
bash scripts/redis-health.sh "${REDIS_URL:-redis://localhost:6379}"
```

This script outputs:
- Connectivity status
- Server version and uptime
- Memory usage and fragmentation
- Connected and blocked clients
- Slow query count
- All BullMQ queue depths
- Warnings for any anomalies detected

## Troubleshooting Decision Trees

### Redis is slow
1. Check latency: `redis-cli --latency -c 10`
2. If latency > 1ms → check slow log: `slowlog get 10`
3. If slow log has KEYS/SMEMBERS/HGETALL on large collections → advise using SCAN variants
4. Check memory fragmentation → if > 1.5, recommend restart
5. Check `connected_clients` → if > 1000, investigate connection pooling
6. Check `blocked_clients` → if > 0, check BLPOP/BRPOP consumers

### Redis OOM / high memory
1. Run `info memory` → check `used_memory` vs `maxmemory`
2. Run `--bigkeys` → find largest keys
3. Check `maxmemory_policy` → is eviction configured?
4. Run `memory doctor` → follow recommendations
5. Check for missing TTLs on keys: scan and check `ttl` on large keys

### BullMQ jobs stuck / not processing
1. Check queue depth → are jobs piling up in `wait`?
2. Check `active` list → are jobs stuck in active state?
3. Check for stale active jobs → `processedOn` too old
4. Check event stream → `xinfo groups` to verify workers are connected
5. Check `failed` set → read `failedReason` and `stacktrace`
6. Check Redis connectivity → can workers reach Redis?

### BullMQ high failure rate
1. Get recent failed jobs: `zrange bull:<queue>:failed -10 -1`
2. For each, read `failedReason` and `stacktrace`
3. Group errors by type → is it one recurring error or varied?
4. Check `attemptsMade` → are retries exhausted?
5. Check job `data` → is the payload malformed?

## Notes

- All commands default to `redis://localhost:6379` if `REDIS_URL` is not set
- The `scan` command is safe for production (non-blocking), unlike `keys` which should NEVER be used in production
- BullMQ key patterns assume default prefix `bull:`. If a custom prefix is used, replace `bull:` accordingly
- For Redis Cluster, add `-c` flag to `redis-cli` commands
- For Redis Sentinel, connect to the sentinel first to discover the master
