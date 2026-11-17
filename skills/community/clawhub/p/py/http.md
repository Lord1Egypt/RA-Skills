# HTTP Clients — Sessions, Status, Bodies, Redirects

Calling an API is the most common thing Python does over a network, and the failure modes are the same in every client: no connection reuse, no status check, and a body decoded with the wrong charset.

## Which Client

| Situation | Use | Why |
|---|---|---|
| Zero dependencies allowed (installer, bootstrap script, stdlib-only tool) | `urllib.request.urlopen` | Ships with Python; no pooling, no retries, no `json=`, and `Request` headers must be built by hand |
| Ordinary synchronous code | `requests` | Ubiquitous, readable, every stack trace already known to your team |
| Async code, HTTP/2, or one client for both sync and async | `httpx` | Same API in both modes; strict timeouts by default |
| Thousands of concurrent connections in an async service | `aiohttp` or `httpx.AsyncClient` | Both fine; the deciding factor is what the rest of the stack already uses (`concurrency.md`) |
| Anything else | `requests` for scripts, `httpx` for new services | Do not add a second client to a codebase that already has one |

`urllib.request` reads proxy settings from the environment, ignores `NO_PROXY` exceptions in some versions, and has no connection pool — one TCP plus TLS handshake per call. Acceptable for a handful of requests, never inside a loop.

## Sessions — The Single Biggest Win

- `requests.get(url)` at module level creates a client, opens a connection, and throws both away. Under a loop that is one TLS handshake per item, typically 50–200 ms of pure latency each. `s = requests.Session()` reuses connections and cookies; `httpx.Client()` and `httpx.AsyncClient()` are the same idea.
- Create the client once per process (or per app lifespan), not per call. In async code, an `AsyncClient` created inside the request handler is the same bug wearing async syntax, plus an event-loop-bound resource that leaks if never closed — use `async with` or an explicit lifespan hook.
- The default pool is small: urllib3 keeps 10 connections per host. Twenty threads sharing one Session log `Connection pool is full, discarding connection` and silently serialize. Size it: `s.mount("https://", HTTPAdapter(pool_maxsize=32))`.
- A Session is not a concurrency limiter. Bound in-flight requests with a semaphore or a bounded executor, or a retry storm turns into a self-inflicted DDoS (`concurrency.md`).

## The Response Is Not An Exception

- A 404 or a 500 returns normally. `resp.json()` on an HTML error page raises `JSONDecodeError` three lines later, which is why the traceback never mentions the real problem. Call `resp.raise_for_status()` first, always.
- `resp.ok` is True for 3xx as well — it means "not 4xx/5xx", not "success". Check `resp.status_code` when the distinction matters.
- `resp.text` guesses the charset from the `Content-Type` header; when a `text/*` response omits it, `requests` falls back to ISO-8859-1 and hands you mojibake for a UTF-8 body. Prefer `resp.content.decode("utf-8")`, or set `resp.encoding` before reading `.text` (`files.md`).
- Empty body with a 204, or `Content-Length: 0` on a 200: `resp.json()` raises. Check `if not resp.content` before parsing.
- Errors carry the useful part in the body. Log `resp.status_code` AND the first ~500 chars of `resp.text` — a bare "request failed" line makes the incident twice as long.

## Sending Data

- `json=payload` sets `Content-Type: application/json` and serializes; `data=dict` sends form-encoded; `data=string_or_bytes` sends it raw. Passing an already-serialized string to `json=` double-encodes it into a JSON string.
- `params={"q": "a b", "tags": ["x", "y"]}` handles percent-encoding and repeats the key per list item. Hand-built query strings are where `+` versus `%20` bugs live: `urllib.parse.quote` leaves `/` alone and encodes space as `%20`, `quote_plus` encodes it as `+`.
- File upload: `files={"f": ("name.csv", fh, "text/csv")}` builds the multipart body and the boundary. Setting `Content-Type: multipart/form-data` yourself strips the boundary and the server rejects the request.
- `json.dumps` cannot serialize `datetime` or `Decimal` — decide the wire representation once, centrally (`files.md`).

## Timeouts, Retries, Redirects

- Every call gets a timeout; the formula, the backoff, and which status codes are retryable live in `errors.md`. `requests` has no default at all, so the omission is unbounded.
- The library-level retry: `HTTPAdapter(max_retries=Retry(total=5, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504], respect_retry_after_header=True))`. By default `Retry` only replays idempotent methods — adding POST to `allowed_methods` is a decision about duplicate side effects, not a configuration detail.
- Redirects follow automatically. A 301/302 on a POST is re-issued as a GET by nearly every client (matching browsers, not the RFC); 307/308 preserve the method and body. If your POST "succeeds" but nothing was created, print `resp.history`.
- `requests` strips the `Authorization` header when a redirect crosses to a different host, and keeps it on the same host. Do not rely on either: resolve the final URL yourself when the credential matters.
- `allow_redirects=False` plus an explicit hop check is the only safe form when the URL came from a user — one redirect to `169.254.169.254` turns a fetch into credential theft (`security.md`).

## Streaming And Large Bodies

- `resp.content` materializes the whole body in memory: a 2 GB download becomes a 2 GB allocation and an OOM kill (`performance.md`).
- Stream it, and close it: `with s.get(url, stream=True) as r: for chunk in r.iter_content(1 << 16): f.write(chunk)`. Without the `with` (or a `.close()`), the connection is held until garbage collection returns it to the pool.
- `iter_lines()` is convenient for NDJSON and Server-Sent Events, but it buffers until a newline arrives — a server that never sends one hangs past your read timeout, because a read timeout is per-socket-read, not per-request. Cap total elapsed time yourself.
- Uploading a large file: pass the open file object as `data=fh` for a chunked upload instead of reading it into memory.

## Debugging A Request You Cannot See

- `logging.getLogger("urllib3").setLevel(logging.DEBUG)` prints connection reuse and retries; `http.client.HTTPConnection.debuglevel = 1` prints raw request and response headers to stdout (`logging.md`).
- `resp.request.headers` and `resp.request.body` show what actually went out, including what the library added.
- SSL handshake failures name the cause: an expired CA bundle, a corporate MITM proxy, or a server missing an intermediate certificate. Fix by installing the CA, never with `verify=False` (`security.md`).
- Works with `curl`, fails in Python: compare the two header sets. The usual differences are `User-Agent`, `Accept-Encoding`, and a cookie your browser had.

## Testing HTTP Code

- Do not hit the network in unit tests. `responses` (requests) and `respx` (httpx) intercept at the transport layer and let you assert the request that was made; a plain `Mock` on the client asserts nothing about the URL or the body (`testing.md`).
- Record one real response per endpoint into a fixture file and replay it; refresh it on a schedule so the contract drift shows up as a test failure rather than an incident.
- Test the failure paths that production will actually hit: a timeout, a 500, a 429 with `Retry-After`, and a body that is valid HTTP but invalid JSON.
