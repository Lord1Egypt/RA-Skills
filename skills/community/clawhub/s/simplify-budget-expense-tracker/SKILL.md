---
name: simplify-budget
description: "Log, find, update, and delete expenses and income in the Simplify Budget Google Sheet, and answer read-only recurring schedule questions. NEVER use sessions_spawn or ACP — ONLY use the exec tool to run bash scripts. Categories are hardcoded in this skill — NEVER invent category names, ALWAYS pick from the exact list provided. Income uses name, account, source, and notes. For edits/deletes, find rows first, then mutate by transaction id. Amounts are always stored in the configured tracker currency. Just do it."
version: 1.2.0
user-invocable: true
metadata:
  openclaw:
    primaryEnv: GOOGLE_SA_FILE
    emoji: "💸"
    requires:
      env:
        - GOOGLE_SA_FILE
        - SPREADSHEET_ID
        - TRACKER_CURRENCY
      bins:
        - curl
        - jq
        - python3
        - openssl
---

# Simplify Budget Tracker

> **CRITICAL EXECUTION RULE**: You MUST use the `exec` tool to run the bash scripts below. Do NOT call `sessions_spawn`. Do NOT create ACP sessions. These are standalone shell scripts. Resolve script paths relative to this skill directory and run the resulting absolute path with `exec`.

## 🔴 SCRIPT-FIRST RULE — NON-NEGOTIABLE

**You are not allowed to answer any question about expenses, income, recurring items, or budget data from memory or conversation history. Ever. Not once.**

Every single response must begin by running the appropriate script from the list below. The script output is your only source of truth. Conversation history, prior responses, and your own assumptions are all irrelevant and must be ignored.

| User asks about | Run this script first |
|---|---|
| Today's / a specific date's expenses | `find_expenses.sh --date YYYY-MM-DD --limit 20` |
| A specific expense (to find, fix, or delete) | `find_expenses.sh "<query>" 10` |
| Monthly spending totals | `find_summary.sh --month YYYY-MM` |
| Today's / a specific date's income | `find_income.sh --date YYYY-MM-DD --limit 20` |
| A specific income entry | `find_income.sh "<query>" 10` |
| Recurring items | `find_recurring.sh --month YYYY-MM` or `find_recurring.sh --query "<name>"` |
| Logging a new expense | `log.sh "<user message>"` |
| Logging new income | `write_income.sh` |

If you have not run the script yet, you have not started your response yet. Run the script. Then respond conversationally based on what it returns.

## ⛔ CATEGORY RULES — READ BEFORE ANYTHING ELSE

**WRONG** (never do this):
> "Here are suggested categories: Fuel/Transport, Food & Drink, Medical/Pharmacy. Please confirm."

**CORRECT** (always do this):
> "Here's what I'll log: Shell → Transport 🚙, Baker's Cottage → Groceries 🍎, Klinik → Medical 🩺. Shall I go ahead?"

Rules that must never be broken:
1. Category names MUST come from the exact list below — never invent names like "Fuel/Transport" or "Food & Drink"
2. Always confirm with the user before writing — relay the `question` field from `preview_expense.sh` verbatim
3. NEVER say "your choice" or ask the user to pick from a list — the script picks and you relay its suggestion
4. DO NOT call `get_categories.sh` — the full category list is hardcoded right here:

| Formula | Name |
|---|---|
| `=zategory1` | Housing 🏡 |
| `=zategory2` | Transport 🚙 |
| `=zategory3` | Groceries 🍎 |
| `=zategory4` | Dining Out 🍕 |
| `=zategory5` | Personal Care ❤️ |
| `=zategory6` | Shopping 🛍️ |
| `=zategory7` | Utilities 💡 |
| `=zategory8` | Fun 🎬 |
| `=zategory9` | Business 💻️ |
| `=zategory10` | Other ❓ |
| `=zategory11` | Donation 🕌 |
| `=zategory12` | Childcare 🐣 |
| `=zategory13` | Travel ✈️ |
| `=zategory14` | Zakat 🌟 |
| `=zategory15` | Debt Payment 💸 |
| `=zategory16` | Fitness 💪 |
| `=zategory17` | Family Support 🏘️ |
| `=zategory18` | Taxes 💵 |
| `=zategory19` | Maintenance 🧰 |
| `=zategory20` | Painting 🎨 |
| `=zategory21` | TestGround 🤖 |
| `=zategory22` | Learning 📚 |
| `=zategory23` | Sports 🏀 |
| `=zategory24` | Pet 🐶 |
| `=zategory25` | Gifts 🎁 |
| `=zategory26` | Special Occasions 🥰 |
| `=zategory27` | Dress 👚 |
| `=zategory28` | Hobby 🪂 |
| `=zategory29` | Insurance 🛡️ |
| `=zategory30` | Medical 🩺 |

These are the ONLY valid categories. Use the name exactly as shown above (including emoji) when confirming with the user.

## When to use
- The user mentions spending money, making a purchase, paying for something
- The user says things like "I spent X on Y", "X euros for coffee", "paid X for Y", "log X"
- The user asks to fix, correct, undo, or update the last expense entry
- The user asks to search for or identify an existing expense
- The user asks what they've spent or asks about their budget
- The user wants to add an expense to their budget tracker
- The user wants to log income, salary, withdrawal, remittance, sale proceeds, or any other incoming money
- The user asks what recurring payments are due this month, when something recurring is due, or what subscriptions are upcoming

## Configuration
Required environment variables:
- `GOOGLE_SA_FILE` — absolute path to the Google service account JSON file
- `SPREADSHEET_ID` — the Simplify Budget spreadsheet ID
- `TRACKER_CURRENCY` — the base currency code for the tracker (for example `EUR`)

Optional environment variables:
- `TRACKER_CURRENCY_SYMBOL` — display symbol for the base currency (for example `€`)

## ⛔ NEVER ASK THE USER TO REFORMAT

If the user says "log a pencil for 10 euro under business" — log it. Do not ask the user to rephrase, reformat, or provide the amount differently. Extract what you need from their message and run the script. This applies to every possible phrasing. The model's job is to parse natural language, not to ask the user to become a CLI.

If a script returns an error, report the actual error message. Never invent an error or silently fail.

## Currency Rules
- The configured `TRACKER_CURRENCY` is the system of record for stored amounts.
- If the user gives an amount without a currency, assume it is already in `TRACKER_CURRENCY`.
- If the user gives an explicit foreign currency, keep that currency in the amount argument you pass to the script, for example `"50 MYR"` or `"12 USD"`.
- The scripts handle natural language amounts directly. Pass these as-is:
  - `"10 euro"` → `--amount "10 euro"` ✅
  - `"€10"` → `--amount "€10"` ✅
  - `"10 euros"` → `--amount "10 euros"` ✅
  - `"50 ringgit"` → `--amount "50 ringgit"` ✅
  - `"12 dollars"` → `--amount "12 dollars"` ✅
  - `"10"` → `--amount "10"` ✅
- The scripts fetch a live ECB FX rate, convert into `TRACKER_CURRENCY`, and store the converted amount in the sheet.
- When conversion happens, the scripts append an `[auto-fx]` audit line to `notes` with the original amount, converted amount, rate, and rate date.
- Never read the sheet to discover the base currency during normal operation. Use the configured environment instead.

## Category Matching Rules
1. Use the category list in the ⛔ CATEGORY RULES section above — never call `get_categories.sh` during normal operation
2. The script picks the category and generates the confirmation question — relay it verbatim, do not pick or rephrase.
3. Pass the plain English category name to the script (e.g. `"Dining Out"`, `"Business"`, `"Transport"`). The script resolves it to the correct formula internally. Never construct `=zategory{N}` yourself.
4. Disambiguation hints:
   - Coffee or café → Dining Out
   - Netflix/Spotify/streaming → Utilities
   - Concert, bar, night out → Fun
   - Gym or fitness class → Fitness
   - Doctor, pharmacy, clinic → Medical
   - Clothes, shoes, fashion → Dress
   - Electronics, gadgets, general retail → Shopping
   - Birthday gift or present → Gifts
   - Flight, hotel, vacation → Travel
   - Daily commute, taxi, fuel → Transport
   - Books, courses, online learning → Learning
   - Zakat → Zakat
   - Test entry → TestGround (only if user says it's a test)

## Workflows

### Log a new expense

When the user mentions spending money, buying something, paying for something, or asks to log an expense — follow this flow:

**Step 1 — Preview:**
```
bash <skill_dir>/scripts/log.sh --preview "<user's message, word-for-word>"
```
Pass the raw message. Do not reformat. Add `--date YYYY-MM-DD` if the user names a date, `--account "<name>"` if they name an account (default is Cash).

The script parses amount, description, and category. It returns JSON with `question`, `category`, `explicitCategory`, and `categorySource`.

**Step 2 — Confirm or write directly:**
- If `explicitCategory` is `true`: skip confirmation, go straight to Step 3.
- If `categorySource` is `"builtin"` or `"learned"`: relay the `question` field verbatim and wait for the user's reply.
- Otherwise: relay the `question` field (it includes a "best guess" note) and wait.

When the user replies:
- **"yes"** → proceed with the proposed category
- **A category name** (e.g. "Transport") → use that category instead
- **"no" / "cancel"** → stop

**Step 3 — Write:**
```
bash <skill_dir>/scripts/log.sh "<user's message>" --category "<confirmed category>"
```
The script writes to the sheet and outputs a `REPLY:` line. Send everything after `REPLY: ` verbatim. Do not paraphrase.

**Examples:**

- User: `i bought a pencil for 10 euro under business category`
  → preview detects explicit category → write directly (no confirmation needed)

- User: `spent 23 on mcdonalds`
  → preview suggests Dining Out (builtin match) → ask "Log mcdonalds under Dining Out 🍕?" → on yes, write

- User: `€12 coffee`
  → preview suggests Dining Out → confirm → write

**Rules:**
1. Never edit or reformat the user's message. Pass it verbatim.
2. Never ask the user to rephrase. The script handles any phrasing.
3. For multiple expenses in one message (e.g. "10 on coffee and 5 on parking"), run the preview → confirm → write flow once per expense, sequentially.
4. Duplicate check: if the write step outputs `DUPLICATE_FOUND:`, tell the user and ask if they want to log anyway. If yes, re-run with `--skip-duplicate-check`.
5. Relay `REPLY:` lines verbatim — do not paraphrase or confirm from memory.

### Log an expense from a receipt image

When the user uploads a receipt image or asks you to log a receipt:

1. Read the receipt visually and extract the likely:
   - merchant
   - final charged total or grand total
   - transaction date if visible
   - broad purchase type
2. Default to exactly one expense row per receipt.
3. Do NOT create one expense per line item unless the user explicitly asks to split the receipt.
4. Prefer the actual charged total, final total, or grand total.
   - Do not use subtotal unless that is the only total shown.
   - Do not sum visible item lines if a final total is already present.
5. Use the merchant name or a short summary as the `description`.
6. Best-match the whole receipt into one real category using the **Active Categories** table above.
7. If the receipt is materially mixed, such as fuel plus snacks:
   - default to one expense using the dominant purpose
   - ask one short clarification only if the split is important or the category is genuinely ambiguous
8. Then run the normal expense write flow.

Examples:
- grocery receipt with 10 items -> one Groceries expense using the grand total
- restaurant receipt with food and tax lines -> one Dining Out expense using the final total
- petrol station receipt with mostly fuel and a small snack -> one Transport expense by default unless the user asks to split it

### Find or inspect expenses

When the user wants to inspect, fix, or delete an expense, resolve it from the sheet first:

1. Build a short natural-language query from the user's message.
2. Search the sheet:
   ```
   bash <skill_dir>/scripts/find_expenses.sh "<query>" 10
   ```
3. Matching MUST consider both `description` and `notes`.
4. If one clear match exists, proceed. If multiple plausible matches exist, ask one short disambiguation question.

### Log a new income

When the user provides income (amount + name, with optional date/account/source/notes):

1. Extract from the user's message:
   - `amount` — required. If the user mentions a foreign currency, preserve it in the amount string you pass to the script, for example `"500 USD"` or `"1000 MYR"`. If they give no currency, pass a plain number.
   - `name` — required. This is the income title, e.g. `Salary`, `BMW Sale`, `Etoro withdrawal`
   - `date` — in YYYY-MM-DD format. Default to today if not specified.
   - `account` — default to `Other` if not specified.
   - `source` — default to `Other` if not specified. Use the user’s wording when it is clear, e.g. `Salary`, `Capital Gains`, `Remittance`, `Crypto`, `MTS`.
   - `notes` — optional supporting context.

2. Write the income:
   ```
   bash <skill_dir>/scripts/write_income.sh "<amount_or_amount_with_currency>" "<name>" "<YYYY-MM-DD>" "<account>" "<source>" "<notes>"
   ```

3. Confirm to the user in a concise way:
   "✅ Logged income [name] — [amount] into [account] from [source] on [date]"
   Include notes only when present.

### Find or inspect income

When the user wants to inspect, fix, or delete income, resolve it from the sheet first:

1. Build a short natural-language query from the user's message.
2. Search the sheet:
   ```
   bash <skill_dir>/scripts/find_income.sh "<query>" 10
   ```
3. Matching MUST consider `name`, `source`, and `notes`.
4. If one clear match exists, proceed. If multiple plausible matches exist, ask one short disambiguation question.

### Check today's or a specific day's expenses

Triggers: "check my expenses for today", "what are my expenses today", "what did I spend today", "show me today's expenses", "expenses for [date]", "what did I spend on [date]", or any question about spending on a specific day.

**Always run `find_expenses.sh` with a date filter. This is not optional.**
```
bash <skill_dir>/scripts/find_expenses.sh --date <YYYY-MM-DD> --limit 20
```
- Use the script output to answer. Never use conversation history or memory.
- If the script returns entries, list them: `[description] — [amount] under [category] ([account])`
- Only say "no expenses for today" if the script returns an empty array `[]`.

**`find_summary.sh` is for month-level questions only. Never use it for today/yesterday/specific-date queries.**

### Read monthly totals

Triggers: "what did I spend this month", "what's my income this month", "monthly totals", "how much did I save this month". These are month-level questions with no specific date.

```
bash <skill_dir>/scripts/find_summary.sh --month YYYY-MM
```

Rules:
1. This is read-only.
2. `Dontedit` is the source of truth for monthly totals.
3. Never use `find_summary.sh` for today/yesterday or any specific date — that always goes to `find_expenses.sh`.
4. Respond concisely with income, spending, and savings when available.

### Inspect recurring schedule

When the user asks read-only recurring questions like:
- `what is due this month`
- `when is capcut due`
- `what subscriptions are due next`

Use the recurring query script. Do NOT write anything into `Expenses` or `Income`.

Examples:
```
bash <skill_dir>/scripts/find_recurring.sh --month 2026-03
bash <skill_dir>/scripts/find_recurring.sh --query "CapCut" --date 2026-03-28
bash <skill_dir>/scripts/find_recurring.sh --query "CapCut" --mode next --date 2026-03-28
```

Rules:
1. This is read-only. Never materialize recurring rows into the ledgers.
2. The script calculates cycles from `Recurring` using the same recurrence rules as the existing Apps Script logic.
3. For month-style questions, return the current-month cycle entries.
4. For `when is X due`, prefer `--mode next`.
5. Respond concisely with the due date, amount, account, and whether it is expense or income.

### Fix or delete recurring items

When the user wants to change or delete a recurring item in the `Recurring` tab:

1. Resolve the target recurring row using `find_recurring.sh`.
2. If one clear match exists, mutate the `Recurring` row itself. Never write anything into `Expenses` or `Income` for this task.
3. To update a recurring row, use `__KEEP__` for unchanged fields and `__CLEAR__` for optional end date / notes / source:
   ```
   bash <skill_dir>/scripts/update_recurring.sh "<recurring_id>" "<YYYY-MM-DD_or___KEEP__>" "<name_or___KEEP__>" "<category_or___KEEP__>" "<expense_or_income_or___KEEP__>" "<Monthly_or_Quarterly_or_Yearly_or___KEEP__>" "<amount_or___KEEP__>" "<account_or___KEEP__>" "<YYYY-MM-DD_or___KEEP___or___CLEAR__>" "<notes_or___KEEP___or___CLEAR__>" "<source_or___KEEP___or___CLEAR__>"
   ```
4. To delete a recurring row, clear the row by recurring id:
   ```
   bash <skill_dir>/scripts/delete_recurring.sh "<recurring_id>"
   ```
5. Confirm concisely what changed.

### Add a recurring item

When the user wants to add a recurring expense or recurring income to the `Recurring` tab:

1. Extract:
   - `start_date` in `YYYY-MM-DD`
   - `name`
   - `category` must use the live active category list; never invent a category
   - `type` as `expense` or `income`
   - `frequency` as `Monthly`, `Quarterly`, or `Yearly`
   - `amount`
   - optional `account`, `end_date`, `notes`, `source`
2. Write it with:
   ```
   bash <skill_dir>/scripts/write_recurring.sh "<YYYY-MM-DD>" "<name>" "<category>" "<expense_or_income>" "<Monthly_or_Quarterly_or_Yearly>" "<amount>" "<account>" "<YYYY-MM-DD_optional_end_date>" "<notes>" "<source>"
   ```
3. This must reuse the first empty row in `Recurring` starting from row 6, matching the SB_LIVE hole-reuse behavior.
4. Recurring categories follow SB_LIVE rules:
   - expense recurring items must store a `=zategory<stableId>` formula — use the **Active Categories** table above to resolve it
   - recurring income is the only case that may store the literal `Income 💵`
5. Never ask the user to pick a category unless they explicitly want to choose. Best-match into an existing category.
6. Confirm concisely.

### Fix or correct income

When the user wants to change amount, name, date, account, source, or notes for an income row:

1. Resolve the target income from the sheet using `find_income.sh`. Do NOT trust chat memory as the source of truth.
2. Infer the correction from their message. If the new amount is in a foreign currency, preserve that currency in the amount argument you pass to the script.
3. Run the update. Use `__KEEP__` for unchanged fields and `__CLEAR__` to blank notes:
   ```
   bash <skill_dir>/scripts/update_income.sh "<transaction_id>" "<amount_or_amount_with_currency_or___KEEP__>" "<name_or___KEEP__>" "<YYYY-MM-DD_or___KEEP__>" "<account_or___KEEP__>" "<source_or___KEEP__>" "<notes_or___KEEP___or___CLEAR__>"
   ```
4. Confirm: "✅ Updated income — now [name] — [amount] into [account] from [source]"

### Delete income

If the user asks to undo or delete an income entry:

1. Resolve the target income from the sheet using `find_income.sh`.
2. If there is one clear match, clear the row by transaction id:
   ```
   bash <skill_dir>/scripts/delete_income.sh "<transaction_id>"
   ```
3. Confirm that the income row was cleared.
4. Never delete sheet rows. Clear the existing row contents instead.


### Fix or correct the last expense

When the user says things like "fix that", "that was wrong", "change the amount", "put that under X instead", "it was 4 not 5", "actually that was yesterday", "actually I bought that on [date]", "wrong date":

1. Run `find_expenses.sh` to resolve the target from the sheet. Do not use chat memory.
2. Infer the correction (amount, category, description, date, account, notes).
3. Run the update. Use `__KEEP__` for unchanged fields, `__CLEAR__` to blank notes. Pass category as plain English name:
   ```
   bash <skill_dir>/scripts/update_expense.sh --id "<transaction_id>" --amount "<amount_or___KEEP__>" --description "<description_or___KEEP__>" --category "<category_name_or___KEEP__>" --date "<YYYY-MM-DD_or___KEEP__>" --account "<account_or___KEEP__>" --notes "<notes_or___KEEP___or___CLEAR__>"
   ```
4. Relay the `REPLY:` line from the script output word for word.

### Undo / delete last expense
If the user asks to undo or delete an entry:

1. Run `find_expenses.sh` to resolve the target from the sheet.
2. If one clear match, delete it:
   ```
   bash <skill_dir>/scripts/delete_expense.sh "<transaction_id>"
   ```
3. Relay the `REPLY:` line from the script output word for word.
4. Never delete sheet rows — the script clears the row contents.

## Rules
- Pass category as plain English to scripts — never construct `=zategory{N}` yourself
- Do NOT call `get_categories.sh` at runtime — the category table is hardcoded in the scripts
- For income, use the explicit `name`, `account`, `source`, and `notes` fields.
- Relay `REPLY:` lines from scripts verbatim — do not paraphrase or confirm from memory
- Never include transaction IDs or internal record IDs in any response
- Never use conversation history as evidence of what is or isn't in the sheet — always check the sheet
- Always relay what the script confirmed — the user should never have to guess if it worked
- If a script returns an error, tell the user clearly and do not silently retry
- Default date is always today in the user's local timezone
- Default account is always "Revolut" unless the user specifies otherwise
- Default income account is always "Other" unless the user specifies otherwise
- Default income source is always "Other" unless the user specifies otherwise
- Amounts are always stored as plain numbers in `TRACKER_CURRENCY`
- If a foreign currency is provided, keep it in the script input and let the script convert it into `TRACKER_CURRENCY`
- Notes are a first-class field. Search them, preserve them on update unless changed, and clear them on delete.
- The sheet is always the source of truth — for reads, edits, deletes, and duplicate checks.
- Recurring schedule questions are read-only. Never create expense or income rows just because the user asked what is due.
- The 🤖 label on written rows identifies bot-added entries in the sheet
