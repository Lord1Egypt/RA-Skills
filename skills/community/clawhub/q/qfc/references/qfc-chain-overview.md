# QFC Chain Overview

## What is QFC?

QFC (Quantum-Flux Chain) is a Layer 1 blockchain that combines traditional staking with AI compute contributions. Validators earn rewards through both staking and running AI inference tasks.

## Consensus: Proof of Contribution (PoC)

Unlike pure Proof-of-Stake, QFC uses a multi-dimensional scoring system:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Staking | 30% | Amount of QFC staked |
| Compute | 20% | AI inference tasks completed |
| Uptime | 15% | Node availability |
| Accuracy | 15% | Inference verification pass rate |
| Network | 10% | Bandwidth, latency |
| Storage | 5% | Data availability |
| Reputation | 5% | Historical reliability |

## Chain IDs

| Network | Chain ID | Status |
|---------|----------|--------|
| Testnet | 9000 | Active |
| Mainnet | 9001 | Planned |
| Localhost | 9000 | Development |

## Token: QFC

- **Symbol**: QFC
- **Decimals**: 18
- **Min Stake**: 10,000 QFC
- **Min Delegation**: 100 QFC
- **Unstake Delay**: 7 days

## AI Compute (v2.0)

Validators can contribute GPU compute for AI inference tasks:
- **GPU Tiers**: Hot (24GB+), Warm (8-16GB), Cold (CPU/low GPU)
- **Approved Models**: qfc-embed-small, qfc-embed-medium, qfc-classify-small
- **Verification**: 5% spot-check re-execution of random proofs
- **Backends**: CUDA, Metal, CPU

## RPC Endpoints

### Standard (Ethereum-compatible)
- `eth_getBalance`, `eth_sendRawTransaction`, `eth_getBlockByNumber`, etc.

### QFC-specific
- `qfc_getValidators` — List active validators
- `qfc_getEpoch` — Current epoch info
- `qfc_getInferenceStats` — AI inference statistics
- `qfc_getSupportedModels` — Approved model list
