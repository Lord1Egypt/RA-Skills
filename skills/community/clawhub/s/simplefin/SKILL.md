---
name: simplefin
description: Connects to bank accounts and fetches financial transactions via the SimpleFIN API. Use when the user wants to check bank balances, review recent transactions, track expenses, or connect to a new bank account using SimpleFIN. It automatically guides the user through the Setup Token claim process if they haven't connected before.
---

# SimpleFIN Bank Connection Skill

## Overview

The `simplefin` skill allows you to connect to the user's bank accounts to retrieve account balances and transaction history using the SimpleFIN Bridge API.

## Setup & Authentication (Always do this first!)

Before you can fetch any data, you need the user's **SimpleFIN Access URL**.

1. **Check if you have it:** Look for a stored URL in the workspace at `memory/simplefin_url.txt` or in the environment variables (e.g., `openclaw.json` under `SIMPLEFIN_ACCESS_URL`).
2. **Prompt the user if missing:** If you don't have the Access URL, you **must** ask the user for a **Setup Token**.
   - **Instruction to provide to the user:** 
     "To get started, I need a SimpleFIN Setup Token. 
      If you don't have one yet, here's how to get it:
      1. Go to [SimpleFIN Bridge](https://bridge.simplefin.org/) and sign up.
      2. Connect your bank accounts.
      3. Generate a **Setup Token** (a long string of characters).
      Please paste that Setup Token here so I can connect!"
3. **Claim the Token:** Once the user provides the Setup Token, use the script to claim it and get the Access URL:
   ```bash
   node scripts/simplefin_api.js claim "THE_SETUP_TOKEN_HERE"
   ```
   *The script will output the true Access URL (`https://username:password@...`).*
4. **Save it:** Save the Access URL to `memory/simplefin_url.txt` so the user doesn't have to provide it again in the future. **The Setup Token is single-use and cannot be used again.**

## Fetching Data

Use the provided Node.js script `scripts/simplefin_api.js` to interact with the API. It requires the `access_url` as the first argument.

### 1. List Accounts & Balances

To view all connected bank accounts and their current balances:

```bash
node scripts/simplefin_api.js "https://username:password@beta-bridge.simplefin.org/simplefin" accounts
```

*This will output a JSON array of accounts, including their IDs, names, currencies, and balances.*

### 2. List Transactions

To retrieve the transaction history across accounts:

```bash
node scripts/simplefin_api.js "https://username:password@beta-bridge.simplefin.org/simplefin" transactions [options]
```

**Options:**
- `--start-date YYYY-MM-DD`: Filter transactions on or after this date.
- `--end-date YYYY-MM-DD`: Filter transactions on or before this date.
- `--account "Account Name or ID"`: Filter transactions for a specific account.

**Example: Fetching transactions for March 2026**
```bash
node scripts/simplefin_api.js "https://username:password@beta-bridge.simplefin.org/simplefin" transactions --start-date 2026-03-01 --end-date 2026-03-31
```

## Processing Output

- Always format financial data clearly for the user (e.g., Markdown tables or bulleted lists).
- If the API returns an authentication error, remind the user that their SimpleFIN token might have expired or been revoked, and ask them to generate a new Setup Token.

## References
If you need to make changes to the SimpleFIN integration, look up error schemas, or review API limits, consult the developer guide:
- See [developer_guide.md](references/developer_guide.md) for the SimpleFIN setup token flow and API documentation.
