---
name: rust-best-practice
description: Comprehensive, exhaustive reference for idiomatic and production-grade Rust engineering — covers ownership/borrowing/lifetimes, error handling, trait & generic API design, concurrency and async (Tokio), performance and memory layout, unsafe Rust and soundness, testing and property-based testing, Cargo/CI tooling and Clippy lints, web/backend frameworks (Axum/Actix), CLI and systems tools, workspace/project structure, and dependency/supply-chain security. ALWAYS load and consult this skill whenever the word "rust" (or "Rust", "cargo", "crate", ".rs file", "tokio", "actix", "axum", "clippy", "rustc") appears in the conversation, whether the user is writing new Rust code, reviewing/refactoring existing Rust code, debugging a Rust compiler error, designing a Rust API/library/crate, setting up a Rust project or CI pipeline, or asking any question about Rust idioms, ownership, lifetimes, traits, async, unsafe code, performance, or testing. Trigger proactively even for small Rust snippets or one-off questions — do not wait for the user to explicitly ask for "best practices".
---

# Rust Best Practice — Master Reference

This skill is an exhaustive, book-grade reference for writing, reviewing, and reasoning about production-quality Rust. It exists to make every piece of Rust code Claude touches — no matter how small — idiomatic, sound, performant, and maintainable by default.

## How to use this skill

1. **Always consult this file first** whenever Rust is involved, even for a two-line snippet. Do not skip straight to writing code.
2. **Identify the task type** using the table below, then **read the matching reference file(s)** in `references/` before writing or reviewing code. Reference files are self-contained "book chapters" — each has its own table of contents, code examples, rationale, anti-patterns, and a Real References section with authoritative URLs (The Rust Book, Rust Reference, Rust API Guidelines, RFCs, Clippy lint docs, official crate docs).
3. **For code review**: read the relevant reference(s), then check the user's code against the checklists at the end of each file. Report violations grouped by severity (soundness/correctness > API design > style/idiom > performance/micro-optimization), citing the specific guideline (e.g. "C-GETTER" from the Rust API Guidelines, or a specific Clippy lint name).
4. **For writing new code**: read the relevant reference(s) first, then write code that satisfies every applicable checklist item. Prefer standard library and well-established crates (see `references/13-security-and-supply-chain.md` for vetting criteria) over reinventing functionality.
5. **Cite sources**: when explaining *why* a practice matters, point to the specific guideline/RFC/lint referenced in the file, and give the user the real URL — don't invent or paraphrase from memory alone.
6. Multiple reference files often apply to one task (e.g. writing an async web handler touches error handling, async, and API design) — read all that are relevant, not just one.

## Task → Reference file map

| If the task involves... | Read this file |
|---|---|
| Naming, formatting, idiomatic control flow, `impl Trait`, iterators, `match` ergonomics, general "does this look like idiomatic Rust" review | `references/01-idiomatic-style-and-naming.md` |
| Borrow checker errors, lifetimes, `'static`, `Rc`/`Arc`/`RefCell`/`Cell`, move semantics, `Clone`/`Copy`, self-referential structs, `Pin` | `references/02-ownership-borrowing-lifetimes.md` |
| `Result`/`Option`, `?` operator, custom error types, `thiserror`/`anyhow`, panics vs. errors, fallibility in library vs. application code | `references/03-error-handling.md` |
| Designing traits, generics, trait objects vs. generics, `From`/`Into`, operator overloading, builder pattern, sealed traits, orphan rule | `references/04-traits-generics-and-type-design.md` |
| `async`/`.await`, Tokio runtime, `Send`/`Sync`, threads, channels, `Mutex` vs. message passing, cancellation, structured concurrency | `references/05-concurrency-and-async.md` |
| Performance tuning, allocation, `Vec`/`String` capacity, `Cow`, zero-copy, SIMD, profiling, `#[inline]`, benchmark methodology | `references/06-performance-and-memory.md` |
| `unsafe` blocks, raw pointers, FFI, soundness invariants, `unsafe impl Send/Sync`, Miri, undefined behavior | `references/07-unsafe-rust.md` |
| Unit/integration tests, `#[test]` organization, mocking, property-based testing (`proptest`/`quickcheck`), fuzzing, doctest, coverage | `references/08-testing-and-quality.md` |
| `Cargo.toml` setup, feature flags, lint configuration, Clippy, rustfmt, CI pipelines, MSRV, release profiles | `references/09-tooling-cargo-and-ci.md` |
| HTTP servers/clients, Axum/Actix-web, `serde`, middleware, extractors, database access (`sqlx`/`diesel`), REST/gRPC API design | `references/10-web-backend-and-networking.md` |
| CLI tools (`clap`), argument parsing, terminal I/O, systems programming, file I/O, process management, cross-platform concerns | `references/11-cli-and-systems-tools.md` |
| Workspace layout, module organization, crate splitting, public API surface, `pub(crate)`/visibility, versioning/SemVer | `references/12-project-structure-workspaces-and-dependencies.md` |
| Dependency vetting, `cargo audit`/`cargo deny`, supply-chain risk, unsafe-in-dependencies, license compliance, secrets handling | `references/13-security-and-supply-chain.md` |

## Core philosophy (applies everywhere)

- **Make invalid states unrepresentable.** Prefer encoding invariants in the type system over runtime checks (newtypes, enums, the typestate pattern) — see `01` and `04`.
- **Parse, don't validate.** Convert unstructured input into structured types at the boundary; the rest of the program works with types that are already known-valid.
- **Explicit over implicit.** No silent truncation, no hidden panics, no surprising allocations. Prefer `TryFrom` over lossy `as` casts, `checked_*`/`saturating_*` arithmetic over raw operators where overflow matters.
- **Errors are values, panics are bugs.** Reserve `panic!`/`unwrap()`/`expect()` for genuine programmer errors or truly unrecoverable states; propagate everything else as `Result`.
- **Zero-cost abstraction is a goal, not an excuse.** Write clear code first; reach for `unsafe` or manual optimization only with a measured bottleneck and a documented safety argument.
- **Lint at maximum strictness.** Every new project should enable `clippy::all`, `clippy::pedantic` (selectively), and `#![deny(unsafe_op_in_unsafe_fn)]` in `unsafe`-heavy crates — see `09`.

## Quick anti-pattern smell test (use during any review)

Flag these immediately regardless of which reference file is primary:
- `.unwrap()`/`.expect()` on `Result`/`Option` in library or production code paths (not tests/prototypes)
- `unsafe` blocks without a `// SAFETY:` comment explaining the invariant upheld
- `.clone()` used to silence a borrow-checker error without understanding why it was needed
- Stringly-typed errors (`Result<T, String>`) instead of a proper error enum
- `#[allow(warnings)]` or blanket `#[allow(clippy::all)]`
- Public structs with all-`pub` fields where invariants should be enforced by constructors
- Blocking calls (`std::thread::sleep`, sync file I/O, `std::sync::Mutex` held across `.await`) inside async functions
- Manual `impl Drop` fighting the borrow checker instead of RAII guard types
- `Box<dyn Error>` in library public APIs (fine in application `main.rs`, not in reusable crates)

Always ground recommendations in the cited real-world sources inside each reference file rather than general impressions — link the user to the primary source when explaining a rule.
