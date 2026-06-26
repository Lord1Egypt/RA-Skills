# spanDEX Agentic Swap

An OpenClaw skill for fetching token swap quotes and executing swaps onchain via [spanDEX](https://spandex.sh) and [Privy](https://privy.io) agentic wallets.

## What it does

- Fetches swap quotes from the spanDEX meta-aggregator (0x, Fabric, KyberSwap, LiFi, Odos, Relay, Velora)
- Returns best price or fastest route across all providers
- Produces wallet-ready EVM transaction calldata (approval + swap steps)
- Executes swaps onchain via Privy's agentic wallet RPC

Quotes can be fetched and inspected without a wallet. Execution requires the Privy skill.

## Install

```bash
clawhub install spandex-agentic-swap
clawhub install privy
```

## Configuration

| Variable | Required | Description |
| --- | --- | --- |
| `SPANDEX_URL` | No | spanDEX API endpoint. Defaults to `https://edge.spandex.sh` |

Privy credentials are managed by the Privy skill — follow its setup instructions after installing.

## Usage

Once both skills are installed, just ask naturally:

- `"What's the best rate to swap 10 USDC to WETH on Base?"`
- `"Swap 5 USDC to WETH"`
- `"Do a dry run of swapping 100 USDC to ETH"`

The skill will handle quote fetching, wallet selection, approval, and execution.

## Links

- [spanDEX](https://spandex.sh)
- [spanDEX docs](https://docs.spandex.sh)
- [Privy](https://privy.io)
