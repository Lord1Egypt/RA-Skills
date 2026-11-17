# Ownership, Borrowing, and Lifetimes

## Table of contents
1. The three rules
2. Move semantics and `Clone`/`Copy`
3. Borrowing rules and the borrow checker
4. Lifetime elision and explicit lifetimes
5. Interior mutability: `Cell`, `RefCell`, `Rc`, `Arc`
6. `Pin` and self-referential structs (brief)
7. Common borrow-checker error patterns and fixes
8. Anti-patterns checklist

---

## 1. The three rules

From *The Rust Programming Language*, ch. 4:
1. Each value has a single owner.
2. When the owner goes out of scope, the value is dropped.
3. Ownership can be moved, or the value can be borrowed (immutably, many times, or mutably, exactly once) — never both a mutable and any other borrow at once, within the same scope (subject to non-lexical lifetimes, see §3).

## 2. Move semantics and `Clone`/`Copy`

By default, assignment **moves** non-`Copy` types. Only implement `Copy` for types that are cheap to duplicate bit-for-bit (small, stack-only, no destructor) — `#[derive(Copy, Clone)]` requires all fields to be `Copy`.

```rust
#[derive(Clone, Copy, Debug, PartialEq)]
struct Point { x: f64, y: f64 } // fine: small, no heap allocation, no Drop

#[derive(Clone, Debug)]
struct Buffer { data: Vec<u8> } // NOT Copy: owns heap memory
```

Rule of thumb: reach for `.clone()` only when you've confirmed the borrow checker genuinely requires an independent owned copy (e.g. storing into a new data structure that must outlive the source), not as a reflexive fix for a compile error you haven't understood. Cloning a `Vec`/`String`/`HashMap` in a hot loop is a common accidental-quadratic-cost bug — profile before assuming it's fine (see `references/06-performance-and-memory.md`).

## 3. Borrowing rules and the borrow checker

Since Rust 2018 (NLL — Non-Lexical Lifetimes), a borrow's scope ends at its last use, not at the end of the enclosing block, which makes many common patterns compile that didn't in Rust 1.0:

```rust
let mut v = vec![1, 2, 3];
let first = &v[0];      // immutable borrow starts
println!("{first}");    // ...and ends here (last use)
v.push(4);               // OK under NLL: no active borrow at this point
```

Rules to internalize:
- Any number of `&T` (shared/immutable) borrows can coexist.
- Only one `&mut T` (exclusive/mutable) borrow may exist, and it must not coexist with any `&T`.
- A reference must never outlive the data it points to (enforced via lifetimes).

## 4. Lifetime elision and explicit lifetimes

Most function signatures don't need explicit lifetimes thanks to the three elision rules (Rust Reference, "Lifetime elision"):
1. Each elided input lifetime gets its own parameter.
2. If there's exactly one input lifetime, it's assigned to all elided output lifetimes.
3. If one of the inputs is `&self`/`&mut self`, its lifetime is assigned to all elided output lifetimes.

Write explicit lifetimes only when elision doesn't apply or when documenting intent helps readers:

```rust
// Elision handles this: output borrows from `s` by rule 2
fn first_word(s: &str) -> &str { s.split_whitespace().next().unwrap_or("") }

// Explicit lifetime needed: output could come from either input
fn longest<'a>(a: &'a str, b: &'a str) -> &'a str {
    if a.len() > b.len() { a } else { b }
}
```

`'static` means "valid for the entire program", not "always safe to use everywhere" — a very common misconception. `&'static str` literals are fine; reaching for `'static` bounds on generic type parameters (`T: 'static`) to make a compile error go away often signals a design problem (e.g. trying to store a borrowed value in a struct that should own its data, or in a spawned task — see `references/05-concurrency-and-async.md` on `tokio::spawn` requiring `'static`).

## 5. Interior mutability: `Cell`, `RefCell`, `Rc`, `Arc`

| Type | Mutability | Thread-safe? | Cost | Use when |
|---|---|---|---|---|
| `Cell<T>` | interior, `Copy` types (or via `replace`) | No | none (no runtime check) | Simple `Copy` counters/flags shared within a single-threaded structure |
| `RefCell<T>` | interior, runtime-checked borrow | No | small (borrow flag check, panics on violation) | Single-threaded graph/tree structures needing shared mutable access |
| `Rc<T>` | shared ownership, immutable by default | No | refcount increment/decrement | Single-threaded shared ownership (e.g. parent/child graph nodes) |
| `Arc<T>` | shared ownership, immutable by default | Yes | atomic refcount (more overhead than `Rc`) | Cross-thread shared ownership |
| `Mutex<T>`/`RwLock<T>` | interior, thread-safe, blocking | Yes | lock overhead | Shared *mutable* state across threads — pair with `Arc<Mutex<T>>` |

`Rc<RefCell<T>>` is a legitimate and common pattern for single-threaded shared mutable graphs (trees with parent pointers, observer patterns) — it is **not** automatically an anti-pattern, but reach for it deliberately, and prefer restructuring with indices/arenas (`slotmap`, `generational-arena` crates) or ownership redesign when the graph gets complex, since `RefCell` borrow panics move a compile-time guarantee to a runtime one.

```rust
use std::{cell::RefCell, rc::Rc};

struct Node {
    value: i32,
    children: Vec<Rc<RefCell<Node>>>,
}
```

## 6. `Pin` and self-referential structs (brief)

Self-referential structs (a struct holding a reference into its own field) are not directly expressible in safe Rust because moving the struct would invalidate the internal reference. `Pin<P>` pins a value at a memory address so it can't be moved, which is the mechanism `async fn` state machines rely on internally. Application code rarely needs to touch `Pin` directly unless implementing a custom `Future` by hand or building low-level async primitives — prefer `async fn`/`async` blocks, which handle this for you. If you do need manual `Future` implementations, read `std::pin` module docs closely and consider the `pin-project` crate to avoid unsafe boilerplate.

## 7. Common borrow-checker error patterns and fixes

**"cannot borrow as mutable because it is also borrowed as immutable"** — usually means you're calling a `&mut self` method while an existing borrow (often accidentally kept alive via a variable binding used later) is still live. Fix: shrink the borrow's lifetime, restructure to do reads first then writes, or split the struct into fields borrowed independently (the borrow checker understands **disjoint field borrows**: `&mut self.a` and `&self.b` can coexist).

**"cannot move out of borrowed content"** — trying to move a value you only have `&T` to. Fix: `.clone()` if a copy is genuinely needed, or restructure to take ownership (`self` instead of `&self`), or use `std::mem::take`/`std::mem::replace` to swap out a value while leaving something valid behind:

```rust
struct Machine { state: State }
impl Machine {
    fn advance(&mut self) {
        let old = std::mem::replace(&mut self.state, State::Transitioning);
        self.state = old.next();
    }
}
```

**"does not live long enough"** — a reference is being used after the referent is dropped. Fix: extend the referent's lifetime (bind it to an outer variable), return an owned value instead of a reference, or restructure so the borrow doesn't need to outlive its source.

## 8. Anti-patterns checklist

- [ ] `.clone()` sprinkled to silence borrow-checker errors without understanding root cause
- [ ] `Rc<RefCell<T>>` reached for reflexively in code that's actually single-owner
- [ ] `Arc<Mutex<T>>` where a channel-based / message-passing design would avoid shared mutable state entirely (see `references/05`)
- [ ] Fighting the borrow checker with raw pointers / `unsafe` instead of restructuring ownership (see `references/07` for when `unsafe` is actually warranted)
- [ ] Storing borrowed data (`&'a T`) in a long-lived struct where owning the data (or `Arc<T>`) would be simpler
- [ ] `'static` bounds added to make an error disappear without understanding why it was required

---

## Real references

- The Rust Programming Language, ch. 4 (Ownership) and ch. 10.3 (Lifetimes): https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html , https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html
- The Rust Reference — Lifetime elision: https://doc.rust-lang.org/reference/lifetime-elision.html
- The Rustonomicon — ownership-adjacent unsafe topics: https://doc.rust-lang.org/nomicon/
- `std::cell` module docs (Cell/RefCell semantics): https://doc.rust-lang.org/std/cell/index.html
- `std::rc` / `std::sync::Arc` docs: https://doc.rust-lang.org/std/rc/index.html , https://doc.rust-lang.org/std/sync/struct.Arc.html
- `std::pin` module docs: https://doc.rust-lang.org/std/pin/index.html
- `std::mem::replace` / `std::mem::take`: https://doc.rust-lang.org/std/mem/fn.replace.html
- Non-Lexical Lifetimes RFC: https://rust-lang.github.io/rfcs/2094-nll.html
