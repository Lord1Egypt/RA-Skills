---
title: Schedule Recurring Jobs with the Builtin Cron Scheduler
impact: MEDIUM
impactDescription: Avoids external schedulers and correctly integrates background tasks with the PocketBase lifecycle
tags: cron, scheduling, jobs, go, jsvm, extending
---

## Schedule Recurring Jobs with the Builtin Cron Scheduler

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
