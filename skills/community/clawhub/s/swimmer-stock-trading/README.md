# Swimmer Finance stock-order skill for agents

An OpenClaw skill for discovering Swimmer Finance stock-token routes on Solana and submitting market or limit order instructions from a dedicated wallet.

Official website: [swimmer.finance](https://swimmer.finance)

No registration, login, service API key, or configurable trading API URL is required. Set up a dedicated Solana wallet, deposit canonical Solana USDC plus a small amount of SOL for fees, and ask the agent to discover tradable stocks or prepare an order.

## Important: this is a custodial transfer

Order submission transfers the offered SPL token irreversibly to the fixed Swimmer recipient and publishes the order data in a memo. It is not an atomic on-chain swap. The transaction itself cannot guarantee execution, delivery of the requested tokens, cancellation, or refund. Independently verify the destination and current custody, settlement, and refund terms through [swimmer.finance](https://swimmer.finance) before funding or signing.

The package is designed to reduce hot-wallet risk: it reads one fixed config path, rejects symlinks and unsafe permissions, requires a trusted mint allowlist and per-mint spending caps, derives the destination internally, binds confirmation to the complete intent, and never prints the key. A hardware wallet or isolated signer remains safer than any private key stored on the agent host. Use only a dedicated low-balance wallet.

## Install

```bash
clawhub install swimmer-stock-trading
python3 -m venv "$HOME/.local/share/swimmer-stock-trading/venv"
"$HOME/.local/share/swimmer-stock-trading/venv/bin/pip" install \
  -r "<SKILL_DIR>/scripts/requirements.txt"
install -d -m 700 "$HOME/.config/swimmer-stock-trading"
install -m 600 "<SKILL_DIR>/config.example.json" \
  "$HOME/.config/swimmer-stock-trading/config.json"
```

Edit the destination config in a trusted local editor. Add a new dedicated base58 Solana keypair, the independently verified fixed recipient, verified stock mint mappings, and conservative raw spending caps. Never paste the config or key into OpenClaw. See [`references/keypair-setup.md`](references/keypair-setup.md).

The fixed no-key endpoints are:

- Trading discovery: `https://api.sharesdao.com:8443`
- Solana mainnet RPC: `https://api.mainnet-beta.solana.com`

## Capabilities

- Fetch pools and determine exact `USDC-{STOCK}s` and `{STOCK}s-USDC` routes.
- Check SOL, canonical USDC, and trusted stock-token balances.
- Optionally request a market estimate only when the user asks.
- Prepare market orders without a quote and limit orders without any quote or swap API.
- Create a fresh local transaction containing exactly one SPL transfer and one public memo.
- Enforce a trusted mint allowlist, per-mint raw spending caps, a fixed destination, simulation, preflight, and digest-bound human confirmation.
- Distinguish on-chain submission from off-chain custodial settlement.

Only canonical `{STOCK}s` symbols and independently verified Solana mints are supported.

## Example prompts

```text
Use swimmer-stock-trading to show the stock tokens currently tradable against USDC on Solana.
```

```text
Use swimmer-stock-trading to check my SOL, USDC, and trusted AAPL stock-token balances.
```

```text
Use swimmer-stock-trading to prepare an unquoted market order spending 25 USDC. Explain the irreversible custodial transfer before asking me to authorize it.
```

```text
Use swimmer-stock-trading to prepare a limit order offering 25 USDC for exactly 1.25 AAPLs. Do not call a quote or swap API.
```

## Package verification

```bash
python3 scripts/verify_package.py
python3 -m unittest discover -s tests -v
```

These checks verify required documentation, references, secret placeholders, signer policy, and core validation behavior. Publishing is a separate maintainer action.
