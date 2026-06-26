---
title: Version Your Schema with Go Migrations
impact: HIGH
impactDescription: Guarantees repeatable, transactional schema evolution and eliminates manual dashboard changes in production
tags: go, migrations, schema, database, migratecmd, extending
---

## Version Your Schema with Go Migrations

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
