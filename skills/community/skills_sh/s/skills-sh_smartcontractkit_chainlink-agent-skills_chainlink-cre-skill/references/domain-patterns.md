# Domain Patterns

Use this file when a prompt combines CRE with domain-specific product logic such as prediction markets, token-pool rebalancing, arbitrage monitoring, supply-chain DvP, or RWA lending.

## Trigger Conditions

- "Build a prediction market with CRE"
- "Use CRE to monitor arbitrage opportunities"
- "Create a token-pool rebalancing agent"
- "Use Chainlink workflows for DvP or RWA lending"

Do not use this file for generic CRE workflow mechanics, CLI usage, or SDK API lookup. Load the relevant CRE capability reference after identifying the domain shape.

## Product-First Rule

For broad product or platform prompts, preserve the user's domain architecture first. CRE is usually one layer:

- monitoring and verification
- scheduled or event-driven automation
- consensus over external data
- report generation or controlled writes
- operator alerts and review queues

Do not make CRE the whole architecture unless the user explicitly asks for a CRE workflow, deployability in CRE, or decentralized execution.

## Prediction Markets

For up/down or interval markets, protect the market lifecycle before adding CRE automation.

### Required Lifecycle

1. Create market with an asset, interval, entry deadline, opening price time, close time, and settlement rules.
2. Accept positions only before the entry deadline.
3. Fix the opening price after entries close.
4. Reject all new bets after the opening price is fixed.
5. Resolve from a closing price after the interval ends.
6. Enforce staleness bounds, market-hours handling for RWA assets, cancellation/refund paths, and a dispute or admin recovery path.

Never generate a contract that lets users bet after the opening price is known.

### CRE Fit

CRE can resolve markets by reading Chainlink feeds, fetching approved external data where needed, checking stale data, and submitting a signed report to a settlement contract. Keep the contract lifecycle and backend/indexer responsibilities visible when the user asks for smart contracts and a backend, not only the workflow.

## Rebalancing And Arbitrage

Separate recommendation from execution unless the user explicitly asks for automated execution and has defined risk controls.

- Model balances, costs, slippage, liquidity depth, bridge/CEX limits, and urgency with scaled integers.
- Treat CEX custody, bridge signing, and privileged fund movement as external systems with approval, rate limits, and reconciliation.
- Use CRE for monitoring, scoring, dry-run recommendations, alerting, signed reports, or guarded onchain calls.
- For arbitrage, start with dry-run quote analysis and human approval. Add execution only after limits, compliance, custody, and failure handling are explicit.

## RWA, DvP, And Lending

CRE can verify events, refresh valuations, produce reports, and trigger settlement milestones, but it does not replace legal agreements, identity checks, custody design, servicing operations, or market-specific valuation processes.

- Keep offchain verification, appraisal, servicing, and dispute workflows explicit.
- Do not invent property-specific Chainlink feeds. Use existing feeds only where they exist, and otherwise model valuation as an approved oracle/process boundary.
- Treat compliance, privacy, and access control as first-class product requirements.
