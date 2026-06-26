# xflows-bridge Skill

A Claude Code skill that enables Claude to perform cross-chain bridge operations using the [xflows CLI](https://github.com/wandevs/xflows-cli).

## What It Does

When this skill is active, Claude can autonomously:

- Create and manage EVM wallets (with optional encryption)
- Query supported chains, tokens, pairs, bridges, and DEXes
- Get cross-chain swap quotes with fee estimates
- Build, sign, and send cross-chain transactions
- Track transaction status until completion

All operations are executed as single CLI commands, making them fully compatible with AI agent workflows.

## When It Triggers

Claude will automatically use this skill when you mention:

- Cross-chain transfers or bridging tokens
- Swapping tokens between different EVM chains
- Wanchain, WanBridge, QUiX
- Moving ETH, BNB, USDC, or other tokens between chains like Ethereum, BSC, Polygon, Arbitrum, etc.

## Prerequisite

The `xflows` CLI must be installed globally:

```bash
npm install -g xflows
```

## Skill Structure

```
xflows-bridge/
├── SKILL.md                 # Core instructions, workflow, and quick reference
└── references/
    └── commands.md           # Complete command reference with all flags
```

## Example Prompts

- "Help me bridge 0.1 ETH from Ethereum to BSC"
- "Create a wallet and check my WAN balance on Wanchain"
- "What tokens can I bridge from Polygon to Arbitrum?"
- "Get a quote for swapping USDC from Ethereum to BSC"
- "Track my cross-chain transaction 0x..."
