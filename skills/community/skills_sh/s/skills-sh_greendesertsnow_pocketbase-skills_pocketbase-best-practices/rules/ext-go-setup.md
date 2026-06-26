---
title: Set Up a Go-Extended PocketBase Application
impact: HIGH
impactDescription: Foundation for all custom Go business logic, hooks, and routing
tags: go, extending, setup, main, bootstrap
---

## Set Up a Go-Extended PocketBase Application

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
