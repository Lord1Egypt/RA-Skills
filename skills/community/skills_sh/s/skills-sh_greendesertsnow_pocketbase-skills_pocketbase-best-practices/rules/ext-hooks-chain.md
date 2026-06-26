---
title: Always Call e.Next() and Use e.App Inside Hook Handlers
impact: CRITICAL
impactDescription: Forgetting e.Next() silently breaks the execution chain; reusing parent-scope app causes deadlocks
tags: hooks, events, extending, transactions, deadlock
---

## Always Call e.Next() and Use e.App Inside Hook Handlers

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
