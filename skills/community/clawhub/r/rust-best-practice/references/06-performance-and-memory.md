# Performance and Memory

## Table of contents
1. Measure before optimizing
2. Allocation awareness
3. `Cow` and avoiding unnecessary clones
4. Data layout and cache friendliness
5. Compiler-assisted optimization
6. Benchmarking methodology
7. Anti-patterns checklist

---

## 1. Measure before optimizing

Rust's ergonomics make it tempting to micro-optimize prematurely. Always profile first — `cargo flamegraph`, `perf` (Linux), `samply`, or `cargo bench` with `criterion` — and optimize the actual bottleneck, not the code that merely *looks* slow. Algorithmic complexity (`O(n^2)` accidental loops, especially from repeated `.clone()`/`.contains()` on `Vec` inside a loop) is almost always a bigger win than micro-tuning.

## 2. Allocation awareness

Every `Vec::push` beyond capacity, `String::push_str` beyond capacity, `.to_string()`, `.clone()` on heap-owning types, and `Box::new` allocates. None of these are wrong to use — but be deliberate in hot paths:

```rust
// Reallocates repeatedly as it grows (may realloc O(log n) times, still wasteful if size is known)
let mut v = Vec::new();
for i in 0..10_000 { v.push(i); }

// Pre-sized: one allocation
let mut v = Vec::with_capacity(10_000);
for i in 0..10_000 { v.push(i); }
```

Prefer `&str` over `String`, `&[T]` over `Vec<T>` in function parameters when you don't need ownership — this avoids forcing callers to allocate just to call your function (accept borrowed, return owned is the general rule, per API Guidelines flexibility guidance).

## 3. `Cow` and avoiding unnecessary clones

`std::borrow::Cow<'a, T>` ("clone on write") lets a function return borrowed data in the common case and only allocate when it actually needs to modify/own the data:

```rust
fn normalize(input: &str) -> Cow<str> {
    if input.chars().all(|c| !c.is_uppercase()) {
        Cow::Borrowed(input) // no allocation — nothing needed to change
    } else {
        Cow::Owned(input.to_lowercase()) // only allocate when actually transforming
    }
}
```

Useful in parsers, string-processing pipelines, and APIs where the "no-op" path is common.

## 4. Data layout and cache friendliness

- Prefer `Vec<T>` (contiguous, cache-friendly) over `LinkedList<T>` for almost all use cases — `LinkedList` is rarely the right choice in Rust; even its own docs note `Vec`/`VecDeque` usually outperform it.
- Struct-of-arrays (SoA) layout can beat array-of-structs (AoS) for hot loops that only touch a subset of fields across many elements (common in game/simulation code) — but only refactor toward this after profiling shows it matters.
- Be aware of struct padding/alignment; `#[repr(C)]` and field reordering can reduce a struct's size when memory footprint matters (check with `std::mem::size_of::<T>()`), but don't hand-optimize layout without a measured reason — the default `repr(Rust)` compiler-chosen layout is usually fine.
- `Box<[T]>` (or `Arc<[T]>`) is a leaner alternative to `Vec<T>` when a collection's size is fixed after construction (drops the separate `capacity` field).

## 5. Compiler-assisted optimization

- Release builds (`cargo build --release`) enable optimizations (`opt-level = 3` by default) — never benchmark or ship debug builds.
- Tune `Cargo.toml` `[profile.release]` for further wins where it matters: `lto = "fat"` (link-time optimization, slower compile / faster runtime, good for final release binaries), `codegen-units = 1` (more optimization opportunity, slower compile), `panic = "abort"` (smaller binary, no unwind tables, but loses `catch_unwind`).
- `#[inline]`/`#[inline(always)]` are hints, not guarantees — the compiler already inlines aggressively within a crate; these mostly matter for small, hot functions exposed across a crate boundary. Don't sprinkle them speculatively; use profiling data (or the fact that a generic function in a library crate won't get monomorphized+inlined at the call site without visibility into its body) to decide.
- Iterator chains generally compile to loops as tight as hand-written ones (verified historically via the Rust Blog and community benchmarks) — don't "de-sugar" idiomatic iterator code into manual loops in the name of performance without measuring first.

## 6. Benchmarking methodology

Use `criterion` (statistically rigorous, handles warm-up/variance/outliers) rather than naively timing with `std::time::Instant` around a single run:

```rust
use criterion::{criterion_group, criterion_main, Criterion, black_box};

fn bench_parse(c: &mut Criterion) {
    c.bench_function("parse_config", |b| {
        b.iter(|| parse_config(black_box(SAMPLE_INPUT)))
    });
}
criterion_group!(benches, bench_parse);
criterion_main!(benches);
```

`black_box` prevents the optimizer from constant-folding away the benchmarked computation because its input/output looks "used" to the compiler. For allocation-focused profiling, `dhat`/`heaptrack`/`valgrind --tool=massif` show allocation counts and peak memory, which `criterion` alone won't reveal.

## 7. Anti-patterns checklist

- [ ] Optimizing (or asking Claude to optimize) without a profile pointing at the actual bottleneck
- [ ] `Vec::new()` + repeated `.push()` in a loop with a known/computable final size, instead of `Vec::with_capacity`
- [ ] `.clone()` on large owned data inside a loop where a borrow would do
- [ ] `LinkedList<T>` used by default instead of `Vec`/`VecDeque`
- [ ] Benchmarking/timing debug builds, or naive `Instant::now()` deltas for micro-benchmarks instead of `criterion`
- [ ] Hand-unrolling/de-sugaring idiomatic iterator chains into manual loops "for speed" without a benchmark showing a difference
- [ ] `#[inline(always)]` scattered speculatively across many functions

---

## Real references

- The Rust Performance Book (community-maintained, endorsed reference for Rust perf work): https://nnethercote.github.io/perf-book/
- `std::borrow::Cow` docs: https://doc.rust-lang.org/std/borrow/enum.Cow.html
- `criterion.rs` docs: https://bheisler.github.io/criterion.rs/book/
- `cargo-flamegraph` project: https://github.com/flamegraph-rs/flamegraph
- Cargo Book — Profiles (`opt-level`, `lto`, `codegen-units`): https://doc.rust-lang.org/cargo/reference/profiles.html
- `std::collections::LinkedList` docs (see "NOTE" recommending Vec/VecDeque in most cases): https://doc.rust-lang.org/std/collections/struct.LinkedList.html
- `std::vec::Vec::with_capacity` docs: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.with_capacity
