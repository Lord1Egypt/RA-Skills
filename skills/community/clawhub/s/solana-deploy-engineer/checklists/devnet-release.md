# Devnet Release Checklist

Devnet is for testing the full release flow end-to-end before mainnet, not for production. Treat it like a dress rehearsal.

## Pre-flight

- [ ] `solana config get` shows `https://api.devnet.solana.com` (or a devnet RPC provider URL)
- [ ] `solana address` returns the expected payer pubkey
- [ ] `solana balance` ≥ 3 SOL (airdrop or top up from a funded devnet wallet; public faucet is rate-limited)
- [ ] Correct wallet keypair path is set (`solana config get` → `Keypair Path`)
- [ ] Toolchain versions recorded:
  - `rustc --version`
  - `solana --version` (Agave client)
  - `avm --version && anchor --version`
  - `node --version && pnpm --version`
- [ ] `anchor keys sync` has been run and `declare_id!` / `Anchor.toml` / program keypair all match
- [ ] Repo is on the intended git commit (`git rev-parse HEAD` recorded)

## Build & test

- [ ] `pnpm install` (or matching package manager) clean
- [ ] `anchor build` succeeds
- [ ] `sha256sum target/deploy/<program>.so` recorded
- [ ] `anchor test` passes (or `anchor test --skip-local-validator` against a dedicated validator)
- [ ] IDL generated at `target/idl/<program>.json` and inspected for expected instructions/accounts
- [ ] TS types generated at `target/types/<program>.ts` used by SDK

## Cost estimate

- [ ] Program `.so` size: `ls -l target/deploy/<program>.so`
- [ ] Rent-exempt cost via `solana rent <2 * size_in_bytes>` recorded
- [ ] Deploy budget ≥ estimate + 30% margin

## Deploy

- [ ] Decide direct deploy vs buffer-based (buffer recommended for programs > 100 KB or unreliable network)
- [ ] Priority-fee value chosen (e.g. `--with-compute-unit-price 10000` for devnet baseline)
- [ ] If buffer-based:
  - [ ] `solana program write-buffer target/deploy/<program>.so --with-compute-unit-price <μL>` — buffer pubkey recorded
  - [ ] `solana program deploy --buffer <buf> --program-id target/deploy/<program>-keypair.json --max-len <2x_size>`
- [ ] If direct: `anchor deploy --provider.cluster devnet`
- [ ] Deploy transaction signature(s) recorded

## Post-deploy verification

- [ ] `solana program show <program_id>` — Authority, Data Length, Last Deployed In Slot all recorded
- [ ] `anchor idl init <program_id>` (first deploy) or `anchor idl upgrade <program_id>` — IDL confirmed on-chain
- [ ] `anchor idl fetch <program_id>` diffed against local IDL (should match)
- [ ] Frontend/SDK env vars updated to new program ID
- [ ] Smoke test: at least one read-only call and one state-mutating call succeed
- [ ] Leftover buffer accounts closed: `solana program close --buffers`

## Record results

- [ ] Entry added to `memory/deploy-history.md`
- [ ] Any novel error added to `memory/error-catalog.md`
- [ ] Version pinning notes added to `memory/version-decisions.md` if anything changed
