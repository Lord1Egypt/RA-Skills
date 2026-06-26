---
title: Pick the Right Record Hook - Model vs Request vs Enrich
impact: HIGH
impactDescription: Wrong hook = missing request context, double-fired logic, or leaked fields in realtime events
tags: hooks, onRecordEnrich, onRecordRequest, model-hooks, extending
---

## Pick the Right Record Hook - Model vs Request vs Enrich

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
