# Tooling, Cargo, and CI

## Table of contents
1. Essential `Cargo.toml` setup
2. Lint configuration (Clippy + rustc)
3. Feature flags
4. MSRV policy
5. Release profiles
6. Recommended CI pipeline
7. Anti-patterns checklist

---

## 1. Essential `Cargo.toml` setup

```toml
[package]
name = "my_crate"
version = "0.1.0"
edition = "2021"
rust-version = "1.75"       # MSRV — see §4
license = "MIT OR Apache-2.0"
description = "..."
repository = "https://github.com/org/repo"

[dependencies]
serde = { version = "1", features = ["derive"] }

[dev-dependencies]
criterion = "0.5"
proptest = "1"

[lints.rust]
unsafe_op_in_unsafe_fn = "deny"

[lints.clippy]
all = "warn"
pedantic = "warn"
```

The `[lints]` table (stabilized in Cargo 1.74) is now the idiomatic place to configure lints workspace-wide instead of scattering `#![warn(...)]` at each crate root — set it once in the workspace root `Cargo.toml` and inherit with `[lints] workspace = true` in member crates.

## 2. Lint configuration (Clippy + rustc)

Run `cargo clippy --all-targets --all-features -- -D warnings` in CI so lint regressions fail the build, not just show as warnings developers ignore.

Recommended lint groups:
- `clippy::all` — default lint set, should always be clean.
- `clippy::pedantic` — stricter, more opinionated; enable and then `#[allow]` specific lints you've deliberately decided don't fit your codebase, rather than skipping the group entirely.
- `clippy::nursery` — experimental lints, more false positives; opt-in per-project judgment.
- `clippy::cargo` — checks `Cargo.toml` metadata quality (useful for published crates).

Never blanket `#![allow(warnings)]` or `#![allow(clippy::all)]` — this silences genuinely useful lints along with noisy ones. Suppress specific lints at the narrowest possible scope with a comment explaining why:

```rust
#[allow(clippy::too_many_arguments)] // FFI signature mirrors the C API exactly
extern "C" fn callback(a: i32, b: i32, c: i32, d: i32, e: i32, f: i32, g: i32, h: i32) {}
```

## 3. Feature flags

Keep features **additive** (enabling a feature should never remove functionality — this breaks the "feature unification" model where Cargo merges the union of features requested by all dependents in a build). Use `#[cfg(feature = "...")]` to gate optional functionality and heavy optional dependencies:

```toml
[features]
default = ["std"]
std = []
serde = ["dep:serde"]
```

Document every feature in `Cargo.toml` comments or a `README`/`docs.rs` feature section — undocumented features are a frequent source of confusion for downstream users. Test feature combinations in CI (at minimum: `--no-default-features`, `--all-features`, and `default`) since feature-gated code paths are otherwise easy to silently break.

## 4. MSRV policy

Declare `rust-version` in `Cargo.toml` (the Minimum Supported Rust Version) so Cargo itself errors clearly if a user's toolchain is too old, rather than a confusing compile failure deep in a dependency. Pick an MSRV deliberately (e.g. "current stable minus N releases", or pinned to a specific LTS-like target for your organization) and verify it in CI with a pinned toolchain job, not just the latest stable.

## 5. Release profiles

```toml
[profile.release]
opt-level = 3
lto = "thin"        # or "fat" for maximum optimization at the cost of build time
codegen-units = 1   # trade compile time for more cross-function optimization
panic = "unwind"    # keep "unwind" unless you specifically want smaller binaries + no catch_unwind
strip = true         # strip symbols from the final binary
```

See `references/06-performance-and-memory.md` §5 for when these trade-offs are worth making.

## 6. Recommended CI pipeline

A thorough Rust CI pipeline (GitHub Actions shown, but the steps generalize) runs, at minimum:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with: { components: "clippy, rustfmt" }
      - run: cargo fmt --all -- --check
      - run: cargo clippy --all-targets --all-features -- -D warnings
      - run: cargo test --all-features
      - run: cargo doc --no-deps --all-features
      - run: cargo build --release
```

Add as the project matures: `cargo audit`/`cargo deny` (see `references/13-security-and-supply-chain.md`), an MSRV-pinned job, `cargo llvm-cov` for coverage reporting, Miri for `unsafe`-heavy crates, and cross-compilation checks if targeting multiple platforms. Cache `~/.cargo` and `target/` (e.g. via `Swatinem/rust-cache`) to keep CI fast — Rust compile times are the most common CI pain point.

## 7. Anti-patterns checklist

- [ ] No `cargo clippy`/`cargo fmt --check` in CI, or lints run but not enforced (`-D warnings` missing)
- [ ] `#![allow(warnings)]` or blanket `#[allow(clippy::all)]`
- [ ] No `rust-version` (MSRV) declared for a published/shared library
- [ ] Feature flags that remove functionality rather than add it (breaks feature unification)
- [ ] Debug builds shipped/benchmarked in place of `--release`
- [ ] CI without dependency caching, making every run painfully slow
- [ ] No `cargo test --all-features` / feature-combination testing for a crate with non-default features

---

## Real references

- The Cargo Book (official): https://doc.rust-lang.org/cargo/
- Cargo Book — `[lints]` table: https://doc.rust-lang.org/cargo/reference/manifest.html#the-lints-section
- Cargo Book — Features: https://doc.rust-lang.org/cargo/reference/features.html
- Cargo Book — Profiles: https://doc.rust-lang.org/cargo/reference/profiles.html
- Cargo Book — `rust-version` field (MSRV): https://doc.rust-lang.org/cargo/reference/manifest.html#the-rust-version-field
- Clippy documentation and lint groups: https://doc.rust-lang.org/clippy/
- Clippy lint index (searchable, all lints with rationale): https://rust-lang.github.io/rust-clippy/master/index.html
- `rustfmt` configuration options: https://rust-lang.github.io/rustfmt/
- `Swatinem/rust-cache` GitHub Action: https://github.com/Swatinem/rust-cache
- `dtolnay/rust-toolchain` GitHub Action: https://github.com/dtolnay/rust-toolchain
