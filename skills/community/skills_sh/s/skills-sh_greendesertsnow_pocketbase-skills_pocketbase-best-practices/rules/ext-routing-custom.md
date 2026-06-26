---
title: Register Custom Routes Safely with Built-in Middlewares
impact: HIGH
impactDescription: Protects custom endpoints with auth, avoids /api path collisions, inherits rate limiting
tags: routing, middleware, extending, requireAuth, apis
---

## Register Custom Routes Safely with Built-in Middlewares

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
