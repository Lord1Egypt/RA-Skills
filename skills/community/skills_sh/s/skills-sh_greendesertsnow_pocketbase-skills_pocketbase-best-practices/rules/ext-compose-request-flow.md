---
title: Compose Hooks, Transactions, Routing, and Enrich in One Request Flow
impact: HIGH
impactDescription: Individual rules are atomic; this composite example shows which app instance applies at each layer and how errors propagate
tags: extending, composition, transactions, hooks, enrich, routing, mental-model
---

## Compose Hooks, Transactions, Routing, and Enrich in One Request Flow

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
