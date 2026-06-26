# Examples

## Airdrop Campaign (Solana)

### 1. Generate wallets for the campaign
```
generate_wallets(chain="solana", count=100, label="drop_apr", tags="airdrop|season1")
```

### 2. Check they were created
```
group_summary()
```
Output:
```json
{
  "groups": [{"label": "drop_apr", "solana": 100, "evm": 0, "total": 100}]
}
```

### 3. Fund all wallets from your main wallet
```
send_native_multi(
  from_key="5Kd3NBo...",
  label="drop_apr",
  amount=0.05,
  chain="solana",
  randomize=True,
  delay_min=2,
  delay_max=12,
  retries=3
)
```

### 4. Verify balances
```
get_balance_batch(label="drop_apr", chain="solana")
```

### 5. Tag funded wallets
```
tag_wallets(label="drop_apr", tag="funded")
```

---

## Multi-Chain Wallet Management

### Generate EVM wallets
```
generate_wallets(chain="evm", count=20, label="eth_test", tags="ethereum|testgroup")
```

### List only Solana wallets
```
list_wallets(chain="solana")
```

### List wallets by tag
```
list_wallets(tag="funded")
```

### Get all balances across chains
```
get_balance_batch()
```

---

## Solana Rent Recovery

### Scan token accounts first (read-only)
```
scan_token_accounts(address="So1anaWa11etPubkey...")
```
Output:
```json
{
  "total": 23,
  "empty": 18,
  "non_empty": 5,
  "accounts": [...]
}
```

### Close empty accounts
```
close_token_accounts(private_key="5Kd3NBo...")
```
Output:
```json
{
  "closed": 18,
  "failed": 0,
  "skipped": 5,
  "total_found": 23,
  "reclaimed_sol_estimate": 0.036707
}
```

---

## Custom RPC Endpoints

Pass `rpc` parameter to any tool that interacts with the chain:

```
# Helius (Solana)
get_balance_batch(label="drop_apr", rpc="https://mainnet.helius-rpc.com/?api-key=xxx")

# QuickNode (Solana)
send_native_multi(..., rpc="https://your-endpoint.quiknode.pro/token/")

# Alchemy (EVM)
get_balance_batch(chain="evm", label="eth_test", rpc="https://eth-mainnet.g.alchemy.com/v2/key")

# BSC
send_native_multi(..., chain="evm", rpc="https://bsc-dataseed.binance.org/")

# Polygon
send_native_multi(..., chain="evm", rpc="https://polygon-rpc.com")
```

---

## Wallet Cleanup

### Delete a group permanently
```
delete_group(label="old_campaign")
```

### Check what will be deleted first
```
list_wallets(label="old_campaign")
```

---

## Sweep — Collect Funds Back

### After a campaign: sweep all remaining SOL to your main wallet
```
sweep_wallets(
  to_address="YourMainWalletPubkey...",
  chain="solana",
  label="drop_apr",
  leave_lamports=5000
)
```
Output:
```json
{
  "status": "success",
  "chain": "solana",
  "to_address": "YourMainWalletPubkey...",
  "total": 100,
  "swept": 97,
  "skipped": 3,
  "failed": 0,
  "total_swept": 4.823719,
  "results": [...]
}
```

### Sweep EVM wallets tagged "used" back to treasury
```
sweep_wallets(
  to_address="0xYourTreasury...",
  chain="evm",
  tag="used"
)
```

---

## Token Balance Scan

### Scan all SPL tokens across a Solana wallet group
```
scan_token_balances(chain="solana", label="drop_apr")
```
Output:
```json
{
  "status": "success",
  "chain": "solana",
  "token": null,
  "total_wallets": 100,
  "wallets_with_balance": 42,
  "results": [
    {
      "address": "So1ana...",
      "tokens": [
        {"mint": "EPjFW...", "balance": 10.5, "decimals": 6},
        {"mint": "Es9vM...", "balance": 0.0, "decimals": 6}
      ],
      "status": "ok"
    }
  ]
}
```

### Check USDC balance for a specific EVM group
```
scan_token_balances(
  chain="evm",
  label="eth_test",
  token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
)
```
Output:
```json
{
  "status": "success",
  "chain": "evm",
  "token": "0xA0b8...",
  "total_wallets": 20,
  "wallets_with_balance": 5,
  "results": [
    {"address": "0xABCD...", "balance": 250.0, "symbol": "USDC", "status": "ok"},
    {"address": "0x1234...", "balance": 0.0,   "symbol": "USDC", "status": "ok"}
  ]
}
```

### Filter by tag + specific Solana mint
```
scan_token_balances(
  chain="solana",
  tag="funded",
  token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
)
```

---

## Export Wallets

### Export a Solana group to JSON (no private keys — safe to share)
```
export_wallets(label="drop_apr", chain="solana", format="json")
```
Output:
```json
{
  "status": "success",
  "path": "/home/user/.wallet-mcp/exports/wallets_2026-04-10_12-00-00.json",
  "format": "json",
  "count": 100,
  "include_keys": false
}
```

### Export to a specific path with private keys (for backup)
```
export_wallets(
  label="drop_apr",
  format="json",
  path="/secure/backup/drop_apr.json",
  include_keys=True
)
```

### Export filtered group to CSV
```
export_wallets(chain="evm", tag="funded", format="csv")
```

---

## Import Wallets

### Import from a JSON backup (duplicates auto-skipped)
```
import_wallets(path="/backups/airdrop1.json", label="airdrop2")
```
Output:
```json
{
  "status": "success",
  "file": "/backups/airdrop1.json",
  "format": "json",
  "total_in_file": 100,
  "imported": 98,
  "skipped_duplicates": 2,
  "failed": 0
}
```

### Import CSV and override label + add tags
```
import_wallets(
  path="/backups/wallets.csv",
  fmt="csv",
  label="campaign3",
  tags="restored|batch1"
)
```

### Auto-detect format from file extension
```
import_wallets(path="/backups/export.json")
```

---

## Natural Language (Claude Desktop)

These prompts work directly in Claude Desktop after installing wallet-mcp:

- _"Generate 50 Solana wallets for my new airdrop, label it launch_may"_
- _"Send 0.02 SOL to all launch_may wallets with random delays between 3 and 20 seconds"_
- _"How much total SOL do my launch_may wallets hold?"_
- _"Tag all launch_may wallets as funded"_
- _"Show me all my wallet groups"_
- _"Scan token accounts on wallet So1ana... and close the empty ones to reclaim SOL"_
- _"Create 30 EVM wallets for my Ethereum test group"_
- _"List all Solana wallets with the tag funded"_
- _"Sweep all remaining SOL from my airdrop1 wallets back to my main wallet"_
- _"Check which wallets in eth_test hold USDC"_
- _"Export all my airdrop1 wallets to a JSON file for backup"_
- _"Export funded EVM wallets to CSV without private keys"_
- _"Import wallets from my backup file and put them in the airdrop2 group"_
- _"Import wallets from campaign.csv and tag them as restored"_
