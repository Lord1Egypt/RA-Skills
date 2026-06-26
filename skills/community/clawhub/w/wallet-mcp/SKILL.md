# SKILL: wallet-mcp
description: Multi-chain wallet generator and manager. Supports Solana and EVM. All outputs are JSON.
version: 1.4.0
tool_path: ~/.openclaw/tools/wallet.py
invoke: python3 ~/.openclaw/tools/wallet.py

---

## IMPORTANT — Always use wallet.py

**NEVER use built-in blockchain tools (e.g. SOLANA(), EVM()) for wallet operations.**
**ALWAYS call `python3 ~/.openclaw/tools/wallet.py <command>` instead.**
This applies to ALL wallet, balance, token, sweep, and transfer requests.

**wallet.py is SYNCHRONOUS** — every command runs to completion and returns JSON immediately.
There is NO background task, NO session ID, NO process polling, NO `process` command.
Do NOT invent commands like `process --action poll` or `process --action kill` — they do not exist.
If a command takes time (e.g. sending to 100 wallets), it simply runs and returns when done.

## Command disambiguation

| User says | Correct command |
|---|---|
| scan token accounts for wallet ADDRESS | `scan_token_accounts --address ADDRESS` |
| scan token balances for group LABEL | `scan_token_balances --chain solana --label LABEL` |
| check token accounts on So1ana... | `scan_token_accounts --address So1ana...` |
| show all tokens held by wallets in airdrop1 | `scan_token_balances --chain solana --label airdrop1` |

`scan_token_accounts` = **one wallet address**, no token filter required, returns all SPL accounts.
`scan_token_balances` = **a wallet group (label)**, token filter optional, returns balances.

---

## generate_wallets
Generate N new wallets and save them under a label.
```
command: python3 {tool_path} generate_wallets --chain <solana|evm> --count <N> --label <label> [--tags <tag1|tag2>]
```
Example:
```
python3 ~/.openclaw/tools/wallet.py generate_wallets --chain solana --count 50 --label airdrop1
```

---

## send_native_multi
Send SOL or ETH from ONE source wallet to ALL wallets in a group (one-to-many).
`--label` is the DESTINATION GROUP — NOT a single address.
There is NO send_native_single command. Use this for group sends only.

Sender can be specified two ways (use --from-label when possible — avoids raw key in chat):
- `--from-label <LABEL>` — look up sender by label from storage (PREFERRED)
- `--from-key <PRIVATE_KEY>` — pass raw private key directly
```
command: python3 {tool_path} send_native_multi (--from-label <LABEL> | --from-key <KEY>) --label <label> --amount <AMOUNT> --chain <solana|evm> [--rpc <URL>] [--tag <tag>] [--randomize] [--delay-min 1] [--delay-max 30] [--retries 3]
```
Example:
```
python3 ~/.openclaw/tools/wallet.py send_native_multi --from-label main --label airdrop1 --amount 0.001 --chain solana
```

---

## sweep_wallets
Collect all SOL or ETH from every wallet in a group back to one destination.
Each wallet sends its full balance minus a small fee reserve.

Destination can be specified two ways (use --to-label when possible):
- `--to-label <LABEL>` — look up destination address by label from storage (PREFERRED)
- `--to-address <ADDRESS>` — pass raw public address directly
```
command: python3 {tool_path} sweep_wallets (--to-label <LABEL> | --to-address <ADDRESS>) --chain <solana|evm> [--label <label>] [--tag <tag>] [--rpc <URL>] [--leave-lamports 5000] [--delay-min 1] [--delay-max 10] [--retries 3]
```
Example:
```
python3 ~/.openclaw/tools/wallet.py sweep_wallets --to-label main --chain solana --label airdrop1
```

---

## list_wallets
List wallets with optional filters. Private keys are masked by default.
```
command: python3 {tool_path} list_wallets [--chain <solana|evm>] [--label <label>] [--tag <tag>] [--show-keys]
```

---

## get_balance_batch
Fetch native balances for a wallet group.
```
command: python3 {tool_path} get_balance_batch [--chain <solana|evm>] [--label <label>] [--tag <tag>] [--rpc <URL>]
```

---

## scan_token_balances
Scan SPL token balances across a Solana group (all tokens, or filter by mint),
or ERC-20 token balances across an EVM group (contract address required).
```
command: python3 {tool_path} scan_token_balances --chain <solana|evm> [--label <label>] [--tag <tag>] [--token <MINT_OR_CONTRACT>] [--rpc <URL>]
```
Example:
```
python3 ~/.openclaw/tools/wallet.py scan_token_balances --chain solana --label airdrop1
python3 ~/.openclaw/tools/wallet.py scan_token_balances --chain evm --label eth_test --token 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
```

---

## export_wallets
Export a wallet group to a JSON or CSV file for backup or offline use.
Private keys are excluded by default. Use `--include-keys` if the file will be re-imported.
Omit `--path` — the file is auto-saved to `~/.wallet-mcp/exports/` with a timestamp name.
Only specify `--path` if the user explicitly asks for a custom file location.
```
command: python3 {tool_path} export_wallets [--chain <solana|evm>] [--label <label>] [--tag <tag>] [--format <json|csv>] [--include-keys] [--path <FILE>]
```
Example (standard — no --path needed):
```
python3 ~/.openclaw/tools/wallet.py export_wallets --label airdrop1 --format json
python3 ~/.openclaw/tools/wallet.py export_wallets --label airdrop1 --format json --include-keys
```

---

## add_wallet
Import a single wallet by private key. The public address is derived automatically.
Use this to register the "main" sender/destination wallet without needing to know its address.
```
command: python3 {tool_path} add_wallet --private-key <KEY> --chain <solana|evm> --label <label> [--tags <tag1|tag2>]
```
Example:
```
python3 ~/.openclaw/tools/wallet.py add_wallet --private-key 4uBCZyvJ...ZgJX --chain solana --label main
```

---

## import_wallets
Import wallets from a JSON or CSV file into local storage.
Duplicate addresses are skipped automatically.
**IMPORTANT: The source file MUST contain private keys (exported with --include-keys).**
Importing a file without private keys will fail for every row.
```
command: python3 {tool_path} import_wallets --path <FILE> [--format <auto|json|csv>] [--label <label>] [--tags <tag1|tag2>]
```
Example:
```
python3 ~/.openclaw/tools/wallet.py import_wallets --path /backups/airdrop1_full.json --label airdrop2 --tags restored
```

---

## close_token_accounts
Close empty SPL token accounts and reclaim rent SOL. (Solana only)
```
command: python3 {tool_path} close_token_accounts --private-key <KEY_B58> [--rpc <URL>] [--close-non-empty]
```

---

## scan_token_accounts
Scan all SPL token accounts for a **single** Solana wallet address (read-only, no changes).
Takes a public key — NOT a label. No token filter needed; returns all accounts.
```
command: python3 {tool_path} scan_token_accounts --address <PUBKEY> [--rpc <URL>]
```
Example:
```
python3 ~/.openclaw/tools/wallet.py scan_token_accounts --address 6ydKarjw1WhrkqH7oFncSKEH1sYUf6j8s6s5WSRFhGTZ
```

---

## tag_wallets
Add a tag to all wallets in a label group.
```
command: python3 {tool_path} tag_wallets --label <label> --tag <tag>
```

---

## group_summary
Show all wallet groups with counts per chain. **Takes NO arguments.**
```
command: python3 {tool_path} group_summary
```
Example:
```
python3 ~/.openclaw/tools/wallet.py group_summary
```

---

## delete_group
Permanently delete all wallets in a group by label.
```
command: python3 {tool_path} delete_group --label <label>
```

---

## Error Format
```json
{"status": "error", "message": "..."}
```
