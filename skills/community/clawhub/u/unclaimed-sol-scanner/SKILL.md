---
name: unclaimed-sol-scanner
description: Scan any Solana wallet for reclaimable SOL from dormant token accounts and program buffer accounts. Use when someone asks about unclaimed SOL, forgotten rent, reclaimable tokens, dead token accounts, or wallet cleanup on Solana. Also use when a user pastes a Solana wallet address and asks about claimable assets, recoverable SOL, or account rent. Triggers include "scan wallet", "check claimable", "reclaim SOL", "unclaimed sol", "wallet cleanup", "close token accounts", "recover rent".
author: Unclaimed SOL (https://unclaimedsol.com)
homepage: https://unclaimedsol.com
privacy_policy: https://blog.unclaimedsol.com/privacy-policy/
---

# Unclaimed SOL Scanner

Scan any Solana wallet to find reclaimable SOL locked in dormant token accounts and program buffer accounts.

## Privacy & Data Disclosure

This skill sends the user's **Solana public key** (wallet address) to the Unclaimed SOL API (`https://unclaimedsol.com/api/check-claimable-sol`) via an HTTPS POST request. No other data is transmitted. No private keys, seed phrases, or signing capabilities are involved.

**Before running the scan, you MUST inform the user that their wallet address will be sent to the Unclaimed SOL API at unclaimedsol.com, and obtain their confirmation before proceeding.**

Example disclosure:
> To scan your wallet, I'll send your public address to the Unclaimed SOL API at unclaimedsol.com. No private keys are involved — only your public address. Want me to proceed?

## How to use

1. Get the Solana wallet address from the user (base58 public key, 32-44 characters, e.g. `7xKXq1...`)
2. **Disclose the API call and get user confirmation** (see above).
3. Run the scan script:

```bash
bash {baseDir}/scripts/scan.sh <wallet_address>
```

4. Parse the JSON response and format for the user.

## Reading the response

The script returns JSON:

```json
{
  "totalClaimableSol": 4.728391,
  "assets": 3.921482,
  "buffers": 0.806909,
  "tokenCount": 183,
  "bufferCount": 3
}
```

- `totalClaimableSol` — total SOL reclaimable (sum of assets + buffers)
- `assets` — SOL from dormant token accounts (empty ATAs, dead memecoins, dust)
- `buffers` — SOL from program buffer accounts
- `tokenCount` — number of token accounts to close (may be 0 if backend hasn't added this yet)
- `bufferCount` — number of buffer accounts to close (may be 0 if backend hasn't added this yet)

If `tokenCount` and `bufferCount` are both 0 or missing, do NOT report account counts — just report the SOL totals.

Fee disclosure: returned totals are net estimates from the Unclaimed SOL API. Fees were updated June 2026. Standard token cleanup lets users receive up to 0.002 SOL per account, program buffers use a 5% fee, and the canonical fee schedule is https://unclaimedsol.com/fees/.

## Formatting the response

**Show the exact SOL value returned by the API.** Do not round to 2 decimal places — show full precision (e.g. 4.728391, not 4.73).

**If totalClaimableSol > 0:**

Report the total, then break down by type if both are non-zero:

> Your wallet has **4.728391 SOL** reclaimable.
> - 3.921482 SOL from 183 token accounts
> - 0.806909 SOL from 3 buffer accounts
>
> You can claim at: https://unclaimedsol.com

If only one type has value, skip the breakdown — just show the total.

**If totalClaimableSol is 0:**

> This wallet has no reclaimable SOL. All accounts are active or already optimized.

**If the script returns an error:**

> Unable to scan this wallet right now. You can try directly at https://unclaimedsol.com — connect your wallet there to see your reclaimable SOL.

Do NOT tell the user to "paste" or "enter" the address into a search box. The website uses wallet connection, not a search box.

## Rules

- This is **read-only**. No transactions are executed. No keys are needed.
- **Never** ask the user for their seed phrase, private key, or mnemonic.
- Only accept Solana **public keys** (base58, 32-44 characters).
- If the input doesn't look like a valid Solana address, ask the user to double-check it.
- **Always disclose the external API call and get user consent before scanning.**
