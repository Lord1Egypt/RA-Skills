---
title: Use DBConnect Only When You Need a Custom SQLite Driver
impact: MEDIUM
impactDescription: Incorrect driver setup breaks both data.db and auxiliary.db, or introduces unnecessary CGO
tags: go, extending, sqlite, custom-driver, cgo, fts5, dbconnect
---

## Use DBConnect Only When You Need a Custom SQLite Driver

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
