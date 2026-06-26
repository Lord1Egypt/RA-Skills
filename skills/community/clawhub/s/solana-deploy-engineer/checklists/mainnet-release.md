# Mainnet-beta Release Checklist

Mainnet is production. Assume anything that can go wrong will cost real SOL and real users. Do not skip steps. Do not improvise.

## Explicit go/no-go

- [ ] The user has explicitly and unambiguously asked for a mainnet-beta deployment in this session
- [ ] Devnet dress rehearsal of this exact commit has already been completed and logged in `memory/deploy-history.md`
- [ ] All audits / reviews for this commit are signed off
- [ ] Deploy window is appropriate (avoid mainnet congestion events, ecosystem launches, or weekend-only windows if on-call is thin)

## Authority & signing

- [ ] Upgrade authority decided: single key, Squads multisig, or immutable
- [ ] If single key: signer is a hardware wallet (`usb://ledger…`), not a filesystem keypair
- [ ] If Squads: vault pubkey recorded, required signer set confirmed, proposal path prepared
- [ ] If immutable: confirmed with user that this is intentional and irreversible
- [ ] Program keypair (`target/deploy/<program>-keypair.json`) is the intended program address and is backed up securely — never commit the keypair for a mainnet program

## RPC & network

- [ ] Dedicated mainnet RPC URL configured (Helius / QuickNode / Triton / Alchemy). Public RPC is not acceptable for a deploy.
- [ ] `solana config get` shows the dedicated RPC, not `api.mainnet-beta.solana.com`
- [ ] RPC provider's current rate limit and max transaction size confirmed adequate
- [ ] Priority-fee strategy chosen (static microLamports value or dynamic estimate from RPC)

## Build (verifiable)

- [ ] Toolchain versions recorded: Rust, Solana/Agave, Anchor (via AVM), `cargo-build-sbf`, Node, pnpm
- [ ] Repo on the exact audited git commit (`git rev-parse HEAD` recorded; no dirty working tree)
- [ ] `anchor keys sync` run; `declare_id!` / `Anchor.toml` / program keypair pubkey all match
- [ ] `anchor build --verifiable` succeeded (uses the Solana verifiable Docker image)
- [ ] `sha256sum target/deploy/<program>.so` recorded — matches audit artifact if applicable
- [ ] IDL at `target/idl/<program>.json` reviewed and approved

## Cost estimate

- [ ] Program `.so` size measured
- [ ] `--max-len` chosen (at least 2x current size for upgrade headroom)
- [ ] Rent-exempt cost calculated via `solana rent <max_len>`
- [ ] Payer balance ≥ rent + transaction fees + priority-fee margin + 30% safety buffer
- [ ] If upgrading an existing program: `solana program extend <program_id> <additional_bytes>` run first if `--max-len` was originally too small

## Buffer upload

- [ ] `solana program write-buffer target/deploy/<program>.so --url <dedicated_rpc> --with-compute-unit-price <μL>`
- [ ] Buffer pubkey recorded immediately in deploy report and `memory/deploy-history.md`
- [ ] If upload dies mid-flight: resume with `--buffer <existing_buffer_pubkey>`, do not start over from scratch
- [ ] Buffer content verified: `solana program dump <buffer> /tmp/buf.so && sha256sum /tmp/buf.so` matches the local `.so` hash
- [ ] If upgrade authority is Squads: `solana program set-buffer-authority <buffer> --new-buffer-authority <squads_vault>` executed; Squads proposal created referencing this buffer

## Deploy or upgrade

- [ ] First-time deploy: `solana program deploy --buffer <buf> --program-id target/deploy/<program>-keypair.json --max-len <N> --with-compute-unit-price <μL>`
- [ ] Existing-program upgrade: `solana program upgrade <buffer> <program_id> --upgrade-authority <auth> --with-compute-unit-price <μL>`
- [ ] All transaction signatures recorded
- [ ] `solana program show <program_id>` output recorded:
  - Program ID
  - ProgramData Address
  - Authority
  - Last Deployed In Slot
  - Data Length
- [ ] Deployed `.so` hash matches expected: `solana program dump <program_id> /tmp/onchain.so && sha256sum /tmp/onchain.so`

## IDL

- [ ] `anchor idl upgrade <program_id> --filepath target/idl/<program>.json --provider.cluster mainnet` (or `anchor idl init` for first deploy)
- [ ] `anchor idl fetch <program_id>` diffed against local IDL — matches

## Verification

- [ ] `solana-verify verify-from-repo --url <rpc> <program_id>` succeeded (if repo set up for verifiable builds)
- [ ] Frontend / backend / SDK env vars updated to the new program ID
- [ ] A read-only on-chain call succeeds (fetch a known account)
- [ ] Canary state-mutating instruction succeeds from a burner wallet
- [ ] Dependent services (indexers, webhooks, analytics) acknowledge the new program ID

## Cleanup

- [ ] Close any leftover buffer accounts to recover rent: `solana program close --buffers`
- [ ] Revoke or transfer any temporary authorities used during deploy
- [ ] Confirm `.so` artifacts and deploy keypair are stored in the release archive (not committed to the repo)

## Record & publish

- [ ] Deploy report generated from `templates/deploy-report.template.md` and saved to the release folder
- [ ] Entry written to `memory/deploy-history.md`
- [ ] Any novel error written to `memory/error-catalog.md`
- [ ] Release note published (commit hash, program ID, `.so` sha256, authority, RPC used)
- [ ] Monitoring / alerts updated to watch the new program ID
