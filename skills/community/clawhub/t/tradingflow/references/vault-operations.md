# Vault Operations Guide

TradingFlow uses the **TFV (TradingFlow Vault) Protocol v0.5** for on-chain asset custody across multiple chains.

## Architecture

```
User Wallet ──► TFV Vault (Smart Contract) ◄── Agent (TFP Process)
                    │
                    ├── Role-based access control (ORACLE_ROLE, ADMIN_ROLE)
                    ├── Per-agent permissions (swap/borrow/withdraw/sub_account)
                    ├── Per-token spending limits
                    ├── Withdraw allowances with reset periods
                    ├── Borrow/repay mechanism with configurable deadlines
                    ├── Sub-account registry (V0.4)
                    └── VaultRouter + trustedRouters whitelist (V0.5)
```

## Supported Chains

| Chain | ID | Status |
|-------|----|--------|
| BSC (BNB Smart Chain) | `bsc` | Active |
| Aptos | `aptos` | Active |
| Solana | `solana` | Active |

## Vault Lifecycle

### 1. Create Vault

```bash
# Build the create-vault transaction
curl -X POST $BASE/vault/bsc/create \
  -H "Authorization: Bearer $KEY" \
  -d '{"investor":"0xYourWallet","oracle":"0xOracleAddr"}'

# Response: unsigned txData → sign with wallet and submit
```

### 2. Check Status

```bash
curl "$BASE/vault/bsc/status?address=0xYourWallet" \
  -H "Authorization: Bearer $KEY"
```

### 3. View Balances

```bash
curl "$BASE/vault/bsc/balances?address=0xVaultAddr" \
  -H "Authorization: Bearer $KEY"
```

## Vault Features

### Agent Permissions

Fine-grained permission bitmask per agent:

| Bit | Value | Permission | Description |
|-----|-------|------------|-------------|
| 0 | 1 | SWAP | Execute token swaps |
| 1 | 2 | BORROW | Borrow vault assets temporarily |
| 2 | 4 | WITHDRAW | Withdraw within allowance limits |
| 3 | 8 | SUB_ACCOUNT | Register/close sub-accounts (V0.4) |

Combine with bitwise OR: `permissions = 3` grants SWAP + BORROW.

```bash
# Query
curl "$BASE/vault/bsc/0xVault/agent-permissions/0xAgent" \
  -H "Authorization: Bearer $KEY"
# → {"data":{"permissions":3}}

# Set
curl -X POST "$BASE/vault/bsc/0xVault/set-agent-permissions" \
  -H "Authorization: Bearer $KEY" \
  -d '{"agent":"0xAgent","permissions":7}'
# → unsigned txData
```

### Per-Token Spending Limits

Daily spending cap per token. Resets automatically.

```bash
# Query current limit
curl "$BASE/vault/bsc/0xVault/token-spending-limit/0xToken" \
  -H "Authorization: Bearer $KEY"
# → {"data":{"limit":"1000...","spentToday":"250...","resetsAt":"1706745600"}}

# Set daily limit (in raw token units)
curl -X POST "$BASE/vault/bsc/0xVault/set-token-spending-limit" \
  -H "Authorization: Bearer $KEY" \
  -d '{"token":"0xToken","dailyLimit":"1000000000000000000000"}'
```

### Withdraw Allowance

Total withdrawal budget with periodic reset.

```bash
# Query
curl "$BASE/vault/bsc/0xVault/withdraw-allowance/0xToken" \
  -H "Authorization: Bearer $KEY"
# → {"data":{"total":"5000...","used":"1000...","remaining":"4000...","resetsAt":"..."}}

# Set allowance: amount + reset period in seconds
curl -X POST "$BASE/vault/bsc/0xVault/set-withdraw-allowance" \
  -H "Authorization: Bearer $KEY" \
  -d '{"token":"0xToken","amount":"5000000000000000000000","period":86400}'

# Agent withdraw (within allowance)
curl -X POST "$BASE/vault/bsc/0xVault/agent-withdraw" \
  -H "Authorization: Bearer $KEY" \
  -d '{"token":"0xToken","amount":"500000000000000000000","to":"0xRecipient"}'
```

Common period values: `3600` (1h), `43200` (12h), `86400` (24h), `604800` (7d), `2592000` (30d).

### Borrow / Repay

Agents can borrow vault assets with a deadline. Overdue borrows can be force-closed.

```bash
# List active borrows
curl "$BASE/vault/bsc/0xVault/borrows" \
  -H "Authorization: Bearer $KEY"

# Borrow (duration in seconds)
curl -X POST "$BASE/vault/bsc/0xVault/borrow" \
  -H "Authorization: Bearer $KEY" \
  -d '{"token":"0xToken","amount":"1000000000000000000","duration":86400}'

# Repay
curl -X POST "$BASE/vault/bsc/0xVault/repay" \
  -H "Authorization: Bearer $KEY" \
  -d '{"borrowId":0,"tokenRepaid":"0xToken","amountRepaid":"1000000000000000000"}'

# Force close (for overdue borrows)
curl -X POST "$BASE/vault/bsc/0xVault/force-close-borrow" \
  -H "Authorization: Bearer $KEY" \
  -d '{"borrowId":0}'
```

## Two Trading Modes

TradingFlow supports two modes for vault operations:

### Mode 1: Manual (Approval Flow)

For one-off operations or when the user wants to review and sign each transaction.

1. Agent calls a vault endpoint → receives unsigned `txData`
2. Agent creates an approval request via `/claw/approval/request` (include `txData` and optionally `requiredAddress`)
3. User receives an approval URL on TradingFlow's platform
4. User reviews and approves in browser → signs the transaction with their wallet (address must match `requiredAddress`)
5. Agent polls `/claw/approval/status/:id` until approved/rejected

> If the user has no linked wallet (Google login), the approval request returns `wallet_not_linked` — Agent should guide the user to connect their wallet at the Dashboard first.

```bash
curl -X POST $BASE/claw/approval/request \
  -H "Authorization: Bearer $KEY" \
  -d '{
    "action": "withdraw",
    "description": "Withdraw 100 USDT from BSC vault to 0xRecipient",
    "chain": "bsc",
    "params": {
      "token": "0xUSDT",
      "amount": "100000000000000000000",
      "to": "0xRecipient"
    }
  }'

# Poll until decision
curl "$BASE/claw/approval/status/{approvalId}" \
  -H "Authorization: Bearer $KEY"
```

> **Security rule**: Always explain WHAT and WHY before presenting the approval link.

### Mode 2: Automated (Per-User Oracle Key)

For recurring automated strategies (DCA, grid trading, signal-driven execution). The TFP process signs and submits transactions autonomously using a dedicated Oracle key.

**Prerequisite: R&D Mode must be enabled.** Check `GET /auth/me` → `data.user.rdMode.enabled`. If not enabled, direct the user to Settings to enable it before proceeding. The API will reject `POST /user-secrets` with `category=secret` if R&D Mode is off (403 `RD_MODE_REQUIRED`).

**One-time setup** (agent guides the user):

1. Verify R&D Mode is enabled (see above)
2. Generate a new wallet keypair (the "Oracle wallet")
3. Store the private key as a `secret` in Secrets: `POST /user-secrets {name:"VAULT_ORACLE_KEY", category:"secret"}`
4. Grant `ORACLE_ROLE` to the Oracle address on the vault (requires user approval)
5. Set `agentPermissions` — start with `1` (SWAP only)
6. Set `tokenSpendingLimits` — e.g., 100 USDT/day
7. Store `VAULT_ADDRESS` as an `env_var` for TFP access

**TFP runtime execution:**

```python
# Python: Retrieve Oracle key and execute on-chain
import os, requests
from web3 import Web3

token = os.environ['TFP_SECRET_TOKEN']
endpoint = os.environ['TFP_SECRETS_ENDPOINT']
resp = requests.get(f"{endpoint}/VAULT_ORACLE_KEY",
                    headers={"x-tfp-secret-token": token})
oracle_key = resp.json()['data']['value']

w3 = Web3(Web3.HTTPProvider(os.environ.get('BSC_RPC_URL',
          'https://bsc-testnet-rpc.publicnode.com')))
account = w3.eth.account.from_key(oracle_key)
vault_addr = os.environ['VAULT_ADDRESS']

vault = w3.eth.contract(address=vault_addr, abi=VAULT_ABI)
tx = vault.functions.exec(module_id, swap_data).build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 300000,
    'gasPrice': w3.eth.gas_price,
})
signed = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
```

```javascript
// JS/TS: Same flow with ethers.js
const { ethers } = require('ethers');

const oracleKey = await fetchSecret('VAULT_ORACLE_KEY');
const provider = new ethers.JsonRpcProvider(process.env.BSC_RPC_URL);
const wallet = new ethers.Wallet(oracleKey, provider);
const vault = new ethers.Contract(process.env.VAULT_ADDRESS, VAULT_ABI, wallet);

const tx = await vault.exec(moduleId, swapData);
console.log(`Trade executed: ${tx.hash}`);
```

**Security guarantees for Mode 2:**

| Layer | Protection |
|-------|-----------|
| On-chain | `agentPermissions` bitmask — only allowed operations |
| On-chain | `tokenSpendingLimits` — daily cap per token |
| On-chain | `withdrawAllowances` — withdrawal budget with periodic reset |
| On-chain | `MAX_ACTIVE_BORROWS = 5`, configurable `maxBorrowDuration` (0 = unlimited) |
| Platform | AES-256-GCM envelope encryption for stored private key |
| Platform | `TFP_SECRET_TOKEN` (JWT) scoped to specific process + user |
| Platform | Automatic log redaction of all secret values |
| User | Can revoke `ORACLE_ROLE` instantly from Owner wallet |

> **Best practice**: Start with `permissions = 1` (SWAP only) and conservative daily limits. Escalate only when the user explicitly requests it.

## V0.4 Features: Sub-Account Registry

Sub-accounts allow the vault to track external accounts (Polymarket, CEX wallets, cross-chain addresses) linked to the vault.

- `registerSubAccount(address, chainId, accountType, description)` — requires `PERM_SUB_ACCOUNT`
- `closeSubAccount(subAccountId)` — Oracle or Owner
- `getSubAccounts()` / `getActiveSubAccounts()` — view all or active only
- `borrow()` can link to a sub-account; `repay()` can optionally close the linked sub-account
- `maxBorrowDuration` is now configurable (0 = unlimited)

## V0.5 Features: VaultRouter + Trusted Routers

V0.5 adds router-assisted deposit/withdraw for better UX (e.g., auto-wrap BNB → WBNB):

- `depositFor(token, amount, depositor)` — trusted router deposits on behalf of investor
- `withdrawFor(token, amount, recipient, withdrawer)` — trusted router withdraws on behalf of investor
- `withdrawNativeFor(amount, recipient, withdrawer)` — same for native token
- `setTrustedRouter(router, trusted)` — Owner manages router whitelist
- Security: `msg.sender == investor || trustedRouters[msg.sender]` — non-whitelisted contracts cannot call these functions

## Token Decimals

All amounts in the API are in **raw token units** (wei for EVM chains). Common conversions:

| Token | Decimals | 1 token in raw |
|-------|----------|----------------|
| USDT (BSC) | 18 | 1000000000000000000 |
| BNB | 18 | 1000000000000000000 |
| USDC (BSC) | 18 | 1000000000000000000 |
| WBTC | 8 | 100000000 |

Always check `decimals` from the `/balances` response for accurate conversion.
