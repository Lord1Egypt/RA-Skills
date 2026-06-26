# Redis Commands Quick Reference

## Connection
| Command | Description |
|---------|-------------|
| `ping` | Test connectivity |
| `auth <password>` | Authenticate |
| `select <db>` | Switch database (0-15) |
| `client setname <name>` | Name current connection |

## Info Sections
| Section | What it shows |
|---------|---------------|
| `info server` | Version, uptime, OS |
| `info clients` | Connected/blocked clients |
| `info memory` | Memory usage, fragmentation |
| `info stats` | Hits, misses, ops/sec |
| `info replication` | Master/replica status |
| `info cpu` | CPU consumption |
| `info keyspace` | Keys per database |
| `info commandstats` | Per-command call counts |
| `info all` | Everything |

## BullMQ Key Patterns
| Key Pattern | Type | Description |
|-------------|------|-------------|
| `bull:<name>:meta` | hash | Queue metadata |
| `bull:<name>:wait` | list | Jobs waiting to be processed |
| `bull:<name>:active` | list | Jobs currently being processed |
| `bull:<name>:delayed` | sorted set | Jobs scheduled for future |
| `bull:<name>:failed` | sorted set | Failed jobs (DLQ) |
| `bull:<name>:completed` | sorted set | Successfully completed jobs |
| `bull:<name>:paused` | list | Jobs in paused queue |
| `bull:<name>:repeat` | sorted set | Repeatable job definitions |
| `bull:<name>:events` | stream | Event stream for workers |
| `bull:<name>:<id>` | hash | Individual job data |

## Job Hash Fields
| Field | Description |
|-------|-------------|
| `data` | Job payload (JSON) |
| `opts` | Job options (JSON) |
| `name` | Job name |
| `timestamp` | When job was created |
| `processedOn` | When processing started |
| `finishedOn` | When job completed/failed |
| `attemptsMade` | Number of attempts |
| `failedReason` | Error message if failed |
| `stacktrace` | Error stack trace (JSON array) |
| `returnvalue` | Return value if completed |

## Safe Production Commands
These commands are non-blocking and safe to run in production:
- `scan` (use instead of `keys`)
- `info`
- `slowlog get`
- `client list`
- `memory usage <key>`
- `memory doctor`
- `object encoding <key>`
- `ttl <key>` / `pttl <key>`
- `type <key>`
- `dbsize`
- `llen` / `scard` / `zcard` / `hlen`

## Dangerous Commands (avoid in production)
- `keys *` — blocks Redis, use `scan` instead
- `flushdb` / `flushall` — deletes everything
- `debug` — can crash Redis
- `monitor` — high overhead, use briefly
- `save` — blocks Redis for RDB snapshot, use `bgsave`
