# Version Decisions

Record every time a toolchain version is pinned, upgraded, or downgraded. The Anchor ↔ Agave ↔ Rust triangle has sharp edges — log the reason.

---

## Entry Template

- **Date (UTC):**
- **Project:**
- **Decision:** pin / upgrade / downgrade / initial install
- **Selected versions:**
  - Rust (`rustc`):
  - Solana / Agave CLI:
  - AVM:
  - Anchor (`avm use <ver>`):
  - `cargo-build-sbf`:
  - Node:
  - pnpm:
- **Repo constraints driving the choice:**
  - `anchor-lang` in `Cargo.toml`:
  - `solana-program` in `Cargo.toml`:
  - `packageManager` in `package.json`:
  - MSRV declared:
  - `Cargo.lock` version (3 / 4):
- **Why these versions (one or two sentences):**
- **Known incompatibilities avoided:**
- **Verified with:** `anchor build` / `anchor test` / full deploy to <cluster>
- **Notes for the next person:**

---
