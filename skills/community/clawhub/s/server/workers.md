# Concurrency Math — Workers, Threads, Pools, and Descriptors

How many of everything. Every number here is derived from a constraint, and the constraint is almost never the CPU count people size by.

**Before proposing numbers**, read `## Baselines` in `~/Clawic/data/server/memory.md` (or `baselines.md` if `## Boxes` points there): this box has been measured before, and last month's saturation point beats any formula.

**Contents:** [The Two Bounds](#the-two-bounds) · [Concurrency Model by Runtime](#concurrency-model-by-runtime) · [Gunicorn](#gunicorn) · [uvicorn and ASGI](#uvicorn-and-asgi) · [Puma](#puma) · [php-fpm](#php-fpm) · [Node](#node) · [The Database Ceiling](#the-database-ceiling) · [File Descriptors](#file-descriptors) · [Backlog and Ephemeral Ports](#backlog-and-ephemeral-ports) · [Keepalive Accounting](#keepalive-accounting) · [Worker Recycling](#worker-recycling) · [Write It Down](#write-it-down)

## The Two Bounds

For blocking (one-request-at-a-time) workers, take the **smaller** of:

```
CPU bound     : workers = 2 × cores + 1
Memory bound  : workers = (usable_RAM_MB × 0.75) ÷ RSS_per_worker_MB
```

`usable_RAM` is total RAM minus everything else on the box — database, proxy, OS page cache you want to keep. The 0.75 is headroom for request-time allocation spikes; an app whose RSS doubles under load needs 0.5.

Worked, on a 4-core / 4 GB box also running Postgres (reserve 1 GB) with a Django app at 400 MB RSS per worker:

```
CPU    : 2 × 4 + 1 = 9
Memory : (3000 × 0.75) ÷ 400 = 5.6 → 5
Run 5.
```

Same box, a Go binary at 40 MB: memory says 56, CPU says 9, run 9 — and Go does not use worker processes at all, so the real answer is one process and `GOMAXPROCS` at the core count.

`RSS_per_worker` is measured, never guessed: start one worker, drive real traffic through it for a few minutes, read RSS at steady state, and use *that* number. Copy-pasted worker counts from tutorials are the single biggest cause of OOM on small boxes — the tutorial's box had 16 GB.

## Concurrency Model by Runtime

| Model | Concurrency equals | Blocked by | Scale with |
|---|---|---|---|
| Process-per-request (Gunicorn sync, php-fpm) | Number of workers | One slow client occupies one worker entirely | Workers, bounded by memory |
| Threaded (Puma, `gthread`) | workers × threads | The interpreter lock on CPU work; threads only help IO wait | Threads for IO-bound, workers for CPU-bound |
| Evented single-thread (Node, uvicorn/asyncio) | Thousands of connections per process | Any synchronous CPU work in a handler stalls *everything* | One process per core, never more |
| Native threads (Go, Rust, Java) | The runtime's scheduler | Downstream pools, not the runtime | Rarely — one process, tuned pool sizes |

The mistake that crosses all four: adding worker processes to an evented runtime past the core count. It adds context switches and memory, and the event loop was never the bottleneck.

## Gunicorn

```
gunicorn app:application \
  --workers 5 --worker-class gthread --threads 4 \
  --bind unix:/run/api/api.sock \
  --timeout 30 --graceful-timeout 30 --keep-alive 75 \
  --max-requests 2000 --max-requests-jitter 200
```

- Default is **1 worker, sync class, 30s timeout** — a stock Gunicorn serves exactly one request at a time.
- `--timeout` kills a worker whose request exceeds it. It is a hang detector, not a request deadline; with async workers it stops applying the same way.
- Sync workers and slow clients do not mix: a client on a bad mobile connection holds a worker for the whole upload. Either put a buffering proxy in front (nginx buffers request bodies by default; that is what it is for) or use `gthread`.
- `--keep-alive` must exceed the proxy's keepalive (SKILL.md Rule 4). Gunicorn's default is 2 seconds, which is below nginx's 75 — the classic intermittent 502 in Python deployments.
- `--max-requests` recycles workers to cap slow leaks; always with `--jitter`, or every worker recycles at the same moment and the site stalls in unison.

## uvicorn and ASGI

- One worker per core; concurrency inside a worker comes from the event loop.
- The killer is a blocking call in an async handler — a synchronous DB driver, `requests`, `time.sleep`, an unbuffered file read. It freezes every concurrent request on that worker, and the symptom is p99 collapsing while CPU sits at 15%. Push blocking work into a thread pool (`run_in_executor`, `asyncio.to_thread`) or use an async driver.
- `--workers` in uvicorn does not give the graceful-restart behavior Gunicorn's arbiter does; for production, Gunicorn with `-k uvicorn.workers.UvicornWorker` is the more operable combination.
- `--limit-concurrency` returns 503 instead of queueing without bound — a shed valve worth setting, because unbounded queueing turns a slow dependency into a total outage.

## Puma

- `workers` (processes) × `threads` (per process). MRI's global lock means threads only overlap IO; CPU-bound work needs workers.
- Start at `workers = cores`, `threads = 5` and measure. Thread count above ~16 on MRI usually costs more in contention than it gains.
- `preload_app!` plus `on_worker_boot` to reconnect the database — without the reconnect, forked workers share a connection and fail in ways that look random.
- Database pool must be **≥ threads per worker**, or threads block waiting for a connection while the CPU idles.

## php-fpm

```ini
pm = dynamic
pm.max_children = 12
pm.start_servers = 4
pm.min_spare_servers = 2
pm.max_spare_servers = 6
pm.max_requests = 500
```

- `pm.max_children` **is** the concurrency limit. Formula: `(usable_RAM × 0.75) ÷ average_process_RSS` — check the real RSS of a busy child, not the idle one.
- When the limit is hit, the log says "server reached pm.max_children setting, consider raising it" and requests queue in the proxy; the user sees a 502 or a 504 depending on which timeout fires first. That log line is the most direct capacity signal in this whole file — grep for it before touching anything else.
- One pool per app, each with its own user and its own `max_children`. A shared pool means the memory-hungry app decides the fate of the cheap one.
- `pm = ondemand` for low-traffic sites (idle children exit, memory returns); `pm = static` only when the box is dedicated and the number is known.

## Node

- One process per core, via the app's own cluster logic, PM2 cluster mode, or N systemd template instances behind the proxy (`processes.md`).
- Cluster mode requires statelessness: in-memory sessions, in-process caches and local WebSocket rooms all break at worker #2. Move sessions to a shared store, and WebSocket fan-out to a pub/sub backend, before adding the second process.
- `keepAliveTimeout` defaults to 5s and must exceed the proxy's keepalive (Rule 4); `headersTimeout` must exceed `keepAliveTimeout`.
- The default thread pool (`UV_THREADPOOL_SIZE`, 4) serves file IO, DNS, and crypto. A crypto- or fs-heavy service saturates it long before the event loop, and the symptom is uniform latency growth across unrelated endpoints.
- `--max-old-space-size` matters on containers: the default heap is derived from what the runtime believes the memory limit to be, and older versions read the host's memory, not the cgroup's.

## The Database Ceiling

The bound that catches teams after the app is already sized:

```
total_connections = app_processes × pool_size_per_process   (× every app on that database)
must stay below:  max_connections − superuser_reserved_connections
```

Postgres defaults: `max_connections = 100`, `superuser_reserved_connections = 3`. Five app workers with a pool of 10 is 50; add a worker queue at 4 × 10 and a cron job, and the next deploy fails with "too many clients already" — during the deploy, when both old and new processes are briefly alive, so the real peak is up to double the steady state.

Three fixes, in order of preference: shrink the pool (most apps need 2-5 connections per process, not 10-20); put a pooler in front (PgBouncer in transaction mode multiplexes hundreds of clients onto a few backend connections); raise `max_connections` last, because each Postgres backend costs memory and the server was not sized for 500 of them.

## File Descriptors

Every connection costs descriptors, and the proxy pays twice — one for the client, one for the upstream.

| Setting | Rule |
|---|---|
| `LimitNOFILE` in the service unit | 65535 for anything network-facing; the soft default of 1024 caps you near 500 concurrent clients |
| `worker_rlimit_nofile` (nginx) | ≥ 2 × `worker_connections`, or the proxy hits the wall before its own configured limit |
| `worker_connections` × `worker_processes` | The proxy's theoretical maximum concurrent connections; halve it for a mental model of real clients |
| Container limits | The runtime's default may be lower than the host's; check inside the container, not outside |

`Too many open files` in a log is unambiguous: raise the limit for that process, then look for the leak that made 1024 insufficient — unclosed HTTP clients and forgotten file handles are far more common than genuine load.

## Backlog and Ephemeral Ports

- `somaxconn` bounds the accept queue: 128 on kernels before 5.4, 4096 after. A listen backlog smaller than a traffic burst produces refused connections that never appear in the application log, because the app never saw them.
- The app's own `listen()` backlog argument is capped by `somaxconn`, so raising one without the other does nothing.
- Ephemeral ports (~32768-60999) bound *outbound* connections per destination tuple at roughly 28,000, and `TIME_WAIT` holds each for 60 seconds after close. A proxy that opens a fresh upstream connection per request hits this at a few hundred requests per second — the fix is upstream keepalive (below), not `tcp_tw_reuse` tuning.

## Keepalive Accounting

nginx does **not** keep upstream connections alive unless told to. Without a `keepalive` directive in the upstream block, every proxied request is a new TCP handshake, a new ephemeral port, and 60 seconds of `TIME_WAIT` afterwards. With it:

```
keepalive N   →  N idle connections kept per worker process
real pool     =  N × worker_processes
```

Set `N` near the concurrency you actually serve, not higher: idle upstream connections consume a worker slot on the app side too. And the upstream's idle timeout must exceed the proxy's keepalive, always (Rule 4).

## Worker Recycling

Recycling workers after a fixed number of requests papers over leaks and buys time; it does not fix them. Use it, but with jitter, and only after confirming the leak is in a dependency you do not control. A memory graph that saws up and down at exactly `max_requests` intervals is a recycled leak, not a healthy service — and it will still OOM the day traffic doubles, because the leak rate did too.

## Write It Down

Any number derived here is a baseline: write the row to `## Baselines` in `memory.md` — date, service, what was configured (worker count, threads, pool size), the result, and what saturated first (`memory-template.md`). Without the configuration column the number cannot be reproduced, and "it used to handle more" becomes unfalsifiable. Full load-test output goes to `~/Clawic/data/server/artifacts/loadtest-<service>-<date>.md` with its `## Boxes` line in the same turn (`capacity.md`).
