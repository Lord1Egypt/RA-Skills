---
name: wallet-agent
skill: wallet
description: Manages encrypted BIP39 wallet lifecycle — create, import, unlock, lock, switch, and export wallets stored at ~/.aibtc/.
---

# Wallet Agent

Handles all wallet lifecycle operations for the AIBTC skill suite. Manages BIP39 wallets encrypted with AES-GCM at `~/.aibtc/`, providing Stacks L2 and Bitcoin L1 (native SegWit + Taproot) addresses. Nearly all other skills depend on an unlocked wallet for write operations — this agent is the prerequisite gatekeeper.

## Prerequisites

- No prerequisites — this skill bootstraps all others
- For `unlock`, `delete`, `export`, `rotate-password`: a wallet must already exist (`create` or `import` first)
- For `switch`: the target wallet ID must be from the `list` output

## Decision Logic

| Goal | Subcommand |
|------|-----------|
| First-time setup | `create` — generates a new 24-word mnemonic |
| Restore existing wallet | `import` — requires the mnemonic phrase |
| Enable write operations | `unlock` — required before transfers or contract calls |
| Disable write operations | `lock` — clears key material from memory |
| See all wallets | `list` — metadata only, no sensitive data |
| Change active wallet | `switch` — then `unlock` with the new wallet's password |
| Check readiness | `status` — first call to make in any workflow |
| View addresses | `info` — requires an unlocked wallet |
| Check STX funds | `stx-balance` — can pass `--address` to check any address |
| Back up a wallet | `export` — requires password + `I_UNDERSTAND_THE_RISKS` |
| Change encryption password | `rotate-password` — atomic: backs up, re-encrypts, verifies |
| Configure auto-lock | `set-timeout` — set minutes (0 = never) |

## Safety Checks

- Always call `status` first to check if a wallet is unlocked before write operations
- Never log or expose `--password`, `--mnemonic`, `--old-password`, or `--new-password` values
- `export` prints the mnemonic in plaintext output — handle the output as a secret
- `delete` is irreversible — confirm the wallet mnemonic is backed up before deleting
- `rotate-password` locks the wallet on success — re-unlock with the new password

## Error Handling

| Error message | Cause | Fix |
|--------------|-------|-----|
| "No active wallet found" | No wallet exists or no wallet set as active | Run `create` or `import`, then `list` to get the wallet ID |
| "Wallet is locked" | Wallet exists but not unlocked | Run `unlock --password <password>` |
| "Invalid password" | Wrong password supplied | Check the password; use `export` only with the correct password |
| "Confirmation required" | `--confirm` flag not set to exact value | Pass `--confirm DELETE` or `--confirm I_UNDERSTAND_THE_RISKS` exactly |

## Output Handling

- `status`: check `readyForTransactions` (boolean) — if `false`, follow `nextAction` before proceeding
- `create` / `import` / `unlock`: extract `walletId`, `Bitcoin (L1)`, and `Stacks (L2)` fields for display or downstream use
- `list`: use `id` field values for `--wallet-id` in subsequent subcommands; check `isActive` and `isUnlocked`
- `stx-balance`: read `balance.stx` for display; use `balance.microStx` for transaction calculations
- `export`: treat the `mnemonic` field as a secret — do not log or display in insecure contexts

## Example Invocations

```bash
# Check wallet status before any operation
bun run wallet/wallet.ts status

# Create a new wallet on mainnet
bun run wallet/wallet.ts create --name main --password <password> --network mainnet

# Unlock the active wallet to enable write operations
bun run wallet/wallet.ts unlock --password <password>

# List all wallets to find wallet IDs
bun run wallet/wallet.ts list
```
