# redis

**Redis Command Reference & Connection Tool** — Instantly look up Redis commands, test your connection, and monitor key statistics. Works offline too — shows the full cheatsheet even without a Redis instance.

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `cheatsheet` | Display Redis command reference by category | `cheatsheet` / `cheatsheet string` |
| `test` | Test a Redis connection and show server info | `test` / `test redis://localhost:6379` |
| `monitor` | Show key count and memory stats per DB | `monitor` / `monitor localhost 6379` |

## Usage

```bash
bash script.sh cheatsheet [category]
bash script.sh test [host] [port] [password]
bash script.sh monitor [host] [port] [password]
```

## Categories for `cheatsheet`

| Category | Commands Covered |
|----------|-----------------|
| `string` | SET, GET, MSET, INCR, APPEND, STRLEN, SETNX… |
| `list` | LPUSH, RPUSH, LRANGE, LLEN, LPOP, BRPOP… |
| `hash` | HSET, HGET, HMGET, HGETALL, HDEL, HKEYS… |
| `set` | SADD, SMEMBERS, SISMEMBER, SUNION, SINTER… |
| `zset` | ZADD, ZRANGE, ZRANK, ZSCORE, ZREM, ZCOUNT… |
| `key` | DEL, EXISTS, EXPIRE, TTL, RENAME, TYPE, SCAN… |
| `server` | INFO, DBSIZE, CONFIG GET, FLUSHDB, DEBUG… |
| `scripting` | EVAL, EVALSHA, SCRIPT LOAD/EXISTS/FLUSH |

## Requirements

- `bash` >= 4.0
- `redis-cli` (optional — required only for `test` and `monitor` commands; offline mode activates automatically if not found)

## Install Redis CLI

```bash
# Debian/Ubuntu
sudo apt install redis-tools

# macOS
brew install redis

# Alpine
apk add redis
```

## Examples

```
$ bash script.sh cheatsheet string

🔴 Redis Cheatsheet — Strings
─────────────────────────────────────────────
SET key value [EX seconds] [PX ms] [NX|XX]
  Set key to value. Options: EX (expire secs), NX (only if not exists)
  Example: SET user:1:name "Alice" EX 3600

GET key
  Get the value of a key. Returns nil if not exists.
  Example: GET user:1:name

MSET key value [key value ...]
  Set multiple keys atomically.
  Example: MSET k1 v1 k2 v2 k3 v3
...
```

```
$ bash script.sh test localhost 6379

🔴 Redis Connection Test
─────────────────────────────────────────────
Host     : localhost
Port     : 6379
Status   : ✅ CONNECTED

Server Info:
  redis_version  : 7.2.3
  uptime_days    : 4
  connected_clients: 3
  used_memory    : 1.23M
  maxmemory      : 0 (unlimited)
  role           : master
  aof_enabled    : 0
```

```
$ bash script.sh monitor

🔴 Redis Key Monitor
─────────────────────────────────────────────
Host     : localhost:6379

DB   Keys   Avg TTL
────────────────────
db0  1247   —
db1  89     —

Total keys : 1336
Memory     : 4.56M
```
