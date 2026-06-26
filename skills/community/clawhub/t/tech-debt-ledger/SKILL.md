---
name: tech-debt-ledger
version: 1.0.0
description: >
  Tracks technical debt as actual financial debt — with principal, interest
  rates, minimum payments, and compound growth. Turns vague "we should fix
  that someday" into quantified obligations with real costs, maturity dates,
  and payoff strategies. Because debt you can't measure is debt you'll
  never pay.
author: J. DeVere Cooley
category: everyday-tools
tags:
  - tech-debt
  - estimation
  - planning
  - project-health
metadata:
  openclaw:
    emoji: "📒"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - everyday
      - planning
---

# Tech Debt Ledger

> "Technical debt is like financial debt. It's fine to take on debt to move faster — as long as you know the interest rate, track the balance, and have a payoff plan. The problem is, most teams have a pile of IOUs they can't even read."

## What It Does

Your codebase has technical debt. Everyone knows this. Nobody knows *how much*, what it *costs*, or when it becomes *unsustainable*.

Tech Debt Ledger applies **double-entry bookkeeping** to technical debt. Every shortcut, workaround, and "we'll fix it later" becomes a ledger entry with:

- **Principal**: The cost to fix it today
- **Interest rate**: How fast the cost grows if you don't fix it
- **Interest type**: Does it compound (gets exponentially worse) or accrue linearly?
- **Minimum payment**: The maintenance cost to keep it from breaking
- **Maturity date**: When it becomes a crisis if not addressed

## The Financial Model

### Debt Instruments

Not all tech debt is the same. Different types carry different interest rates:

| Debt Type | Principal | Interest Rate | Interest Type | Example |
|---|---|---|---|---|
| **Prudent-Deliberate** | Known, planned | Low (2-5%) | Simple | "Ship with manual deploy; automate later" |
| **Prudent-Inadvertent** | Discovered later | Medium (5-15%) | Simple | "Now we know we should have used X pattern" |
| **Reckless-Deliberate** | Known, ignored | High (15-30%) | Compound | "We don't have time for tests" |
| **Reckless-Inadvertent** | Unknown until crisis | Very High (30%+) | Compound | "What do you mean there's no input validation?" |

### The Debt Equation

```
CURRENT COST = Principal + Accumulated Interest

Where:
  Simple interest:   Accumulated = Principal × Rate × Time
  Compound interest: Accumulated = Principal × (1 + Rate)^Time - Principal

TOTAL DEBT BURDEN = Σ(Current Cost of all entries)

DEBT SERVICE RATIO = Monthly interest payments / Monthly development capacity
  < 0.15  →  Healthy
  0.15-0.30 → Manageable (prioritize payoff)
  0.30-0.50 → Stressed (debt is slowing you down)
  > 0.50   → Crisis (most work is fighting debt, not building features)
```

## Ledger Entry Structure

Each debt entry is a complete financial instrument:

```
╔══════════════════════════════════════════════════════════════╗
║  DEBT ENTRY: #TD-2025-047                                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  DESCRIPTION: No integration tests for payment flow          ║
║  LOCATION: src/payments/*, src/checkout/*                    ║
║  CATEGORY: Reckless-Deliberate                               ║
║  INCURRED: 2025-01-15 (Sprint 42, "launch deadline")        ║
║                                                              ║
║  PRINCIPAL:          16 dev-hours to write comprehensive     ║
║                      integration test suite                  ║
║                                                              ║
║  INTEREST RATE:      20% per quarter (compound)              ║
║  INTEREST TYPE:      Compound — untested code attracts more  ║
║                      untested code; complexity grows          ║
║                                                              ║
║  CURRENT BALANCE:    23.1 dev-hours (7.1h interest accrued)  ║
║                                                              ║
║  MINIMUM PAYMENT:    2 dev-hours/month                       ║
║                      (manual testing each deploy,            ║
║                       investigating payment bugs)            ║
║                                                              ║
║  MATURITY DATE:      2025-07-01 (EU compliance audit)        ║
║  MATURITY PENALTY:   Compliance failure, potential fine       ║
║                                                              ║
║  INTEREST EXPLANATION:                                       ║
║  Every month without tests, the payment code changes.        ║
║  Each change makes the eventual test suite harder to write.  ║
║  Developers avoid refactoring because there's no safety net. ║
║  Bad patterns calcify. The 16-hour fix today becomes a       ║
║  40-hour fix in 6 months.                                    ║
╚══════════════════════════════════════════════════════════════╝
```

## Debt Classification System

### By Severity

| Rating | Debt-to-Capacity Ratio | Translation |
|---|---|---|
| **AAA** | < 5% | Minimal debt, healthy codebase |
| **AA** | 5-10% | Low debt, well-managed |
| **A** | 10-20% | Moderate debt, payoff plan needed |
| **BBB** | 20-30% | Significant debt, slowing development |
| **BB** | 30-40% | High debt, feature velocity declining |
| **B** | 40-50% | Severe debt, most work is maintenance |
| **CCC** | 50-70% | Distressed, rewrite being discussed |
| **D** | > 70% | Default, codebase is effectively unmaintainable |

### By Location

```
DEBT HEATMAP:
├── src/payments/    ████████████████████  42h (36% of total debt)
├── src/auth/        ████████████          24h (21%)
├── src/checkout/    ████████              18h (15%)
├── src/api/         ██████                14h (12%)
├── src/utils/       ████                  9h (8%)
└── src/ui/          ████                  9h (8%)
                                    Total: 116 dev-hours
```

## The Ledger Operations

### 1. Debt Audit (Discovery)

```
AUTOMATED DISCOVERY:
├── TODO/FIXME/HACK/WORKAROUND comments → convert to ledger entries
├── Code complexity hotspots → potential structural debt
├── Test coverage gaps → testing debt
├── Outdated dependencies → maintenance debt
├── Copy-pasted code → duplication debt
├── Dead code / unused exports → cleanliness debt
├── Missing error handling → reliability debt
└── Hardcoded values → configuration debt

MANUAL DISCOVERY:
├── "We know this is wrong but..." decisions
├── Shortcuts taken for deadlines
├── Deferred refactoring
├── Missing documentation
└── Known security gaps
```

### 2. Debt Valuation (Principal Estimation)

```
FOR EACH ITEM:
├── Estimate fix time (optimistic, realistic, pessimistic)
│   └── Principal = realistic estimate
├── Estimate interest rate:
│   ├── Does this area change frequently? (high change = high interest)
│   ├── Do bugs cluster here? (high bugs = high interest)
│   ├── Does this block other work? (blocking = high interest)
│   └── Does this have a deadline? (deadline = maturity date)
├── Classify interest type:
│   ├── Simple: cost grows linearly (tech stays the same)
│   └── Compound: cost grows exponentially (complexity breeds complexity)
└── Set minimum payment: ongoing maintenance cost to keep it alive
```

### 3. Payoff Strategies

| Strategy | Description | Best For |
|---|---|---|
| **Avalanche** | Pay highest interest rate first | Maximum long-term savings |
| **Snowball** | Pay smallest principal first | Quick wins, team morale |
| **Targeted** | Pay debts blocking specific goals | Deadline-driven projects |
| **Minimum** | Pay only minimum payments | When feature work is critical |
| **Refinance** | Replace expensive debt with cheaper debt (e.g., swap hack with simpler hack) | When full fix isn't feasible |

### 4. Debt Budget

```
QUARTERLY DEBT BUDGET:
├── Total development capacity: 480 dev-hours
├── Feature work allocation: 384 dev-hours (80%)
├── Debt payoff allocation: 96 dev-hours (20%)
│
├── PAYOFF PLAN (Avalanche strategy):
│   ├── #TD-2025-047: Payment tests (16h principal, 20% interest) → PAY IN FULL
│   ├── #TD-2025-023: Auth refactor (24h principal, 15% interest) → PAY IN FULL
│   ├── #TD-2025-031: API versioning (18h principal, 10% interest) → PAY IN FULL
│   └── #TD-2024-089: Legacy utils (38h principal, 8% interest) → PARTIAL (38h remaining)
│
├── PROJECTED BALANCE AFTER QUARTER:
│   ├── Before: 116 dev-hours
│   ├── Paid off: 58 dev-hours
│   ├── New interest on remaining: 4.2 dev-hours
│   └── After: 62.2 dev-hours
│
└── DEBT RATING CHANGE: BBB → A (improvement)
```

## Output Format

```
╔══════════════════════════════════════════════════════════════╗
║                   TECH DEBT LEDGER                          ║
║              Balance Sheet — Q1 2025                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  TOTAL DEBT BALANCE: 116 dev-hours                           ║
║  DEBT RATING: BBB (Significant)                              ║
║  DEBT SERVICE RATIO: 0.23 (Manageable)                       ║
║  MONTHLY INTEREST ACCRUAL: 8.4 dev-hours                     ║
║  MONTHLY MINIMUM PAYMENT: 12 dev-hours                       ║
║                                                              ║
║  TOP 5 DEBTS BY INTEREST COST:                               ║
║  #  | Description              | Balance | Rate | Monthly $  ║
║  ───┼──────────────────────────┼─────────┼──────┼──────────  ║
║  1  | No payment tests         | 23.1h   | 20%  | 1.5h/mo   ║
║  2  | Auth module no types     | 28.8h   | 15%  | 1.1h/mo   ║
║  3  | Hardcoded config values  | 12.0h   | 12%  | 0.5h/mo   ║
║  4  | No API versioning        | 21.6h   | 10%  | 0.7h/mo   ║
║  5  | Legacy utility functions | 42.0h   | 8%   | 1.1h/mo   ║
║                                                              ║
║  TREND:                                                      ║
║  ├── Last quarter: 94h → This quarter: 116h (+23%)           ║
║  ├── New debt incurred: 31h                                   ║
║  ├── Debt paid off: 17h                                       ║
║  └── Interest accrued: 8.4h                                   ║
║                                                              ║
║  ⚠ ALERT: Debt is growing faster than payoff.                ║
║  At current rate, balance reaches 180h in 6 months.          ║
║  Recommend: Increase payoff allocation from 15% to 25%.      ║
╚══════════════════════════════════════════════════════════════╝
```

## When to Invoke

- **Sprint planning** — allocate debt payoff hours alongside feature work
- **When taking on new debt** — log it immediately so it's not forgotten
- **Quarterly reviews** — assess debt health, adjust payoff strategy
- **Before rewrite discussions** — quantify whether a rewrite makes financial sense
- **When velocity is declining** — check if debt service is consuming capacity

## Why It Matters

Teams that track tech debt as a vague "we should fix that" never fix it. Teams that track it as **quantified financial obligations** make rational decisions about when to pay, how much to pay, and which debts to accept.

The goal isn't zero debt. The goal is **informed debt** — knowing exactly what you owe, what it costs, and having a plan.

Zero external dependencies. Zero API calls. Pure estimation and tracking.
