---
title: Bind User Input in Server-Side Filters with {:placeholder} Params
impact: CRITICAL
impactDescription: String-concatenating user input into filter expressions is a direct injection vulnerability
tags: extending, filter, injection, security, FindRecordsByFilter, dbx
---

## Bind User Input in Server-Side Filters with {:placeholder} Params

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
