---
name: finance
description: >
  Manage personal finances: record expenses, income, transfers, check balances, and generate reports.
  TRIGGER when: user asks to record a transaction, expense, income, transfer between wallets, check balance,
  or get a spending report. Keywords: трата, расход, доход, перевод, баланс, отчёт, потратил, заработал,
  купил, оплатил, списание, пополнение, кошелёк, expense, income, transfer, balance, report.
  Do NOT trigger for: creating/modifying database structure.
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Finance Skill

Record and query personal financial data stored in PostgreSQL via the `assistant` CLI.

## Commands Reference

All commands: `assistant <command> [json-args]`
Output: JSON to stdout on success, error to stderr with exit code 1.

| Command | Arguments | Description |
|---|---|---|
| `create-expense` | amount, walletId, currencyCode, categoryId, description? | Record an expense |
| `create-income` | amount, walletId, currencyCode, description? | Record income |
| `create-transfer` | amount, walletId, currencyCode, toWalletId, toCurrencyCode, toAmount, description? | Transfer between wallets |
| `list-transactions` | walletId?, categoryId?, type?, limit?, offset?, dateFrom?, dateTo? | List transactions |
| `delete-transaction` | id | Delete a transaction |
| `get-wallets` | — | Get all wallets with balances |
| `get-wallet-balance` | walletId | Get wallet balance |
| `create-wallet` | name | Create a wallet |
| `get-categories` | — | Get all categories |
| `create-category` | name | Create a category |
| `delete-category` | id | Delete a category |
| `spending-report` | groupBy, walletId?, dateFrom?, dateTo? | Spending report |

## Transaction Types

### 1. Expense (Трата)

- Use `assistant create-expense '{"amount":"100","walletId":"...","currencyCode":"ARS","categoryId":"..."}'`
- Amount is always positive — the system negates it automatically
- Requires: amount, walletId, currencyCode, categoryId
- Optional: description

### 2. Income (Пополнение)

- Use `assistant create-income '{"amount":"5000","walletId":"...","currencyCode":"ARS"}'`
- Amount is positive
- Requires: amount, walletId, currencyCode
- Optional: description

### 3. Transfer (Перевод)

- Use `assistant create-transfer '{"amount":"100","walletId":"...","currencyCode":"USD","toWalletId":"...","toCurrencyCode":"USD","toAmount":"100"}'`
- The system creates two linked transactions automatically
- Requires: amount, walletId, currencyCode, toWalletId, toCurrencyCode, toAmount
- Optional: description
- For same-currency transfers, `toAmount` equals `amount`

## Workflow

### Step 1: Parse the Request

Extract from the user's message:

- **Amount** — number (always positive)
- **Currency** — currency code (e.g. ARS, RUB, USDT)
- **Description** — what was bought / reason for transaction (optional)
- **Wallet** — which wallet to use
- **Category** — spending category (required for expenses only)
- **Type** — expense, income, or transfer (infer from context)

### Step 2: Resolve References

Before creating a transaction:

1. Run `assistant get-wallets` to find the correct wallet ID
2. Run `assistant get-categories` to find the correct category ID
3. If category doesn't exist, ask the user or create it with `assistant create-category '{"name":"..."}'`

### Step 3: Handle Ambiguity

If any required field is unclear or missing, ask the user **one concise clarifying question**. Common cases:

- Wallet not specified and user has multiple wallets
- Category is ambiguous
- Amount is missing
- Transfer destination unclear

Do NOT guess — ask. But do NOT over-ask if the context is obvious.

### Step 4: Create the Transaction

Run the appropriate command (`assistant create-expense`, `assistant create-income`, or `assistant create-transfer`) with the resolved data as a JSON argument.

### Step 5: Report Back

After creating the transaction, run `assistant get-wallet-balance '{"walletId":"..."}'` and reply with a **concise confirmation** including:

- What was created (description, amount, wallet, category)
- Updated wallet balance

Example reply format for an expense:

```
Записал: Булочка -200 ARS (Наличка ARS, Продукты)
Баланс Наличка ARS: 15 300 $
```

Example reply format for a transfer:

```
Перевод: 100 USD Tinkoff → Наличка
Баланс Tinkoff: 500 $
Баланс Наличка: 300 $
```

## Constraints

- NEVER create transactions without confirming ambiguous details first
- Always respond in the same language as the user's message (default: Russian)
- Keep responses short and action-oriented — no unnecessary explanations
