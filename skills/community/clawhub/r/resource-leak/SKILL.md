---
name: resource-leak
description: Files, sockets, subscriptions, or other finite resources are acquired without a guaranteed release path.
emoji: 💧
metadata:
  clawdis:
    os: [macos, linux, windows]
---

# resource-leak

A resource is opened but not closed. Under low load the process recycles or the OS cleans up on exit, so the bug stays hidden. Under real load, file-descriptor exhaustion, memory bloat, or orphaned connections appear and cascade.

## Symptoms

- `open(...)` without a matching `close()` or `with` block.
- Database connections or HTTP clients instantiated per-request without pooling or teardown.
- Event listeners / observers / subscriptions registered but never removed.
- Background tasks or timers spawned without cancellation paths.
- Gradual memory growth that correlates with request count.

## What to do

- Pair every acquire with a release. Use language constructs that guarantee teardown: `with` (Python), `using` / `try-with-resources` (C#/Java), `defer` (Go), `try/finally` (JS/TS).
- For resources that outlive a single function, document ownership: who closes it, when, on which code path — including error paths.
- Prefer pooled clients (HTTP, database) over creating a new one per call.
- When registering event listeners, return the unregister function in the same scope so the caller can clean up.
- Test the teardown path. Kill a process or trigger an error mid-operation and confirm resources are released.
