# Testing and Quality Assurance

## Table of contents
1. Unit test organization
2. Integration tests
3. Doctests
4. Property-based testing
5. Mocking and test doubles
6. Fuzzing
7. Coverage
8. Anti-patterns checklist

---

## 1. Unit test organization

Idiomatic Rust puts unit tests in the same file as the code they test, inside a `#[cfg(test)] mod tests` submodule — this gives tests access to private items (unlike integration tests, see §2):

```rust
pub fn add(a: i32, b: i32) -> i32 { a + b }

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn adds_two_positive_numbers() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    #[should_panic(expected = "divide by zero")]
    fn panics_on_invalid_input() {
        divide(1, 0);
    }
}
```

Name tests descriptively (`adds_two_positive_numbers`, not `test1`) — the name is the first thing a developer sees in a failure report. Prefer `assert_eq!`/`assert_ne!` over bare `assert!(a == b)` since they print both values on failure. For fallible tests, return `Result<(), E>` from the test function and use `?` instead of `.unwrap()` chains, which gives cleaner failure output via `Termination`.

## 2. Integration tests

Live in a top-level `tests/` directory (each file compiles as a separate crate, only sees the crate's public API — exactly what an external consumer would see):

```
my_crate/
├── src/
│   └── lib.rs
└── tests/
    └── api_smoke_test.rs   // uses `my_crate::PublicApi` only
```

Use integration tests to verify the crate's public contract end-to-end; use unit tests for internal logic and edge cases that need access to private functions. A `tests/common/mod.rs` (not `tests/common.rs`, to avoid it being treated as its own test binary) is the idiomatic place for shared test setup/helpers across integration test files.

## 3. Doctests

Code examples in `///` doc comments are compiled and run as tests by `cargo test`, guaranteeing documentation never goes stale:

```rust
/// Adds two numbers.
///
/// # Examples
/// ```
/// assert_eq!(my_crate::add(2, 3), 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 { a + b }
```

Use `# ` prefixed lines to hide setup boilerplate from rendered docs while keeping it part of the compiled example; use ` ```rust,ignore` sparingly (only for genuinely non-runnable illustrative snippets) and ` ```rust,no_run` when the example compiles but shouldn't execute (e.g. it starts a server or needs network access).

## 4. Property-based testing

Instead of hand-picking example inputs, property-based tests assert an invariant holds for a large, randomly-generated, shrinking set of inputs — excellent for parsers, serialization round-trips, and algorithms with mathematical invariants:

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn roundtrip_serialize_deserialize(v: Vec<i32>) {
        let bytes = serialize(&v);
        let decoded = deserialize(&bytes).unwrap();
        prop_assert_eq!(v, decoded);
    }
}
```

When a failing case is found, `proptest` automatically **shrinks** it to the smallest reproducing input, making the failure much easier to debug than a random 500-element vector. `quickcheck` is the older, simpler alternative with similar goals.

## 5. Mocking and test doubles

Prefer designing for **testability via traits** over heavy mocking frameworks — define a trait for the external dependency (database, HTTP client, clock) and inject a test implementation:

```rust
trait Clock { fn now(&self) -> SystemTime; }
struct RealClock;
impl Clock for RealClock { fn now(&self) -> SystemTime { SystemTime::now() } }

struct FixedClock(SystemTime);
impl Clock for FixedClock { fn now(&self) -> SystemTime { self.0 } }
```

For more complex mock generation, `mockall` derives mock implementations from a trait definition, reducing hand-written boilerplate. Avoid mocking concrete structs/global state where a trait seam would be cleaner and more idiomatic.

## 6. Fuzzing

For code that parses untrusted input (file formats, network protocols, deserializers), fuzz testing (`cargo-fuzz`, built on libFuzzer) explores the input space far beyond what property tests typically cover and is the standard tool for finding panics/crashes/UB in parsing code:

```bash
cargo install cargo-fuzz
cargo fuzz init
cargo fuzz run fuzz_target_1
```

Any crate parsing untrusted bytes (image decoders, config parsers accepting arbitrary files, protocol implementations) should have at least one fuzz target in CI or run periodically (e.g. via OSS-Fuzz for open-source projects).

## 7. Coverage

`cargo llvm-cov` (built on LLVM source-based coverage, the current recommended tool, superseding the older `cargo-tarpaulin` for most use cases) reports line/branch coverage:

```bash
cargo install cargo-llvm-cov
cargo llvm-cov --html
```

Treat coverage as a signal for **untested code paths to investigate**, not a target to game — 100% coverage doesn't mean bug-free, and forcing coverage of genuinely untestable code (e.g. `unreachable!()` arms) adds noise without value.

## 8. Anti-patterns checklist

- [ ] Tests named `test1`/`test_thing`/`it_works` with no indication of what's being verified
- [ ] `assert!(a == b)` instead of `assert_eq!(a, b)` (loses the printed diff on failure)
- [ ] No integration tests at all for a crate with a meaningful public API
- [ ] Doc examples marked `ignore` to avoid fixing a genuinely broken/stale example
- [ ] Mocking concrete types via unsafe tricks/global mutable state instead of a trait seam
- [ ] Parsers/deserializers for untrusted input with zero fuzz coverage
- [ ] Flaky tests tolerated/re-run instead of fixed (often hides real concurrency bugs — see `references/05`)

---

## Real references

- The Rust Programming Language, ch. 11 (Writing Automated Tests): https://doc.rust-lang.org/book/ch11-00-testing.html
- The Rustdoc Book — Documentation tests: https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html
- `proptest` crate docs and book: https://proptest-rs.github.io/proptest/
- `quickcheck` crate docs: https://docs.rs/quickcheck/latest/quickcheck/
- `mockall` crate docs: https://docs.rs/mockall/latest/mockall/
- `cargo-fuzz` (Rust Fuzz Book): https://rust-fuzz.github.io/book/cargo-fuzz.html
- `cargo-llvm-cov` project: https://github.com/taiki-e/cargo-llvm-cov
- Rust API Guidelines — Documentation (C-EXAMPLE): https://rust-lang.github.io/api-guidelines/documentation.html
