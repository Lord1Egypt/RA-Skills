#!/usr/bin/env bash
# redis skill - Redis command cheatsheet, connection test, key monitor
# Usage: bash script.sh <cheatsheet|test|monitor> [args...]
set -euo pipefail

COMMAND="${1:-}"
ARG1="${2:-localhost}"
ARG2="${3:-6379}"
ARG3="${4:-}"

BOLD='\033[1m'
RED_C='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RESET='\033[0m'

SEP="─────────────────────────────────────────────"
REDIS_ICON="🔴"

usage() {
  cat <<EOF
${BOLD}redis skill${RESET} — Redis command reference & connection tool

Commands:
  cheatsheet [category]         Show Redis command reference
  test [host] [port] [pass]     Test Redis connection
  monitor [host] [port] [pass]  Show key statistics per DB

Categories: string  list  hash  set  zset  key  server  scripting

Examples:
  bash script.sh cheatsheet
  bash script.sh cheatsheet string
  bash script.sh test localhost 6379
  bash script.sh monitor 127.0.0.1 6379 mypassword
EOF
  exit 0
}

# ── Cheatsheet content ───────────────────────────────────────────────────────

show_cheatsheet_string() {
  cat <<'EOF'

STRING COMMANDS
───────────────

SET key value [EX seconds] [PX ms] [NX|XX]
  Set key to value. Options:
    EX  — expire in seconds
    PX  — expire in milliseconds
    NX  — only set if key does NOT exist
    XX  — only set if key DOES exist
  Example: SET user:1:name "Alice" EX 3600

GET key
  Get the value of a key. Returns nil if not exists.
  Example: GET user:1:name

MSET key value [key value ...]  /  MGET key [key ...]
  Set / get multiple keys atomically.
  Example: MSET k1 v1 k2 v2
           MGET k1 k2

INCR key  /  INCRBY key n  /  INCRBYFLOAT key f
  Atomically increment a numeric value.
  Example: INCR pageviews:home
           INCRBY stock:item1 -5

APPEND key value
  Append value to existing string.
  Example: APPEND log:today "entry\n"

STRLEN key
  Return the length of the string at key.
  Example: STRLEN user:1:name

SETNX key value
  Set key only if it does not exist (legacy; use SET ... NX).
  Example: SETNX lock:job 1

GETEX key [EX s|PX ms|EXAT ts|PERSIST]
  Get value and set/reset expiry (Redis 6.2+).
  Example: GETEX session:abc EX 1800

GETDEL key
  Get value and delete the key atomically.
  Example: GETDEL one_time_token
EOF
}

show_cheatsheet_list() {
  cat <<'EOF'

LIST COMMANDS
─────────────

LPUSH key val [val ...]  /  RPUSH key val [val ...]
  Push values to the left/right of the list.
  Example: RPUSH queue:jobs job1 job2 job3

LPOP key [count]  /  RPOP key [count]
  Remove and return elements from left/right.
  Example: LPOP queue:jobs
           RPOP queue:jobs 3

LRANGE key start stop
  Get a range of elements (0-indexed, -1 = last).
  Example: LRANGE mylist 0 -1

LLEN key
  Return the length of the list.
  Example: LLEN queue:jobs

LINDEX key index
  Get element at index.
  Example: LINDEX mylist 0

LSET key index value
  Set element at index.
  Example: LSET mylist 0 "newval"

LINSERT key BEFORE|AFTER pivot value
  Insert value before/after pivot element.

LREM key count value
  Remove count occurrences of value.

BLPOP key [key ...] timeout  /  BRPOP key [key ...] timeout
  Blocking left/right pop — useful for queues.
  Example: BLPOP queue:jobs 5
EOF
}

show_cheatsheet_hash() {
  cat <<'EOF'

HASH COMMANDS
─────────────

HSET key field value [field value ...]
  Set one or more hash fields.
  Example: HSET user:1 name "Alice" age 30 email "a@b.com"

HGET key field
  Get the value of a hash field.
  Example: HGET user:1 name

HMGET key field [field ...]
  Get multiple hash fields.
  Example: HMGET user:1 name age

HGETALL key
  Get all fields and values.
  Example: HGETALL user:1

HDEL key field [field ...]
  Delete hash fields.
  Example: HDEL user:1 email

HEXISTS key field
  Check if field exists (returns 0 or 1).

HKEYS key  /  HVALS key  /  HLEN key
  Get all fields / values / count.

HINCRBY key field n  /  HINCRBYFLOAT key field f
  Increment a numeric hash field.
  Example: HINCRBY user:1 logincount 1

HSCAN key cursor [MATCH pattern] [COUNT n]
  Iteratively scan hash fields (safe for large hashes).
EOF
}

show_cheatsheet_set() {
  cat <<'EOF'

SET COMMANDS
────────────

SADD key member [member ...]
  Add one or more members to a set.
  Example: SADD tags:post1 redis nosql cache

SMEMBERS key
  Return all members of a set.
  Example: SMEMBERS tags:post1

SISMEMBER key member  /  SMISMEMBER key member [member ...]
  Check membership.
  Example: SISMEMBER tags:post1 redis

SREM key member [member ...]
  Remove members from a set.

SCARD key
  Return the number of members.

SUNION key [key ...]  /  SUNIONSTORE dest key [key ...]
  Union of multiple sets.
  Example: SUNION tags:post1 tags:post2

SINTER key [key ...]  /  SINTERSTORE dest key [key ...]
  Intersection of multiple sets.

SDIFF key [key ...]  /  SDIFFSTORE dest key [key ...]
  Difference of sets.

SRANDMEMBER key [count]
  Get random member(s).

SSCAN key cursor [MATCH pattern] [COUNT n]
  Iteratively scan set members.
EOF
}

show_cheatsheet_zset() {
  cat <<'EOF'

SORTED SET (ZSET) COMMANDS
───────────────────────────

ZADD key [NX|XX] [GT|LT] [CH] [INCR] score member [score member ...]
  Add members with scores.
  Example: ZADD leaderboard 1500 "alice" 2000 "bob"

ZRANGE key start stop [BYSCORE|BYLEX] [REV] [LIMIT offset count] [WITHSCORES]
  Get members by rank, score, or lex range (Redis 6.2+).
  Example: ZRANGE leaderboard 0 -1 WITHSCORES REV

ZRANK key member  /  ZREVRANK key member
  Get the rank of a member (0-indexed).

ZSCORE key member
  Get the score of a member.

ZINCRBY key increment member
  Increment the score of a member.
  Example: ZINCRBY leaderboard 50 "alice"

ZREM key member [member ...]
  Remove members.

ZCOUNT key min max
  Count members with scores between min and max.
  Example: ZCOUNT leaderboard 1000 2000

ZPOPMIN key [count]  /  ZPOPMAX key [count]
  Remove and return members with lowest/highest scores.

ZCARD key
  Return number of members.

ZSCAN key cursor [MATCH pattern] [COUNT n]
  Iteratively scan sorted set members.
EOF
}

show_cheatsheet_key() {
  cat <<'EOF'

KEY COMMANDS
────────────

DEL key [key ...]
  Delete one or more keys.
  Example: DEL user:1 session:abc

EXISTS key [key ...]
  Check if key(s) exist. Returns count of existing keys.
  Example: EXISTS user:1

EXPIRE key seconds  /  PEXPIRE key ms
  Set expiry in seconds / milliseconds.
  Example: EXPIRE session:abc 1800

EXPIREAT key unix-time  /  PEXPIREAT key unix-ms
  Set expiry to a Unix timestamp.

TTL key  /  PTTL key
  Get remaining TTL in seconds / milliseconds.
  Returns -1 (no expiry) or -2 (key does not exist).

PERSIST key
  Remove expiry from a key (make it permanent).

RENAME key newkey  /  RENAMENX key newkey
  Rename a key (NX variant: only if newkey does not exist).

TYPE key
  Return the type of a key: string, list, hash, set, zset, stream.

OBJECT ENCODING key
  Show internal encoding (e.g., ziplist, listpack, hashtable).

SCAN cursor [MATCH pattern] [COUNT n] [TYPE type]
  Iteratively scan all keys safely (preferred over KEYS in prod).
  Example: SCAN 0 MATCH user:* COUNT 100

KEYS pattern
  Find all keys matching a glob pattern.
  ⚠️  Use SCAN in production — KEYS blocks the server.
  Example: KEYS session:*

DUMP key  /  RESTORE key ttl serialized
  Serialize / deserialize a key's value.

COPY source dest [DB db] [REPLACE]
  Copy a key to another key or database.

OBJECT FREQ key  /  OBJECT IDLETIME key
  Get LFU frequency or idle time of a key.
EOF
}

show_cheatsheet_server() {
  cat <<'EOF'

SERVER COMMANDS
───────────────

INFO [section]
  Get server information and statistics.
  Sections: server, clients, memory, stats, replication, cpu, keyspace
  Example: INFO memory

DBSIZE
  Return the number of keys in the selected database.

SELECT db
  Switch to a database (0-15 by default).
  Example: SELECT 1

FLUSHDB [ASYNC|SYNC]
  Delete all keys in the current database.
  ⚠️  Irreversible!

FLUSHALL [ASYNC|SYNC]
  Delete all keys in all databases.
  ⚠️  Irreversible!

CONFIG GET parameter
  Get config values (supports glob).
  Example: CONFIG GET maxmemory
           CONFIG GET save

CONFIG SET parameter value
  Set a config value at runtime.
  Example: CONFIG SET maxmemory 512mb

CONFIG REWRITE
  Persist current config to redis.conf.

DEBUG SLEEP seconds
  Make the server sleep (for testing).

COMMAND COUNT  /  COMMAND INFO cmd [cmd ...]
  Get count of commands / info about specific commands.

SLOWLOG GET [count]  /  SLOWLOG RESET
  Get / reset the slow query log.

MONITOR
  Stream all commands received by the server (debugging only).
  ⚠️  High overhead — do not use in production.

BGSAVE  /  BGREWRITEAOF
  Trigger background RDB save / AOF rewrite.

LASTSAVE
  Get Unix timestamp of last successful RDB save.

REPLICAOF host port  /  REPLICAOF NO ONE
  Configure replication.
EOF
}

show_cheatsheet_scripting() {
  cat <<'EOF'

SCRIPTING COMMANDS
──────────────────

EVAL script numkeys [key [key ...]] [arg [arg ...]]
  Execute a Lua script.
  KEYS and ARGV are 1-indexed inside the script.
  Example:
    EVAL "return redis.call('GET', KEYS[1])" 1 mykey

EVALSHA sha1 numkeys [key ...] [arg ...]
  Execute a script by its SHA1 hash (cached on server).
  Example: EVALSHA abc123def 1 mykey

SCRIPT LOAD script
  Load a script into the cache without executing it.
  Returns the SHA1 hash.

SCRIPT EXISTS sha1 [sha1 ...]
  Check if scripts are cached (returns 0/1 per sha1).

SCRIPT FLUSH [ASYNC|SYNC]
  Remove all cached scripts.

SCRIPT KILL
  Kill the currently running script (if it hasn't written).

FCALL function numkeys [key ...] [arg ...]
  Call a Redis Function (Redis 7.0+).
  Example: FCALL myfunc 1 mykey

FUNCTION LIST [LIBRARYNAME name] [WITHCODE]
  List registered functions/libraries.

FUNCTION LOAD [REPLACE] function-code
  Load a function library from Lua code.

FUNCTION DELETE library-name
  Delete a function library.
EOF
}

do_cheatsheet() {
  local cat="${1:-all}"
  local cat_lower
  cat_lower="$(echo "$cat" | tr '[:upper:]' '[:lower:]')"

  echo -e "\n${BOLD}${REDIS_ICON} Redis Cheatsheet${cat:+ — ${cat^^}}${RESET}"
  echo "$SEP"

  case "$cat_lower" in
    string|str)   show_cheatsheet_string ;;
    list)         show_cheatsheet_list ;;
    hash)         show_cheatsheet_hash ;;
    set)          show_cheatsheet_set ;;
    zset|sorted)  show_cheatsheet_zset ;;
    key|keys)     show_cheatsheet_key ;;
    server|srv)   show_cheatsheet_server ;;
    scripting|lua|script) show_cheatsheet_scripting ;;
    all|"")
      show_cheatsheet_string
      show_cheatsheet_list
      show_cheatsheet_hash
      show_cheatsheet_set
      show_cheatsheet_zset
      show_cheatsheet_key
      show_cheatsheet_server
      show_cheatsheet_scripting
      ;;
    *)
      echo -e "${YELLOW}Unknown category: $cat${RESET}"
      echo "Available: string  list  hash  set  zset  key  server  scripting  all"
      exit 1
      ;;
  esac
  echo
}

# ── Connection helpers ────────────────────────────────────────────────────────

check_redis_cli() {
  if ! command -v redis-cli &>/dev/null; then
    echo -e "${YELLOW}⚠️  redis-cli not found.${RESET}"
    echo "Install with:"
    echo "  Ubuntu/Debian : sudo apt install redis-tools"
    echo "  macOS         : brew install redis"
    echo "  Alpine        : apk add redis"
    return 1
  fi
  return 0
}

build_redis_cmd() {
  local host="$1"
  local port="$2"
  local pass="$3"
  local cmd="redis-cli -h $host -p $port"
  if [[ -n "$pass" ]]; then
    cmd="$cmd -a $pass --no-auth-warning"
  fi
  echo "$cmd"
}

do_test() {
  local host="${ARG1:-localhost}"
  local port="${ARG2:-6379}"
  local pass="${ARG3:-}"

  echo -e "\n${BOLD}${REDIS_ICON} Redis Connection Test${RESET}"
  echo "$SEP"
  echo -e "Host     : ${CYAN}$host${RESET}"
  echo -e "Port     : ${CYAN}$port${RESET}"

  if ! check_redis_cli; then
    return 1
  fi

  RCMD="$(build_redis_cmd "$host" "$port" "$pass")"

  # Test PING
  PONG="$($RCMD PING 2>&1 || true)"
  if [[ "$PONG" == "PONG" ]]; then
    echo -e "Status   : ${GREEN}✅ CONNECTED${RESET}"
  else
    echo -e "Status   : ${RED_C}❌ FAILED${RESET}"
    echo -e "Response : $PONG"
    echo
    echo "Troubleshooting:"
    echo "  • Is Redis running?  sudo systemctl status redis"
    echo "  • Is the port open?  ss -tlnp | grep $port"
    echo "  • Is auth required?  redis-cli -h $host -p $port -a <password> PING"
    return 1
  fi

  echo
  echo -e "${BOLD}Server Info:${RESET}"

  # Parse INFO output
  INFO="$($RCMD INFO server INFO clients INFO memory INFO replication 2>&1 || true)"

  extract() {
    echo "$INFO" | grep "^${1}:" | head -1 | cut -d: -f2 | tr -d '[:space:]'
  }

  ver="$(extract redis_version)"
  uptime="$(extract uptime_in_days)"
  clients="$(extract connected_clients)"
  mem="$(extract used_memory_human)"
  maxmem="$(extract maxmemory_human)"
  role="$(extract role)"
  aof="$(extract aof_enabled)"

  [[ -n "$ver" ]]     && printf "  %-22s: %s\n" "redis_version"      "$ver"
  [[ -n "$uptime" ]]  && printf "  %-22s: %s days\n" "uptime"         "$uptime"
  [[ -n "$clients" ]] && printf "  %-22s: %s\n" "connected_clients"  "$clients"
  [[ -n "$mem" ]]     && printf "  %-22s: %s\n" "used_memory"        "$mem"
  if [[ -n "$maxmem" && "$maxmem" != "0B" ]]; then
    printf "  %-22s: %s\n" "maxmemory" "$maxmem"
  else
    printf "  %-22s: 0 (unlimited)\n" "maxmemory"
  fi
  [[ -n "$role" ]]    && printf "  %-22s: %s\n" "role"               "$role"
  [[ -n "$aof" ]]     && printf "  %-22s: %s\n" "aof_enabled"        "$aof"
  echo
}

do_monitor() {
  local host="${ARG1:-localhost}"
  local port="${ARG2:-6379}"
  local pass="${ARG3:-}"

  echo -e "\n${BOLD}${REDIS_ICON} Redis Key Monitor${RESET}"
  echo "$SEP"
  echo -e "Host     : ${CYAN}$host:$port${RESET}"
  echo

  if ! check_redis_cli; then
    return 1
  fi

  RCMD="$(build_redis_cmd "$host" "$port" "$pass")"

  # Test connection first
  PONG="$($RCMD PING 2>&1 || true)"
  if [[ "$PONG" != "PONG" ]]; then
    echo -e "${RED_C}❌ Cannot connect to Redis at $host:$port${RESET}"
    echo "Run: bash script.sh test $host $port"
    return 1
  fi

  # Get keyspace info
  KEYSPACE="$($RCMD INFO keyspace 2>&1 || true)"
  MEMORY="$($RCMD INFO memory 2>&1 | grep used_memory_human | head -1 | cut -d: -f2 | tr -d '[:space:]' || true)"
  DBSIZE="$($RCMD DBSIZE 2>&1 || true)"

  printf "%-6s %-8s %s\n" "DB" "Keys" "Avg TTL"
  printf "%-6s %-8s %s\n" "────" "────────" "────────"

  TOTAL=0
  if echo "$KEYSPACE" | grep -q "^db"; then
    while IFS= read -r line; do
      if [[ "$line" =~ ^db([0-9]+):keys=([0-9]+) ]]; then
        dbnum="${BASH_REMATCH[1]}"
        keys="${BASH_REMATCH[2]}"
        TOTAL=$((TOTAL + keys))
        # Extract avg_ttl if present
        avg_ttl="—"
        if [[ "$line" =~ avg_ttl=([0-9]+) ]]; then
          ttl_ms="${BASH_REMATCH[1]}"
          if [[ "$ttl_ms" -gt 0 ]]; then
            avg_ttl="${ttl_ms}ms"
          fi
        fi
        printf "%-6s %-8s %s\n" "db${dbnum}" "$keys" "$avg_ttl"
      fi
    done < <(echo "$KEYSPACE")
  else
    printf "%-6s %-8s %s\n" "db0" "$DBSIZE" "—"
    TOTAL="$DBSIZE"
  fi

  echo
  echo -e "Total keys : ${BOLD}$TOTAL${RESET}"
  echo -e "Memory     : ${BOLD}${MEMORY:-unknown}${RESET}"
  echo
}

# ── Main ─────────────────────────────────────────────────────────────────────

case "$COMMAND" in
  cheatsheet|cs|ref)
    do_cheatsheet "${ARG1:-all}"
    ;;
  test|ping|connect)
    do_test
    ;;
  monitor|stats|keys)
    do_monitor
    ;;
  help|--help|-h|"")
    usage
    ;;
  *)
    echo -e "${RED_C}Unknown command: $COMMAND${RESET}"
    echo "Run: bash script.sh help"
    exit 1
    ;;
esac
