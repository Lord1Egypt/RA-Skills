---
name: cm-redis-cluster-analyzer
description: Analyze Redis Sentinel and Cluster configurations for high availability, performance, and memory efficiency. Checks sentinel topology, cluster slot distribution, memory policies, persistence settings, connection pooling, replication lag, and key patterns. Use when asked to review Redis config, audit Redis cluster, check sentinel setup, optimize Redis memory, review Redis HA, troubleshoot Redis failover, or analyze Redis performance. Triggers on "redis", "redis cluster", "redis sentinel", "redis ha", "redis memory", "redis config", "redis failover", "redis replication", "redis performance", "redis audit".
metadata:
  tags: ["redis", "cache", "database", "sentinel", "cluster", "high-availability", "memory", "performance", "replication", "infrastructure"]
---

# Redis Cluster Analyzer

Analyze Redis Sentinel and Cluster configurations for high availability, performance, and memory efficiency. Reviews sentinel topology, cluster slot distribution, replication health, memory policies, persistence settings, connection pooling, and key design patterns. Acts as a senior infrastructure engineer auditing your Redis deployment for production readiness.

## Usage

Invoke this skill when you need to review Redis configurations, validate HA setup, optimize memory usage, or troubleshoot failover issues.

**Basic invocation:**
> Analyze the Redis configuration files in /etc/redis/
> Review this Redis Sentinel setup for high availability
> Audit Redis Cluster configuration for production readiness

**Focused analysis:**
> Check memory policies and eviction strategy
> Audit sentinel failover configuration
> Review cluster slot distribution for hotspots
> Analyze connection pooling settings

The agent reads Redis configuration files, sentinel configs, cluster node definitions, and application connection code, then produces a comprehensive quality report.

## How It Works

### Step 1: Discover and Parse Redis Configuration

The agent locates all Redis-related configuration:

```bash
# Find Redis configuration files
find /etc/redis/ -name "*.conf" -type f
find /path/to/project/ -name "redis*.conf" -o -name "sentinel*.conf"

# Find application Redis connection code
grep -rl "Redis\|redis\|ioredis\|redis-py\|RedisCluster" /path/to/app/ --include="*.py" --include="*.ts" --include="*.js" --include="*.go"

# Check running Redis processes
redis-cli INFO server 2>/dev/null
redis-cli CLUSTER INFO 2>/dev/null
redis-cli SENTINEL masters 2>/dev/null
```

The agent parses each configuration to extract:
- **Server configuration** (bind, port, requirepass, maxclients)
- **Memory settings** (maxmemory, maxmemory-policy, lazyfree)
- **Persistence** (RDB snapshots, AOF, hybrid)
- **Replication** (replica-of, repl-backlog-size, min-replicas)
- **Sentinel topology** (masters, quorum, failover-timeout)
- **Cluster settings** (cluster-enabled, node-timeout, migration-barrier)
- **Connection pool config** (from application code)
- **Key patterns** (TTL, naming conventions, data structures)

### Step 2: Audit Sentinel Configuration

For Redis Sentinel deployments, the agent checks HA topology:

```
Sentinel Topology Analysis:

  Sentinels: 3 nodes
    sentinel-1: 10.0.1.10:26379
    sentinel-2: 10.0.1.11:26379
    sentinel-3: 10.0.1.12:26379

  Monitored Masters: 2
    mymaster: 10.0.1.20:6379 (2 replicas)
    cachemaster: 10.0.1.30:6379 (1 replica)

  PASS: 3 sentinels — meets minimum for quorum (need N/2 + 1)
  PASS: Sentinels on separate hosts — survives single-node failure

  FAIL: Master "cachemaster" has only 1 replica
    RISK: If replica fails, no failover target available
    During maintenance on the single replica, master has zero redundancy
    FIX: Add at least 1 more replica for cachemaster

  FAIL: Sentinels co-located with Redis nodes
    sentinel-1 (10.0.1.10) hosts both sentinel and Redis replica
    RISK: Node failure takes out both sentinel and data node
    FIX: Run sentinels on independent infrastructure
```

**Sentinel configuration audit:**

```
Sentinel Config Analysis:

  Master "mymaster":
    sentinel monitor mymaster 10.0.1.20 6379 2
    sentinel down-after-milliseconds mymaster 5000
    sentinel failover-timeout mymaster 60000
    sentinel parallel-syncs mymaster 1

  FAIL: down-after-milliseconds = 5000 (5 seconds)
    Too aggressive — network blips trigger unnecessary failovers
    Each failover causes ~10s of write unavailability
    FIX: sentinel down-after-milliseconds mymaster 30000 (30 seconds)
    Balances detection speed vs. false positive failovers

  WARN: failover-timeout = 60000 (60 seconds)
    If failover fails, retry waits 120 seconds (2x timeout)
    Total downtime in worst case: 3+ minutes
    CONSIDER: failover-timeout 180000 (3 min) for complex resyncs
    Prevents premature failover abort during large dataset sync

  WARN: parallel-syncs = 1
    Only 1 replica syncs from new master at a time after failover
    With 3 replicas, full sync takes 3x single replica sync time
    FIX: parallel-syncs = 2 (if replicas can handle sync load)
    Tradeoff: Faster recovery vs. higher load on new master during sync

  FAIL: No sentinel auth-pass configured
    Sentinels connect to master without authentication
    RISK: Unauthorized sentinel can trigger failover
    FIX: sentinel auth-pass mymaster <password>

  FAIL: No sentinel notification-script configured
    No alerting on failover events
    FIX: sentinel notification-script mymaster /opt/redis/notify.sh
    Script receives: event-type, event-description
    Hook into PagerDuty/Slack for operational awareness

  FAIL: No sentinel client-reconfig-script configured
    Application does not know about master change
    FIX: sentinel client-reconfig-script mymaster /opt/redis/reconfig.sh
    OR: Use Sentinel-aware client library (recommended):
      redis-py: Redis.from_url("redis+sentinel://...")
      ioredis: new Redis({ sentinels: [...], name: "mymaster" })
```

### Step 3: Analyze Cluster Configuration

For Redis Cluster deployments, the agent checks slot distribution and node health:

```
Cluster Topology Analysis:

  Nodes: 6 (3 masters, 3 replicas)
    master-1: 10.0.1.50:6379 — slots 0-5460 (5461 slots)
    master-2: 10.0.1.51:6379 — slots 5461-10922 (5462 slots)
    master-3: 10.0.1.52:6379 — slots 10923-16383 (5461 slots)
    replica-1: 10.0.1.60:6379 — replicates master-1
    replica-2: 10.0.1.61:6379 — replicates master-2
    replica-3: 10.0.1.62:6379 — replicates master-3

  PASS: Slots evenly distributed (5461/5462/5461)
  PASS: Each master has at least 1 replica
  PASS: Replicas on different hosts than their masters
```

**Cluster configuration audit:**

```
Cluster Config Analysis:

  FAIL: cluster-node-timeout = 15000 (15 seconds)
    Too aggressive for cross-AZ deployments
    Network latency spikes between AZs can trigger false failovers
    FIX: cluster-node-timeout 30000 for cross-AZ
    Keep 15000 for single-AZ deployments

  FAIL: cluster-migration-barrier = 1 (default)
    Master with only 1 replica won't donate replica to orphaned master
    If a master loses all replicas, no automatic migration occurs
    FIX: cluster-migration-barrier 0 — allow replica migration when needed
    NOTE: Only effective if some masters have 2+ replicas

  FAIL: cluster-require-full-coverage = yes (default)
    If any slot range has no master, ENTIRE cluster stops accepting writes
    RISK: Single master failure can take down whole cluster
    FIX: cluster-require-full-coverage no
    Allows cluster to serve keys in available slot ranges

  WARN: cluster-allow-reads-when-down = no (default)
    Cluster rejects all operations when marked as down
    FIX: cluster-allow-reads-when-down yes
    Allows read operations during partial failures (stale reads possible)

  WARN: No cluster-announce-ip configured
    In Docker/NAT environments, nodes advertise internal IPs
    Clients outside the network cannot connect
    FIX: Set cluster-announce-ip to external/routable IP

  FAIL: All nodes in same availability zone
    master-1, master-2, master-3 all in us-east-1a
    RISK: AZ failure takes down entire cluster
    FIX: Distribute across 3 AZs:
      AZ-a: master-1, replica-2
      AZ-b: master-2, replica-3
      AZ-c: master-3, replica-1
```

**Key distribution analysis:**

```
Slot Hotspot Analysis:

  WARN: Uneven key distribution detected
    master-1 (slots 0-5460): 2.1M keys, 1.8 GB
    master-2 (slots 5461-10922): 850K keys, 600 MB
    master-3 (slots 10923-16383): 3.2M keys, 2.4 GB

  FAIL: master-3 has 3.8x more keys than master-2
    Likely cause: Hot key prefix hashes to slot range 10923-16383
    Common pattern: All "user:{id}" keys hash similarly
    FIX: Use hash tags to control distribution:
      user:{12345} — hashes on "12345", distributed
      {user}:12345 — hashes on "user", all same slot (BAD)
    OR: Reshard slots to balance memory across masters

  WARN: Large key detected
    Key "cache:product_catalog" — 450 MB (hash with 100K fields)
    RISK: Migration of this key's slot blocks cluster operations
    FIX: Split into smaller keys using key prefixing:
      cache:product_catalog:{category_id}
```

### Step 4: Review Memory Configuration

The agent audits memory settings:

```
Memory Configuration Analysis:

  FAIL: maxmemory not set
    Redis will use all available system memory
    RISK: OOM killer terminates Redis process — data loss
    FIX: maxmemory 4gb (set to ~75% of available RAM)
    Reserve 25% for fork operations (RDB/AOF), OS, and buffer

  FAIL: maxmemory-policy = noeviction (default)
    When maxmemory reached, all write operations return OOM error
    RISK: Application crashes when cache is full
    FIX: Choose policy based on workload:
      allkeys-lru — cache workload, evict least recently used
      volatile-lru — mixed workload, only evict keys with TTL
      allkeys-lfu — frequency-based, better hit rate than LRU
      volatile-ttl — evict keys closest to expiry

  WARN: maxmemory-samples = 5 (default)
    LRU/LFU approximation uses 5 samples — may evict suboptimally
    FIX: maxmemory-samples 10 — better eviction accuracy, minimal CPU cost

  FAIL: lazyfree-lazy-eviction = no
    Eviction blocks the main thread — large key eviction causes latency spike
    FIX: lazyfree-lazy-eviction yes
    AND: lazyfree-lazy-expire yes
    AND: lazyfree-lazy-server-del yes
    AND: lazyfree-lazy-user-del yes
    Lazy-free delegates memory reclamation to background thread

  Memory Efficiency:
    Used memory: 3.2 GB
    Peak memory: 3.8 GB
    Fragmentation ratio: 1.42
    WARN: Fragmentation ratio > 1.2 — 42% wasted memory
    FIX: Set activedefrag yes (Redis 4.0+)
      active-defrag-enabled yes
      active-defrag-threshold-lower 10
      active-defrag-threshold-upper 100
      active-defrag-cycle-min 1
      active-defrag-cycle-max 25
```

### Step 5: Audit Persistence Settings

The agent checks data durability configuration:

```
Persistence Analysis:

  RDB Snapshots:
    save 900 1      — snapshot if 1 change in 15 min
    save 300 10     — snapshot if 10 changes in 5 min
    save 60 10000   — snapshot if 10000 changes in 1 min

  WARN: RDB snapshot frequency may be too aggressive
    save 60 10000 causes fork every 60 seconds under write load
    Fork on 4 GB dataset copies page tables — 100-500ms freeze
    FIX: For cache-only workloads, disable RDB:
      save ""
    For durability, prefer AOF over frequent RDB

  AOF Configuration:
    appendonly no

  FAIL: AOF disabled — data loss window = RDB interval
    With save 300 10, up to 5 minutes of data lost on crash
    FIX: appendonly yes
    appendfsync everysec (good balance of performance and durability)
    auto-aof-rewrite-percentage 100
    auto-aof-rewrite-min-size 64mb

  FAIL: No hybrid persistence (RDB + AOF)
    Redis 4.0+ supports aof-use-rdb-preamble for faster restart
    FIX: aof-use-rdb-preamble yes
    AOF file starts with RDB snapshot, followed by append-only log
    Combines fast restart (RDB) with minimal data loss (AOF)

  WARN: stop-writes-on-bgsave-error = yes
    If RDB snapshot fails, Redis stops accepting writes
    Correct for primary data store, too strict for cache
    FIX: For cache workloads: stop-writes-on-bgsave-error no

  Replica Persistence:
    FAIL: Replicas have RDB enabled (same schedule as master)
    RISK: Fork storm — master and all replicas fork simultaneously
    FIX: Disable RDB on replicas, rely on replication + master RDB:
      replica: save ""
    Exception: Enable on ONE replica for backup purposes
```

### Step 6: Review Connection and Client Settings

The agent checks connection configuration:

```
Connection Analysis:

  FAIL: maxclients = 10000 (default)
    System file descriptor limit: 1024 (ulimit -n)
    Redis needs: maxclients + 32 (internal FDs) = 10032
    But only 1024 FDs available — effective maxclients = 992
    FIX: Increase system limit:
      /etc/security/limits.conf: redis soft nofile 65535
    OR: Reduce maxclients to match available FDs

  FAIL: timeout = 0 (no idle timeout)
    Idle connections never close — accumulate until maxclients reached
    RISK: Connection leak exhausts available connections
    FIX: timeout 300 (close idle connections after 5 minutes)

  WARN: tcp-keepalive = 300 (default)
    Dead connections detected after 5 minutes of silence
    For latency-sensitive apps, reduce to detect failures faster
    FIX: tcp-keepalive 60

  FAIL: No requirepass configured
    Redis accessible without authentication
    RISK: Data exposure, unauthorized access, crypto mining attacks
    FIX: requirepass <strong-password>
    AND: For Redis 6+, use ACL system for fine-grained access:
      user app on >password ~app:* +@read +@write -@admin

  Application Connection Pool:
    Python (redis-py):
      pool = redis.ConnectionPool(max_connections=50)

    WARN: max_connections = 50 per application instance
      With 10 app instances = 500 connections to Redis
      Plus Sentinel connections = ~515 total
      Verify: 515 < maxclients (992 effective)
      PASS: Within limits

    FAIL: No connection timeout configured
      ConnectionPool(max_connections=50)
      FIX: ConnectionPool(
          max_connections=50,
          socket_timeout=5,
          socket_connect_timeout=2,
          retry_on_timeout=True,
          health_check_interval=30,
      )

    FAIL: No retry strategy for connection failures
      Single connection failure raises exception to application
      FIX: Use retry decorator or Retry class:
        from redis.retry import Retry
        from redis.backoff import ExponentialBackoff
        retry = Retry(ExponentialBackoff(), 3)
        Redis(retry=retry, retry_on_error=[ConnectionError, TimeoutError])
```

### Step 7: Analyze Key Design Patterns

The agent reviews key naming and TTL strategy:

```
Key Pattern Analysis:

  FAIL: No consistent key naming convention
    Found patterns: "user:123", "USER_123", "cache-user-123", "u.123"
    FIX: Standardize on colon-delimited hierarchy:
      {service}:{entity}:{id}:{field}
      app:user:123:profile
      app:session:abc-def
      app:cache:products:category:5

  FAIL: 45% of keys have no TTL set
    Total keys: 2.1M, keys without TTL: 945K
    RISK: Memory grows unbounded — keys never evicted (if policy=volatile-*)
    FIX: Set TTL on all cache keys:
      SET key value EX 3600  (1 hour)
    For session data: match session expiry
    For cache: match data freshness requirements

  WARN: TTL distribution skewed
    Keys with TTL < 60s: 12%
    Keys with TTL 60s-1h: 8%
    Keys with TTL 1h-24h: 15%
    Keys with TTL > 24h: 20%
    Keys with no TTL: 45%
    RECOMMEND: Review keys with TTL > 24h — do they need to persist that long?

  FAIL: Large keys detected (> 1 MB)
    cache:all_products — 12 MB (JSON string)
    RISK: Large key operations block event loop (single-threaded)
    GET on 12 MB key takes ~6ms — blocks all other clients
    FIX: Break into smaller keys or use Redis Hash with HSCAN
    OR: Compress before storage: zlib.compress(json.dumps(data))

  WARN: Hot key detected
    cache:homepage_feed — 50K reads/sec from monitoring
    RISK: Single master handles all reads for this key
    FIX: Read from replicas for hot keys:
      Redis(read_from_replicas=True) (cluster mode)
    OR: Implement client-side caching (Redis 6+ client tracking)

  FAIL: Key pattern "lock:*" without TTL safety
    Distributed locks without TTL — if holder crashes, lock held forever
    FIX: Always set TTL on lock keys:
      SET lock:resource value NX EX 30
    Use Redlock algorithm for distributed locking across nodes
```

### Step 8: Review Replication Health

The agent checks replication configuration:

```
Replication Analysis:

  Master: 10.0.1.20:6379
    Connected replicas: 2
    Replication backlog: 1 MB (default)
    Min replicas to write: 0

  FAIL: repl-backlog-size = 1mb (default)
    If replica disconnects for > backlog duration, full resync required
    Full resync on 4 GB dataset: ~30 seconds of high CPU + network
    FIX: repl-backlog-size 256mb
    Size = write_rate_bytes_per_sec * max_acceptable_disconnect_seconds
    At 1 MB/s writes: 256 MB covers 256 seconds of disconnect

  FAIL: min-replicas-to-write = 0 (default)
    Master accepts writes even if ALL replicas are down
    RISK: Data only on master — if master fails, data lost
    FIX: min-replicas-to-write 1
    AND: min-replicas-max-lag 10
    Master rejects writes if no replica acknowledged within 10 seconds

  WARN: Replication lag detected
    replica-1: lag = 0 bytes (healthy)
    replica-2: lag = 45000 bytes (45 KB behind)
    Possible causes: slow network, disk I/O on replica, large key writes
    Monitor: redis-cli INFO replication | grep lag

  WARN: replica-read-only = yes but no replica routing
    Replicas accept read queries but application only connects to master
    FIX: Route reads to replicas to reduce master load:
      Python: Redis(host=master, port=6379).slave_for("mymaster")
      Node: new Redis({ role: "slave", preferredSlaves: [...] })

  FAIL: replica-lazy-flush = no
    Full resync flushes replica synchronously — blocks for seconds on large DB
    FIX: replica-lazy-flush yes — flush in background thread
```

### Step 9: Security Audit

The agent evaluates security configuration:

```
Security Analysis:

  FAIL: protected-mode = no
    Redis accessible from any network interface
    FIX: protected-mode yes (when bind is set)
    OR: Ensure bind 127.0.0.1 or specific internal IPs

  FAIL: bind 0.0.0.0
    Listening on all interfaces including public
    RISK: Internet-accessible Redis — common crypto mining target
    FIX: bind 127.0.0.1 10.0.1.20 (localhost + internal network only)

  FAIL: No TLS configured
    Data in transit is unencrypted — visible to network sniffers
    FIX: For Redis 6+:
      tls-port 6380
      tls-cert-file /etc/redis/tls/redis.crt
      tls-key-file /etc/redis/tls/redis.key
      tls-ca-cert-file /etc/redis/tls/ca.crt
      port 0 (disable non-TLS port)

  FAIL: Using single password (requirepass) instead of ACL
    All clients share one password with full access
    FIX: Use Redis ACL (6.0+) for least-privilege access:
      user app-read on >readpass ~app:cache:* +@read -@all
      user app-write on >writepass ~app:* +@read +@write -@admin
      user admin on >adminpass ~* +@all

  WARN: rename-command used for security
    rename-command FLUSHALL ""
    rename-command CONFIG ""
    NOTE: rename-command is deprecated in Redis 7+
    FIX: Use ACL to restrict dangerous commands instead:
      user default on >pass -FLUSHALL -FLUSHDB -CONFIG -DEBUG
```

### Step 10: Produce the Analysis Report

The agent generates a comprehensive report:

```
# Redis Configuration Analysis Report
# Deployment: Sentinel | Date: April 30, 2026

## Overview
  Deployment type: Sentinel (3 sentinels, 1 master, 2 replicas)
  Redis version: 7.2
  Total memory: 3.2 GB used / 4 GB max
  Total keys: 2.1M
  Connected clients: 127

## Overall Health Score: 48/100

## Category Scores
  Sentinel/Cluster Config: 5/10  (aggressive timeouts, no alerting)
  Memory Management:       4/10  (no eviction policy, fragmentation)
  Persistence:             4/10  (AOF disabled, fork storm risk)
  Connection Settings:     5/10  (no timeout, no auth, no TLS)
  Replication:             5/10  (small backlog, no min-replicas)
  Key Design:              4/10  (no TTL, large keys, hot keys)
  Security:                3/10  (no TLS, no ACL, bound to 0.0.0.0)
  Performance:             6/10  (lazy-free disabled, no defrag)

## Critical Issues
  1. No authentication — Redis accessible without password
  2. Bound to 0.0.0.0 — exposed to public network
  3. maxmemory-policy noeviction — writes fail when memory full
  4. AOF disabled — up to 5 minutes of data loss on crash
  5. Replication backlog 1 MB — full resync on brief disconnect

## Recommendations Summary
  Estimated effort: 2-3 days for critical + high priority fixes
  Expected improvement: 48 -> 82 health score
  Risk reduction: Eliminates security exposure and data loss scenarios
```

## Output

The agent produces:

- **Health score**: 0-100 overall Redis configuration quality rating
- **Category scores**: granular ratings for each quality dimension
- **Topology diagram**: text-based visualization of Sentinel/Cluster layout
- **Critical issues**: problems that pose availability or security risk
- **Memory analysis**: usage, fragmentation, eviction, and key distribution
- **Persistence review**: RDB/AOF configuration with durability assessment
- **Replication health**: lag, backlog, and failover readiness
- **Security audit**: authentication, encryption, and access control
- **Remediation config**: exact redis.conf directives to fix each issue
- **Priority matrix**: issues ranked by risk and effort

## Deployment Type Support

| Feature | Standalone | Sentinel | Cluster |
|---------|-----------|----------|---------|
| HA analysis | N/A | Full sentinel audit | Slot + node analysis |
| Failover review | N/A | Quorum, timeouts | Node-timeout, migration |
| Memory analysis | Single node | Master + replicas | Per-shard distribution |
| Key distribution | N/A | N/A | Slot hotspot detection |
| Scaling advice | Vertical only | Add replicas | Reshard + add nodes |

## Tips for Best Results

- Provide both redis.conf and sentinel.conf for complete analysis
- Include application connection code for pool configuration review
- Share Redis INFO output for runtime metrics correlation
- For Cluster deployments, provide all node configurations
- Run during peak traffic hours for realistic hotspot detection
- Combine with slow log analysis (SLOWLOG GET) for performance correlation
