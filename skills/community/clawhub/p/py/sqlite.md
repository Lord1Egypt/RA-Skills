# SQLite — The Database That Ships With Python

`sqlite3` is in the stdlib, needs no server, and is the right answer for caches, queues, local state, desktop apps, and test fixtures. Everything below is a default that is fine for a script and wrong for anything concurrent.

## Does It Fit

| Workload | Verdict |
|---|---|
| One process, or many readers and one writer | Yes — this is what SQLite is best at |
| Many concurrent writers | No. Writes serialize on a whole-database lock; queue them through one writer or use a server database |
| Database file on NFS, SMB, or a shared network mount | No. The locking primitives are unreliable there and corruption is the documented outcome |
| Test fixtures, caches, embedded app state, a durable job queue | Yes, including in production — file size is not the constraint (terabyte-scale is supported) |
| Anything else | Start with SQLite; migrate when a second writer appears, not before |

## Transactions — The Default Is Legacy

- Default `isolation_level=""` means the module opens a transaction implicitly before `INSERT`/`UPDATE`/`DELETE`/`REPLACE` and leaves `SELECT` and DDL outside it. Nothing is durable until `conn.commit()`; closing without committing rolls back, which is how "the script ran and the table is empty" happens.
- Own it explicitly instead: `connect(..., isolation_level=None)` disables the implicit `BEGIN`, and you write `BEGIN`/`COMMIT` yourself. `python >=3.12` exposes the same thing as `conn.autocommit = False` with PEP 249 semantics; below that floor, `isolation_level` is the only lever.
- Use the connection as a context manager for the commit boundary: `with conn:` commits on success and rolls back on exception. It does NOT close the connection — a persistent source of confusion, since `with open(...)` does.
- `BEGIN` is deferred by default: the write lock is taken at the first write, so two connections that both started reading and then both try to write produce an immediate `database is locked` that no timeout retries away. When a transaction will write, start it with `BEGIN IMMEDIATE`.
- DDL inside a transaction works in SQLite (unlike MySQL), so migrations can be atomic — one `BEGIN`, all the `ALTER TABLE`s, one `COMMIT`.

## Concurrency Settings To Set On Every Connection

```python
conn = sqlite3.connect(path, timeout=30.0, isolation_level=None)
conn.execute("PRAGMA journal_mode=WAL")     # persists in the file; set once, survives
conn.execute("PRAGMA synchronous=NORMAL")   # per connection
conn.execute("PRAGMA foreign_keys=ON")      # per connection, OFF by default, every time
conn.execute("PRAGMA busy_timeout=30000")   # milliseconds
```

- **WAL** lets readers proceed while a writer is active; the default rollback journal blocks them. It is written into the database file, so it survives reconnection, and it creates `-wal` and `-shm` siblings that must travel with the file. Not usable on a network filesystem.
- **synchronous=NORMAL** with WAL trades the last few transactions on a power cut for a large write speedup, and cannot corrupt the database. `FULL` is the default and the right choice only when losing a committed transaction is unacceptable.
- **foreign_keys** is OFF by default and per connection: every pool member, every reconnect, every test fixture sets it again or your `REFERENCES` clauses are documentation.
- `connect(timeout=…)` is the busy timeout in seconds (default 5.0). It retries a lock held by another connection; it does nothing for the deferred-upgrade deadlock above.
- `check_same_thread=False` only removes Python's guard — it does not make the connection thread-safe. One connection per thread (`threading.local`), or one writer thread fed by a queue (`concurrency.md`).

## Queries

- Placeholders always: `cur.execute("SELECT * FROM t WHERE id = ?", (id,))` or named `:id` with a dict. Never an f-string, and note the one-element tuple needs the trailing comma (`security.md`).
- `IN (?, ?, …)` is built from the list length — and hits `sqlite3.OperationalError: too many SQL variables` past the host-parameter limit (999 before SQLite 3.32, 32766 after). Chunk the list or insert the ids into a temp table.
- `conn.row_factory = sqlite3.Row` gives access by column name and `dict(row)`; a `Row` is not a dict and has no `.get`.
- `executemany(sql, iterable)` for bulk work, and it accepts a generator, so a million rows never exist in memory at once.
- Bulk inserts belong in ONE transaction: each autocommitted statement is its own durability barrier, so 10k inserts go from minutes to under a second when wrapped (`performance.md`).
- `EXPLAIN QUERY PLAN SELECT …` prints `SCAN t` for a full table scan and `SEARCH t USING INDEX …` when an index is used. That one line is the whole optimization loop.

## Types — There Are Almost None

- Column types are affinities, not constraints: a `TEXT` column stores an int if you insert one. Add `CHECK` constraints when the shape matters, and turn on `STRICT` tables (SQLite 3.37+) for real type enforcement.
- No date, time, or boolean type. Store dates as ISO-8601 text (`"2026-07-25T10:00:00+00:00"`, sortable and comparable as text) or as an integer epoch, and pick ONE for the whole database. Booleans are 0 and 1 (`datetime.md`).
- The implicit `datetime` adapters and `detect_types=PARSE_DECLTYPES` converters are deprecated as of `python >=3.12`: register your own with `sqlite3.register_adapter`/`register_converter`, or convert at the boundary and keep the driver dumb (`data-modeling.md`).
- `TEXT` values are decoded as UTF-8; a column holding invalid UTF-8 raises on read. `conn.text_factory = bytes` when the data is genuinely not text (`files.md`).
- `INTEGER PRIMARY KEY` IS the rowid — fast and free. `AUTOINCREMENT` adds a bookkeeping table and only guarantees ids are never reused; skip it unless a deleted id must never come back.

## Operations

- Backup a live database with the online API, never a file copy: `dest = sqlite3.connect(path); conn.backup(dest); dest.close()`. Copying the file while a writer is active captures a torn state, and copying it without the `-wal` sibling loses committed transactions.
- `VACUUM` rebuilds the file to reclaim space; it needs roughly twice the database size free and cannot run inside a transaction. `PRAGMA auto_vacuum=INCREMENTAL` for long-lived databases that churn.
- Corruption is almost always the environment: a network filesystem, a copied file without its WAL, or two processes through different mount paths. `PRAGMA integrity_check` reports it; the recovery path is `.dump` into a fresh database.
- Full-text search (FTS5) and JSON functions (`json_extract`) are compiled into the CPython build — check with `SELECT sqlite_version()` and a probe query rather than assuming a distro build has everything.

## Testing With SQLite

- `":memory:"` is a distinct database per connection: two connections see two empty databases. For a shared in-memory database use `sqlite3.connect("file:test?mode=memory&cache=shared", uri=True)` and keep one connection open for its lifetime.
- A `tmp_path` file per test is slower but behaves exactly like production, including WAL and locking (`testing.md`).
- Testing on SQLite and deploying on Postgres hides real bugs: different type coercion, different `LIKE` case sensitivity (ASCII-only folding here), no `RETURNING` on old builds, and far looser constraint enforcement. Test on the engine you deploy.
