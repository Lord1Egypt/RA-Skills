# Concurrency and Async

## Table of contents
1. Threads vs. async — when to use which
2. `Send` and `Sync`
3. Message passing vs. shared state
4. Tokio fundamentals
5. Common async pitfalls
6. Cancellation and structured concurrency
7. Anti-patterns checklist

---

## 1. Threads vs. async — when to use which

- **OS threads** (`std::thread`, `rayon` for data-parallelism): best for CPU-bound work. Simpler mental model, no `.await` coloring, true parallelism. `rayon` is the standard choice for parallel iterators (`par_iter()`).
- **Async** (`tokio`, `async-std`, `smol`): best for I/O-bound work with high concurrency (thousands of open connections/tasks) where OS threads would be too heavy (each thread ~MB of stack; async tasks are much cheaper). Async does **not** make CPU-bound work faster — it lets you multiplex many *waiting* operations over few threads.

Don't reach for async by default — if you're writing a CLI tool doing a handful of sequential HTTP requests, synchronous code (`reqwest::blocking`, `ureq`) is simpler and entirely appropriate. Reach for async when you need concurrency at scale (web servers, proxies, many simultaneous connections).

## 2. `Send` and `Sync`

- `T: Send` — safe to move `T` to another thread.
- `T: Sync` — safe to share `&T` across threads (equivalent to `&T: Send`).

Most types are auto-derived `Send + Sync` by the compiler based on their fields; `Rc<T>`/`RefCell<T>` are notably **not** `Send`/`Sync` (use `Arc`/`Mutex` for cross-thread equivalents — see `references/02-ownership-borrowing-lifetimes.md` §5). Raw pointers are `!Send + !Sync` by default. You should essentially never need `unsafe impl Send/Sync` by hand unless implementing a low-level concurrent data structure — if you find yourself doing this, read `references/07-unsafe-rust.md` first and be certain of the soundness argument.

## 3. Message passing vs. shared state

Prefer **message passing** (channels) over **shared mutable state** (`Arc<Mutex<T>>`) where the design allows it — "Do not communicate by sharing memory; share memory by communicating" (from the Book, echoing Go's proverb, but equally idiomatic in Rust via `std::sync::mpsc` or `tokio::sync::mpsc`).

```rust
// Message passing — no lock contention, clear ownership handoff
let (tx, mut rx) = tokio::sync::mpsc::channel::<Job>(32);
tokio::spawn(async move {
    while let Some(job) = rx.recv().await {
        process(job).await;
    }
});
tx.send(Job::new(...)).await?;
```

When shared mutable state genuinely is the right model (e.g. a cache many tasks read/write), use `Arc<Mutex<T>>` / `Arc<RwLock<T>>`, keep the critical section as small as possible, and never hold a lock across an `.await` point (see §5).

## 4. Tokio fundamentals

- `#[tokio::main]` sets up the runtime for `main`; libraries should almost never depend on a specific runtime being initialized — accept `&Handle` or be runtime-agnostic where feasible.
- `tokio::spawn(future)` requires the future to be `'static + Send` — this is why moving owned data (not borrows) into spawned tasks is required; a common compile error ("future cannot be sent between threads safely") usually traces back to a non-`Send` type (like `Rc` or a `MutexGuard` held across `.await`) captured in the task.
- Use `tokio::select!` for racing multiple futures (e.g. a timeout vs. an operation, or a shutdown signal vs. work).
- Use `JoinSet`/`JoinHandle` and always check/handle join errors (a panicked task doesn't crash the whole program, but silently ignoring `JoinError` hides bugs).
- Choose the right runtime flavor: `#[tokio::main(flavor = "current_thread")]` for tests/simple tools (lower overhead), the default multi-threaded flavor for servers that benefit from work-stealing across cores.

## 5. Common async pitfalls

- **Holding a `std::sync::MutexGuard` across an `.await`** — blocks the executor thread while waiting, can deadlock the whole runtime under load. Fix: use `tokio::sync::Mutex` if you must hold the lock across an await point, or (better) restructure to drop the guard before awaiting.
- **Blocking calls inside async functions** — synchronous file I/O, `std::thread::sleep`, CPU-heavy computation, or a blocking DB driver call inside an `async fn` starves the executor. Fix: `tokio::task::spawn_blocking` for blocking work, `tokio::time::sleep` instead of `std::thread::sleep`, and prefer async-native drivers (`sqlx`, `tokio-postgres`) over sync ones.
- **Not `.await`ing a future** — futures are lazy; a future that's constructed but never awaited or spawned simply never runs. Clippy's `clippy::unused_must_use` combined with `#[must_use]` on `Future`-returning functions helps catch this.
- **Accidentally sequential "concurrent" code** — `a().await; b().await;` runs sequentially even though both are async. Use `tokio::join!`/`futures::join!` (both must complete) or `tokio::spawn` (independent tasks) for real concurrency.

```rust
// Sequential (probably not intended if independent):
let a = fetch_a().await?;
let b = fetch_b().await?;

// Concurrent:
let (a, b) = tokio::try_join!(fetch_a(), fetch_b())?;
```

## 6. Cancellation and structured concurrency

Dropping a future cancels it at its next `.await` point (Rust async is "cancel on drop", unlike some other languages' async models) — this means `tokio::select!` branches that "lose" the race are cleanly cancelled, but it also means you must design cleanup carefully (e.g. use RAII guards / `Drop` for resources that must be released even on cancellation, rather than "cleanup code after the operation" that a cancellation would skip).

For coordinating graceful shutdown across many tasks, use a broadcast channel or `tokio_util::sync::CancellationToken` rather than ad-hoc `AtomicBool` flags polled irregularly.

## 7. Anti-patterns checklist

- [ ] `std::sync::Mutex` (not `tokio::sync::Mutex`) guard held across an `.await`
- [ ] Blocking/synchronous I/O or `std::thread::sleep` inside `async fn`
- [ ] `Arc<Mutex<T>>` used where a channel/actor-style design would eliminate the shared state entirely
- [ ] Sequential `.await` chains for logically-independent operations that should run concurrently (`join!`/`spawn`)
- [ ] Unbounded channels (`mpsc::unbounded_channel`) used by default instead of bounded ones (backpressure) without a deliberate reason
- [ ] Spawned tasks whose `JoinHandle`/`JoinError` is dropped/ignored, silently swallowing panics
- [ ] Using async for pure CPU-bound work expecting a speedup (should be threads/`rayon` instead)
- [ ] `unsafe impl Send`/`Sync` added to silence a compiler error without a documented soundness proof

---

## Real references

- The Rust Programming Language, ch. 16 (Fearless Concurrency) and ch. 17 (Async): https://doc.rust-lang.org/book/ch16-00-concurrency.html , https://doc.rust-lang.org/book/ch17-00-async-await.html
- The Async Book (official, community-maintained): https://rust-lang.github.io/async-book/
- Tokio official tutorial and docs: https://tokio.rs/tokio/tutorial
- Tokio "Shared State" tutorial page (Mutex guidance): https://tokio.rs/tokio/tutorial/shared-state
- `tokio::select!` macro docs: https://docs.rs/tokio/latest/tokio/macro.select.html
- `std::marker::Send` / `Sync` docs: https://doc.rust-lang.org/std/marker/trait.Send.html , https://doc.rust-lang.org/std/marker/trait.Sync.html
- `rayon` crate docs (data parallelism): https://docs.rs/rayon/latest/rayon/
- "Alice Ryhl — Actors with Tokio" (widely-cited pattern for message-passing task design): https://ryhl.io/blog/actors-with-tokio/
- `tokio_util::sync::CancellationToken` docs: https://docs.rs/tokio-util/latest/tokio_util/sync/struct.CancellationToken.html
