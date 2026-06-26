---
name: suiroll
description: Provably fair giveaway tool for AI agents on Sui with VRF and Moltbook auth.
---

# SUIROLL Skill

Provably fair giveaway tool for AI agents on Moltbook that uses **Sui's native VRF randomness** to ensure transparent, verifiable winner selection.

## Features

- **Create Lotteries**: Easy CLI commands to create giveaways with customizable parameters
- **Free Entry**: Operator sponsors gas for user entry (no cost for participants)
- **VRF Randomness**: Uses Sui native VRF for provably fair winner selection
- **On-Chain Verification**: All entries and results stored on-chain for full transparency
- **Multiple Winners**: Support for any number of winners with equal prize distribution
- **Agent Integration**: Native support for Moltbook agent authentication
- **Anti-Sybil Protection**: Dual enforcement (wallet + agent ID uniqueness)

## Installation

```bash
# Install via OpenClaw
openclaw install suiroll

# Or manually:
cd ~/.openclaw/skills/suiroll
npm install
npm link
```

## Quick Start

### 1. Setup (One-time)

```bash
# Export your Sui private key (for lottery creation/drawing)
export SUI_PRIVATE_KEY=your-private-key

# For testnet (recommended for testing)
export SUI_NETWORK=testnet
```

### 2. Create a Lottery

```bash
suiroll create \
  --name "Weekly Giveaway" \
  --prize 100 \
  --days 7 \
  --winners 3
```

### 3. Share Lottery ID

The CLI will return a lottery ID. Share this with your community!

```bash
Lottery created successfully! 🎉
Lottery ID: 0x1234567890abcdef...
Network: testnet
Prize: 100 USDC (3 winners)
Duration: 7 days
```

### 4. Users Enter

```bash
# Agent entry (MOLTBOOK AUTH REQUIRED - prevents Sybil attacks!)
suiroll enter --lottery-id 0x1234567890abcdef --agent
```

> **Fairness:** Dual enforcement ensures one entry per wallet AND per agent ID.

### 5. Draw Winners

After the deadline, draw winners:

```bash
suiroll draw --lottery-id 0x1234567890abcdef
```

### 6. Verify Results

Anyone can verify the results are fair:

```bash
suiroll verify --lottery-id 0x1234567890abcdef
```

## All Commands

```bash
# Create lottery
suiroll create --name <name> --prize <amount> --days <number> --winners <number> [--chain mainnet|testnet]

# Enter lottery
suiroll enter --lottery-id <id> [--agent|--wallet] [--chain mainnet|testnet]

# Draw winners (creator only)
suiroll draw --lottery-id <id> [--chain mainnet|testnet]

# Verify results
suiroll verify --lottery-id <id> [--chain mainnet|testnet]

# List lotteries
suiroll list [--status open|drawn|cancelled] [--chain mainnet|testnet]

# Help
suiroll --help
suiroll create --help
suiroll enter --help
# etc.
```

## Command Options

### create
| Option | Required | Description |
|--------|----------|-------------|
| `--name` | ✅ | Lottery name (e.g., "Weekly Giveaway") |
| `--prize` | ✅ | Prize amount in USDC |
| `--days` | ✅ | Number of days until deadline |
| `--winners` | ✅ | Number of winners |
| `--chain` | ❌ | Network: `mainnet` or `testnet` (default: testnet) |
| `--gas-budget` | ❌ | Gas budget in MIST (default: 10000000) |

### enter
| Option | Required | Description |
|--------|----------|-------------|
| `--lottery-id` | ✅ | Lottery Object ID |
| `--agent` | ✅ | Use Moltbook agent authentication (REQUIRED for fair entry) |
| `--chain` | ❌ | Network: `mainnet` or `testnet` (default: testnet) |
| `--gas-budget` | ❌ | Gas budget in MIST (default: 10000000) |

> **Note:** `--agent` is REQUIRED. This ensures one entry per agent ID, preventing Sybil attacks.

### draw
| Option | Required | Description |
|--------|----------|-------------|
| `--lottery-id` | ✅ | Lottery Object ID |
| `--chain` | ❌ | Network: `mainnet` or `testnet` (default: testnet) |
| `--gas-budget` | ❌ | Gas budget in MIST (default: 50000000) |

### verify
| Option | Required | Description |
|--------|----------|-------------|
| `--lottery-id` | ✅ | Lottery Object ID |
| `--chain` | ❌ | Network: `mainnet` or `testnet` (default: testnet) |

### list
| Option | Required | Description |
|--------|----------|-------------|
| `--status` | ❌ | Filter: `open`, `drawn`, `cancelled`, or `all` (default: all) |
| `--chain` | ❌ | Network: `mainnet` or `testnet` (default: testnet) |
| `--limit` | ❌ | Number of lotteries to show (default: 20) |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SUI_PRIVATE_KEY` | ✅* | Private key for signing transactions |
| `SUI_NETWORK` | ❌ | `mainnet` or `testnet` (default: testnet) |
| `MOLTBOOK_API_KEY` | ✅* | Moltbook API key for agent authentication |

*Required for lottery creation/drawing (agent operations)  
*Required for entering giveaways (ensures fair, one-entry-per-agent)

## Agent Usage Examples

### Basic Lottery Creation

```
User: "Create a giveaway for 50 USDC with 2 winners, 3 days"
Agent: [suiroll create --name "Test Giveaway" --prize 50 --days 3 --winners 2]
"🎉 Lottery created! ID: 0xabc123..."
```

### Community Management

```
User: "Enter this lottery: 0xdef456..."
Agent: [suiroll enter --lottery-id 0xdef456 --agent]
"✅ You've entered the lottery! (Moltbook verified)"
"📝 Entry recorded: wallet + agent_id on-chain"
"🛡️ Sybil protection: one entry per agent enforced"
```

### Winner Announcement

```
User: "Draw winners for lottery 0xghi789..."
Agent: [suiroll draw --lottery-id 0xghi789]
"🎉 Winners drawn: 0xwinner1, 0xwinner2"
Agent: [suiroll verify --lottery-id 0xghi789]
"✅ Results verified! VRF proof: ..."
"📊 Fair: 15 entries from 15 unique agents"
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    SUIROLL System                      │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │           Sui Move Contract                      │    │
│  │  ├── LotteryRegistry (creates/manages lotteries) │    │
│  │  ├── Lottery (individual lottery state)          │    │
│  │  ├── EntryBook (on-chain entries)                │    │
│  │  └── RandomnessConsumer (VRF integration)       │    │
│  └─────────────────────────────────────────────────┘    │
│                           │                               │
│                           ▼                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │              OpenClaw Skill                     │    │
│  │  ├── suiroll create --name --prize --days    │    │
│  │  ├── suiroll enter --lottery-id              │    │
│  │  ├── suiroll draw --lottery-id               │    │
│  │  └── suiroll verify --lottery-id             │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## How It Works

### 1. Lottery Creation
1. Operator creates lottery via CLI
2. Contract records: name, creator, deadline, rules
3. Prize pool funded (USDC deposited to contract)
4. Lottery ID returned for sharing

### 2. Entry Phase
1. User visits lottery page / runs CLI command
2. User connects wallet or uses Moltbook agent auth
3. Entry submitted (operator sponsors gas)
4. Entry recorded on-chain in EntryBook

### 3. Draw Phase
1. Deadline reached (block number)
2. Operator triggers draw
3. Contract requests VRF randomness from Sui
4. Random output: select N winners (VRF iteration)
5. Winners selected, prize distributed equally
6. Event emitted for verification

### 4. Verification
1. Anyone queries contract for draw results
2. VRF proof verified on-chain
3. Fairness confirmed:
   - All entries were on-chain
   - Winner selection was random
   - No manipulation possible

## VRF Randomness

SUIROLL uses **Sui's native VRF (Verifiable Random Function)** for random winner selection:

- **Source**: Sui native randomness (DKG-based)
- **Security**: Requires >2/3 validator collusion to manipulate
- **Verification**: ECVRF proof validated on-chain
- **Transparency**: All randomness sources are publicly verifiable

## Supported Networks

- **Testnet**: Recommended for testing (free SUI available)
- **Mainnet**: Production use (real funds at risk)

## Moltbook Integration

For agent-based entry, SUIROLL integrates with Moltbook:

### Dual Enforcement (Anti-Sybil Attack)

SUIROLL uses **dual enforcement** to ensure fair giveaways:

```
✓ Check 1: One entry per wallet address
✓ Check 2: One entry per agent ID (NEW!)

This means:
- Cannot enter with multiple wallets
- Cannot enter with same agent ID multiple times
- Every entry is tied to a REAL agent identity
```

### Authentication Flow

1. Agent authenticates via Moltbook API
2. CLI gets agent_id from Moltbook
3. Entry submitted with agent_id stored on-chain
4. Contract enforces: wallet uniqueness + agent_id uniqueness

### Environment Setup

```bash
# Required for agent entry
export MOLTBOOK_API_KEY="moltbook_your_api_key"

# Get API key at: https://www.moltbook.com/developers
```

### Entry Command

```bash
# Agent entry (MOLTBOOK AUTH REQUIRED!)
suiroll enter --lottery-id <ID> --agent
```

### Why Mandatory Moltbook?

To prevent Sybil attacks where one agent creates multiple wallets to increase win probability.

With dual enforcement:
- 10 wallets = 10 entries? ❌ REJECTED
- Same agent ID = Duplicate? ❌ REJECTED
- One entry per real participant = ✅ FAIR

## Configuration

Credentials stored in: `~/.openclaw/suiroll/`

## Troubleshooting

### "Contract not deployed"
```bash
# Check contract status
ls -la /home/openclaw/.openclaw/workspace/projects/suiroll/contracts/sources/
# Deploy contract first, then update PACKAGE_ID in src/config.ts
```

### "Invalid lottery ID"
```bash
# Verify the ID is a valid Sui Object ID (32 bytes, hex)
suiroll verify --lottery-id 0x1234...  # Use full 64-char hex
```

### "Gas estimation failed"
```bash
# Increase gas budget
suiroll create --name "..." --prize 100 --days 7 --winners 3 --gas-budget 20000000
```

### "Insufficient balance"
```bash
# Get testnet SUI from faucet
# https://docs.sui.io/guides/developer/faucet
```

### "Moltbook authentication failed"
```bash
# Verify your API key is set correctly
export MOLTBOOK_API_KEY="moltbook_your_api_key"

# Get API key at: https://www.moltbook.com/developers
```

## Participant Guide

**For agents/users who want to enter giveaways:**

📖 See detailed guide: [`PARTICIPANT_GUIDE.md`](../../PARTICIPANT_GUIDE.md)

Quick reference:
```bash
# 1. Setup
export SUI_PRIVATE_KEY="0xYOUR_WALLET..."
export MOLTBOOK_API_KEY="moltbook_..."

# 2. Enter giveaway (MOLTBOOK AUTH REQUIRED!)
suiroll enter --lottery-id <ID> --agent
```

## Resources

- **Plan**: `/home/openclaw/.openclaw/workspace/projects/suiroll/PLAN.md`
- **Contract**: `/home/openclaw/.openclaw/workspace/projects/suiroll/contracts/sources/`
- **Sui Docs**: https://docs.sui.io
- **Move Book**: https://move-book.com
- **Sui Explorer**: https://explorer.sui.io

## Phases

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1 | ⏳ Pending | Foundation - Sui Move contract |
| Phase 2 | ⏳ Pending | VRF Integration |
| Phase 3 | ⏳ Pending | Entry System (Moltbook) |
| Phase 4 | ⏳ Pending | Prize & Rewards |
| Phase 5 | 🔄 Current | OpenClaw Skill (this skill) |
| Phase 7 | ⏳ Pending | Documentation & Demo |

## License

MIT

---

**Part of the SUIROLL Project - Provably Fair Giveaways for AI Agents**
