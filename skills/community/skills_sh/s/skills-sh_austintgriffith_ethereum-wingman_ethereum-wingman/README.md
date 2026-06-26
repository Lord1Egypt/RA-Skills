# Ethereum Wingman

A comprehensive Ethereum development skill for AI coding agents. Provides security warnings, DeFi protocol guidance, and the critical gotchas that prevent costly mistakes.

## Installation

### For Cursor Users

**Important:** Open your project in Cursor **first**, then run the install command.

```bash
# 1. Open your project folder in Cursor
# 2. Then run in the terminal:
npx skills add austintgriffith/ethereum-wingman
```

> **Why this order?** Cursor indexes skills when the project opens. Installing before Cursor is open may not be detected until you reload.

### For Other Agents (Claude Code, Codex, etc.)

```bash
npx skills add austintgriffith/ethereum-wingman
```

## What It Does

This skill enhances AI agents with deep knowledge of:

- **SpeedRun Ethereum Challenges** - Hands-on learning curriculum
- **Scaffold-ETH 2 Tooling** - Full-stack dApp development
- **DeFi Protocol Integration** - Uniswap, Aave, Chainlink patterns
- **Security Best Practices** - Critical gotchas and historical hacks

## The Most Important Concept

**🚨 NOTHING IS AUTOMATIC ON ETHEREUM 🚨**

Smart contracts cannot execute themselves. For any function that "needs to happen":

1. Make it callable by **ANYONE**
2. Give callers a **REASON** (profit, reward)
3. Make the incentive **SUFFICIENT**

**Always ask: "Who calls this function? Why would they pay gas?"**

## Critical Gotchas

1. **Token Decimals** - USDC has 6 decimals, not 18!
2. **Approve Pattern** - Required for ERC-20 token transfers
3. **Reentrancy** - Use CEI pattern + ReentrancyGuard
4. **Oracle Security** - Never use DEX spot prices
5. **No Floats** - Use basis points (500 = 5%)
6. **Vault Inflation** - Protect first depositors

## Trigger Phrases

The skill activates when you mention:
- "build a dApp"
- "create smart contract"
- "help with Solidity"
- "SpeedRun Ethereum"
- Any Ethereum/DeFi development task

## Scripts

### Initialize Project
```bash
bash scripts/init-project.sh my-dapp base
```

### Check for Gotchas
```bash
bash scripts/check-gotchas.sh ./contracts
```

## MCP Integration

For the full experience with eth-mcp tools:
- Project scaffolding: `stack_init`, `stack_start`
- Address lookup: `addresses_getToken`, `addresses_getProtocol`
- DeFi data: `defi_getYields`, `defi_compareYields`
- Education: `education_getChecklist`, `education_getCriticalLessons`

## Resources

- [SpeedRun Ethereum](https://speedrunethereum.com/)
- [Scaffold-ETH 2](https://scaffoldeth.io/)
- [BuidlGuidl](https://buidlguidl.com/)

## License

MIT License - Use freely for learning and building.
