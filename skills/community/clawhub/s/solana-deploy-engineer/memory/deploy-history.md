# Deploy History

Append one entry per deploy attempt (success OR failure). Newest at the top.

---

## Entry Template

- **Date (UTC):**
- **Project / repo:**
- **Git commit:**
- **Cluster:** `localnet` | `devnet` | `mainnet-beta`
- **Operator:**
- **Toolchain:**
  - Rust:
  - Solana (Agave):
  - AVM:
  - Anchor:
  - `cargo-build-sbf`:
  - Node:
  - pnpm:
- **RPC:**
- **Build mode:** standard / verifiable
- **`.so` sha256 (local):**
- **`.so` sha256 (on-chain, post-deploy):**
- **Deploy mode:** direct / buffer / Squads
- **Buffer pubkey (if any):**
- **Program ID:**
- **ProgramData address:**
- **Upgrade authority:**
- **Priority fee (μL/CU):**
- **`--max-len`:**
- **Total SOL cost:**
- **Transaction signatures:**
- **Result:** success / partial / failure
- **Issues encountered:**
- **Fixes applied:**
- **Verification notes:** (`solana program show` output, IDL diff, smoke test)
- **Follow-up actions:**

---
