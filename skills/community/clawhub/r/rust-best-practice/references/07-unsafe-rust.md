# Unsafe Rust

## Table of contents
1. What `unsafe` actually enables
2. The `unsafe` contract and `// SAFETY:` comments
3. Common `unsafe` use cases
4. FFI basics
5. Undefined behavior to never risk
6. Verification tools
7. Anti-patterns checklist

---

## 1. What `unsafe` actually enables

`unsafe` does **not** turn off the borrow checker or type checking — it unlocks exactly five additional capabilities (per the Nomicon and the Rust Reference):
1. Dereferencing a raw pointer (`*const T`/`*mut T`).
2. Calling an `unsafe fn` (including FFI functions).
3. Implementing an `unsafe trait` (e.g. `unsafe impl Send for MyType`).
4. Accessing/modifying a mutable `static`.
5. Accessing fields of a `union`.

Everything else about the language (ownership, type checking, most borrow rules on non-raw references) still applies inside `unsafe` blocks.

## 2. The `unsafe` contract and `// SAFETY:` comments

Every `unsafe` block or function should be paired with a `// SAFETY:` comment explaining **why** the invariants required for soundness are actually upheld at this call site — this is standard practice across the ecosystem (enforced by `clippy::undocumented_unsafe_blocks` and used pervasively in `std` itself):

```rust
/// # Safety
/// `ptr` must be non-null, properly aligned for `T`, and point to a valid, initialized `T`
/// that is not concurrently mutated for the duration of the borrow.
unsafe fn read_raw<T>(ptr: *const T) -> T {
    // SAFETY: caller guarantees ptr is valid, aligned, and initialized (see fn doc above).
    unsafe { std::ptr::read(ptr) }
}
```

An `unsafe fn`'s doc comment should have a `# Safety` section listing the preconditions the caller must uphold — this is the *contract*; the implementation's `// SAFETY:` comment explains why a specific `unsafe` operation inside is sound *given* that contract.

## 3. Common use cases

- **FFI** — calling into C libraries (`extern "C"` blocks), see §4.
- **Implementing low-level data structures** — custom collections, intrusive linked lists, lock-free structures — where the standard safe abstractions can't express the needed sharing pattern.
- **Performance-critical slicing** — `slice::get_unchecked` to skip bounds checks after you've already proven the index is valid (only after profiling shows the bounds check matters — see `references/06-performance-and-memory.md`).
- **Implementing `Send`/`Sync` by hand** for a type whose fields would normally prevent auto-derivation but which you've proven is actually safe to share (e.g. a type wrapping a raw pointer that's only ever accessed through a proper synchronization mechanism).

## 4. FFI basics

```rust
#[link(name = "m")]
extern "C" {
    fn sqrt(x: f64) -> f64;
}

fn safe_sqrt(x: f64) -> f64 {
    // SAFETY: sqrt from libm is a pure function with no preconditions on x's value
    // (NaN in, NaN out; no memory safety concerns for f64 by-value FFI).
    unsafe { sqrt(x) }
}
```

Wrap every `unsafe extern "C"` call in a safe function at the boundary rather than leaking raw FFI calls throughout the codebase — callers of your crate should not need to write `unsafe` themselves for well-behaved wrapped functionality. For nontrivial FFI surfaces, prefer `bindgen` (generate Rust bindings from C headers) and `cbindgen` (generate C headers from Rust) over hand-written signatures, since hand transcription of ABI details is a common source of UB.

## 5. Undefined behavior to never risk

These cause UB even inside `unsafe` and are not "sometimes okay" — they are always bugs:
- Dereferencing a null, dangling, or misaligned pointer.
- Creating two `&mut T` (or a `&mut T` and a `&T`) aliasing the same memory at the same time (aliasing rules — this includes through raw pointers derived from references, governed by Stacked Borrows / Tree Borrows).
- Reading uninitialized memory as if it were initialized (use `MaybeUninit<T>` explicitly for genuinely uninitialized buffers).
- Producing an invalid value for a type (e.g. a `bool` that isn't 0 or 1, a `char` outside valid Unicode scalar values, a `&T` that's null or unaligned).
- Data races (concurrent unsynchronized access where at least one access is a write).
- Unwinding across an `extern "C"` boundary (use `catch_unwind` or `panic = "abort"` for that boundary).

## 6. Verification tools

- **Miri** (`cargo +nightly miri test`) — an interpreter that detects many classes of UB (invalid memory access, some aliasing violations, uninitialized reads) that compile and "work" but are unsound. Run it on any crate with non-trivial `unsafe` as part of CI.
- **`cargo careful`** — runs with extra runtime checks in a normal (non-Miri) build.
- **AddressSanitizer / ThreadSanitizer** (`-Z sanitizer=address`, nightly) — catches memory errors and data races at a lower level than Miri, useful for FFI-heavy code Miri can't fully model.
- **`clippy::undocumented_unsafe_blocks`**, **`unsafe_op_in_unsafe_fn`** (deny this — since Rust 2021 unsafe operations inside an `unsafe fn` body still require an explicit inner `unsafe {}` block, which is the correct, more precise style).

## 7. Anti-patterns checklist

- [ ] `unsafe` block with no `// SAFETY:` comment
- [ ] `unsafe fn` with no `# Safety` doc section describing caller obligations
- [ ] Reaching for `unsafe`/raw pointers to "fight" a borrow-checker error instead of restructuring ownership (see `references/02`) — this is almost always the wrong fix and frequently introduces real UB
- [ ] `unsafe impl Send`/`Sync` without a written soundness argument
- [ ] Large `unsafe` blocks doing many things at once instead of the smallest possible `unsafe` scope with safe code around it
- [ ] No Miri/sanitizer runs in CI for a crate with meaningful `unsafe` usage
- [ ] Unwinding permitted to cross an `extern "C"` boundary

---

## Real references

- The Rustonomicon (official unsafe Rust guide): https://doc.rust-lang.org/nomicon/
- The Rust Reference — Unsafety: https://doc.rust-lang.org/reference/unsafety.html
- `std::ptr` module docs (safety preconditions for raw pointer ops): https://doc.rust-lang.org/std/ptr/index.html
- `std::mem::MaybeUninit` docs: https://doc.rust-lang.org/std/mem/union.MaybeUninit.html
- Miri project (Undefined Behavior detector): https://github.com/rust-lang/miri
- Rust Unsafe Code Guidelines working group reference: https://rust-lang.github.io/unsafe-code-guidelines/
- `rustonomicon` chapter on Send/Sync: https://doc.rust-lang.org/nomicon/send-and-sync.html
- Clippy lint: `undocumented_unsafe_blocks`: https://rust-lang.github.io/rust-clippy/master/index.html#undocumented_unsafe_blocks
- `bindgen` / `cbindgen` project docs: https://rust-lang.github.io/rust-bindgen/ , https://github.com/mozilla/cbindgen
