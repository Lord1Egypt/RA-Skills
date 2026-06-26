# Server-Side Extending

**Impact: HIGH**

Extending PocketBase with Go or embedded JavaScript (JSVM) - event hooks, custom routes, transactions, cron jobs, filesystem, migrations, and safe server-side filter binding.

---

## 1. Compose Hooks, Transactions, Routing, and Enrich in One Request Flow

**Impact: HIGH (Individual rules are atomic; this composite example shows which app instance applies at each layer and how errors propagate)**

The atomic rules (`ext-hooks-chain`, `ext-transactions`, `ext-routing-custom`, `ext-hooks-record-vs-request`, `ext-filesystem`, `ext-filter-binding-server`) each teach a single trap. Real extending code touches **all of them in the same handler**. This rule walks through one complete request flow and annotates **which app instance is active at each layer** - the single most common source of extending bugs is reaching for the wrong one.

### The flow

`POST /api/myapp/posts` that: authenticates the caller, validates uniqueness with a bound filter, creates a record inside a transaction, uploads a thumbnail through a scoped filesystem, writes an audit log from an `OnRecordAfterCreateSuccess` hook, and shapes the response (including the realtime broadcast) in `OnRecordEnrich`.

```
HTTP request
 │
 ▼
[group middleware]  apis.RequireAuth("users")          ◄── e.Auth is set after this
 │
 ▼
[route handler]     se.App.RunInTransaction(func(txApp) {
 │                    // ⚠️ inside the block, use ONLY txApp, never se.App or outer `app`
 │                    FindFirstRecordByFilter(txApp, ...) // bound {:slug}
 │                    txApp.Save(post)                     // fires OnRecord*Create / *Request
 │                        │
 │                        ▼
 │                     [OnRecordAfterCreateSuccess hook]  ◄── e.App IS txApp here
 │                        │                                    (hook fires inside the tx)
 │                        e.App.Save(auditRecord)              → participates in rollback
 │                        e.Next()                             → REQUIRED
 │                        │
 │                        ▼
 │                     return to route handler
 │                    fs := txApp.NewFilesystem()
 │                    defer fs.Close()
 │                    post.Set("thumb", file); txApp.Save(post)
 │                    return nil  // commit
 │                  })
 │
 ▼
[enrich pass]       OnRecordEnrich fires                ◄── RUNS AFTER the tx committed
 │                   (also fires for realtime SSE and list responses)
 │                   e.App is the outer app; tx is already closed
 ▼
[response serialization] e.JSON(...)
```

### The code

```go
app.OnServe().BindFunc(func(se *core.ServeEvent) error {
    g := se.Router.Group("/api/myapp")
    g.Bind(apis.RequireAuth("users"))

    g.POST("/posts", func(e *core.RequestEvent) error {
        // ── Layer 1: route handler ────────────────────────────────────────
        // e.App is the top-level app. e.Auth is populated by RequireAuth.
        // e.RequestInfo holds headers/body/query.
        body := struct {
            Slug  string `json:"slug"`
            Title string `json:"title"`
        }{}
        if err := e.BindBody(&body); err != nil {
            return e.BadRequestError("invalid body", err)
        }

        var created *core.Record

        // ── Layer 2: transaction ──────────────────────────────────────────
        txErr := e.App.RunInTransaction(func(txApp core.App) error {
            // ⚠️ From here until the closure returns, every DB call MUST go
            //    through txApp. Capturing e.App or the outer `app` deadlocks
            //    on the writer lock.

            // Bound filter - see ext-filter-binding-server
            existing, _ := txApp.FindFirstRecordByFilter(
                "posts",
                "slug = {:slug}",
                dbx.Params{"slug": body.Slug},
            )
            if existing != nil {
                return apis.NewBadRequestError("slug already taken", nil)
            }

            col, err := txApp.FindCollectionByNameOrId("posts")
            if err != nil {
                return err
            }
            post := core.NewRecord(col)
            post.Set("slug", body.Slug)
            post.Set("title", body.Title)
            post.Set("author", e.Auth.Id)

            // txApp.Save fires record hooks INSIDE the tx
            if err := txApp.Save(post); err != nil {
                return err
            }

            // ── Layer 3: filesystem (scoped to this request) ─────────────
            fs, err := txApp.NewFilesystem()
            if err != nil {
                return err
            }
            defer fs.Close() // REQUIRED - see ext-filesystem

            if uploaded, ok := e.RequestInfo.Body["thumb"].(*filesystem.File); ok {
                post.Set("thumb", uploaded)
                if err := txApp.Save(post); err != nil {
                    return err
                }
            }

            created = post
            return nil // commit
        })
        if txErr != nil {
            return txErr // framework maps it to a proper HTTP error
        }

        // ── Layer 5: response (enrich runs automatically) ────────────────
        // e.App is the OUTER app again here - the tx has committed.
        // OnRecordEnrich will fire during JSON serialization and for any
        // realtime subscribers receiving the "create" event.
        return e.JSON(http.StatusOK, created)
    })

    return se.Next()
})

// ── Layer 4: hooks ──────────────────────────────────────────────────────
// These are registered once at startup, NOT inside the route handler.

app.OnRecordAfterCreateSuccess("posts").Bind(&hook.Handler[*core.RecordEvent]{
    Id: "audit-post-create",
    Func: func(e *core.RecordEvent) error {
        // ⚠️ e.App here is txApp when the parent Save happened inside a tx.
        //    Always use e.App - never a captured outer `app` - so that the
        //    audit record participates in the same transaction (and the
        //    same rollback) as the parent Save.
        col, err := e.App.FindCollectionByNameOrId("audit")
        if err != nil {
            return err
        }
        audit := core.NewRecord(col)
        audit.Set("action", "post.create")
        audit.Set("record", e.Record.Id)
        audit.Set("actor", e.Record.GetString("author"))
        if err := e.App.Save(audit); err != nil {
            return err // rolls back the whole request
        }
        return e.Next() // REQUIRED - see ext-hooks-chain
    },
})

app.OnRecordEnrich("posts").BindFunc(func(e *core.RecordEnrichEvent) error {
    // Runs for:
    //   - GET /api/collections/posts/records (list)
    //   - GET /api/collections/posts/records/{id} (view)
    //   - realtime SSE create/update broadcasts
    //   - any apis.EnrichRecord call in a custom route
    // Does NOT run inside a transaction; e.App is the outer app.
    e.Record.Hide("internalNotes")

    if e.RequestInfo != nil && e.RequestInfo.Auth != nil {
        e.Record.WithCustomData(true)
        e.Record.Set("isMine", e.Record.GetString("author") == e.RequestInfo.Auth.Id)
    }
    return e.Next()
})
```

### The cheat sheet: "which app am I holding?"

| Where you are | Use | Why |
|---|---|---|
| Top of a route handler (`func(e *core.RequestEvent)`) | `e.App` | Framework's top-level app; same object the server started with |
| Inside `RunInTransaction(func(txApp) { ... })` | `txApp` **only** | Capturing the outer app deadlocks on the SQLite writer lock |
| Inside a record hook fired from a `Save` inside a tx | `e.App` | The framework has already rebound `e.App` to `txApp` for you |
| Inside a record hook fired from a non-tx `Save` | `e.App` | Same identifier, same rules, just points to the top-level app |
| Inside `OnRecordEnrich` | `e.App` | Runs during response serialization, **after** the tx has committed |
| Inside a `app.Cron()` callback | captured `app` / `se.App` | Cron has no per-run scoped app; wrap in `RunInTransaction` if you need atomicity |
| Inside a migration function | the `app` argument | `m.Register(func(app core.App) error { ... })` - already transactional |

### Error propagation in the chain

- `return err` inside `RunInTransaction` → **rolls back everything**, including any audit records written by hooks that fired from nested `Save` calls.
- `return err` from a hook handler → propagates back through the `Save` call → propagates out of the tx closure → rolls back.
- **Not** calling `e.Next()` in a hook → the chain is broken **silently**. The framework's own post-save work (realtime broadcast, enrich pass, activity log) is skipped but no error is reported.
- A panic inside the tx closure is recovered by PocketBase, the tx rolls back, and the panic is converted to a 500 response.
- A panic inside a cron callback is recovered and logged - it does **not** take down the process.

### When NOT to compose this much

This example is realistic but also the ceiling of what should live in a single handler. If you find yourself stacking six concerns in one route, consider splitting the logic into a service function that takes `txApp` as a parameter and is called by the route. The same function is then reusable from cron jobs, migrations, and tests.

Reference: cross-references `ext-hooks-chain.md`, `ext-transactions.md`, `ext-routing-custom.md`, `ext-hooks-record-vs-request.md`, `ext-filesystem.md`, `ext-filter-binding-server.md`.

## 2. Schedule Recurring Jobs with the Builtin Cron Scheduler

**Impact: MEDIUM (Avoids external schedulers and correctly integrates background tasks with the PocketBase lifecycle)**

PocketBase includes a cron scheduler that starts automatically with `serve`. Register jobs before calling `app.Start()` (Go) or at the top level of a `pb_hooks` file (JSVM). Each job runs in its own goroutine and receives a standard cron expression.

**Incorrect (external timer, blocking hook, replacing system jobs):**

```go
// ❌ Using a raw Go timer instead of the app cron – misses lifecycle management
go func() {
    for range time.Tick(2 * time.Minute) {
        log.Println("cleanup")
    }
}()

// ❌ Blocking inside a hook instead of scheduling
app.OnServe().BindFunc(func(se *core.ServeEvent) error {
    for {
        time.Sleep(2 * time.Minute)
        log.Println("cleanup") // ❌ blocks the hook and never returns se.Next()
    }
})

// ❌ Removing all cron jobs wipes PocketBase's own log-cleanup and auto-backup jobs
app.Cron().RemoveAll()
```

```javascript
// ❌ JSVM: using setTimeout – not supported in the embedded goja engine
setTimeout(() => console.log("run"), 120_000); // ReferenceError
```

**Correct – Go:**

```go
package main

import (
    "log"

    "github.com/pocketbase/pocketbase"
    "github.com/pocketbase/pocketbase/core"
)

func main() {
    app := pocketbase.New()

    // Register before app.Start() so the scheduler knows about the job at launch.
    // MustAdd panics on an invalid cron expression (use Add if you prefer an error return).
    app.Cron().MustAdd("cleanup-drafts", "0 3 * * *", func() {
        // Runs every day at 03:00 UTC in its own goroutine.
        // Use app directly here (not e.App) because this is not inside a hook.
        records, err := app.FindAllRecords("posts",
            core.FilterData("status = 'draft' && created < {:cutoff}"),
        )
        if err != nil {
            app.Logger().Error("cron cleanup-drafts", "err", err)
            return
        }
        for _, r := range records {
            if err := app.Delete(r); err != nil {
                app.Logger().Error("cron delete", "id", r.Id, "err", err)
            }
        }
    })

    // Remove a job by ID (e.g. during a feature flag toggle)
    // app.Cron().Remove("cleanup-drafts")

    if err := app.Start(); err != nil {
        log.Fatal(err)
    }
}
```

**Correct – JSVM:**

```javascript
// pb_hooks/crons.pb.js
/// <reference path="../pb_data/types.d.ts" />

// Top-level cronAdd() registers the job at hook-load time.
// The handler runs in its own goroutine and has access to $app.
cronAdd("notify-unpublished", "*/30 * * * *", () => {
    // Runs every 30 minutes
    const records = $app.findAllRecords("posts",
        $dbx.hashExp({ status: "draft" })
    );
    console.log(`Found ${records.length} unpublished posts`);
});

// Remove a registered job by ID (useful in tests or feature toggles)
// cronRemove("notify-unpublished");
```

**Cron expression reference:**

```
┌─── minute        (0 - 59)
│  ┌── hour         (0 - 23)
│  │  ┌─ day-of-month (1 - 31)
│  │  │  ┌ month       (1 - 12)
│  │  │  │  ┌ day-of-week  (0 - 6, Sunday = 0)
│  │  │  │  │
*  *  *  *  *

Examples:
  */2 * * * *    every 2 minutes
  0 3 * * *      daily at 03:00
  0 0 * * 0      weekly on Sunday midnight
  @hourly        macro equivalent to 0 * * * *
```

**Key rules:**
- System jobs use the `__pb*__` ID prefix (e.g. `__pbLogsCleanup__`). Never call `RemoveAll()` or use that prefix for your own jobs.
- All registered cron jobs are visible and can be manually triggered from _Dashboard > Settings > Crons_.
- JSVM handlers have access to `$app` but **not** to outer-scope variables (see JSVM scope rule).
- Go jobs can use `app` directly (not `e.App`) because they run outside the hook/transaction context.

Reference: [Go – Jobs scheduling](https://pocketbase.io/docs/go-jobs-scheduling/) | [JS – Jobs scheduling](https://pocketbase.io/docs/js-jobs-scheduling/)

## 3. Always Close the Filesystem Handle Returned by NewFilesystem

**Impact: HIGH (Leaked filesystem clients keep S3 connections and file descriptors open until the process exits)**

`app.NewFilesystem()` (Go) and `$app.newFilesystem()` (JS) return a filesystem client backed by either the local disk or S3, depending on the app settings. **The caller owns the handle** and must close it - there is no finalizer and no automatic pooling. Leaking handles leaks TCP connections to S3 and file descriptors on disk, and eventually the server will stop accepting uploads.

PocketBase also ships a second client: `app.NewBackupsFilesystem()` for the backups bucket/directory, with the same ownership rules.

**Incorrect (no close, raw bytes buffered in memory):**

```go
// ❌ Forgets to close fs - connection leaks
func downloadAvatar(app core.App, key string) ([]byte, error) {
    fs, err := app.NewFilesystem()
    if err != nil {
        return nil, err
    }
    // ❌ no defer fs.Close()

    // ❌ GetFile loads the whole file into a reader; reading it all into a
    //    byte slice defeats streaming for large files
    r, err := fs.GetFile(key)
    if err != nil {
        return nil, err
    }
    defer r.Close()
    return io.ReadAll(r)
}
```

**Correct (defer Close, stream to the HTTP response):**

```go
func serveAvatar(app core.App, key string) echo.HandlerFunc {
    return func(e *core.RequestEvent) error {
        fs, err := app.NewFilesystem()
        if err != nil {
            return e.InternalServerError("filesystem init failed", err)
        }
        defer fs.Close() // REQUIRED

        // Serve directly from the filesystem - handles ranges, content-type,
        // and the X-Accel-Redirect / X-Sendfile headers when available
        return fs.Serve(e.Response, e.Request, key, "avatar.jpg")
    }
}

// Uploading a local file to the PocketBase-managed filesystem
func importAvatar(app core.App, record *core.Record, path string) error {
    f, err := filesystem.NewFileFromPath(path)
    if err != nil {
        return err
    }
    record.Set("avatar", f) // assignment + app.Save() persist it
    return app.Save(record)
}
```

```javascript
// JSVM - file factories live on the $filesystem global
const file1 = $filesystem.fileFromPath("/tmp/import.jpg");
const file2 = $filesystem.fileFromBytes(new Uint8Array([0xff, 0xd8]), "logo.jpg");
const file3 = $filesystem.fileFromURL("https://example.com/a.jpg");

// Assigning to a record field triggers upload on save
record.set("avatar", file1);
$app.save(record);

// Low-level client - MUST be closed
const fs = $app.newFilesystem();
try {
    const list = fs.list("thumbs/");
    for (const obj of list) {
        console.log(obj.key, obj.size);
    }
} finally {
    fs.close(); // REQUIRED
}
```

**Rules:**
- `defer fs.Close()` **immediately** after a successful `NewFilesystem()` / `NewBackupsFilesystem()` call (Go). In JS, wrap in `try { ... } finally { fs.close() }`.
- Prefer the high-level record-field API (`record.Set("field", file)` + `app.Save`) over direct `fs.Upload` calls - it handles thumbs regeneration, orphan cleanup, and hook integration.
- File factory functions (`filesystem.NewFileFromPath`, `NewFileFromBytes`, `NewFileFromURL` / JS `$filesystem.fileFromPath|Bytes|URL`) capture their input; they do not stream until save.
- `fileFromURL` performs an HTTP GET and loads the body into memory - not appropriate for large files.
- Do not share a single long-lived `fs` across unrelated requests; the object is cheap to create per request.

Reference: [Go Filesystem](https://pocketbase.io/docs/go-filesystem/) · [JS Filesystem](https://pocketbase.io/docs/js-filesystem/)

## 4. Bind User Input in Server-Side Filters with {:placeholder} Params

**Impact: CRITICAL (String-concatenating user input into filter expressions is a direct injection vulnerability)**

Server-side helpers like `FindFirstRecordByFilter`, `FindRecordsByFilter`, and `dbx.NewExp` accept a filter string that supports `{:name}` placeholders. **Never** concatenate user input into the filter - PocketBase's filter parser has its own syntax that is sensitive to quoting, and concatenation allows an attacker to alter the query (same class of bug as SQL injection).

**Incorrect (string interpolation - filter injection):**

```go
// ❌ attacker sets email to:   x' || 1=1 || email='
//    resulting filter bypasses the intended match entirely
email := e.Request.URL.Query().Get("email")
record, err := app.FindFirstRecordByFilter(
    "users",
    "email = '"+email+"' && verified = true", // ❌
)
```

```javascript
// JSVM - same class of bug
const email = e.request.url.query().get("email");
const record = $app.findFirstRecordByFilter(
    "users",
    `email = '${email}' && verified = true`, // ❌
);
```

**Correct (named placeholders + params map):**

```go
import "github.com/pocketbase/dbx"

email := e.Request.URL.Query().Get("email")
record, err := app.FindFirstRecordByFilter(
    "users",
    "email = {:email} && verified = true",
    dbx.Params{"email": email}, // values are quoted/escaped by the framework
)
if err != nil {
    return e.NotFoundError("user not found", err)
}

// Paginated variant: FindRecordsByFilter(collection, filter, sort, limit, offset, params...)
recs, err := app.FindRecordsByFilter(
    "posts",
    "author = {:author} && status = {:status}",
    "-created",
    20, 0,
    dbx.Params{"author": e.Auth.Id, "status": "published"},
)
```

```javascript
// JSVM - second argument after the filter is the params object
const record = $app.findFirstRecordByFilter(
    "users",
    "email = {:email} && verified = true",
    { email: email },
);

const recs = $app.findRecordsByFilter(
    "posts",
    "author = {:author} && status = {:status}",
    "-created", 20, 0,
    { author: e.auth.id, status: "published" },
);
```

**Rules:**
- Placeholder syntax is `{:name}` inside the filter string, and the value is supplied via `dbx.Params{"name": value}` (Go) or a plain object (JS).
- The same applies to `dbx.NewExp("LOWER(email) = {:email}", dbx.Params{"email": email})` when writing raw `dbx` expressions.
- Passing a `types.DateTime` / `DateTime` value binds it correctly - do not stringify dates manually.
- `nil` / `null` binds as SQL NULL; use `field = null` or `field != null` in the filter expression.
- The filter grammar is the same as used by collection API rules - consult [Filter Syntax](https://pocketbase.io/docs/api-rules-and-filters/#filters) for operators.

Reference: [Go database - FindRecordsByFilter](https://pocketbase.io/docs/go-records/#fetch-records-via-filter-expression) · [JS database - findRecordsByFilter](https://pocketbase.io/docs/js-records/#fetch-records-via-filter-expression)

## 5. Use DBConnect Only When You Need a Custom SQLite Driver

**Impact: MEDIUM (Incorrect driver setup breaks both data.db and auxiliary.db, or introduces unnecessary CGO)**

PocketBase ships with the **pure-Go** `modernc.org/sqlite` driver (no CGO required). Only reach for a custom driver when you specifically need SQLite extensions like ICU, FTS5, or spatialite that the default driver doesn't expose. `DBConnect` is called **twice** — once for `pb_data/data.db` and once for `pb_data/auxiliary.db` — so driver registration and PRAGMAs must be idempotent.

**Incorrect (unnecessary custom driver, mismatched builder, CGO without justification):**

```go
// ❌ Adding a CGO dependency with no need for extensions
import _ "github.com/mattn/go-sqlite3"

func main() {
    app := pocketbase.NewWithConfig(pocketbase.Config{
        DBConnect: func(dbPath string) (*dbx.DB, error) {
            // ❌ "sqlite3" builder name used but "pb_sqlite3" driver was registered —
            //    or vice versa — causing "unknown driver" / broken query generation
            return dbx.Open("sqlite3", dbPath)
        },
    })
    if err := app.Start(); err != nil {
        log.Fatal(err)
    }
}
```

**Correct (mattn/go-sqlite3 with CGO — proper PRAGMA init hook and builder map entry):**

```go
package main

import (
    "database/sql"
    "log"

    "github.com/mattn/go-sqlite3"
    "github.com/pocketbase/dbx"
    "github.com/pocketbase/pocketbase"
)

func init() {
    // Use a unique driver name to avoid conflicts with other packages.
    // sql.Register panics if called twice with the same name, so put it in init().
    sql.Register("pb_sqlite3", &sqlite3.SQLiteDriver{
        ConnectHook: func(conn *sqlite3.SQLiteConn) error {
            _, err := conn.Exec(`
                PRAGMA busy_timeout      = 10000;
                PRAGMA journal_mode      = WAL;
                PRAGMA journal_size_limit = 200000000;
                PRAGMA synchronous       = NORMAL;
                PRAGMA foreign_keys      = ON;
                PRAGMA temp_store        = MEMORY;
                PRAGMA cache_size        = -32000;
            `, nil)
            return err
        },
    })
    // Mirror the sqlite3 query builder so PocketBase generates correct SQL
    dbx.BuilderFuncMap["pb_sqlite3"] = dbx.BuilderFuncMap["sqlite3"]
}

func main() {
    app := pocketbase.NewWithConfig(pocketbase.Config{
        DBConnect: func(dbPath string) (*dbx.DB, error) {
            return dbx.Open("pb_sqlite3", dbPath)
        },
    })
    if err := app.Start(); err != nil {
        log.Fatal(err)
    }
}
```

**Correct (ncruces/go-sqlite3 — no CGO, PRAGMAs via DSN query string):**

```go
package main

import (
    "log"

    "github.com/pocketbase/dbx"
    "github.com/pocketbase/pocketbase"
    _ "github.com/ncruces/go-sqlite3/driver"
    _ "github.com/ncruces/go-sqlite3/embed"
)

func main() {
    const pragmas = "?_pragma=busy_timeout(10000)" +
        "&_pragma=journal_mode(WAL)" +
        "&_pragma=journal_size_limit(200000000)" +
        "&_pragma=synchronous(NORMAL)" +
        "&_pragma=foreign_keys(ON)" +
        "&_pragma=temp_store(MEMORY)" +
        "&_pragma=cache_size(-32000)"

    app := pocketbase.NewWithConfig(pocketbase.Config{
        DBConnect: func(dbPath string) (*dbx.DB, error) {
            return dbx.Open("sqlite3", "file:"+dbPath+pragmas)
        },
    })
    if err := app.Start(); err != nil {
        log.Fatal(err)
    }
}
```

**Conditional custom driver with default fallback:**

```go
app := pocketbase.NewWithConfig(pocketbase.Config{
    DBConnect: func(dbPath string) (*dbx.DB, error) {
        // Use custom driver only for the main data file; fall back for auxiliary
        if strings.HasSuffix(dbPath, "data.db") {
            return dbx.Open("pb_sqlite3", dbPath)
        }
        return core.DefaultDBConnect(dbPath)
    },
})
```

**Decision guide:**

| Need | Driver |
|------|--------|
| Default (no extensions) | Built-in `modernc.org/sqlite` — no `DBConnect` config needed |
| FTS5, ICU, spatialite | `mattn/go-sqlite3` (CGO) or `ncruces/go-sqlite3` (WASM, no CGO) |
| Reduce binary size | `go build -tags no_default_driver` to exclude the default driver (~4 MB saved) |
| Conditional fallback | Call `core.DefaultDBConnect(dbPath)` inside your `DBConnect` function |

Reference: [Extend with Go - Custom SQLite driver](https://pocketbase.io/docs/go-overview/#custom-sqlite-driver)

## 6. Version Your Schema with Go Migrations

**Impact: HIGH (Guarantees repeatable, transactional schema evolution and eliminates manual dashboard changes in production)**

PocketBase ships with a `migratecmd` plugin that generates versioned `.go` migration files, applies them automatically on `serve`, and lets you roll back with `migrate down`. Because the files are compiled into your binary, no extra migration tool is needed.

**Incorrect (one-off SQL or dashboard changes in production):**

```go
// ❌ Running raw SQL directly at startup without a migration file –
//    the change is applied every restart and has no rollback path.
app.OnServe().BindFunc(func(se *core.ServeEvent) error {
    _, err := app.DB().NewQuery(
        "ALTER TABLE posts ADD COLUMN summary TEXT DEFAULT ''",
    ).Execute()
    return err
})

// ❌ Forgetting to import the migrations package means
//    registered migrations are never executed.
package main

import (
    "github.com/pocketbase/pocketbase"
    "github.com/pocketbase/pocketbase/plugins/migratecmd"
    // _ "myapp/migrations"  ← omitted: migrations never run
)
```

**Correct (register migratecmd, import migrations package):**

```go
// main.go
package main

import (
    "log"
    "os"

    "github.com/pocketbase/pocketbase"
    "github.com/pocketbase/pocketbase/plugins/migratecmd"
    "github.com/pocketbase/pocketbase/tools/osutils"

    // Import side-effects only; this registers all init() migrations.
    _ "myapp/migrations"
)

func main() {
    app := pocketbase.New()

    migratecmd.MustRegister(app, app.RootCmd, migratecmd.Config{
        // Automigrate generates a new .go file whenever you make
        // collection changes in the Dashboard (dev-only).
        Automigrate: osutils.IsProbablyGoRun(),
    })

    if err := app.Start(); err != nil {
        log.Fatal(err)
    }
}
```

**Create and write a migration:**

```bash
# Create a blank migration file in ./migrations/
go run . migrate create "add_summary_to_posts"
```

```go
// migrations/1687801090_add_summary_to_posts.go
package migrations

import (
    "github.com/pocketbase/pocketbase/core"
    m "github.com/pocketbase/pocketbase/migrations"
)

func init() {
    m.Register(func(app core.App) error {
        // app is a transactional App instance – safe to use directly.
        collection, err := app.FindCollectionByNameOrId("posts")
        if err != nil {
            return err
        }

        collection.Fields.Add(&core.TextField{
            Name:     "summary",
            Required: false,
        })

        return app.Save(collection)
    }, func(app core.App) error {
        // Optional rollback
        collection, err := app.FindCollectionByNameOrId("posts")
        if err != nil {
            return err
        }
        collection.Fields.RemoveByName("summary")
        return app.Save(collection)
    })
}
```

**Snapshot all collections (useful for a fresh repo):**

```bash
# Generates a migration file that recreates your current schema from scratch.
go run . migrate collections
```

**Clean up dev migration history:**

```bash
# Remove _migrations table entries that have no matching .go file.
# Run after squashing or deleting intermediate dev migration files.
go run . migrate history-sync
```

**Apply / roll back manually:**

```bash
go run . migrate up        # apply all unapplied migrations
go run . migrate down 1    # revert the last applied migration
```

**Key details:**
- Migration functions receive a **transactional** `core.App` – treat it as the database source of truth. Never use the outer `app` variable inside migration callbacks.
- New unapplied migrations run automatically on every `serve` start – no manual step in production.
- `Automigrate: osutils.IsProbablyGoRun()` limits auto-generation to `go run` (development) and prevents accidental file creation in production binaries.
- Prefer the collection API (`app.Save(collection)`) over raw SQL `ALTER TABLE` so PocketBase's internal schema cache stays consistent.
- Commit all generated `.go` files to version control; do **not** commit `pb_data/`.

Reference: [Extend with Go – Migrations](https://pocketbase.io/docs/go-migrations/)

## 7. Set Up a Go-Extended PocketBase Application

**Impact: HIGH (Foundation for all custom Go business logic, hooks, and routing)**

When extending PocketBase as a Go framework (v0.36+), the entry point is a small `main.go` that creates the app, registers hooks on `OnServe()`, and calls `app.Start()`. Avoid reaching for a global `app` variable inside hook handlers - use `e.App` instead so code works inside transactions.

**Incorrect (global app reuse, no OnServe hook, bare http.Handler):**

```go
package main

import (
    "log"
    "net/http"

    "github.com/pocketbase/pocketbase"
)

var app = pocketbase.New() // global reference used inside handlers

func main() {
    // Routes registered directly via net/http - bypasses PocketBase's router,
    // middleware chain, auth, rate limiter and body limit
    http.HandleFunc("/hello", func(w http.ResponseWriter, r *http.Request) {
        w.Write([]byte("hello"))
    })

    if err := app.Start(); err != nil {
        log.Fatal(err)
    }
}
```

**Correct (register routes inside `OnServe`, use `e.App` in handlers):**

```go
package main

import (
    "log"
    "net/http"
    "os"

    "github.com/pocketbase/pocketbase"
    "github.com/pocketbase/pocketbase/apis"
    "github.com/pocketbase/pocketbase/core"
)

func main() {
    app := pocketbase.New()

    app.OnServe().BindFunc(func(se *core.ServeEvent) error {
        // Serve static assets from ./pb_public (if present)
        se.Router.GET("/{path...}", apis.Static(os.DirFS("./pb_public"), false))

        // Custom API route - namespaced under /api/{yourapp}/ to avoid
        // colliding with built-in /api/collections, /api/realtime, etc.
        se.Router.GET("/api/myapp/hello/{name}", func(e *core.RequestEvent) error {
            return e.JSON(http.StatusOK, map[string]string{
                "message": "hello " + e.Request.PathValue("name"),
            })
        }).Bind(apis.RequireAuth())

        return se.Next()
    })

    if err := app.Start(); err != nil {
        log.Fatal(err)
    }
}
```

**Project bootstrap:**

```bash
go mod init myapp
go mod tidy
go run . serve           # development
go build && ./myapp serve  # production (statically linked binary)
```

**Key details:**
- Requires **Go 1.25.0+** (PocketBase v0.36.7+ bumped the minimum to Go 1.25.0).
- PocketBase ships with the pure-Go `modernc.org/sqlite` driver - **no CGO required** by default.
- If you need FTS5, ICU, or a custom SQLite build, pass `core.DBConnect` in `pocketbase.NewWithConfig(...)` - it is called twice (once for `pb_data/data.db`, once for `pb_data/auxiliary.db`).
- Inside hooks, prefer `e.App` over a captured parent-scope `app` - the hook may run inside a transaction and the parent `app` would deadlock.

Reference: [Extend with Go - Overview](https://pocketbase.io/docs/go-overview/)

## 8. Always Call e.Next() and Use e.App Inside Hook Handlers

**Impact: CRITICAL (Forgetting e.Next() silently breaks the execution chain; reusing parent-scope app causes deadlocks)**

Every PocketBase event hook handler is part of an execution chain. If the handler does not call `e.Next()` (Go) or `e.next()` (JS), **the remaining handlers and the core framework action are skipped silently**. Also, hooks may run inside a DB transaction - any database call made through a captured parent-scope `app`/`$app` instead of the event's own `e.App`/`e.app` will deadlock against the transaction.

**Incorrect (missing `Next`, captured parent-scope app, global mutex):**

```go
var mu sync.Mutex // ❌ global lock invoked recursively by cascade hooks = deadlock
app := pocketbase.New()

app.OnRecordAfterCreateSuccess("articles").BindFunc(func(e *core.RecordEvent) error {
    mu.Lock()
    defer mu.Unlock()

    // ❌ uses outer `app`, not `e.App` - deadlocks when the hook fires
    //    inside a transaction, because the outer app is blocked on the
    //    transaction's write lock
    _, err := app.FindRecordById("audit", e.Record.Id)
    if err != nil {
        return err
    }
    return nil // ❌ forgot e.Next() - framework never persists the record
})
```

```javascript
// JSVM
onRecordAfterCreateSuccess((e) => {
    // ❌ no e.next() = downstream hooks and response serialization skipped
    console.log("created", e.record.id);
}, "articles");
```

**Correct (call Next, use `e.App`, attach an Id for later unbinding):**

```go
app := pocketbase.New()

app.OnRecordAfterCreateSuccess("articles").Bind(&hook.Handler[*core.RecordEvent]{
    Id:       "audit-article-create",
    Priority: 10, // higher = later; default 0 = order of registration
    Func: func(e *core.RecordEvent) error {
        // Always use e.App - it is the transactional app when inside a tx
        audit := core.NewRecord(/* ... */)
        audit.Set("record", e.Record.Id)
        if err := e.App.Save(audit); err != nil {
            return err
        }
        return e.Next() // REQUIRED
    },
})

// Later: app.OnRecordAfterCreateSuccess("articles").Unbind("audit-article-create")
```

```javascript
// JSVM - e.app is the transactional app instance
onRecordAfterCreateSuccess((e) => {
    const audit = new Record($app.findCollectionByNameOrId("audit"));
    audit.set("record", e.record.id);
    e.app.save(audit);

    e.next(); // REQUIRED
}, "articles");
```

**Rules of the execution chain:**

- `Bind(handler)` vs `BindFunc(func)`: `Bind` lets you set `Id` (for `Unbind`) and `Priority`; `BindFunc` auto-generates both.
- Priority defaults to `0` = order of source registration. Lower numbers run first, negative priorities run before defaults (the built-in middlewares use priorities like `-1010`, `-1000`, `-990`).
- **Never hold a global mutex across `e.Next()`** - cascade-delete and nested saves can re-enter the same hook and deadlock.
- `Unbind(id)` removes a specific handler; `UnbindAll()` also removes **system handlers**, so only call it if you really mean to replace the default behavior.
- `Trigger(event, ...)` is almost never needed in user code.

Reference: [Go Event hooks](https://pocketbase.io/docs/go-event-hooks/) · [JS Event hooks](https://pocketbase.io/docs/js-event-hooks/)

## 9. Pick the Right Record Hook - Model vs Request vs Enrich

**Impact: HIGH (Wrong hook = missing request context, double-fired logic, or leaked fields in realtime events)**

PocketBase v0.23+ splits record hooks into three families. Using the wrong one is the #1 source of "my hook doesn't fire" and "my hidden field still shows up in realtime events" bugs.

| Family | Examples | Fires for | Has request context? |
|--------|----------|-----------|----------------------|
| **Model hooks** | `OnRecordCreate`, `OnRecordAfterCreateSuccess`, `OnRecordValidate` | Any save path - Web API **and** cron jobs, custom commands, migrations, calls from other hooks | No - `e.Record`, `e.App`, **no** `e.RequestInfo` |
| **Request hooks** | `OnRecordCreateRequest`, `OnRecordsListRequest`, `OnRecordViewRequest` | **Only** the built-in Web API endpoints | Yes - `e.RequestInfo`, `e.Auth`, HTTP headers/body |
| **Enrich hook** | `OnRecordEnrich` | Every response serialization, **including realtime SSE events** and `apis.enrichRecord` | Yes, via `e.RequestInfo` |

**Incorrect (hiding a field in the request hook - leaks in realtime):**

```go
// ❌ Only runs for GET /api/collections/users/records/{id}.
//    Realtime SSE subscribers still receive the "role" field.
app.OnRecordViewRequest("users").BindFunc(func(e *core.RecordRequestEvent) error {
    e.Record.Hide("role")
    return e.Next()
})
```

**Correct (use `OnRecordEnrich` so realtime and list responses also hide the field):**

```go
app.OnRecordEnrich("users").BindFunc(func(e *core.RecordEnrichEvent) error {
    e.Record.Hide("role")

    // Add a computed field only for authenticated users
    if e.RequestInfo.Auth != nil {
        e.Record.WithCustomData(true) // required to attach non-schema data
        e.Record.Set("isOwner", e.Record.Id == e.RequestInfo.Auth.Id)
    }
    return e.Next()
})
```

```javascript
// JSVM
onRecordEnrich((e) => {
    e.record.hide("role");

    if (e.requestInfo.auth?.collection()?.name === "users") {
        e.record.withCustomData(true);
        e.record.set("computedScore",
            e.record.get("score") * e.requestInfo.auth.get("base"));
    }
    e.next();
}, "users");
```

**Selection guide:**
- Need to mutate the record before **any** save (API, cron, migration, nested hook)? → `OnRecordCreate` / `OnRecordUpdate` (pre-save) or `OnRecord*Success` (post-save).
- Need access to HTTP headers, query params, or the authenticated client? → `OnRecord*Request`.
- Need to hide fields, redact values, or attach computed props on responses including realtime? → **`OnRecordEnrich`** - this is the safest default for response shaping.
- Need to validate before save? → `OnRecordValidate` (proxy over `OnModelValidate`).

Reference: [Go Record request hooks](https://pocketbase.io/docs/go-event-hooks/#record-crud-request-hooks) · [JS Record model hooks](https://pocketbase.io/docs/js-event-hooks/#record-model-hooks)

## 10. Write JSVM Migrations as pb_migrations/*.js Files

**Impact: HIGH (JSVM migrations look different from Go ones; missing the timestamp prefix or the down-callback silently breaks replay)**

JSVM migrations live in `pb_migrations/` next to the executable. Unlike Go migrations (which use `init()` + `m.Register(...)` inside a package imported from `main.go`), JSVM migrations are **auto-discovered by filename** and call the global `migrate()` function with an `up` callback and an optional `down` callback. `--automigrate` is on by default in v0.36+, so admin-UI changes generate these files for you; you also write them by hand for data migrations, seed data, and index changes that the UI can't express.

**Incorrect (wrong filename format, missing down, raw SQL without cache invalidation):**

```javascript
// pb_migrations/add_audit.js   ❌ missing <unix>_ prefix - never runs
migrate((app) => {
    // ❌ Raw ALTER TABLE leaves PocketBase's internal collection cache stale
    app.db().newQuery(
        "ALTER TABLE posts ADD COLUMN summary TEXT DEFAULT ''"
    ).execute();
});
// ❌ No down callback - `migrate down` cannot revert this in dev
```

**Correct (timestamped filename, collection API, both up and down):**

```javascript
// pb_migrations/1712500000_add_audit_collection.js
/// <reference path="../pb_data/types.d.ts" />

migrate(
    // UP - runs on `serve` / `migrate up`
    (app) => {
        const collection = new Collection({
            type: "base",
            name: "audit",
            fields: [
                { name: "action", type: "text", required: true },
                { name: "actor",  type: "relation", collectionId: "_pb_users_auth_", cascadeDelete: false },
                { name: "meta",   type: "json" },
                { name: "created", type: "autodate", onCreate: true },
            ],
            indexes: [
                "CREATE INDEX idx_audit_actor ON audit (actor)",
                "CREATE INDEX idx_audit_created ON audit (created)",
            ],
        });
        app.save(collection);
    },
    // DOWN - runs on `migrate down N`
    (app) => {
        const collection = app.findCollectionByNameOrId("audit");
        app.delete(collection);
    },
);
```

**Seed data migration (common pattern):**

```javascript
// pb_migrations/1712500100_seed_default_tags.js
/// <reference path="../pb_data/types.d.ts" />

migrate(
    (app) => {
        const tags = app.findCollectionByNameOrId("tags");
        for (const name of ["urgent", "bug", "feature", "docs"]) {
            const r = new Record(tags);
            r.set("name", name);
            app.save(r); // `app` here is the transactional app - all or nothing
        }
    },
    (app) => {
        const tags = app.findCollectionByNameOrId("tags");
        for (const name of ["urgent", "bug", "feature", "docs"]) {
            const r = app.findFirstRecordByFilter(
                "tags",
                "name = {:name}",
                { name },
            );
            if (r) app.delete(r);
        }
    },
);
```

**CLI commands (same as Go migrations):**

```bash
./pocketbase migrate create "add_audit_collection"  # templated blank file
./pocketbase migrate up                              # apply pending
./pocketbase migrate down 1                          # revert last
./pocketbase migrate history-sync                    # reconcile _migrations table
```

**Rules:**
- **Filename format**: `<unix_timestamp>_<description>.js`. The timestamp sets ordering. Never renumber a committed file.
- **The `app` argument is transactional**: every migration runs inside its own transaction. Throw to roll back. Do not capture `$app` from the outer scope - use the `app` parameter so the work participates in the tx.
- **Use the collection API** (`new Collection`, `app.save(collection)`), not raw `ALTER TABLE`. Raw SQL leaves PocketBase's in-memory schema cache stale until the next restart.
- **Always write the down callback** in development. In production, down migrations are rare but the callback is what makes `migrate down 1` work during emergency rollbacks.
- **Do not import from other files** - goja has no ES modules, and at migration time the `pb_hooks` loader has not necessarily run. Keep each migration self-contained.
- **Commit `pb_migrations/` to version control**. Never commit `pb_data/`.
- **Conflicting with Go migrations**: you can run either Go or JS migrations, not a mix of both in the same project. JSVM migrations are enabled by default; Go migrations require `migratecmd.MustRegister(...)` in `main.go`.

Reference: [Extend with JavaScript - Migrations](https://pocketbase.io/docs/js-migrations/)

## 11. Set Up JSVM (pb_hooks) for Server-Side JavaScript

**Impact: HIGH (Correct setup unlocks hot-reload, type-completion, and the full JSVM API)**

The prebuilt PocketBase executable embeds an ES5 JavaScript engine (goja). Drop `*.pb.js` files into a `pb_hooks` directory next to the executable and they load automatically at startup. Files are loaded in **filename sort order**, and on UNIX platforms the process auto-reloads when any `pb_hooks` file changes.

**Incorrect (TypeScript without transpile, wrong filename, missing types reference):**

```typescript
// pb_hooks/main.ts  ❌ PocketBase loads ONLY *.pb.js - a .ts file is ignored
import { something } from "./lib"; // ❌ ES modules not supported in goja

routerAdd("GET", "/hello", (e) => e.json(200, { ok: true }));
```

```javascript
// pb_hooks/hooks.js  ❌ wrong extension - must be *.pb.js
// No /// reference -> editor shows every call as "any"
onRecordAfterUpdateSuccess((e) => {
    console.log(e.record.get("email"));
    // Missing e.next() - stops the execution chain silently
}, "users");
```

**Correct (valid filename, types reference, `e.next()` called):**

```javascript
// pb_hooks/main.pb.js
/// <reference path="../pb_data/types.d.ts" />

// Hooks defined earlier in the filename sort order run first.
// Use prefixes like "01_", "10_", "99_" if order matters.

routerAdd("GET", "/api/myapp/hello/{name}", (e) => {
    const name = e.request.pathValue("name");
    return e.json(200, { message: "Hello " + name });
});

onRecordAfterUpdateSuccess((e) => {
    console.log("user updated:", e.record.get("email"));
    e.next(); // REQUIRED - otherwise the execution chain is broken
}, "users");
```

**Key details:**
- JS method names are **camelCase** versions of their Go equivalents (`FindRecordById` → `$app.findRecordById`).
- Errors are thrown as regular JS exceptions, not returned as values.
- Global objects: `$app` (the app), `$apis` (routing helpers/middlewares), `$os` (OS primitives), `$security` (JWT, random strings, AES), `$filesystem` (file factories), `$dbx` (query builder), `$mails` (email helpers), `__hooks` (absolute path to `pb_hooks`).
- `pb_data/types.d.ts` is regenerated automatically - commit the triple-slash reference but not the file itself if you prefer.
- Auto-reload on file change works on UNIX only. On Windows, restart the process manually.

Reference: [Extend with JavaScript - Overview](https://pocketbase.io/docs/js-overview/)

## 12. Load Shared Code with CommonJS require() in pb_hooks

**Impact: MEDIUM (Correct module usage prevents require() failures, race conditions, and ESM import errors)**

The embedded JSVM (goja) supports **only CommonJS** (`require()`). ES module `import` syntax is not supported without pre-bundling. Modules use a shared registry — they are evaluated once and cached, so avoid mutable module-level state to prevent race conditions across concurrent requests.

**Incorrect (ESM imports, mutable shared state, Node.js APIs):**

```javascript
// ❌ ESM import syntax — not supported by goja
import { sendEmail } from "./utils.js";

// ❌ Node.js APIs don't exist in the JSVM sandbox
const fs = require("fs");
fs.writeFileSync("output.txt", "hello"); // ReferenceError

// ❌ Mutable module-level state is shared across concurrent requests
// pb_hooks/counter.js
let requestCount = 0;
module.exports = { increment: () => ++requestCount }; // race condition
```

**Correct (CommonJS require, stateless helpers, JSVM bindings for OS/file ops):**

```javascript
// pb_hooks/utils.js  — stateless helper module
module.exports = {
    formatDate: (d) => new Date(d).toISOString().slice(0, 10),
    validateEmail: (addr) => /^[^@]+@[^@]+\.[^@]+$/.test(addr),
};

// pb_hooks/main.pb.js
/// <reference path="../pb_data/types.d.ts" />

onRecordAfterCreateSuccess((e) => {
    const utils = require(`${__hooks}/utils.js`);
    const date = utils.formatDate(e.record.get("created"));
    console.log("Record created on:", date);
    e.next();
}, "posts");

// Use $os.* for file system operations (not Node.js fs)
routerAdd("GET", "/api/myapp/read-config", (e) => {
    const raw = $os.readFile(`${__hooks}/config.json`);
    const cfg = JSON.parse(raw);
    return e.json(200, { name: cfg.appName });
});

// Use $filesystem.s3(...) or $filesystem.local(...) for storage (v0.36.4+)
routerAdd("POST", "/api/myapp/upload", (e) => {
    const bucket = $filesystem.s3({
        endpoint: "s3.amazonaws.com",
        bucket:   "my-bucket",
        region:   "us-east-1",
        accessKey: $app.settings().s3.accessKey,
        secret:    $app.settings().s3.secret,
    });
    // ... use bucket to store/retrieve files
    return e.json(200, { ok: true });
}, $apis.requireAuth());
```

**Using third-party CJS packages:**

```javascript
// node_modules/ is searched automatically alongside __hooks.
// Install packages with npm next to the pb_hooks directory, then require by name.
onBootstrap((e) => {
    e.next();
    // Only CJS-compatible packages work without bundling
    const slugify = require("slugify");
    console.log(slugify("Hello World")); // "Hello-World"
});
```

**Using ESM-only packages (bundle to CJS first):**

```bash
# Bundle an ESM package to CJS with rollup before committing it to pb_hooks
npx rollup node_modules/some-esm-pkg/index.js \
  --file pb_hooks/vendor/some-esm-pkg.js \
  --format cjs
```

```javascript
onBootstrap((e) => {
    e.next();
    const pkg = require(`${__hooks}/vendor/some-esm-pkg.js`);
});
```

**JSVM engine limitations:**
- No `setTimeout` / `setInterval` — no async scheduling inside handlers.
- No Node.js APIs (`fs`, `Buffer`, `process`, etc.) — use `$os.*` and `$filesystem.*` JSVM bindings instead.
- No browser APIs (`fetch`, `window`, `localStorage`) — use `$app.newHttpClient()` for outbound HTTP requests.
- ES6 is mostly supported but not fully spec-compliant (goja engine).
- The prebuilt PocketBase executable starts a **pool of 15 JS runtimes** by default; adjust with `--hooksPool=N` for high-concurrency workloads (more runtimes = more memory, better throughput).
- `nullString()`, `nullInt()`, `nullFloat()`, `nullBool()`, `nullArray()`, `nullObject()` helpers are available (v0.35.0+) for scanning nullable DB columns safely.

Reference: [Extend with JavaScript - Loading modules](https://pocketbase.io/docs/js-overview/#loading-modules)

## 13. Avoid Capturing Variables Outside JSVM Handler Scope

**Impact: HIGH (Variables defined outside a handler are undefined at runtime due to handler serialization)**

Each JSVM handler (hook, route, middleware) is **serialized and executed as an isolated program**. Variables or functions declared at the module/file scope are NOT accessible inside handler bodies. This is the most common source of `undefined` errors in `pb_hooks` code.

**Incorrect (accessing outer-scope variable inside handler):**

```javascript
// pb_hooks/main.pb.js
const APP_NAME = "myapp"; // ❌ will be undefined inside handlers

onBootstrap((e) => {
    e.next();
    console.log(APP_NAME); // ❌ undefined — APP_NAME is not in handler scope
});

// ❌ Even $app references captured here may not work as expected
const helper = (id) => $app.findRecordById("posts", id);

onRecordAfterCreateSuccess((e) => {
    helper(e.record.id); // ❌ helper is undefined inside the handler
}, "posts");
```

**Correct (move shared state into a required module, or use `$app`/`e.app` directly):**

```javascript
// pb_hooks/config.js  — stateless CommonJS module
module.exports = {
    APP_NAME: "myapp",
    MAX_RETRIES: 3,
};

// pb_hooks/main.pb.js
/// <reference path="../pb_data/types.d.ts" />

onBootstrap((e) => {
    e.next();
    // Load the shared module INSIDE the handler
    const config = require(`${__hooks}/config.js`);
    console.log(config.APP_NAME); // ✅ "myapp"
});

routerAdd("GET", "/api/myapp/status", (e) => {
    const config = require(`${__hooks}/config.js`);
    return e.json(200, { app: config.APP_NAME });
});

onRecordAfterCreateSuccess((e) => {
    // Access the app directly via e.app inside the handler
    const post = e.app.findRecordById("posts", e.record.id);
    e.next();
}, "posts");
```

**Key rules:**
- Every handler body is serialized to a string and executed in its own isolated goja runtime context. There is no shared global state between handlers at runtime.
- `require()` loads modules from a **shared registry** — modules are evaluated once and cached. Keep module-level code stateless; avoid mutable module exports to prevent data races under concurrent requests.
- `__hooks` is always available inside handlers and resolves to the absolute path of the `pb_hooks` directory.
- Error stack trace line numbers may not be accurate because of the handler serialization — log meaningful context manually when debugging.
- Workaround for simple constants: move them to a `config.js` module and `require()` it inside each handler that needs it.

Reference: [Extend with JavaScript - Handlers scope](https://pocketbase.io/docs/js-overview/#handlers-scope)

## 14. Send Email via app.NewMailClient, Never the Default example.com Sender

**Impact: HIGH (Default sender is no-reply@example.com; shipping it bounces every email and damages your SMTP reputation)**

PocketBase ships with a mailer accessible through `app.NewMailClient()` (Go) or `$app.newMailClient()` (JS). It reads the SMTP settings configured in **Admin UI → Settings → Mail settings**, or falls back to a local `sendmail`-like client if SMTP is not configured. Two things bite people: (1) the default `Meta.senderAddress` is `no-reply@example.com` - shipping with that bounces every email and poisons your sender reputation; (2) there is no connection pooling, so long-lived mail client handles are **not** safe to share across requests - create one per send.

**Incorrect (default sender, shared client, no error handling):**

```go
// ❌ Default sender is example.com, and this mailer instance is captured
//    for the process lifetime - SMTP connections go stale
var mailer = app.NewMailClient()

app.OnRecordAfterCreateSuccess("orders").BindFunc(func(e *core.RecordEvent) error {
    msg := &mailer.Message{
        From:    mail.Address{Address: "no-reply@example.com"}, // ❌
        To:      []mail.Address{{Address: e.Record.GetString("email")}},
        Subject: "Order confirmed",
        HTML:    "<p>Thanks</p>",
    }
    mailer.Send(msg) // ❌ error swallowed
    return e.Next()
})
```

**Correct (sender from settings, per-send client, explicit error path):**

```go
import (
    "net/mail"
    pbmail "github.com/pocketbase/pocketbase/tools/mailer"
)

app.OnRecordAfterCreateSuccess("orders").BindFunc(func(e *core.RecordEvent) error {
    // IMPORTANT: resolve the sender from settings at send-time, not at
    // startup - an admin can change it live from the UI
    meta := e.App.Settings().Meta
    from := mail.Address{
        Name:    meta.SenderName,
        Address: meta.SenderAddress,
    }

    msg := &pbmail.Message{
        From:    from,
        To:      []mail.Address{{Address: e.Record.GetString("email")}},
        Subject: "Order confirmed",
        HTML:    renderOrderEmail(e.Record), // your template function
    }

    // Create the client per send - avoids stale TCP sessions
    if err := e.App.NewMailClient().Send(msg); err != nil {
        e.App.Logger().Error("order email send failed",
            "err",      err,
            "recordId", e.Record.Id,
        )
        // Do NOT return the error - a failed email should not roll back the order
    }
    return e.Next()
})
```

```javascript
// JSVM - $mails global exposes message factories
onRecordAfterCreateSuccess((e) => {
    const meta = $app.settings().meta;

    const message = new MailerMessage({
        from: {
            address: meta.senderAddress,
            name:    meta.senderName,
        },
        to:      [{ address: e.record.get("email") }],
        subject: "Order confirmed",
        html:    `<p>Thanks for order ${e.record.id}</p>`,
    });

    try {
        $app.newMailClient().send(message);
    } catch (err) {
        $app.logger().error("order email send failed", "err", err, "id", e.record.id);
        // swallow - do not rollback the order
    }
    e.next();
}, "orders");
```

**Templated emails via the built-in verification/reset templates:**

```go
// PocketBase has baked-in templates for verification, password reset, and
// email change. Trigger them via apis.*Request helpers rather than building
// your own message:
//   apis.RecordRequestPasswordReset(app, authRecord)
//   apis.RecordRequestVerification(app, authRecord)
//   apis.RecordRequestEmailChange(app, authRecord, newEmail)
//
// These use the templates configured in Admin UI → Settings → Mail templates.
```

**Rules:**
- **Always change `Meta.SenderAddress`** before shipping. In development, use Mailpit or MailHog; in production, use a verified domain that matches your SPF/DKIM records.
- **Resolve the sender from `app.Settings().Meta` at send-time**, not at startup. Settings are mutable from the admin UI.
- **Create the client per send** (`app.NewMailClient()` / `$app.newMailClient()`). It is cheap - it re-reads the SMTP settings each time, so config changes take effect without a restart.
- **Never return a send error from a hook** unless the user's action genuinely depends on the email going out. Email failure is common (transient SMTP, address typo) and should not roll back a business transaction.
- **Log failures with context** (record id, recipient domain) so you can grep them later. PocketBase does not retry failed sends.
- **For bulk sending, queue it**. The mailer is synchronous - looping `Send()` over 10k records blocks the request. Push to a cron-drained queue collection instead.
- **Template rendering**: Go users should use `html/template`; JS users can use template literals or pull in a tiny template lib. PocketBase itself only renders templates for its baked-in flows.

Reference: [Go Mailer](https://pocketbase.io/docs/go-sending-emails/) · [JS Mailer](https://pocketbase.io/docs/js-sending-emails/)

## 15. Register Custom Routes Safely with Built-in Middlewares

**Impact: HIGH (Protects custom endpoints with auth, avoids /api path collisions, inherits rate limiting)**

PocketBase routing is built on top of `net/http.ServeMux`. Custom routes are registered inside the `OnServe()` hook (Go) or via `routerAdd()` / `routerUse()` (JSVM). **Always** namespace custom routes under `/api/{yourapp}/...` to avoid colliding with built-in endpoints, and attach `apis.RequireAuth()` / `$apis.requireAuth()` (or stricter) to anything that is not meant to be public.

**Incorrect (path collision, no auth, raw ResponseWriter):**

```go
// ❌ "/api/records" collides with /api/collections/{name}/records built-in
se.Router.POST("/api/records", func(e *core.RequestEvent) error {
    // ❌ no auth check - anyone can call this
    // ❌ returns raw text; no content-type
    e.Response.Write([]byte("ok"))
    return nil
})
```

**Correct (namespaced, authenticated, group-scoped middleware):**

```go
app.OnServe().BindFunc(func(se *core.ServeEvent) error {
    // Group everything under /api/myapp/ and require auth for the entire group
    g := se.Router.Group("/api/myapp")
    g.Bind(apis.RequireAuth())                  // authenticated users only
    g.Bind(apis.Gzip())                         // compress responses
    g.Bind(apis.BodyLimit(10 << 20))            // per-route override of default 32MB limit

    g.GET("/profile", func(e *core.RequestEvent) error {
        return e.JSON(http.StatusOK, map[string]any{
            "id":    e.Auth.Id,
            "email": e.Auth.GetString("email"),
        })
    })

    // Superuser-only admin endpoint
    g.POST("/admin/rebuild-index", func(e *core.RequestEvent) error {
        // ... do the work
        return e.JSON(http.StatusOK, map[string]bool{"ok": true})
    }).Bind(apis.RequireSuperuserAuth())

    // Resource the owner (or a superuser) can access
    g.GET("/users/{id}/private", func(e *core.RequestEvent) error {
        return e.JSON(http.StatusOK, map[string]string{"private": "data"})
    }).Bind(apis.RequireSuperuserOrOwnerAuth("id"))

    return se.Next()
})
```

```javascript
// JSVM
routerAdd("GET", "/api/myapp/profile", (e) => {
    return e.json(200, {
        id: e.auth.id,
        email: e.auth.getString("email"),
    });
}, $apis.requireAuth());

routerAdd("POST", "/api/myapp/admin/rebuild-index", (e) => {
    return e.json(200, { ok: true });
}, $apis.requireSuperuserAuth());
```

**Built-in middlewares (Go: `apis.*`, JS: `$apis.*`):**

| Middleware | Use |
|---|---|
| `RequireGuestOnly()` | Reject authenticated clients (e.g. public signup forms) |
| `RequireAuth(...collections)` | Require any auth record; optionally restrict to specific auth collections |
| `RequireSuperuserAuth()` | Alias for `RequireAuth("_superusers")` |
| `RequireSuperuserOrOwnerAuth("id")` | Allow superusers OR the auth record whose id matches the named path param |
| `Gzip()` | Gzip-compress the response |
| `BodyLimit(bytes)` | Override the default 32MB request body cap (0 = no limit) |
| `SkipSuccessActivityLog()` | Suppress activity log for successful responses |

**Path details:**
- Patterns follow `net/http.ServeMux`: `{name}` = single segment, `{name...}` = catch-all.
- A trailing `/` acts as a prefix wildcard; use `{$}` to anchor to the exact path only.
- **Always** prefix custom routes with `/api/{yourapp}/` - do not put them under `/api/` alone, which collides with built-in collection / realtime / settings endpoints.
- Order: global middlewares → group middlewares → route middlewares → handler. Use negative priorities to run before built-ins if needed.

Reference: [Go Routing](https://pocketbase.io/docs/go-routing/) · [JS Routing](https://pocketbase.io/docs/js-routing/)

## 16. Read Settings via app.Settings(), Encrypt at Rest with PB_ENCRYPTION

**Impact: HIGH (Hardcoded secrets and unencrypted settings storage are the #1 source of credential leaks)**

PocketBase stores every runtime-mutable setting (SMTP credentials, S3 keys, OAuth2 client secrets, JWT secrets for each auth collection) in the `_params` table as JSON. Admin UI edits write to the same place. There are two knobs that matter: (1) **how you read settings from Go/JS** - always via `app.Settings()` at call time, never captured at startup; (2) **how they are stored on disk** - set the `PB_ENCRYPTION` env var to a 32-char key so the whole blob is encrypted at rest. Without encryption, anyone with a copy of `data.db` has your SMTP password, OAuth2 secrets, and every collection's signing key.

**Incorrect (hardcoded secret, captured at startup, unencrypted at rest):**

```go
// ❌ Secret compiled into the binary - leaks via `strings ./pocketbase`
const slackWebhook = "https://hooks.slack.com/services/T00/B00/XXXX"

// ❌ Captured once at startup - if an admin rotates the SMTP password via the
//    UI, this stale value keeps trying until restart
var smtpHost = app.Settings().SMTP.Host

// ❌ No PB_ENCRYPTION set - `sqlite3 pb_data/data.db "SELECT * FROM _params"`
//    prints every secret in plaintext
./pocketbase serve
```

**Correct (env + settings lookup at call time + encryption at rest):**

```bash
# Generate a 32-char encryption key once and store it in your secrets manager
# (1Password, SOPS, AWS SSM, etc). Commit NOTHING related to this value.
openssl rand -hex 16    # 32 hex chars

# Start with the key exported - PocketBase AES-encrypts _params on write
# and decrypts on read. Losing the key == losing access to settings.
export PB_ENCRYPTION="3a7c...deadbeef32charsexactly"
./pocketbase serve
```

```go
// Reading mutable settings at call time - reflects live UI changes
func notifyAdmin(app core.App, msg string) error {
    meta := app.Settings().Meta
    from := mail.Address{Name: meta.SenderName, Address: meta.SenderAddress}
    // ...
}

// Mutating settings programmatically (e.g. during a migration)
settings := app.Settings()
settings.Meta.AppName = "MyApp"
settings.SMTP.Enabled = true
settings.SMTP.Host = os.Getenv("SMTP_HOST") // inject from env at write time
if err := app.Save(settings); err != nil {
    return err
}
```

```javascript
// JSVM
onBootstrap((e) => {
    e.next();

    const settings = $app.settings();
    settings.meta.appName = "MyApp";
    $app.save(settings);
});

// At send-time
const meta = $app.settings().meta;
```

**Secrets that do NOT belong in `app.Settings()`:**

- Database encryption key itself → `PB_ENCRYPTION` env var (not in the DB, obviously)
- Third-party webhooks your code calls (Slack, Stripe, etc) → env vars, read via `os.Getenv` / `$os.getenv`
- CI tokens, deploy keys → your secrets manager, not PocketBase

`app.Settings()` is for things an **admin** should be able to rotate through the UI. Everything else lives in env vars, injected by your process supervisor (systemd, Docker, Kubernetes).

**Key details:**
- **`PB_ENCRYPTION` must be exactly 32 characters.** Anything else crashes at startup.
- **Losing the key is unrecoverable** - the settings blob cannot be decrypted, and the server refuses to boot. Back up the key alongside (but separately from) your `pb_data` backups.
- **Rotating the key**: start with the old key set, call `app.Settings()` → `app.Save(settings)` to re-encrypt under the new key, then restart with the new key. Do this under a maintenance window.
- **Settings changes fire `OnSettingsReload`** - use it if you have in-memory state that depends on a setting (e.g. a rate limiter sized from `app.Settings().RateLimits.Default`).
- **Do not call `app.Settings()` in a hot loop.** It returns a fresh copy each time. Cache for the duration of a single request, not the process.
- **`app.Save(settings)`** persists and broadcasts the reload event. Mutating the returned struct without saving is a no-op.

Reference: [Settings](https://pocketbase.io/docs/going-to-production/#use-encryption-for-the-pb_data-settings) · [OnSettingsReload hook](https://pocketbase.io/docs/go-event-hooks/#app-hooks)

## 17. Test Hooks and Routes with tests.NewTestApp and ApiScenario

**Impact: HIGH (Without the tests package you cannot exercise hooks, middleware, and transactions in isolation)**

PocketBase ships a `tests` package specifically for integration-testing Go extensions. `tests.NewTestApp(testDataDir)` builds a fully-wired `core.App` over a **temp copy** of your test data directory, so you can register hooks, fire requests through the real router, and assert on the resulting DB state without spinning up a real HTTP server or touching `pb_data/`. The `tests.ApiScenario` struct drives the router the same way a real HTTP client would, including middleware and transactions. Curl-based shell tests cannot do either of these things.

**Incorrect (hand-rolled HTTP client, shared dev DB, no hook reset):**

```go
// ❌ Hits the actual dev server - depends on side-effects from a previous run
func TestCreatePost(t *testing.T) {
    resp, _ := http.Post("http://localhost:8090/api/collections/posts/records",
        "application/json",
        strings.NewReader(`{"title":"hi"}`))
    if resp.StatusCode != 200 {
        t.Fatal("bad status")
    }
    // ❌ No DB assertion, no cleanup, no hook verification
}
```

**Correct (NewTestApp + ApiScenario + AfterTestFunc assertions):**

```go
// internal/app/posts_test.go
package app_test

import (
    "net/http"
    "strings"
    "testing"

    "github.com/pocketbase/pocketbase/core"
    "github.com/pocketbase/pocketbase/tests"

    "myapp/internal/hooks" // your hook registration
)

// testDataDir is a checked-in pb_data snapshot with your collections.
// Create it once with `./pocketbase --dir ./test_pb_data migrate up`
// and commit it to your test fixtures.
const testDataDir = "../../test_pb_data"

func TestCreatePostFiresAudit(t *testing.T) {
    // Each test gets its own copy of testDataDir - parallel-safe
    app, err := tests.NewTestApp(testDataDir)
    if err != nil {
        t.Fatal(err)
    }
    defer app.Cleanup() // REQUIRED - removes the temp copy

    // Register the hook under test against this isolated app
    hooks.RegisterPostHooks(app)

    scenario := tests.ApiScenario{
        Name:   "POST /api/collections/posts/records as verified user",
        Method: http.MethodPost,
        URL:    "/api/collections/posts/records",
        Body:   strings.NewReader(`{"title":"hello","slug":"hello"}`),
        Headers: map[string]string{
            "Authorization": testAuthHeader(app, "users", "alice@example.com"),
            "Content-Type":  "application/json",
        },
        ExpectedStatus: 200,
        ExpectedContent: []string{
            `"title":"hello"`,
            `"slug":"hello"`,
        },
        NotExpectedContent: []string{
            `"internalNotes"`, // the enrich hook should hide this
        },
        ExpectedEvents: map[string]int{
            "OnRecordCreateRequest":       1,
            "OnRecordAfterCreateSuccess":  1,
            "OnRecordEnrich":              1,
        },
        AfterTestFunc: func(t testing.TB, app *tests.TestApp, res *http.Response) {
            // Assert side-effects in the DB using the SAME app instance
            audits, err := app.FindRecordsByFilter(
                "audit",
                "action = 'post.create'",
                "-created", 10, 0,
            )
            if err != nil {
                t.Fatal(err)
            }
            if len(audits) != 1 {
                t.Fatalf("expected 1 audit record, got %d", len(audits))
            }
        },
        TestAppFactory: func(t testing.TB) *tests.TestApp { return app },
    }

    scenario.Test(t)
}
```

**Table-driven variant (authz matrix):**

```go
func TestPostsListAuthz(t *testing.T) {
    for _, tc := range []struct {
        name   string
        auth   string  // "", "users:alice", "users:bob", "_superusers:root"
        expect int
    }{
        {"guest gets public posts",       "",                200},
        {"authed gets own + public",      "users:alice",     200},
        {"superuser sees everything",     "_superusers:root",200},
    } {
        t.Run(tc.name, func(t *testing.T) {
            app, _ := tests.NewTestApp(testDataDir)
            defer app.Cleanup()
            hooks.RegisterPostHooks(app)

            tests.ApiScenario{
                Method:         http.MethodGet,
                URL:            "/api/collections/posts/records",
                Headers:        authHeaderFor(app, tc.auth),
                ExpectedStatus: tc.expect,
                TestAppFactory: func(t testing.TB) *tests.TestApp { return app },
            }.Test(t)
        })
    }
}
```

**Unit-testing a hook in isolation (no HTTP layer):**

```go
func TestAuditHookRollsBackOnAuditFailure(t *testing.T) {
    app, _ := tests.NewTestApp(testDataDir)
    defer app.Cleanup()
    hooks.RegisterPostHooks(app)

    // Delete the audit collection so the hook's Save fails
    audit, _ := app.FindCollectionByNameOrId("audit")
    _ = app.Delete(audit)

    col, _ := app.FindCollectionByNameOrId("posts")
    post := core.NewRecord(col)
    post.Set("title", "should rollback")
    post.Set("slug", "rollback")

    if err := app.Save(post); err == nil {
        t.Fatal("expected Save to fail because audit hook errored")
    }

    // Assert the post was NOT persisted (tx rolled back)
    _, err := app.FindFirstRecordByFilter("posts", "slug = 'rollback'", nil)
    if err == nil {
        t.Fatal("post should not exist after rollback")
    }
}
```

**Rules:**
- **Always `defer app.Cleanup()`** - otherwise temp directories leak under `/tmp`.
- **Use a checked-in `test_pb_data/` fixture** with the collections you need. Do not depend on the dev `pb_data/` - tests must be hermetic.
- **Register hooks against the test app**, not against a package-level `app` singleton. The test app is a fresh instance each time.
- **`ExpectedEvents`** asserts that specific hooks fired the expected number of times - use it to catch "hook silently skipped because someone forgot `e.Next()`" regressions.
- **`AfterTestFunc`** runs with the same app instance the scenario used, so you can query the DB to verify side-effects.
- **Parallelize with `t.Parallel()`** - `NewTestApp` gives each goroutine its own copy, so there's no shared state.
- **Tests run pure-Go SQLite** (`modernc.org/sqlite`) - no CGO, no extra setup, works on `go test ./...` out of the box.
- **For JSVM**, there is no equivalent test harness yet - test pb_hooks by booting `tests.NewTestApp` with the `pb_hooks/` directory populated and exercising the router from Go. Pure-JS unit testing of hook bodies requires extracting the logic into a `require()`able module.

Reference: [Testing](https://pocketbase.io/docs/go-testing/) · [tests package GoDoc](https://pkg.go.dev/github.com/pocketbase/pocketbase/tests)

## 18. Use RunInTransaction with the Scoped txApp, Never the Outer App

**Impact: CRITICAL (Mixing scoped and outer app inside a transaction silently deadlocks or writes outside the tx)**

`app.RunInTransaction` (Go) and `$app.runInTransaction` (JS) wrap a block of work in a SQLite write transaction. The callback receives a **transaction-scoped app instance** (`txApp` / `txApp`). Every database call inside the block must go through that scoped instance - reusing the outer `app` / `$app` bypasses the transaction (silent partial writes) or deadlocks (SQLite allows only one writer).

**Incorrect (outer `app` used inside the tx block):**

```go
// ❌ Uses the outer app for the second Save - deadlocks on the writer lock
err := app.RunInTransaction(func(txApp core.App) error {
    user := core.NewRecord(usersCol)
    user.Set("email", "a@b.co")
    if err := txApp.Save(user); err != nil {
        return err
    }

    audit := core.NewRecord(auditCol)
    audit.Set("user", user.Id)
    return app.Save(audit) // ❌ NOT txApp - blocks forever
})
```

**Correct (always `txApp` inside the block, return errors to roll back):**

```go
err := app.RunInTransaction(func(txApp core.App) error {
    user := core.NewRecord(usersCol)
    user.Set("email", "a@b.co")
    if err := txApp.Save(user); err != nil {
        return err // rollback
    }

    audit := core.NewRecord(auditCol)
    audit.Set("user", user.Id)
    if err := txApp.Save(audit); err != nil {
        return err // rollback
    }
    return nil // commit
})
if err != nil {
    return err
}
```

```javascript
// JSVM - the callback receives the transactional app
$app.runInTransaction((txApp) => {
    const user = new Record(txApp.findCollectionByNameOrId("users"));
    user.set("email", "a@b.co");
    txApp.save(user);

    const audit = new Record(txApp.findCollectionByNameOrId("audit"));
    audit.set("user", user.id);
    txApp.save(audit);

    // throw anywhere in this block to roll back the whole tx
});
```

**Rules of the transaction:**
- **Use only `txApp` / the callback's scoped app** inside the block. Capturing the outer `app` defeats the purpose and can deadlock.
- Inside event hooks, `e.App` is already the transactional app when the hook fires inside a tx - prefer it over a captured parent-scope `app` for the same reason.
- Return an error (Go) or `throw` (JS) to roll back. A successful return commits.
- SQLite serializes writers - keep transactions **short**. Do not make HTTP calls, send emails, or wait on external systems inside the block.
- Do not start a transaction inside another transaction on the same app - nested `RunInTransaction` on `txApp` is supported and reuses the existing transaction, but nested calls on the outer `app` will deadlock.
- Hooks (`OnRecordAfterCreateSuccess`, etc.) fired from a `Save` inside a tx run **inside that tx**. Anything they do through `e.App` participates in the rollback; anything they do through a captured outer `app` does not.

Reference: [Go database](https://pocketbase.io/docs/go-database/#transaction) · [JS database](https://pocketbase.io/docs/js-database/#transaction)

