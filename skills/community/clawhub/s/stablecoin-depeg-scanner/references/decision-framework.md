# Depeg Assessment Decision Framework

## Core Principle

Stablecoin depeg = panic pricing. The key question is NOT "is it safe?" but "is the discount larger than the real loss?"

## Decision Matrix

### Factor 1: Collateral Status (Weight: 50%)

| TVL Status | Meaning | Action |
|-----------|---------|--------|
| INTACT (<20% drop) | Collateral still in contracts, exploit was logic/mint bug | Strong buy signal |
| PARTIAL (20-50% drop) | Some collateral stolen, but majority remains | Moderate buy signal |
| DRAINED (>50% drop) | Most collateral gone | Avoid |

### Factor 2: Exploit Type (Weight: 30%)

| Type | Recovery Probability | Examples |
|------|---------------------|----------|
| Mint/Logic exploit | HIGH - fix code, burn illegal tokens | USR (2026), Euler (2023) |
| Oracle manipulation | MEDIUM - fix oracle, may need to cover gap | Various |
| Collateral theft | LOW-MEDIUM - depends on team treasury | Wormhole (covered by Jump) |
| Algorithm collapse | ZERO - fundamental design failure | UST/Luna (2022) |
| Rug pull | ZERO | Do not touch |

### Factor 3: Odds Ratio (Weight: 20%)

| Current Price | Peg Target | Odds | Risk/Reward |
|--------------|-----------|------|-------------|
| $0.10 | $1.00 | 10x | Exceptional |
| $0.20 | $1.00 | 5x | Very good |
| $0.33 | $1.00 | 3x | Good |
| $0.50 | $1.00 | 2x | Moderate |
| $0.80 | $1.00 | 1.25x | Low, needs high confidence |

## Position Sizing

Based on total available capital:

| Odds | Position % | Rationale |
|------|-----------|-----------|
| 8x+ | 5-6% | High reward justifies larger bet |
| 5-8x | 3-4% | Good risk/reward |
| 3-5x | 2-3% | Conservative but worthwhile |
| 2-3x | 1-2% | Only if very high confidence |

**Golden rule: Never risk more than you can lose without affecting your trading.**

## Recovery Benchmarks

Historical stablecoin depeg recoveries:

| Coin | Depeg Low | Final Recovery | Time | Outcome |
|------|----------|---------------|------|---------|
| USDC (SVB crisis 2023) | $0.87 | $1.00 | 3 days | Full recovery |
| DAI (Black Thursday 2020) | $0.95 | $1.00 | 1 week | Full recovery |
| USDN (2022) | $0.75 | $0.50 | Months | Partial, eventually wound down |
| UST (2022) | $0.10 | $0.00 | Never | Total loss |
| Euler (2023) | N/A | Full | 3 weeks | Hacker returned funds |
| USR (2026) | $0.12 | $0.60+ | Hours | Recovering (ongoing) |

## Red Flags (DO NOT BUY)

1. Algorithmic stablecoin with no real collateral
2. Team social media accounts deleted/silent for >6 hours
3. TVL dropped >90%
4. Multiple exploits in same protocol within 30 days
5. Protocol never had audit from reputable firm
6. Token has <$1M market cap pre-exploit

## Green Flags (LEAN TOWARD BUY)

1. Over-collateralized with ETH/BTC/real assets
2. Team responded within 1 hour, paused protocol
3. Security firm (PeckShield/CertiK/SlowMist) identified the specific bug
4. TVL drop <20%
5. Prior audit from reputable firm exists
6. Similar past incidents recovered (check benchmarks)
