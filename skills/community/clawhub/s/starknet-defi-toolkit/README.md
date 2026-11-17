# Starknet DeFi Toolkit

A Python CLI for AI agents that need to read and simulate Starknet L2 DeFi state. Cairo / Starknet ecosystem coverage without a paid RPC.

## Why this exists

The ClawHub marketplace had `starknet` returning almost no real skills (Cairo had a 0.015 score). Yet Starknet is one of the most active zk-rollup L2s and has a real DeFi stack (Ekubo, JediSwap, STRK staking, account abstraction via Argent X / Braavos). Most agent toolkits on ClawHub only cover Ethereum, Base, and Solana.

This skill fills that gap with code that actually runs.

## Capabilities (verified working)

| Command | What it does |
|---|---|
| `balance` | Reads ERC-20 `balanceOf` for any token via Starknet JSON-RPC |
| `price` | Fetches STRK / ETH USD quote from CoinGecko |
| `pools` | Lists Ekubo concentrated-liquidity pools with TVL |
| `simulate` | Estimates output for a constant-product or CL swap |
| `scaffold` | Emits a Cairo 1 / Sierra ERC-20 skeleton |

## Quick start

```bash
pip install requests
python scripts/starknet_toolkit.py balance --address 0x049d36570d4e46f48e99674bd3fcc8463... --token STRK
```

## Limitations

- Read + simulate only. Never signs or sends.
- Free public RPCs are rate-limited. Set `STARKNET_RPC_URL` for production.
- No MEV protection, no private order flow.

## Files

- `SKILL.md` — the agent-facing manifest
- `scripts/starknet_toolkit.py` — the CLI

## License

MIT
