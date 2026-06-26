---
name: thread
description: Helper for multi-threading and concurrency: when to use threads vs processes vs async, synchronization (locks, queues), thread pools, and language-specific APIs. Use when the user asks about threads, threading, concurrency, race conditions, locks, mutex, thread pool, or parallel execution.
---

# Thread Skill — How to Work

Use this skill when the user asks about **threads or concurrency**: starting threads, thread pools, locks/mutex, race conditions, thread-safe code, or choosing between threads / processes / async.

## Your Workflow

1. **Clarify context**: Identify language/runtime (Python, Java, C#, Node.js, Go, etc.) and what they want (I/O-bound vs CPU-bound, parallelism vs concurrency).
2. **Choose the right tool**: Prefer the language’s recommended approach (e.g. async in Node/Python for I/O; threads or processes for CPU; see [reference/concepts.md](reference/concepts.md)).
3. **Give the right level of detail**:
   - **Quick answer**: Use the Quick Reference below and reply with a minimal example in their language.
   - **Patterns and pitfalls**: Point to or quote [reference/patterns.md](reference/patterns.md) (locks, queues, thread pool, shared state).
   - **Language API**: Point to [reference/languages.md](reference/languages.md) or write a short snippet following that reference.
   - **Templates**: Use or adapt code in [assets/](assets/) when the user wants a starter or copy-paste pattern.

## Quick Reference

| Goal | Prefer | Avoid |
|------|--------|--------|
| I/O-bound (network, disk) | Async (async/await, asyncio, Promise) or thread pool | Many blocking threads |
| CPU-bound (compute) | Processes / process pool, or native threads (Java, Go, C#) | Many threads in Python (GIL) |
| Shared mutable state | Locks (mutex), thread-safe collections, or avoid sharing | Naked shared variables |
| Producer–consumer | Queue (thread-safe) | Busy-wait / ad-hoc signaling |
| Run N tasks in parallel | Thread pool or process pool | Manually creating N threads |

| Concept | One-liner |
|---------|-----------|
| Race condition | Two threads read/write same data without synchronization; fix with lock or immutable design. |
| Deadlock | Two (or more) threads wait for each other’s lock; fix by consistent lock order or timeouts. |
| GIL (Python) | Only one thread runs Python bytecode at a time; use processes or C extensions for CPU-bound. |

## Where to Look

| Need | Location |
|------|----------|
| When to use threads vs processes vs async | [reference/concepts.md](reference/concepts.md) |
| Locks, queues, thread pool, shared state patterns | [reference/patterns.md](reference/patterns.md) |
| Python / Java / C# / Node / Go API quick ref | [reference/languages.md](reference/languages.md) |
| Starter code / templates | [assets/](assets/) |

## Safety and Best Practices

- **Do not** suggest shared mutable state without synchronization (lock, queue, or thread-safe structure).
- Prefer **higher-level** constructs: thread pool, queue, async, instead of raw threads where they fit.
- For Python CPU-bound work, suggest **multiprocessing** or clarify GIL limits; for I/O-bound, suggest **threading** or **asyncio** as appropriate.
- When the user reports deadlock or race, point to [reference/patterns.md](reference/patterns.md) and suggest minimal repro + lock discipline or queue-based design.

## Assets

- **assets/python-thread-starter.py** — Minimal Python threading + lock example.
- **assets/python-thread-pool.py** — Thread pool (e.g. `concurrent.futures`) example.

Add or reference other language templates in assets/ when the user asks for a specific runtime.
