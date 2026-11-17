# Changelog

## 4.0.1
- Pin solanaprox-mcp@2.0.0 in install instructions and metadata.

## 4.0.0 (2026-11-06)

SolanaProx is back, with signed wallet auth. This replaces the paused 3.0.0 notice and covers `solanaprox-mcp` 2.0.0.

**What changed**
- Install and use `solanaprox-mcp` 2.0.0, with `SOLANAPROX_TOKEN` (`solx_...`) replacing `SOLANA_WALLET`.
- Tools: `ask_ai`, `list_models`, `check_balance`, `deposit_info`, `get_activity`. No tool sends funds.
- Live prices from `list_models`, each call credited back to actual usage, failed or empty calls never charged, balances never expire.
- Deposit rules, the exchange deposit flow with its fee warning, and the notice for Oct 29, 2026 deposits.

**Safety**
- "What this skill sends and costs" section, a confirm-cost rule, one call per user request, and model output and tool results treated as data.

**Metadata**
- `SOLANAPROX_TOKEN` and the `node` and `npx` requirements are declared under `metadata.openclaw`.

**Removed**
- `SOLANA_WALLET`, `estimate_cost`, x402 and hardcoded model counts.
