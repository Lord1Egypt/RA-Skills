---
name: trader-portfolio
description: Optimize portfolio allocation using npx neural-trader mean-variance engine with risk constraints and rebalancing plan
allowed-tools: Bash Read mcp__claude-flow__memory_store mcp__claude-flow__memory_retrieve mcp__claude-flow__memory_search mcp__claude-flow__neural_predict mcp__claude-flow__agentdb_pattern-search
argument-hint: "[--risk-target NUMBER]"
---
Optimize portfolio allocation using neural-trader's portfolio engine.

Steps:
1. Ensure neural-trader is available:
   `npm ls neural-trader 2>/dev/null || npm install --ignore-scripts neural-trader`
2. Load current portfolio:
   `mcp__claude-flow__memory_search({ query: "current portfolio holdings", namespace: "trading-portfolio" })`
3. Run portfolio optimization:
   ```bash
   npx neural-trader --portfolio optimize
   ```
   With risk target:
   ```bash
   npx neural-trader --portfolio optimize --risk-target <number>
   ```
4. Get risk metrics:
   ```bash
   npx neural-trader --risk assess --portfolio current
   npx neural-trader --var --portfolio current
   npx neural-trader --correlation --portfolio current --flag-threshold 0.8
   ```
5. Use SONA for expected return prediction:
   `mcp__claude-flow__neural_predict({ input: "expected returns for [HOLDINGS] given current regime" })`
6. Generate rebalancing plan:
   ```bash
   npx neural-trader --portfolio rebalance
   ```
   Output: trades needed, current vs target weights, estimated costs
7. Search for similar allocations in history:
   `mcp__claude-flow__agentdb_pattern-search({ query: "optimized portfolio Sharpe > 1", namespace: "trading-portfolio" })`
8. Store optimized allocation:
   `mcp__claude-flow__memory_store({ key: "portfolio-optimal-TIMESTAMP", value: "ALLOCATION_JSON", namespace: "trading-portfolio" })`
