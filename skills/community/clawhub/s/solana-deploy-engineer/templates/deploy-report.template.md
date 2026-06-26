# Deploy Report

Fill this in for every non-trivial deploy (devnet or mainnet). Save alongside the release in `releases/<date>-<cluster>/` or commit to an ops repo.

## Identity

- **Date (UTC):**
- **Project:**
- **Cluster:** `localnet` | `devnet` | `mainnet-beta`
- **Operator:**
- **Git commit:** `git rev-parse HEAD`
- **Working tree clean:** yes / no
- **Audit reference (if any):**

## Toolchain

- Rust (`rustc --version`):
- Cargo (`cargo --version`):
- Solana / Agave CLI (`solana --version`):
- AVM (`avm --version`):
- Anchor (`anchor --version`):
- `cargo-build-sbf --version`:
- Node (`node --version`):
- pnpm / npm / yarn:

## Build

- Build command: `anchor build` / `anchor build --verifiable`
- `.so` path:
- `.so` size (bytes):
- `.so` sha256 (local):
- Verifiable: yes / no
- `solana-verify` result (if run):

## Tests

- `anchor test` result:
- Skipped/failing tests and justification:

## Cost

- `--max-len` used (bytes):
- Rent-exempt cost (`solana rent <max_len>`):
- Priority fee used (microLamports/CU):
- Total SOL spent on deploy:
- Payer balance before / after:

## Network

- RPC used (deploy):
- RPC used (verification):
- Provider (Helius / QuickNode / Triton / Alchemy / other):
- Congestion observed:

## Authorities & keys

- Program ID:
- ProgramData address:
- Program keypair path:
- Upgrade authority (pubkey):
- Upgrade authority type: hardware wallet / filesystem keypair / Squads multisig / immutable
- Squads vault pubkey (if applicable):
- Squads proposal URL (if applicable):
- IDL authority:

## Deploy actions

- Mode: direct `anchor deploy` / buffer-based / Squads proposal
- Buffer pubkey (if used):
- Buffer content sha256 (verified against local `.so`):
- Deploy transaction signature(s):
- Upgrade transaction signature(s):
- On-chain `.so` sha256 (post-deploy, `solana program dump`):
- `solana program show <program_id>` output captured:
  - Authority:
  - Data Length:
  - Last Deployed In Slot:

## IDL

- IDL action: `init` / `upgrade` / none
- IDL transaction signature:
- On-chain IDL matches local: yes / no

## Config changes downstream

- Frontend env updated: yes / no (where)
- Backend / SDK env updated: yes / no (where)
- Indexer / webhook updated: yes / no
- Dependent services notified:

## Verification

- Read-only smoke call: pass / fail
- State-mutating canary call: pass / fail
- Monitoring / alerts configured for new program ID: yes / no

## Cleanup

- Buffer accounts closed (`solana program close --buffers`): yes / no
- Temporary authorities revoked: yes / no / n/a
- Release archive stored at:

## Risks / follow-ups

-

## Memory log updated

- `memory/deploy-history.md`: yes / no
- `memory/error-catalog.md`: yes / no / n/a
- `memory/version-decisions.md`: yes / no / n/a
- `memory/project-notes.md`: yes / no / n/a
