---
name: yieldsllama
description: 'Query DeFi yield opportunities across chains using the yieldsllama CLI (powered by DeFi Llama API). Use when the user asks about DeFi yields, APY, best staking/lending rates, or wants to compare yield farming opportunities across chains and tokens.'
---

# yieldsllama

Query and compare DeFi yield pool data from DeFi Llama.

## Installation

### Prerequisites

- Rust toolchain (cargo): https://www.rust-lang.org/tools/install

If Rust is not installed, run:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
```

### Build and Install

```bash
# Clone the repo
git clone https://github.com/0x9bb1/yieldsllama.git /tmp/yieldsllama

# Build release binary
cd /tmp/yieldsllama && cargo build --release

# Install to PATH
cp /tmp/yieldsllama/target/release/yieldsllama /usr/local/bin/yieldsllama

# Verify
yieldsllama --help
```

### Environment Setup

The tool needs a `.env` file in the **current working directory** with the DeFi Llama API endpoint. Before each run, ensure it exists:

```bash
if [ ! -f .env ]; then echo 'LLAMA_DOMAIN="https://yields.llama.fi"' > .env; fi
```

## CLI Usage

```bash
yieldsllama [OPTIONS]
```

### Options

| Flag | Description | Default |
|---|---|---|
| `-l, --limit <N>` | Number of results to return | 10 |
| `-e, --exposure <TYPE>` | Pool type: `single` or `multi` | single |
| `-s, --sort <FIELD>` | Sort by: `apy` or `tvl` | apy |
| `-t, --tvl <MIN>` | Minimum TVL in USD | none |
| `-c, --chain <CHAIN>` | Filter by chain name (case-insensitive) | none |
| `-a, --asset <TOKEN>` | Filter by token symbol (case-insensitive) | none |

### Common Examples

```bash
# Top 10 highest APY single-asset pools
yieldsllama

# Top 20 pools sorted by TVL
yieldsllama -l 20 -s tvl

# Best USDC yields with TVL > $10M
yieldsllama -a USDC -t 10000000

# Best USDT yields on Ethereum
yieldsllama -a USDT -c Ethereum

# Best multi-asset pool yields
yieldsllama -e multi -l 10

# Compare stablecoins with TVL > $10M
yieldsllama -a USDC -t 10000000 -l 5
yieldsllama -a USDT -t 10000000 -l 5
yieldsllama -a USDE -t 10000000 -l 5
yieldsllama -a DAI -t 10000000 -l 5

# Best ETH yields with TVL > $1M
yieldsllama -a WETH -t 1000000 -l 10

# Best yields on specific chains
yieldsllama -c Ethereum -t 1000000 -l 10
yieldsllama -c Base -t 1000000 -l 10
yieldsllama -c Arbitrum -t 1000000 -l 10
```

## Output Columns

| Column | Description |
|---|---|
| apy | Total APY (apyBase + apyReward) |
| symbol | Token symbol |
| chain | Blockchain network |
| project | Protocol name |
| tvlUsd | Total Value Locked in USD |
| apyBase | Base lending/staking APY (organic, sustainable) |
| apyReward | Reward token APY (may be unsustainable, subject to token price) |
| exposure | `single` (one asset) or `multi` (LP pair etc.) |

## Guidance for Analyzing Results

When presenting yield data to the user, always consider and mention:

1. **apyBase vs apyReward**: Base APY is from lending/staking fees (more sustainable). Reward APY comes from incentive tokens (can drop to 0 when rewards end or token dumps).
2. **TVL matters**: Very high APY with low TVL (<$1M) is often unsustainable or risky. Recommend filtering with `-t` for serious allocation decisions.
3. **APY > 100% is suspicious**: Flag any extremely high APY and warn the user about sustainability.
4. **Chain risk**: Different chains have different security profiles. Ethereum L1 is generally safest; newer L2s/alt-L1s carry more risk.
5. **Protocol risk**: Well-known protocols (Aave, Compound, Morpho) are generally safer than unknown ones.

## Workflow for Multi-Token Comparison

When the user asks "which token/pool has the best yield", run queries for each token in parallel and present a unified comparison table. Example:

```
User: "Compare USDC, USDT, USDE yields with TVL > $10M"

Run in parallel:
  yieldsllama -a USDC -t 10000000 -l 5
  yieldsllama -a USDT -t 10000000 -l 5
  yieldsllama -a USDE -t 10000000 -l 5

Then summarize the top option for each token and give a recommendation.
```

## Refreshing Data

The tool caches API responses in `data.json` for 12 hours. To force refresh:

```bash
rm -f data.json && yieldsllama
```

## Troubleshooting

| Problem | Solution |
|---|---|
| `yieldsllama: command not found` | Binary not in PATH. Run `cp /path/to/yieldsllama /usr/local/bin/` |
| `读取本地data.json文件异常` | Normal on first run — it fetches from API and creates `data.json` |
| `本地文件过期` | Cache expired (>12h). Tool auto-fetches fresh data |
| Empty results | Token symbol or chain name may not match exactly. Try without `-c`/`-a` filters first |
| Network error | Check internet connection; DeFi Llama API (`yields.llama.fi`) may be temporarily down |
| `.env` error | Ensure `.env` exists in current directory with `LLAMA_DOMAIN="https://yields.llama.fi"` |
