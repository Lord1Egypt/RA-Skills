# SkyInsights

Query the [CertiK SkyInsights](https://skyinsights.certik.com/) API to assess wallet and transaction risk, look up on-chain entity labels, and run AML compliance screening.

## Commands

| Command | Description |
|---|---|
| `/skyinsights kya <address> [chain]` | Address risk score and labels |
| `/skyinsights labels <address> [chain]` | Entity info and on-chain labels |
| `/skyinsights screen <address> [chain]` | AML compliance screening (~5–15s) |
| `/skyinsights kyt <txn_hash> <chain>` | Transaction risk analysis |

## Setup

```bash
SKYINSIGHTS_API_KEY=your_key
SKYINSIGHTS_API_SECRET=your_secret
```

Get credentials at [skyinsights.certik.com](https://skyinsights.certik.com/).

## Supported Chains

| Chain | API Value | kya / labels | kya / risk | screen | kyt |
|---|---|:---:|:---:|:---:|:---:|
| Bitcoin | `btc` | ✓ | ✓ | ✓ | ✓ |
| Bitcoin Cash | `bch` | ✓ | ✓ | | |
| Litecoin | `ltc` | ✓ | ✓ | | |
| Solana | `sol` | ✓ | ✓ | | |
| Ethereum | `eth` | ✓ | ✓ | ✓ | ✓ |
| Polygon | `polygon` | ✓ | ✓ | ✓ | ✓ |
| Optimism | `op` | ✓ | ✓ | ✓ | ✓ |
| Arbitrum | `arb` | ✓ | ✓ | ✓ | ✓ |
| Avalanche | `avax` | ✓ | ✓ | ✓ | ✓ |
| Binance Smart Chain | `bsc` | ✓ | ✓ | ✓ | ✓ |
| Fantom | `ftm` | ✓ | ✓ | | |
| Tron | `tron` | ✓ | ✓ | ✓ | ✓ |
| Wemix | `wemix` | ✓ | ✓ | ✓ | ✓ |
| Base | `base` | ✓ | ✓ | ✓ | ✓ |
| Blast | `blast` | ✓ | ✓ | | |
| Linea | `linea` | ✓ | ✓ | | |
| Sonic | `sonic` | ✓ | ✓ | | |
| Unichain | `unichain` | ✓ | ✓ | | |
| Polygon zkEVM | `polygon_zkevm` | ✓ | ✓ | | |

## Examples

```
/skyinsights kya 0x0fa09C3A328792253f8dee7116848723b72a6d2e eth
/skyinsights screen 0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B eth
/skyinsights kyt 0x0f7998d0563163b86df4a5f1eb8f23fc755e1873e14bded71e1c8ade58cb5419 eth
```

Natural language also works:

- `Is 0x0fa09C3A328792253f8dee7116848723b72a6d2e risky?`
- `What labels does 0x71660c4005BA85c37ccec55d0C4493E66Fe775d3 have on ETH?`
- `Run AML screening on 0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B`
- `Analyze this transaction: 0x0f7998d0563163b86df4a5f1eb8f23fc755e1873e14bded71e1c8ade58cb5419 on ETH`
