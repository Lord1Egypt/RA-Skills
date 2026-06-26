---
name: tonscan-wallet-balance
description: Look up TON blockchain wallet balances, address information, and token holdings using the free TonScan API — no API key required. Use this skill whenever the user wants to check a TON wallet address balance, look up on-chain data for a TON address, convert nanoton values, or fetch TON account details. Trigger even for casual requests like "how much TON is in this wallet?" or "check this address for me".
---

# TonScan Wallet Balance Skill

Query real-time TON blockchain data using TonScan's free public API. No authentication needed.

---

## Core Concepts

### Units: Nanotons vs TON
The TON blockchain stores all balances in **nanotons** (the smallest indivisible unit).

| Unit | Value |
|------|-------|
| 1 TON | 1,000,000,000 nanotons |
| 1 nanoton | 0.000000001 TON |

Always divide raw API values by `1_000_000_000` (1e9) before displaying to users.

**Example:**
```
Raw API value:  1296986856910034000
Divide by 1e9:  1296986856.910034 TON
```

---

## Primary Endpoint: Address Information
```
GET https://api.tonscan.com/api/bt/getAddressInformation?address={ADDRESS}
```

### Quick Balance Lookup (one-liner)
```bash
curl -s "https://api.tonscan.com/api/bt/getAddressInformation?address=EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2" \
  | jq '.json.data.detail.balance'
```

### Full Response with Human-Readable Balance
```bash
ADDRESS="EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2"
curl -s "https://api.tonscan.com/api/bt/getAddressInformation?address=${ADDRESS}" \
  | jq '{
      address: .json.data.detail.address,
      balance_nanoton: .json.data.detail.balance,
      balance_TON: (.json.data.detail.balance | tonumber / 1000000000),
      status: .json.data.detail.status
    }'
```

**Sample output:**
```json
{
  "address": "EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2",
  "balance_nanoton": 1296986856910034000,
  "balance_TON": 1296986856.910034,
  "status": "active"
}
```

---

## Response Structure

The full response nests data under `.json.data.detail`. Key fields:

| Field | Path | Description |
|-------|------|-------------|
| Balance (raw) | `.json.data.detail.balance` | Balance in nanotons (integer string) |
| Address | `.json.data.detail.address` | Canonical address string |
| Status | `.json.data.detail.status` | `active`, `uninitialized`, or `frozen` |
| Last activity | `.json.data.detail.last_activity` | Unix timestamp of last transaction |

---

## Address Format Notes

TON addresses come in two formats — both refer to the same wallet:

- **User-friendly (EQ...):** `EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2`
- **Raw (0:...):** `0:ED169130705004711...`

The TonScan API accepts both formats. Always use the user-friendly `EQ...` or `UQ...` format when displaying addresses back to users.

---

## Python Example
```python
import requests

def get_ton_balance(address: str) -> dict:
    url = "https://api.tonscan.com/api/bt/getAddressInformation"
    resp = requests.get(url, params={"address": address})
    resp.raise_for_status()

    detail = resp.json()["json"]["data"]["detail"]
    nanotons = int(detail["balance"])

    return {
        "address": detail["address"],
        "balance_ton": nanotons / 1_000_000_000,
        "balance_nanoton": nanotons,
        "status": detail.get("status", "unknown"),
    }

# Example
info = get_ton_balance("EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2")
print(f"Balance: {info['balance_ton']:,.9f} TON")
# → Balance: 1,296,986,856.910034000 TON
```

---

## JavaScript / Node.js Example
```javascript
async function getTonBalance(address) {
  const url = new URL("https://api.tonscan.com/api/bt/getAddressInformation");
  url.searchParams.set("address", address);

  const res = await fetch(url);
  const data = await res.json();
  const detail = data.json.data.detail;

  const nanotons = BigInt(detail.balance);
  const ton = Number(nanotons) / 1e9;

  return {
    address: detail.address,
    balanceTon: ton,
    balanceNanoton: nanotons.toString(),
    status: detail.status,
  };
}

// Usage
const info = await getTonBalance("EQDtFpEwcFAEcRe5mLVh2N6C0x-_hJEM7W61_JLnSF74p4q2");
console.log(`Balance: ${info.balanceTon.toLocaleString()} TON`);
```

> ⚠️ **JavaScript precision note:** TON balances can exceed `Number.MAX_SAFE_INTEGER`. Use `BigInt` for the raw nanoton value and only convert to `Number` for display purposes.

---

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 200 | Success | Parse `.json.data.detail` |
| 400 | Invalid address format | Validate address starts with `EQ`, `UQ`, or `0:` |
| 404 | Address not found | Address may be valid but never received TON (balance = 0) |
| 429 | Rate limited | Add exponential backoff; this is a free tier API |
| 5xx | Server error | Retry after a short delay |

**Checking for empty/uninitialized accounts:**
```bash
curl -s "https://api.tonscan.com/api/bt/getAddressInformation?address=..." \
  | jq 'if .json.data.detail.balance == "0" then "Empty wallet" else "Has funds" end'
```

---

## Rate Limits & Usage

- **Free tier, no API key required**
- No official rate limit is published; treat as a shared public resource
- For production use or high-volume lookups, add `429` retry logic with exponential backoff
- For exploratory/one-off queries, no special handling needed

---

## Displaying Results to Users

Always format balances with full precision and comma separators:
```
✅  1,296,986,856.910034 TON
❌  1296986856.910034
❌  1296986857 TON  (rounded — loses nanoton precision)
```

When showing to non-technical users, rounding to 2–4 decimal places is fine for readability, but note that full precision is available.
