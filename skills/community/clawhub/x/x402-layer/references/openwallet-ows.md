# OpenWallet / OWS (Optional Wallet Backend)

Use this reference when the user asks to use **Open Wallet Standard**, **OWS**, or **openwallet.sh** with x402-layer.

## What OWS gives you

OWS is an optional local wallet backend for agent tooling.

It helps when the user wants:
- local delegated wallet access
- encrypted wallet storage instead of raw private keys in env vars
- policy-gated signing for agents
- one wallet interface shared across tools

## Current x402-layer scope

The current x402-layer integration is **optional-first**.

Supported through the `ows_cli.py` wrapper:
- pay x402-enabled API requests
- discover x402-enabled services
- sign chain-specific messages for wallet-auth flows
- list local wallets
- create OWS agent API keys

Still better handled by existing private-key flows today:
- wallet-first ERC-8004 / Solana-8004 on-chain registration transactions
- low-level custom transaction building in the Python scripts
- any workflow where a script currently requires raw EVM or Solana transaction signing

So:
- keep `PRIVATE_KEY` mode working
- keep `AWAL` mode working
- add `OWS` as an optional wallet backend where it fits cleanly first

## Install OWS

Install the OWS CLI:

```bash
npm install -g @open-wallet-standard/core
```

Confirm:

```bash
ows --help
```

If you do not want a global install, you can still inspect the CLI with:

```bash
npx -y @open-wallet-standard/core --help
```

## Basic OWS commands

List wallets:

```bash
ows wallet list
```

Create a wallet:

```bash
ows wallet create --name hackathon-wallet
```

Sign a message:

```bash
ows sign message --chain ethereum --wallet hackathon-wallet --message "hello"
ows sign message --chain solana --wallet hackathon-wallet --message "hello"
```

Pay an x402 endpoint:

```bash
ows pay request --wallet hackathon-wallet https://api.x402layer.cc/e/weather-data
```

Create an API key for agent access:

```bash
ows key create --name codex-agent --wallet hackathon-wallet
```

## x402-layer wrapper commands

The skill includes a thin wrapper:

```bash
python {baseDir}/scripts/ows_cli.py run wallet list
python {baseDir}/scripts/ows_cli.py pay-url https://api.x402layer.cc/e/weather-data --wallet hackathon-wallet
python {baseDir}/scripts/ows_cli.py discover weather
python {baseDir}/scripts/ows_cli.py sign-message --chain ethereum --wallet hackathon-wallet --message "hello"
python {baseDir}/scripts/ows_cli.py key-create --name codex-agent --wallet hackathon-wallet
```

## Recommended environment variables

| Variable | Purpose |
|---|---|
| `OWS_WALLET` | wallet name or ID to use by default |
| `OWS_BIN` | optional explicit path to the `ows` executable |
| `WALLET_ADDRESS` | optional explicit EVM address for scripts that still need address-only owner lookup |
| `SOLANA_WALLET_ADDRESS` | optional explicit Solana address for scripts that still need address-only owner lookup |

## Guidance for agents

Good guidance:
- `Use OWS when you want local delegated wallet access without exporting raw private keys into every agent shell.`
- `Use private-key mode when the current workflow needs direct transaction signing that the x402-layer Python scripts still perform locally.`
- `Use AWAL when you specifically want Coinbase Agentic Wallet flows.`

## Important limitation

In this rollout, OWS is integrated as an **optional wallet backend**, not yet as a universal replacement for every x402-layer script.

That means:
- OWS is great for pay/discover/sign-message flows
- private-key mode remains the default for the deepest registration/signing paths
