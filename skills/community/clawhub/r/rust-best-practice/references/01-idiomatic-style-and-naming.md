# Idiomatic Style, Naming, and Control Flow

## Table of contents
1. Naming conventions
2. Formatting and `rustfmt`
3. Control flow idioms
4. Iterators over manual loops
5. `impl Trait` and return types
6. Pattern matching ergonomics
7. Common conversions (`From`/`Into`/`as`)
8. Anti-patterns checklist

---

## 1. Naming conventions

Rust's naming conventions are codified in RFC 430 and the Rust API Guidelines (`C-CASE`). They are treated as near-mandatory by the ecosystem and enforced by `clippy::style` / `non_snake_case` lints.

| Item | Convention | Example |
|---|---|---|
| Crates | `snake_case` (hyphens allowed in `Cargo.toml` name, become `_` in code) | `my_crate` |
| Modules | `snake_case` | `mod http_client;` |
| Types, traits, enums | `UpperCamelCase` | `struct HttpClient`, `trait Serialize` |
| Enum variants | `UpperCamelCase` | `enum Shape { Circle, Square }` |
| Functions, methods | `snake_case` | `fn read_to_string()` |
| Local variables | `snake_case` | `let user_id = 1;` |
| Constants, statics | `SCREAMING_SNAKE_CASE` | `const MAX_RETRIES: u32 = 3;` |
| Type parameters | short `UpperCamelCase`, usually single letter | `T`, `E`, `K`, `V`, `Idx` |
| Lifetimes | short lowercase | `'a`, `'de`, `'src` |
| Features (Cargo.toml) | `kebab-case` | `feature = "async-std"` |

Additional naming rules from the Rust API Guidelines (`C-CONV`, `C-GETTER`, `C-ITER`):
- Conversion methods: `as_` (cheap, borrowed→borrowed), `to_` (expensive, borrowed→owned), `into_` (owned→owned, consumes `self`). E.g. `str::as_bytes`, `str::to_string`, `String::into_bytes`.
- Getters do **not** prefix with `get_`: use `fn len(&self) -> usize`, not `fn get_len(&self)`. Exception: when there's genuine ambiguity or a paired setter (`fn get(&self)` alongside `fn set(&mut self, v: T)` on something like a cell type).
- Iterator-producing methods: `iter()` (borrow `&T`), `iter_mut()` (borrow `&mut T`), `into_iter()` (owned `T`, consumes collection).
- Fallible constructors: `new()` for infallible, `try_new() -> Result<Self, E>` for fallible.

## 2. Formatting and `rustfmt`

Never hand-format — always run `cargo fmt` and commit a `rustfmt.toml` if the team wants deviations from defaults (e.g. `max_width`, `imports_granularity`). CI should run `cargo fmt --check` so unformatted code fails the build. See `references/09-tooling-cargo-and-ci.md` for the full CI setup.

## 3. Control flow idioms

Prefer expression-oriented style — Rust's `if`, `match`, and blocks are expressions:

```rust
// Idiomatic: if is an expression
let msg = if user.is_admin() { "welcome, admin" } else { "welcome" };

// Idiomatic: early return with `?` instead of nested if-let pyramids
fn load_config(path: &Path) -> Result<Config, ConfigError> {
    let raw = fs::read_to_string(path)?;
    let cfg: Config = toml::from_str(&raw)?;
    cfg.validate()?;
    Ok(cfg)
}
```

Avoid the "arrow anti-pattern" (deeply nested `if let`/`match`). Flatten with early returns, `?`, or combinator chains (`.and_then`, `.map`, `.ok_or`):

```rust
// Anti-pattern
fn find_user(id: u32) -> Option<String> {
    if let Some(db) = get_db() {
        if let Some(row) = db.query(id) {
            if let Some(name) = row.get("name") {
                return Some(name);
            }
        }
    }
    None
}

// Idiomatic
fn find_user(id: u32) -> Option<String> {
    get_db()?.query(id)?.get("name")
}
```

`while let` and `if let` chains (stabilized via `let_chains` in edition 2024, RFC 2497) let you combine conditions cleanly — check the crate's edition before relying on this.

## 4. Iterators over manual loops

Rust's iterator adapters compile down to the same code as hand-written loops (true zero-cost abstraction, verified in "Iterators and Zero-Cost Abstractions" from the Rust Blog) while being harder to get wrong (off-by-one, missed bounds check elision).

```rust
// Prefer
let sum: i64 = numbers.iter().filter(|&&n| n % 2 == 0).map(|&n| n as i64).sum();

// Over manual accumulation
let mut sum: i64 = 0;
for n in &numbers {
    if n % 2 == 0 {
        sum += *n as i64;
    }
}
```

Common adapters to reach for instead of hand-rolled loops: `.filter_map`, `.fold`, `.scan`, `.windows`/`.chunks` (on slices), `.zip`, `.enumerate`, `.take_while`/`.skip_while`, `.peekable`, `.chain`, `.flat_map`, `.partition`.

Clippy actively flags manual reimplementations: `clippy::needless_range_loop`, `clippy::manual_map`, `clippy::manual_filter_map`, `clippy::while_let_on_iterator`.

## 5. `impl Trait` and return types

- Use `impl Trait` in argument position for "accepts anything implementing X" without forcing callers to know about generics: `fn process(items: impl IntoIterator<Item = u32>)`.
- Use `impl Trait` in return position to return an opaque iterator/future without naming it or boxing it: `fn evens(v: &[i32]) -> impl Iterator<Item = &i32>`.
- Only reach for `Box<dyn Trait>` when you need runtime polymorphism (heterogeneous collection, trait object stored in a struct field, recursive types) — it has real allocation + vtable-dispatch cost. See `references/04-traits-generics-and-type-design.md` §"Generics vs. trait objects".
- Return `-> Result<T, E>` rather than `-> Option<T>` when the caller needs to know *why* something failed.

## 6. Pattern matching ergonomics

Exhaustive `match` over `if`/`else if` chains when discriminating on an enum — the compiler enforces exhaustiveness, which is free protection against forgetting a new variant later:

```rust
enum State { Idle, Running { pid: u32 }, Stopped { code: i32 } }

match state {
    State::Idle => {}
    State::Running { pid } => println!("running as {pid}"),
    State::Stopped { code } if code != 0 => eprintln!("failed: {code}"),
    State::Stopped { .. } => {}
}
```

Use `@` bindings and guards for range/condition matching, `matches!()` macro for boolean membership tests instead of a full `match` returning `true`/`false`:

```rust
if matches!(status, Status::Ok | Status::Created) { /* ... */ }
```

Destructure in function signatures and `let` when it clarifies intent:
```rust
fn distance((x1, y1): (f64, f64), (x2, y2): (f64, f64)) -> f64 { /* ... */ }
```

## 7. Common conversions

- Prefer `TryFrom`/`TryInto` over `as` for numeric casts that can lose data (`as` silently truncates/wraps — `clippy::cast_possible_truncation`, `clippy::cast_sign_loss` exist specifically to flag this).
- Implement `From<T>` for your error/wrapper types rather than requiring callers to call a named constructor — this makes `?` work automatically via the blanket `impl<T, U: From<T>> From<T> for Result<..., U>` path (see `references/03-error-handling.md`).
- `Default` should be implemented (often via `#[derive(Default)]`) for structs with a sensible "empty"/zero value — enables `..Default::default()` struct update syntax and works well with builder patterns.

## 8. Anti-patterns checklist (use in code review)

- [ ] Non-idiomatic naming: `get_` prefix on plain getters, `camelCase` variables, `snake_case` types
- [ ] Deep `if let`/`match` nesting that should be flattened with `?` or combinators
- [ ] Manual loops reimplementing `.map`/`.filter`/`.fold`/`.sum` etc.
- [ ] `as` casts where truncation/sign-loss is possible and not intended — should be `TryFrom` or explicit `checked_*`
- [ ] Returning `Box<dyn Trait>` where a generic or `impl Trait` would avoid the allocation
- [ ] Boolean-returning `match` that should be `matches!()`
- [ ] Missing `#[derive(Debug)]` on public types (almost always wanted; `C-DEBUG` in API Guidelines)
- [ ] Missing `#[non_exhaustive]` on public enums/structs that may grow variants/fields in future minor versions

---

## Real references

- The Rust Programming Language (official book), ch. 3, 6, 13, 18: https://doc.rust-lang.org/book/
- RFC 430 — Naming conventions: https://rust-lang.github.io/rfcs/0430-finalizing-naming-conventions.html
- Rust API Guidelines — Naming (C-CASE, C-CONV, C-GETTER, C-ITER): https://rust-lang.github.io/api-guidelines/naming.html
- Rust API Guidelines — full checklist: https://rust-lang.github.io/api-guidelines/checklist.html
- "Iterators and Zero-Cost Abstractions" — Rust Blog: https://blog.rust-lang.org/2015/08/14/Next-year.html (background on zero-cost iterator design; see also the Nomicon's abstraction cost discussion)
- Clippy lint index (searchable): https://rust-lang.github.io/rust-clippy/master/index.html
- RFC 2497 — if-let chains: https://rust-lang.github.io/rfcs/2497-if-let-chains.html
- `rustfmt` configuration reference: https://rust-lang.github.io/rustfmt/
