---
name: zkgov
description: Anonymous governance on HashKey Chain using zero-knowledge proofs. Query proposals, check voter status, register, create proposals, vote anonymously with ZK proofs, and finalize outcomes. Use whenever the user mentions ZKGov, governance proposals, anonymous voting, ZK voting, HashKey Chain governance, or anything related to on-chain voting with privacy.
---

# ZKGov

ZKGov is a zero-knowledge governance platform on HashKey Chain testnet (chain ID 133). Voters register with Semaphore identity commitments and cast anonymous, Groth16-verified votes on governance proposals.

## Install

```bash
# MCP server (preferred — works with Claude Code, Cursor, Windsurf, VS Code)
# https://www.npmjs.com/package/@zkgov/mcp
claude mcp add zkgov npx @zkgov/mcp

# Standalone CLI
# https://www.npmjs.com/package/@zkgov/cli
npm install -g @zkgov/cli
zkgov --help
```

## Mode priority

1. **MCP tools first.** If tools prefixed `mcp__zkgov__*` are available, call them directly.
2. **CLI fallback.** If no MCP tools are available, run `zkgov <command>` via the Bash tool.
3. **`--json` flag.** Always use `--json` when calling CLI from an agent for reliable parsing.

## When to use

- User asks about governance proposals, voting, or on-chain governance
- User wants to create, vote on, or check proposals
- User asks about voter registration or ZK identity
- User asks about HashKey Chain governance activity
- User wants an agent to participate in governance autonomously

## When NOT to use

- General blockchain questions answerable from training data
- Questions about other chains or protocols
- Math, code review, or general programming tasks

## Available tools

### Read tools (no wallet needed)

| MCP Tool | CLI Command | Description |
|---|---|---|
| `zkgov-stats` | `zkgov stats` | Platform stats: total proposals, members, group ID |
| `zkgov-list-proposals` | `zkgov proposals` | List all proposals with vote tallies and status |
| `zkgov-proposal` | `zkgov proposal <id>` | Full proposal detail by ID |
| `zkgov-check-voter` | `zkgov voter <address>` | Check if address is a registered voter |
| `zkgov-members` | `zkgov members` | Semaphore group info: member count, Merkle root |
| `zkgov-activity` | `zkgov activity` | Recent on-chain events with tx hashes |

### Write tools (require wallet with HSK for gas)

| MCP Tool | CLI Command | Description |
|---|---|---|
| `zkgov-wallet` | `zkgov wallet` | Show agent wallet: address, balance, voter status |
| `zkgov-register` | `zkgov register` | Register wallet as voter (one-time on-chain tx) |
| `zkgov-create-proposal` | `zkgov create <title>` | Create a governance proposal |
| `zkgov-vote` | `zkgov vote <id> <choice>` | Cast anonymous ZK-verified vote |
| `zkgov-finalize` | `zkgov finalize <id>` | Finalize proposal after voting period ends |

## Wallet

On first write operation, a wallet is auto-generated at `~/.zkgov/config.json` (mode 0o600). The same private key derives both the EVM account and the Semaphore ZK identity.

Override with env var: `ZKGOV_PRIVATE_KEY=0x...`

The wallet needs testnet HSK for gas (very cheap — 0.001 gwei gas price).

## Workflow

1. **Check state**: `zkgov-stats` to see proposals/members count
2. **Check wallet**: `zkgov-wallet` to see balance and registration
3. **Register**: `zkgov-register` (one-time, ~0.0003 HSK gas)
4. **Browse**: `zkgov-list-proposals` → `zkgov-proposal` for detail
5. **Vote**: `zkgov-vote` with proposalId and choice (generates ZK proof, ~3-5s)
6. **Finalize**: `zkgov-finalize` after voting period ends (anyone can call)

## CLI flags

- `--json` — machine-readable output on every command
- `zkgov activity --limit 10` — limit activity events
- `zkgov create "Title" -d "Body" -p 86400 -q 3` — set period (seconds) and quorum

## Key facts

- **Chain**: HashKey Chain Testnet (ID: 133, RPC: https://testnet.hsk.xyz)
- **Contract**: `0xEa625841E031758786141c8b13dD1b1137C9776C`
- **Explorer**: https://testnet-explorer.hsk.xyz
- **Vote choices**: 0 = Against, 1 = For, 2 = Abstain
- **Nullifiers** prevent double-voting per proposal (hash of identity + proposalId)
- **castVote** does NOT check msg.sender — only the ZK proof matters
- Proof generation uses snarkjs WASM, takes 3-5 seconds

## Error handling

- "Already registered" → wallet is already a voter, skip registration
- "Nullifier" error → already voted on this proposal
- "Voting ended" → voting period has closed, try `zkgov-finalize` instead
- "Proposal does not exist" → invalid proposal ID
- Insufficient balance → wallet needs HSK for gas
