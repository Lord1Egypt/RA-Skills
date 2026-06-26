# Changelog

## 4.0.0 (2026-03-17)

### Breaking Changes
- Scripts now require Python 3 and `psycopg2-binary` (`pip3 install psycopg2-binary`)
- Replaced shell-based `psql` calls with Python/psycopg2 for all database operations

### Security
- **Fixed SQL injection vulnerability** — replaced string interpolation with parameterized queries (`%s` placeholders via psycopg2)
- JSON payloads are now validated with `json.loads()` before database insertion
- Removed `escape_sql()` shell function (was insufficient for safe SQL escaping)

### Reliability
- Added connection retry with exponential backoff (3 attempts: 1s, 2s, 4s)
- Added mid-session reconnect — if connection drops between queries, scripts reconnect and retry once
- Added `connect_timeout=10` to prevent indefinite hangs on unreachable hosts
- Scripts now explicitly check for `python3` and `psycopg2` availability

### Error Handling
- Notification insert in `request-resource.sh` no longer silently fails — errors are reported
- `check-notifications.sh` now distinguishes "no notifications" from "database unreachable"
- Output parsing changed from pipe-delimited `read` loop to `DictCursor` (no more field mangling on `|` in messages)

### Configuration
- Unified environment variable fallback chain: `ISSUE_DB_*` / `REQUEST_DB_*` → `SYSCLAW_DB_*` → defaults
- All scripts now use the same connection pattern (previously inconsistent)
- Added `.env.example` template with placeholder values

### Other
- Improved hostname fallback: `hostname -f` → `hostname` → `"no-host"`
- Error messages include retry attempt count on connection failure
- Context-aware error output in `request-resource.sh` (reports whether the request was created before failure)

## 3.2.0 (2026-03-16)

- Previous release (shell scripts using `psql` with string interpolation)
