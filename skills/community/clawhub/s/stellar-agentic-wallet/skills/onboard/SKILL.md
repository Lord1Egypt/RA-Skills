---
name: onboard
description: One-shot wallet readiness check for the Stellar agent wallet. Verifies the secret is loadable, the account is funded, the USDC Classic trustline is in place, and there is a USDC balance to pay with. Produces a scorecard with the exact next command for each missing piece. Optional --setup mode walks the user through adding the trustline and (on explicit request) swapping XLM for USDC. Triggers on "onboard", "set up wallet", "am I ready to pay", "first time", "get started", or before the user's first pay-per-call.
---

# onboard

The entry-point skill for a new user. Answers one question: **"Can I
pay an MPP Router / x402 API with this wallet right now?"** and, if
not, prints the exact command to fix each gap.

## When to trigger

- User says: "onboard", "set up wallet", "am I ready", "first time",
  "get started", "check my wallet".
- **Proactively, before the first pay-per-call.** If the user has never
  paid and there's no selected wallet / USDC in sight, run onboard
  rather than letting pay-per-call fail mid-flow.

## Not for

- Cross-chain bridging — use `bridge`.
- Ongoing balance checks during use — use `check-balance` (lighter).
- Key generation — use `scripts/generate-keypair.ts` (onboard never
  creates or overwrites a secret file).

## Checks

Run in order; the first failure is the one the user should fix first.

1. **Secret resolvable.** Reads from `--identity <name>` or `--secret-file`
   (default `.stellar-secret`), falling back to `.env.prod` then `.env` only
   when a secret file is missing. Only
   recognises these env keys, all validated against the Stellar strkey
   format `S[A-Z0-9]{55}`:
   - `STELLAR_SECRET` (preferred)
   - `STELLAR_SECRET_KEY`, `STELLAR_PRIVATE_KEY`, `STELLAR_PRIVATE` (legacy)

   If loaded from a legacy name, onboard warns and suggests renaming.
   **Never overwrites any existing file.** If the user has both an old
   and new key, we append a new `STELLAR_SECRET=` line rather than
   editing the old one — that migration step is manual by design.
2. **Account funded.** If Horizon returns 404 → the account has never
   received XLM. Report the pubkey so the user can top up.
3. **XLM reserve.** Stellar requires 1 XLM base + 0.5 XLM per subentry
   (the trustline counts). Onboard recommends ≥ 1.6 XLM (1 base + 0.5
   trustline + 0.1 cushion for fees and a swap).
4. **USDC Classic trustline.** Required to hold Classic USDC. SAC-only
   USDC doesn't need one, but Classic is what swaps, payouts, and most
   wallets use.
5. **USDC balance.** Sum of Classic + SAC. Zero means either receive a
   transfer from elsewhere or swap XLM on the DEX.
6. **.gitignore hygiene.** If a secret file lives inside a git repo and
   isn't matched by any `.gitignore` pattern, onboard warns. `--setup`
   refuses to proceed until the user adds it to `.gitignore` or passes
   `--i-know`.

## How to run

```bash
# Diagnose only — never spends, never writes.
npx tsx skills/onboard/run.ts

# Interactive: also offer to add the USDC trustline.
npx tsx skills/onboard/run.ts --setup

# Setup + swap 10 XLM for USDC.
npx tsx skills/onboard/run.ts --setup --swap 10

# Machine-readable report.
npx tsx skills/onboard/run.ts --json

# Ack the gitignore warning when you really do want to proceed.
npx tsx skills/onboard/run.ts --setup --i-know
```

Base flags (`--identity`, `--secret-file`, `--network`, `--horizon-url`, `--rpc-url`,
`--asset-sac`) behave like every other skill — see `scripts/src/cli-config.ts`.

## Safety

- 🔐 **Never commit `.stellar-secret`, `.env`, `.env.prod`, or `.secrets/*`.**
  The printed banner says this every run. When running inside a git
  repo, we also grep `.gitignore` and block `--setup` if any of these
  files would be committed.
- 🔐 **Secret files are never overwritten.** If one exists, onboard
  reads it. If only an env file has the value under a legacy key name,
  onboard loads it and suggests a rename — it does not rewrite the file.
  Existing Stellar CLI identities are selected with `--identity <name>` and
  are never modified by onboard.
- 💸 **Swapping is opt-in.** `--swap N` is the only path to a swap.
  Onboard never guesses a swap amount.
- 💸 **Mainnet swap prompts.** `swap-xlm-to-usdc.ts` has its own
  confirmation gates — they still fire even when onboard invokes it.

## Example output

```
Account: GABC...XYZ
Network: pubnet
Secret:  /home/me/wallet/.stellar-secret (file)

  ✅ [secret] Secret loaded from /home/me/wallet/.stellar-secret (file)
  ✅ [xlm] XLM balance 3.0000000 (spendable 1.5000000)
  ❌ [trustline] USDC Classic trustline not set
       Run: npx tsx skills/check-balance/add-trustline.ts --network pubnet
       (costs 0.5 XLM reserve + a few stroops for the tx fee)
  ❌ [usdc] USDC balance is zero — can't pay for anything yet
       You can get USDC by:
         (a) receiving a transfer to this address from another wallet or exchange, OR
         (b) swapping XLM → USDC: npx tsx skills/check-balance/swap-xlm-to-usdc.ts --usdc <amount>

🔐 Never commit .stellar-secret, .env, .env.prod, or .secrets/*.
   This wallet's secret key controls real USDC. Treat it like a password.
```

## Anti-patterns

- ❌ Don't call pay-per-call without running onboard first on a new
  machine — 90% of first-call failures are "no trustline" or "no USDC".
- ❌ Don't rewrite a user's `.env` file. Migration is their call.
- ❌ Don't auto-swap. Spending decisions stay explicit.
