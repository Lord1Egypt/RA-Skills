---
name: settlement-predictor
description: Real-time on-chain settlement predictor for Ethereum, Bitcoin, Arbitrum, Optimism, Base & Polygon. Live gas tiers, mempool analysis, sandwich risk detection, transaction tracking, and fee trend analysis — zero API keys required for core features.
version: "1.3.1"
author: Qi Ge
tags:
  - web3
  - ethereum
  - bitcoin
  - gas
  - mempool
  - DeFi
  - settlement
  - crypto
  - arbitrum
  - optimism
  - base
  - polygon
triggers:
  - "btc gas fee"
  - "btc fee estimate"
  - "bitcoin gas"
  - "btc交易费"
  - "比特币手续费"
  - "bitcoin fee sat/vb"
  - "比特币gas"
  - "eth gas趋势"
  - "gas上涨还是下跌"
  - "gas trend"
  - "bitcoin fee trend"
  - "手续费趋势"
  - "链上手续费分析"
  - "查以太坊gas"
  - "btc矿工费"
entry: settlement_predictor.py
runtime: python3
python_version: ">=3.10"
dependencies:
  - web3>=6.0.0
credentials:
  - name: ETHERSCAN_API_KEY
    description: "Optional. Enables: revert reason decoding, contract verification, token metadata lookup, and internal tx tracing. Free key: https://etherscan.io/myapikey"
    env_var: ETHERSCAN_API_KEY
  - name: TENDERLY_API_KEY
    description: "Optional. Enables accurate transaction simulation with gas prediction. Free tier: 1,000 simulations/month. Sign up: https://dashboard.tenderly.co/"
    env_var: TENDERLY_API_KEY
persistence:
  - path: ~/.cache/settlement-predictor/gas-history.json
    description: "Optional rolling cache of last 60 gas snapshots per chain for trend analysis. Auto-created on first use. Safe to delete."
---

# Settlement Predictor Skill

Real-time on-chain settlement prediction and mempool analysis for EVM chains.

## Features

- **Gas Prediction** — Live gas tiers (instant/fast/standard/slow) with congestion metrics
- **Settlement Time Prediction** — Estimates how long a tx takes at a given gas price
- **Optimal Window Finder** — Identifies cheapest time windows to send transactions
- **Pending Pool Analyzer** — Detects sandwich risks and DEX conflicts before you trade
- **Transaction Tracker** — Tracks submitted txs until confirmation or failure
- **Gas Trend Analysis** — Rolling history + linear regression to detect rising/falling channels

## Optional API Keys

All keys are optional. Without them, core features work fully.

```bash
export ETHERSCAN_API_KEY=your_key   # https://etherscan.io/myapikey
export TENDERLY_API_KEY=your_key   # https://dashboard.tenderly.co/
```

## Usage

```bash
# Gas prediction (all 6 chains: ethereum, arbitrum, optimism, base, polygon, bitcoin)
python settlement_predictor.py get-gas-prediction --chain ethereum
python settlement_predictor.py btc-fee-estimate --urgency medium

# Predict settlement time
python settlement_predictor.py predict-settlement --chain ethereum --gas-price 30

# Find optimal window
python settlement_predictor.py get-optimal-window --chain ethereum --urgency high

# Analyze pending pool for sandwich risk
python settlement_predictor.py analyze-pending-pool \
  --chain ethereum \
  --pool-address 0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852 \
  --direction buy \
  --amount-usd 10000

# Track a transaction
python settlement_predictor.py track-tx --chain ethereum --tx-hash 0x...

# Gas trend analysis (run multiple times to accumulate history)
python settlement_predictor.py analyze-gas-trend --chain ethereum

# BTC trend analysis
python settlement_predictor.py analyze-btc-trend

# Verify contract + scan risks (requires ETHERSCAN_API_KEY)
python settlement_predictor.py verify-contract --chain ethereum \
  --address 0xdAC17F958D2ee523a2206206994597C13D831ec7

# Get token info (ERC-20 metadata)
python settlement_predictor.py get-token-info --chain ethereum \
  --address 0xdAC17F958D2ee523a2206206994597C13D831ec7

# Simulate transaction (requires TENDERLY_API_KEY)
python settlement_predictor.py simulate-tx \
  --chain ethereum --to 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D \
  --value 0.01
```

Run `python settlement_predictor.py --help` for all commands.

# On-chain Settlement Predictor
> 链上结算预测器 — 实时 Gas 分析、Mempool 监控与交易追踪

Real-time on-chain settlement prediction, mempool analysis, and transaction
tracking for EVM-compatible chains. No API keys required for basic functions.

---

## 中文说明

### 功能特性

| 工具 | 功能 |
|------|------|
| `get-gas-prediction` | 实时获取各档位 Gas（instant/fast/standard/slow）及网络拥堵度 |
| `predict-settlement` | 根据给定 Gas 价格预测交易结算时间与包含概率 |
| `get-optimal-window` | 分析 24 小时 Gas 规律，找到最优交易窗口 |
| `analyze-pending-pool` | 扫描 Mempool 中的待处理交易，检测三明治攻击与 DEX 冲突风险 |
| `track-tx` | 追踪已提交的交易，等待上链确认或失败回执 |
| `verify-contract` | Etherscan API 验证合约源码 + 安全风险扫描（需 Key）|
| `get-token-info` | 获取代币元数据（名称、符号、总供应量、精度）（需 Key）|
| `get-internal-txs` | 获取交易内部调用追踪（Etherscan API）（需 Key）|
| `btc-fee-estimate` | BTC 实时费率（sat/vB）+ Mempool 拥堵度，无需 API Key |
| `btc-predict-settlement` | 预测给定 sat/vB 费率下的 BTC 交易确认时间和概率 |
| `btc-optimal-window` | 分析 UTC 小时规律，找到最便宜的 BTC 交易时段 |
| `track-btc-tx` | 追踪 BTC 交易状态（mempool.space）|
| `analyze-gas-trend` | EVM 链 Gas 趋势分析，判断涨跌通道 |
| `analyze-btc-trend` | BTC 手续费趋势分析，判断上涨/回落通道 |

### 支持链

| 链 | Chain ID | 费用单位 | API | Key |
|---|---|---|---|---|
| Ethereum | 1 | Gwei | Etherscan V2 | 可选 |
| Arbitrum | 42161 | Gwei | Arbiscan | 可选 |
| Optimism | 10 | Gwei | Optimism Etherscan | 可选 |
| Base | 8453 | Gwei | Basescan | 可选 |
| Polygon | 137 | Gwei | Polygonscan | 可选 |
| **Bitcoin** | 0 | **sat/vB** | mempool.space | **免费无需Key** |

### 安装

```bash
pip install web3>=6.0.0
python settlement_predictor.py --help
```

### API Key 配置（可选）

基础功能（Gas 预测、结算时间、Mempool 分析）**无需 Key**，开箱即用。

可选 Key（通过环境变量设置）：

| Key | 功能 | 免费申请 |
|-----|------|---------|
| `ETHERSCAN_API_KEY` | 合约验证、代币详情、失败原因解码、内部交易追踪 | https://etherscan.io/myapikey |
| `TENDERLY_API_KEY` | 交易模拟（精准 Gas + 回滚预测） | https://dashboard.tenderly.co/ |

```bash
export ETHERSCAN_API_KEY=你的API密钥
export TENDERLY_API_KEY=你的API密钥
```

### 使用示例

```bash
# 1. 查询当前 Gas 行情
python settlement_predictor.py get-gas-prediction -c ethereum

# 2. 预测结算时间
python settlement_predictor.py predict-settlement -c ethereum -g 30

# 3. 寻找最优交易窗口
python settlement_predictor.py get-optimal-window -c ethereum -u high

# 4. 分析 Mempool 风险（防范三明治攻击）
python settlement_predictor.py analyze-pending-pool \
  -c ethereum \
  -p 0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852 \
  -d buy -a 10000

# 5. 追踪交易状态（含 Etherscan 失败原因解码）
python settlement_predictor.py track-tx \
  -c ethereum \
  -t 0xabc123...

# 6. 合约安全验证（源码 + 风险扫描）🔥
python settlement_predictor.py verify-contract \
  -c ethereum \
  -a 0xdAC17F958D2ee523a2206206994597C13D831ec7

# 7. 代币信息查询（名称、符号、总供应量）🔥
python settlement_predictor.py get-token-info \
  -c ethereum \
  -a 0xdAC17F958D2ee523a2206206994597C13D831ec7

# 8. 交易内部调用追踪（需 Etherscan API Key）🔥
python settlement_predictor.py get-internal-txs \
  -c ethereum \
  -t 0xabc123...

# 9. BTC 费率查询
python settlement_predictor.py btc-fee-estimate --urgency medium

# 10. 预测 BTC 结算时间
python settlement_predictor.py btc-predict-settlement --sat 3 --urgency high

# 11. 最优 BTC 交易窗口
python settlement_predictor.py btc-optimal-window --urgency low

# 12. 追踪 BTC 交易
python settlement_predictor.py track-btc-tx \
  --tx 4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b

# 13. Gas 趋势分析（EVM 链）
python settlement_predictor.py analyze-gas-trend -c ethereum

# 14. BTC 手续费趋势分析
python settlement_predictor.py analyze-btc-trend
```

### API 参考

| 参数 | 说明 |
|------|------|
| `--chain, -c` | 链名：`ethereum`/`arbitrum`/`optimism`/`base`/`polygon` |
| `--gas-price, -g` | Gas 价格（Gwei，仅 predict-settlement）|
| `--urgency, -u` | 紧急度：`low`/`medium`/`high`（仅 optimal-window）|
| `--pool-address, -p` | Uniswap 池子地址（仅 analyze-pending-pool）|
| `--direction, -d` | 交易方向：`buy`/`sell`（仅 analyze-pending-pool）|
| `--amount-usd, -a` | 预估 USD 金额（仅 analyze-pending-pool）|
| `--tx-hash, -t` | 交易哈希（仅 track-tx / get-internal-txs）|
| `--address, -a` | 合约/代币地址（仅 verify-contract / get-token-info）|
| `--format, -f` | 输出格式：`json`（默认）/ `table` |

### 输出格式

使用 `--format json`（默认）或 `--format table`：

```bash
python settlement_predictor.py get-gas-prediction -c ethereum --format table
```

### MVP 局限性

| 限制 | 说明 |
|------|------|
| ⚠️ 公开 RPC 限速 | 高频调用可能触发限流，建议添加自己的 RPC API Key |
| ⚠️ 三明治检测为启发式 | 仅基于 Gas 价格和交易方向估算，非 100% 准确 |
| ⚠️ holder_count 需 Pro | Etherscan 免费版不支持 holder count，需 Pro 版 |
| ⚠️ 历史数据有限 | `get-optimal-window` 基于通用 UTC 模式，非链上真实历史 |
| ⚠️ L2 特殊机制 | 部分 L2 批量提交机制可能导致预测偏差 |

---

## English

### Features

| Tool | Description |
|------|-------------|
| `get-gas-prediction` | Live gas tiers (instant/fast/standard/slow) + network congestion |
| `predict-settlement` | Settlement time & inclusion probability at a given gas price |
| `get-optimal-window` | 24-hour gas pattern analysis → cheapest window finder |
| `analyze-pending-pool` | Mempool scanner for sandwich attacks & DEX conflicts |
| `track-tx` | Track submitted txs until confirmed or failed (Etherscan revert decoding) |
| `verify-contract` | Contract source verification + security risk scanning (Etherscan API) |
| `get-token-info` | Token metadata: name, symbol, supply, decimals (ERC-20 RPC) |
| `get-internal-txs` | Internal transaction trace for a tx hash (Etherscan API) |
| `btc-fee-estimate` | BTC live fee in sat/vB via mempool.space, no key required |
| `btc-predict-settlement` | Predict BTC confirmation time at given sat/vB fee |
| `btc-optimal-window` | UTC hourly pattern → cheapest BTC tx window |
| `track-btc-tx` | Track BTC tx status (mempool.space) |
| `analyze-gas-trend` | Rolling history + linear regression → rising/falling channel |
| `analyze-btc-trend` | BTC fee trend analysis → uptrend/downtrend channel |

### Supported Chains

Ethereum, Arbitrum, Optimism, Base, Polygon, Bitcoin

### Installation

```bash
pip install web3>=6.0.0
python settlement_predictor.py --help
```

### API Key Setup (Optional)

Core tools (Gas, Settlement, Mempool, Transaction Tracking) work **without any keys**.

| Key | Enables | Free Key |
|-----|--------|---------|
| `ETHERSCAN_API_KEY` | Contract verification, token metadata, revert decoding, internal txs | https://etherscan.io/myapikey |
| `TENDERLY_API_KEY` | Transaction simulation with accurate gas prediction | https://dashboard.tenderly.co/ |

```bash
export ETHERSCAN_API_KEY=your_key
export TENDERLY_API_KEY=your_key
```

### Usage Examples

```bash
# Gas tiers
python settlement_predictor.py get-gas-prediction -c ethereum

# Settlement prediction
python settlement_predictor.py predict-settlement -c ethereum -g 30

# Optimal window
python settlement_predictor.py get-optimal-window -c ethereum -u high

# Sandwich risk analysis
python settlement_predictor.py analyze-pending-pool \
  -c ethereum -p 0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852 -d buy -a 10000

# Track transaction with revert reason
python settlement_predictor.py track-tx -c ethereum -t 0xabc123...

# Verify contract security
python settlement_predictor.py verify-contract -c ethereum \
  -a 0xdAC17F958D2ee523a2206206994597C13D831ec7

# Token info
python settlement_predictor.py get-token-info -c ethereum \
  -a 0xdAC17F958D2ee523a2206206994597C13D831ec7

# Internal transactions
python settlement_predictor.py get-internal-txs -c ethereum -t 0xabc123...

# BTC fee estimate
python settlement_predictor.py btc-fee-estimate --urgency medium

# BTC settlement prediction
python settlement_predictor.py btc-predict-settlement --sat 3

# BTC optimal window
python settlement_predictor.py btc-optimal-window --urgency low

# BTC tx tracking
python settlement_predictor.py track-btc-tx \
  --tx 4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b

# EVM gas trend
python settlement_predictor.py analyze-gas-trend -c ethereum

# BTC fee trend
python settlement_predictor.py analyze-btc-trend

# Simulate tx (requires TENDERLY_API_KEY)
python settlement_predictor.py simulate-tx \
  -c ethereum -t 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D -v 0.01
```

### Output Format

`--format json` (default) or `--format table`.

### MVP Limitations

| Limitation | Details |
|------------|---------|
| ⚠️ Public RPC rate limits | Use your own RPC API key for high-frequency use |
| ⚠️ Sandwich detection is heuristic | Based on gas price & direction patterns only |
| ⚠️ holder_count requires Pro | Etherscan free tier doesn't support holder count |
| ⚠️ Hourly patterns are generalized | Not based on real on-chain history |
| ⚠️ L2 batch mechanics | Some L2s may have prediction variance |

## 项目结构

```
settlement-predictor/
├── SKILL.md                   # OpenClaw Skill 元数据
├── settlement_predictor.py    # 核心 Python 实现
├── README.md                  # 本文档
└── requirements.txt           # Python 依赖
```
