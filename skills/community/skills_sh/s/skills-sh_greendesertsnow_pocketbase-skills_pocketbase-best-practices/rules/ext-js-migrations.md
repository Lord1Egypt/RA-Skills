---
title: Write JSVM Migrations as pb_migrations/*.js Files
impact: HIGH
impactDescription: JSVM migrations look different from Go ones; missing the timestamp prefix or the down-callback silently breaks replay
tags: jsvm, migrations, pb_migrations, schema, extending
---

## Write JSVM Migrations as pb_migrations/*.js Files

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
