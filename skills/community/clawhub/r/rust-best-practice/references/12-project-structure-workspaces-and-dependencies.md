# Project Structure, Workspaces, and Dependencies

## Table of contents
1. Module organization
2. Workspaces and crate splitting
3. Public API surface and visibility
4. SemVer discipline
5. Dependency selection criteria
6. Anti-patterns checklist

---

## 1. Module organization

Since Rust 2018, `mod.rs` files are no longer required — `src/foo.rs` alongside a `src/foo/` directory is the preferred modern layout over `src/foo/mod.rs`:

```
src/
├── lib.rs
├── config.rs          // mod config; declared in lib.rs
├── http/
│   ├── mod.rs          // or: http.rs at the same level as the http/ dir (2018+ style)
│   ├── client.rs
│   └── server.rs
└── error.rs
```

Keep `lib.rs`/`main.rs` thin — mostly `mod` declarations, `pub use` re-exports for a curated public API, and top-level wiring. Business logic belongs in submodules, not the crate root.

Use `pub use` in `lib.rs` to present a clean, flat public API regardless of internal module depth:

```rust
// lib.rs
mod http { pub mod client; pub mod server; }
pub use http::client::HttpClient; // users write `my_crate::HttpClient`, not `my_crate::http::client::HttpClient`
```

## 2. Workspaces and crate splitting

A Cargo workspace groups multiple related crates sharing one `Cargo.lock` and `target/` directory:

```toml
# top-level Cargo.toml
[workspace]
members = ["core", "cli", "server"]
resolver = "2"

[workspace.dependencies]
serde = { version = "1", features = ["derive"] }
```

Member crates inherit shared dependency versions via `serde = { workspace = true }`, avoiding version drift across a multi-crate project. Split into separate crates when:
- A component (e.g. core domain logic) needs to be reused by multiple binaries (CLI + server + WASM frontend) without pulling in unrelated dependencies.
- Compile times matter and a stable, rarely-changing component would benefit from being cached separately from actively-developed code.
- You want to enforce an architectural boundary at the compiler level (a crate can't accidentally reach into another crate's private internals).

Don't over-split prematurely — a single well-organized crate with clean modules is simpler to maintain than a workspace of 15 tiny crates for a small project; introduce the split when a concrete reuse or compile-time need appears.

## 3. Public API surface and visibility

- Default to the narrowest visibility that works: private by default, `pub(crate)` for "internal to this crate but used across modules", `pub(super)` for "visible to the parent module only", and `pub` only for the genuinely intended public API.
- Every `pub` item is part of your SemVer contract (see §4) — audit what's `pub` deliberately rather than defaulting everything to `pub` for convenience.
- Add `#[non_exhaustive]` to public enums/structs you expect to grow variants/fields in future minor versions, so adding a variant isn't a breaking change for downstream `match` statements (forces downstream code to include a wildcard arm).
- Use `cargo public-api` or `cargo semver-checks` to diff your crate's public API surface between versions and catch accidental breaking changes before publishing.

## 4. SemVer discipline

Follow the Rust API Guidelines' SemVer compatibility rules (`C-*` about breaking changes) and the broader Cargo SemVer guidelines:
- **Breaking (major version bump)**: removing/renaming a public item, adding a required field/variant to a non-`#[non_exhaustive]` type, tightening a trait bound, changing a function signature.
- **Non-breaking (minor version bump)**: adding new public items, adding a variant to a `#[non_exhaustive]` enum, relaxing a trait bound, adding a new default-implemented trait method.
- **Patch version**: bug fixes with no public API change.

`cargo semver-checks` automates this check in CI and is the current standard tool for catching accidental breaking changes before they ship.

## 5. Dependency selection criteria

Before adding a dependency, evaluate (see also `references/13-security-and-supply-chain.md` for the security angle):
- **Maintenance signal**: recent commits/releases, responsive maintainers, issue backlog health (check the repo, not just crates.io download counts).
- **Dependency weight**: does it pull in a large transitive dependency tree for a small amount of functionality you need? (`cargo tree` to inspect.)
- **`unsafe` usage**: does it use `unsafe` internally, and if so, is that justified (FFI, performance-critical, well-tested) — `cargo geiger` reports `unsafe` usage across your dependency tree.
- **License compatibility**: verify the license is compatible with your project's licensing (`cargo deny check licenses`).
- **API stability**: pre-1.0 crates (`0.x`) can introduce breaking changes on any minor bump per Cargo's SemVer convention (`0.x.y`, breaking changes bump `x` not `y`) — pin more conservatively or vet upgrade diffs for these.

## 6. Anti-patterns checklist

- [ ] Old-style `mod.rs` files used throughout a project targeting edition 2018+ (not wrong, but inconsistent with modern convention — flag as a style nit, not a bug)
- [ ] Everything marked `pub` by default instead of narrowest-necessary visibility
- [ ] No `#[non_exhaustive]` on public enums/structs expected to grow
- [ ] No `cargo semver-checks`/`cargo public-api` in CI for a published library
- [ ] A workspace fragmented into many tiny crates with no clear reuse/compile-time justification
- [ ] Business logic living directly in `main.rs`/`lib.rs` instead of organized submodules
- [ ] Dependencies added without checking maintenance status, transitive weight, or license

---

## Real references

- The Rust Programming Language, ch. 7 (Managing Growing Projects with Packages, Crates, and Modules): https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html
- The Cargo Book — Workspaces: https://doc.rust-lang.org/cargo/reference/workspaces.html
- Rust API Guidelines — Future proofing (`C-STRUCT-PRIVATE`, `C-NEWTYPE`, `#[non_exhaustive]` guidance): https://rust-lang.github.io/api-guidelines/future-proofing.html
- Cargo Book — SemVer compatibility reference: https://doc.rust-lang.org/cargo/reference/semver.html
- `cargo-semver-checks` project: https://github.com/obi1kenobi/cargo-semver-checks
- `cargo public-api` project: https://github.com/Enselic/cargo-public-api
- `cargo-geiger` (unsafe usage reporting): https://github.com/geiger-rs/cargo-geiger
