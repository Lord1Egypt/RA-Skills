# Metrics Reference (v1)

## Scope

This skill outputs a **heuristic US stock radar snapshot** from public endpoints. It is optimized for transparent screening and repeatable triage, not full fundamental modeling.

## Modes

- `screener`: rank a list of tickers by heuristic signal score
- `deep-dive`: inspect one ticker in more detail
- `watchlist`: identify alert candidates from a custom list

## Core Metrics

- **PE / forward PE / PB**
  - Rough valuation context only.
- **RSI14**
  - Momentum / stretch proxy.
- **MA20 / MA50**
  - Trend context.
- **Volume spike vs 20d average**
  - Participation / attention proxy.
- **Revenue growth**
  - Basic growth quality check.
- **ROE**
  - Basic profitability quality check.
- **Debt to equity / margins**
  - Optional context fields when available.

## Grade Heuristic

Score combines simple, inspectable checks:
- reasonable PE range
- RSI in healthy zone
- volume expansion
- price above MA50
- positive revenue growth
- healthy ROE

Grade mapping:
- A: score >= 5
- B: score = 4
- C: score = 2-3
- D: score <= 1

Interpretation:
- **A/B**: stronger alignment of conditions
- **C**: mixed setup
- **D**: weak or incomplete setup

## Event Modes

### Normal mode
Balanced thresholds for routine scanning.

### High-alert mode
Use during macro/event windows when you want stricter / more selective screening.

Typical changes:
- PE ceiling tighter
- RSI acceptable range narrower
- emphasis on cleaner trend / risk posture

## Confidence

Confidence score (0-100) should reflect:
- how many tickers returned usable data
- whether quote / chart / summary endpoints were available
- how complete fundamentals are for the requested mode

Incomplete fields should surface via:
- `availability`
- `data_gaps`
- `degraded_mode`

## Limitations

- Free endpoints may be rate-limited, delayed, or partially populated.
- This is a signal triage framework, not investment advice.
- Missing fundamentals are common on some sources and should not be over-interpreted.
