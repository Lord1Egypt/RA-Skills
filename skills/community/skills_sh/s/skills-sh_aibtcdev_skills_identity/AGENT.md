---
name: identity-agent
skill: identity
description: ERC-8004 on-chain agent identity management — register agent identities, update URI and metadata, manage operator approvals, set/unset agent wallet, transfer identity NFTs, and query identity info.
---

# Identity Agent

This agent manages ERC-8004 on-chain agent identities using the identity-registry contract. It handles registration (minting a sequential agent ID), updating identity attributes (URI, metadata, approvals, wallet), NFT transfers, and read-only queries. Read operations (get, get-metadata, get-last-id) work without a wallet. Write operations require an unlocked wallet.

## Prerequisites

- For write operations (register, set-uri, set-metadata, set-approval, set-wallet, unset-wallet, transfer): wallet must be unlocked — run `bun run wallet/wallet.ts unlock` first
- For read operations (get, get-metadata, get-last-id): no wallet required
- Network must be configured (defaults to testnet; set `NETWORK=mainnet` for mainnet)
- The agent ID must already exist on-chain before running set-uri, set-metadata, set-approval, set-wallet, unset-wallet, or transfer

## Decision Logic

| Goal | Subcommand |
|------|-----------|
| Register a new on-chain agent identity | `register` — returns txid; check tx result for assigned agent ID |
| Look up owner, URI, and wallet for an agent | `get --agent-id <id>` — read-only, no wallet needed |
| Update the URI pointing to agent metadata | `set-uri --agent-id <id> --uri <uri>` — caller must be owner or operator |
| Store a key-value metadata pair on the agent | `set-metadata --agent-id <id> --key <k> --value <hex>` — value is hex-encoded buffer |
| Read a metadata value back from the registry | `get-metadata --agent-id <id> --key <k>` — read-only |
| Grant or revoke an operator for the agent | `set-approval --agent-id <id> --operator <addr>` — only NFT owner can call |
| Link the active wallet address to the agent ID | `set-wallet --agent-id <id>` — sets tx-sender as the agent wallet |
| Remove the wallet link from an agent identity | `unset-wallet --agent-id <id>` — caller must be owner or operator |
| Transfer the identity NFT to a new owner | `transfer --agent-id <id> --recipient <addr>` — clears wallet automatically |
| Find the most recently minted agent ID | `get-last-id` — read-only |

## Safety Checks

- `set-approval` can only be called by the NFT owner — not by delegated operators; verify ownership with `get` first
- `transfer` is irreversible — confirm the recipient address is correct; it also clears the agent wallet link
- Metadata values must be hex-encoded buffers (max 512 bytes); the key `agentWallet` is reserved by the contract — use `set-wallet` / `unset-wallet` instead
- Write operations submit Stacks L2 transactions — check status with `bun run stx/stx.ts get-transaction-status --txid <txid>` after submission
- Never include plaintext data directly in `--value`; always hex-encode first (e.g., `echo -n "alice" | xxd -p` gives `616c696365`)

## Error Handling

| Error message | Cause | Fix |
|--------------|-------|-----|
| "No active wallet. Please unlock your wallet first." | Write command called without an unlocked wallet | Run `bun run wallet/wallet.ts unlock --password <password>` |
| "--agent-id must be a non-negative integer" | Invalid or missing `--agent-id` value | Pass a non-negative integer (e.g., `--agent-id 42`) |
| "--value must be a non-empty, even-length hex string" | Metadata value is not valid hex | Hex-encode the value before passing (e.g., use `xxd -p`) |
| "metadata value for key ... exceeds 512 bytes" | Hex-encoded metadata buffer is too large | Reduce the value size to 512 bytes or less |
| "Agent ID not found" | `get` returned no identity for the given ID | The agent may not be registered yet; check `get-last-id` |
| "Metadata key not found for this agent" | `get-metadata` found no value for the key | The key was never set; use `set-metadata` to store it |

## Output Handling

- `register`: extract `txid` and check transaction result to get the assigned `agentId`; `explorerUrl` links directly to the transaction
- `get`: extract `owner` to verify ownership before write operations; `wallet` may be "(no wallet set)" if not linked
- `get-metadata`: extract `valueHex` and decode from hex to get the original value
- `get-last-id`: extract `lastAgentId` to discover the range of registered agent IDs
- Write operations return `txid` and `explorerUrl`; the transaction may take 10–30 seconds to confirm on-chain
- `success: false` responses indicate a not-found condition, not an error — check the `message` field for details

## Example Invocations

```bash
# Register a new on-chain agent identity with a metadata URI
bun run identity/identity.ts register --uri https://myagent.example.com/metadata.json

# Look up an agent's identity by agent ID
bun run identity/identity.ts get --agent-id 42

# Link the active wallet address to the agent
bun run identity/identity.ts set-wallet --agent-id 42
```
