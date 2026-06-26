# $SGL Staking (agentic)

Stake `$SGL` to secure the Singularity compute network and earn USDC + $SGL
rewards — programmatically, with only a Solana wallet keypair. No browser.

- **Base URL:** `https://staking.x402layer.cc` (override with `SGL_STAKING_URL`)
- **Program:** `3zChiHHFxbT3qQJBrwyQgTohfX8jS91bUGT8gpyB7aBC` (Solana mainnet)
- **Token:** `$SGL` `5c4HyD2rSShqnTsf5z3SaoD2H3GE452u2CUuYjviBAGS`
- **Roles:** `compute`, `validator`, `yield` · **min** 50,000 $SGL/position
- **Script:** `scripts/stake_sgl.py`

> Scope: this covers **staking only**. Compute/grid node operation (running a
> node, off-grid, processors) is a separate concern and not part of this skill.

## Ownership model — not x402

Staking is an on-chain Anchor program, so it is **not** an x402 payment. x402
moves a token to a payee; staking locks your *own* tokens in a contract only you
control, which requires your signature. The flow is **prepare → sign → submit**:

1. POST a prepare endpoint with your wallet → get an **unsigned** base64 tx.
2. Sign it locally with your keypair.
3. Submit it (`/api/agent/submit`, or broadcast via your own RPC).

The transaction signature **is** the proof of ownership — the program rejects any
signer that isn't the staker. Reads are public on-chain data and need no auth.

## Credentials

`scripts/stake_sgl.py` reuses the skill's Solana signer:

- `SOLANA_SECRET_KEY` — base58 / JSON-array / base64 secret key. Required for
  `stake`, `unstake`, `claim-unstake`, `claim` (and to derive your wallet for
  reads). Reads also accept an explicit `--wallet`.

Only set `SOLANA_SECRET_KEY` when you intend to sign. `analytics` and
`positions --wallet <addr>` need no secret.

## Commands

```bash
# Reads (no secret)
python3 scripts/stake_sgl.py analytics
python3 scripts/stake_sgl.py positions --wallet <ADDR>

# Mutations (sign + submit with SOLANA_SECRET_KEY)
python3 scripts/stake_sgl.py stake --role compute --amount 50000
python3 scripts/stake_sgl.py unstake --role compute        # begins cooldown
python3 scripts/stake_sgl.py claim-unstake --role compute  # after cooldown
python3 scripts/stake_sgl.py claim                         # claim all rewards
python3 scripts/stake_sgl.py claim --role compute          # claim one position
```

## Endpoints (REST)

| Method | Path | Body / query |
|--------|------|--------------|
| GET | `/api/agent` | — (manifest) |
| GET | `/api/agent/analytics` | — |
| GET | `/api/agent/positions?wallet=` | — |
| POST | `/api/agent/stake` | `{ wallet, role, amount }` |
| POST | `/api/agent/unstake` | `{ wallet, role }` |
| POST | `/api/agent/claim-unstake` | `{ wallet, role }` |
| POST | `/api/agent/claim` | `{ wallet, role? }` |
| POST | `/api/agent/submit` | `{ transaction }` (base64 signed) |

Prepare endpoints return `{ action, transactions: [{ transaction, blockhash,
lastValidBlockHeight, description }], next }`. Submit returns `{ signature,
confirmed, explorer }`.

## Cooldowns

`unstake` starts a cooldown (compute 1d / validator 2d / yield 12h). Poll
`positions` for `claimableUnlock: true`, then `claim-unstake` to withdraw.

## Notes

- You must hold enough `$SGL` (and a little SOL for fees).
- Machine-readable spec: `openapi.json` in the staking app repo.
- Full docs: https://docs.x402layer.cc/staking/agentic-api
