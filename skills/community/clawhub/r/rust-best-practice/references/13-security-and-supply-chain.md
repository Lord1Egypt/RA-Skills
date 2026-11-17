# Security and Supply-Chain

## Table of contents
1. `cargo audit` and vulnerability scanning
2. `cargo deny` for policy enforcement
3. Secrets handling
4. Input validation and injection risks
5. Dependency vetting workflow
6. Anti-patterns checklist

---

## 1. `cargo audit` and vulnerability scanning

`cargo audit` checks `Cargo.lock` against the RustSec Advisory Database (community-maintained registry of known vulnerabilities in published crates):

```bash
cargo install cargo-audit
cargo audit
```

Run this in CI on every build (or at minimum on a schedule, since new advisories can appear for dependencies you haven't changed) — a clean build today doesn't mean a dependency won't have a disclosed CVE next week.

## 2. `cargo deny` for policy enforcement

`cargo deny` is a broader policy tool combining vulnerability checks, license compliance, and dependency source/duplicate-version auditing in one config file (`deny.toml`):

```toml
[advisories]
vulnerability = "deny"
unmaintained = "warn"

[licenses]
allow = ["MIT", "Apache-2.0", "BSD-3-Clause"]
deny = ["GPL-3.0"]

[bans]
multiple-versions = "warn"

[sources]
unknown-registry = "deny"
unknown-git = "deny"
```

```bash
cargo install cargo-deny
cargo deny check
```

This is the standard tool for enforcing "only fetch dependencies from crates.io, only permissive licenses, fail the build on known vulnerabilities" as an automated CI gate rather than a manual review step.

## 3. Secrets handling

- Never commit secrets (API keys, DB credentials, private keys) into source — use environment variables (`std::env::var`) loaded from `.env` files excluded via `.gitignore`, or a proper secrets manager (Vault, AWS Secrets Manager, etc.) in production.
- The `secrecy` crate wraps sensitive in-memory values so they're not accidentally printed via `Debug`/logged, and can zero memory on drop.
- The `zeroize` crate (often used underneath `secrecy`) explicitly zeroes memory holding sensitive data when it's dropped, mitigating exposure via memory dumps/swap — relevant for cryptographic key material especially.
- Avoid `format!("{:?}", config)`-style debug logging of structs containing credentials — either exclude sensitive fields from `#[derive(Debug)]` via a manual impl, or wrap them in a type whose `Debug` impl redacts the value.

## 4. Input validation and injection risks

- **SQL injection**: always use parameterized queries (see `references/10-web-backend-and-networking.md` §5) — never string-concatenate user input into SQL.
- **Command injection**: when invoking `std::process::Command`, pass arguments as separate `.arg()` calls, never build a single shell string with user input interpolated and pass it to `sh -c`.
- **Path traversal**: when accepting user-supplied filenames/paths (e.g. a web upload handler), canonicalize and verify the resulting path stays within the intended base directory before any filesystem operation — don't trust `..`-containing input.
- **Deserialization of untrusted input**: be cautious with formats/crates that support arbitrary code execution or resource exhaustion via crafted input (e.g. unbounded recursive structures causing stack overflow, "billion laughs"-style expansion) — prefer `serde` with formats that don't execute arbitrary logic during deserialization, and consider size/depth limits for untrusted payloads.
- **Integer overflow**: in release builds, Rust arithmetic overflow wraps silently by default (debug builds panic) — use `checked_*`/`saturating_*`/`wrapping_*` explicitly wherever overflow is a real possibility with untrusted input driving the computation (e.g. buffer size calculations), rather than relying on debug-only panic behavior to catch it.

## 5. Dependency vetting workflow

For security-sensitive projects, beyond `cargo audit`/`cargo deny`:
- `cargo vet` (Mozilla-originated) tracks which dependencies have been manually reviewed by your team or a trusted third party, and fails CI on unreviewed new/updated dependencies — used by Firefox and other large Rust codebases.
- `cargo-crev` is a distributed, web-of-trust style code review system for crates — reviews are shared/signed and can be checked as part of a supply-chain policy.
- Minimize total dependency count and prefer well-established crates (high download counts *combined with* active maintenance, not download count alone) — smaller attack surface, fewer transitive advisories to track.

## 6. Anti-patterns checklist

- [ ] No `cargo audit`/`cargo deny` in CI
- [ ] Secrets committed to source control or logged via `Debug`
- [ ] SQL/shell commands built via string concatenation with user input
- [ ] User-supplied paths used in filesystem operations without canonicalization/containment checks
- [ ] Relying on debug-build overflow panics as the only overflow protection in code that also ships release builds
- [ ] Adding dependencies without checking maintenance status or license compatibility
- [ ] No process for reviewing/tracking new transitive dependencies in a security-sensitive project

---

## Real references

- RustSec Advisory Database: https://rustsec.org/
- `cargo-audit` project: https://github.com/rustsec/rustsec/tree/main/cargo-audit
- `cargo-deny` documentation: https://embarkstudios.github.io/cargo-deny/
- `cargo vet` (Mozilla) project: https://mozilla.github.io/cargo-vet/
- `cargo-crev` project: https://github.com/crev-dev/cargo-crev
- `secrecy` crate docs: https://docs.rs/secrecy/latest/secrecy/
- `zeroize` crate docs: https://docs.rs/zeroize/latest/zeroize/
- The Rust Reference — Overflow behavior: https://doc.rust-lang.org/reference/expressions/operator-expr.html#overflow
- OWASP guidance referenced by the broader Rust security community (general web app security background): https://owasp.org/www-project-top-ten/
