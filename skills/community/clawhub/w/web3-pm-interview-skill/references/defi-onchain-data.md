# DeFi And On-chain Data PM

## What Interviewers Test

- Protocol mechanics
- On-chain data literacy
- Ability to define data models and metrics
- Risk awareness
- Protocol integration prioritization
- Cross-team platform thinking

## DeFi Must Know

- AMM and concentrated liquidity
- Lending, collateral, liquidation, health factor
- Staking, LST, LRT, restaking
- Vaults and ERC-4626 basics
- APR vs APY
- Impermanent loss
- Rebase vs exchange-rate assets
- TVL, volume, users, positions, PnL

## On-chain Data Must Know

- Transaction, receipt, event log
- Contract call and ABI
- `eth_call`, `eth_getLogs`, transaction receipt
- Transfer, Swap, Deposit, Borrow, Liquidation events
- Indexing, subgraphs, data pipeline
- Reorg and missing block handling
- Data SLA and accuracy monitoring

## Protocol Integration Framework

Evaluate:

1. User demand
2. TVL and usage
3. Risk and audit status
4. Technical complexity
5. Data availability
6. Strategic value
7. Maintenance cost

Prioritize:

- High user demand + high protocol quality: integrate.
- High demand + high risk: read-only or warning-first.
- Strategic but low demand: roadmap, not sprint.
- Low value + high complexity: skip.

## Data Quality Framework

1. Source quality: official contracts, SDKs, subgraphs, nodes, third-party APIs.
2. Definition quality: metric dictionary, cross-protocol normalization.
3. Monitoring: delay, outliers, coverage, failure rate.
4. User feedback: reports, support tickets, abnormal behavior.
5. Manual audit: compare UI values with on-chain truth.

## Senior-Level Requirement

Ideas must include an execution path:

- What data fields are needed?
- Which are on-chain?
- Which require third parties?
- How does it change ranking, risk, or UX?
- What is the MVP?
- How will it improve conversion, retention, TVL, or risk control?

