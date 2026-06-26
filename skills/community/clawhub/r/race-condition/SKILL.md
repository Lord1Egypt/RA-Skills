---
name: race-condition
description: Shared mutable state is accessed from concurrent contexts without synchronization, producing nondeterministic behavior.
emoji: 🏁
metadata:
  clawdis:
    os: [macos, linux, windows]
---

# race-condition

Two or more concurrent contexts — threads, async tasks, processes, requests — read and write the same state without coordination. Tests pass on a lightly-loaded machine; production corruption appears under real traffic.

## Symptoms

- Counters that "mostly" work but occasionally lose increments.
- Check-then-act sequences (e.g., "if not exists, create") where two contexts both pass the check and both create.
- Shared caches or singletons mutated from request handlers without a lock.
- Data-corruption bugs that only reproduce under load or with specific timing.

## What to do

- Identify every piece of shared mutable state. Draw the boundary: who reads it, who writes it, from which contexts.
- Replace check-then-act with atomic operations: compare-and-swap, `INSERT ... ON CONFLICT`, unique indexes, `setnx`.
- Prefer immutable data or message-passing over shared mutation. Actor-style patterns remove most races by construction.
- When a lock is unavoidable, hold it for the shortest possible span and document what state it protects.
- Test concurrency explicitly. A single-threaded test proves nothing about a multi-threaded code path. Use stress tests or `pytest-asyncio` / concurrent harnesses.
