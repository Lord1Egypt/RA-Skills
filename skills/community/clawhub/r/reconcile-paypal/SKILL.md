---
name: paypal-reconcile
description: Read-only PayPal transaction reconciliation for OpenClaw. Finds a transaction by approximate date, amount, and currency using a narrow search window, identifies the downstream merchant, and captures accounting evidence with minimal browser round-trips.
version: 1.0.1
metadata:
  openclaw:
    emoji: "💳"
---

# PayPal Reconcile

## Purpose

Use this skill to reconcile a PayPal-backed credit-card charge against PayPal transaction history.

Typical user requests include:
- find a PayPal transaction
- reconcile a PAYPAL credit-card charge
- identify the real merchant behind a PayPal charge
- retrieve PayPal transaction details
- obtain accounting evidence or a receipt for a PayPal transaction

This skill is optimized for fast, read-only lookup of a single known or approximate transaction.

## Browser

Use OpenClaw's native `browser` tool only.

Always use the persistent browser profile:

`alibaba`

Never invoke `openclaw browser` using Bash, exec, shell, terminal, or any other command runner from inside the agent.

Do not launch a temporary or fresh browser profile.

If the native browser tool is unavailable, STOP and return:

`BROWSER_TOOL_UNAVAILABLE`

Do not fall back to Bash, exec, shell, or terminal commands.

## Safety

This skill is READ ONLY.

Allowed:
- open PayPal
- read transaction activity
- filter or search transactions
- open transaction details
- download reports
- download receipts
- save or export transaction evidence as PDF

Never:
- send money
- request money
- issue refunds
- cancel payments
- dispute transactions
- change account settings
- change payment methods
- add or remove cards
- add or remove bank accounts
- change security settings
- change PayPal profile information

If any workflow could move money or modify account state, STOP.

## Authentication

Never ask the model to enter:
- PayPal passwords
- OTP codes
- authenticator codes
- recovery codes
- security answers
- other credentials

If PayPal shows a login page, OTP request, CAPTCHA, Security Challenge, unusual account verification, or device approval:

STOP and return:

`PAYPAL_LOGIN_REQUIRED`

Explain what manual action is required.

After the operator manually completes authentication in the same persistent `alibaba` browser profile, the lookup may be resumed.

## Input

A request may include:
- credit-card transaction date
- credit-card posting date
- approximate PayPal transaction date
- amount
- currency
- card description / descriptor
- approximate merchant
- statement row ID

For a normal fast lookup, the preferred minimum input is:
- approximate date
- amount
- currency

# Performance Rules

This skill MUST minimize browser round-trips.

For a lookup with a known approximate date:

1. NEVER select an entire year, year-to-date, all transactions, or a large historical range unless:
   - the user explicitly requests it, or
   - the narrow search fails and expansion is necessary.

2. Calculate a default search window of:
   - `target_date - 3 calendar days`
   - through `target_date + 3 calendar days`

3. Filter PayPal directly to that narrow date range.

4. After the filtered transaction list loads, inspect the relevant transaction list in ONE operation whenever possible.

5. Prefer, in this order:
   - browser evaluate returning structured transaction row text
   - selector-scoped browser snapshot
   - efficient/compact transaction-list snapshot

6. Do NOT visually inspect unrelated rows one by one.

7. Do NOT scroll through months manually when a date filter is available.

8. Search the extracted transaction data locally for:
   - exact amount
   - currency
   - date proximity
   before opening any transaction detail.

9. Only open plausible candidate transaction(s).

10. Avoid screenshots for matching unless DOM/text extraction fails.

11. Avoid unnecessary intermediate snapshots after predictable UI actions.

12. Target approximately 5-7 browser operations for a normal exact-amount lookup:
   - open/focus PayPal Activity
   - set narrow date range
   - extract transaction rows
   - open candidate
   - extract details
   - capture/download evidence

Guiding principle:

**AI navigates; extracted text/data searches. AI should not visually hunt through transaction rows.**

# Fast Search Procedure

Given:
- target date
- target amount
- target currency

calculate:
- `search_start = target_date - 3 days`
- `search_end = target_date + 3 days`

Then:

1. Open or focus the existing PayPal Activity / Transactions page.
2. If PayPal is already on transaction activity, do not navigate through unnecessary dashboard pages.
3. Confirm the account is logged in. If not, return `PAYPAL_LOGIN_REQUIRED`.
4. Set a CUSTOM DATE RANGE from `search_start` through `search_end`.
5. NEVER change the filter to whole year, year-to-date, or all transactions unless the narrow search fails or the user explicitly asks for a broad search.
6. Wait only until the transaction list has updated.
7. Extract the filtered transaction rows in one bounded operation.
8. Prefer structured extraction. Return, when available:
   - date
   - merchant / recipient
   - amount text
   - currency
   - status
   - row text
   - candidate link or stable reference
9. Compare extracted rows against exact amount, exact currency when displayed, and date within the search window.
10. If exactly one plausible candidate matches, open that transaction.
11. If multiple candidates have the same amount, open only those candidates and compare merchant, exact date, payment source, invoice/order reference, and status.
12. If no candidate exists in the +/-3-day window, expand once to +/-7 days and repeat the same narrow extraction strategy.
13. Only if the +/-7-day search still fails may the agent broaden further, and it must explain why.
14. Extract the chosen transaction detail in one bounded operation.
15. Return one of:
   - `MATCHED`
   - `AMBIGUOUS`
   - `NOT_FOUND`
   - `PAYPAL_LOGIN_REQUIRED`
   - `BROWSER_TOOL_UNAVAILABLE`

Never choose randomly between ambiguous candidates.

# Transaction List Extraction

After applying the date filter, prefer browser evaluate or a scoped/efficient snapshot over visual scanning.

Use browser evaluate only to READ data already rendered by PayPal.

Preferred conceptual output:

```json
[
  {
    "date": "2026-05-20",
    "merchant": "Example Merchant",
    "amount_text": "USD 325.00",
    "status": "Completed",
    "row_text": "..."
  }
]
```

Do not:
- modify the DOM
- execute network requests from page JavaScript
- trigger payments or account changes
- scrape unrelated pages
- use evaluate to bypass security controls

If the page structure is unknown:
1. take one efficient snapshot
2. identify the transaction-list container
3. then extract only that container or its rendered rows

# Matching Priority

Use evidence in this order:
1. Exact PayPal transaction ID or reference
2. Exact amount and currency
3. PayPal transaction date near the card charge date
4. Merchant or recipient consistent with card descriptor
5. Payment source consistent with the expected card
6. Invoice ID, order ID, description, or other reference

Do not assume the credit-card posting date equals the PayPal transaction date.

# Matching Rules

If exactly one candidate clearly matches:

`STATUS = MATCHED`

If more than one plausible candidate exists:

`STATUS = AMBIGUOUS`

If no plausible transaction is found after allowed search expansion:

`STATUS = NOT_FOUND`

Never invent a transaction.

# Transaction Details

For a plausible or confirmed candidate, collect when available:
- PayPal transaction date
- merchant / recipient name
- merchant email if displayed
- transaction amount
- currency
- PayPal transaction ID
- invoice ID
- order/reference ID
- payment method
- status
- description
- fees if relevant
- source URL

Always record the downstream merchant / recipient when PayPal reveals it.

# Evidence

For a confirmed match:
1. Prefer an official downloadable PayPal receipt, transaction document, or relevant report if available.
2. If PayPal does not provide suitable downloadable evidence, create PDF evidence from the transaction-detail page.

The evidence should clearly show, when available:
- merchant / recipient
- transaction date
- amount
- currency
- PayPal transaction ID
- status

Do not capture unrelated private account information when avoidable.

# Evidence Filename

Rename evidence using:

`YYYY-MM-DD_PAYPAL_CURRENCY-AMOUNT_TRANSACTIONID.pdf`

Example:

`2026-05-20_PAYPAL_USD-325.00_9AB12345CD678901E.pdf`

Do not leave generic names such as `receipt.pdf`, `download.pdf`, or `document.pdf`.

# Confidence

Suggested confidence:
- `95-100`: exact amount, currency, date proximity, and transaction/merchant evidence strongly agree
- `85-94`: amount and currency exact, with strong date and merchant evidence
- `70-84`: likely match but some evidence is missing
- `<70`: do not auto-match

If confidence is below 85, flag the result for review.

# Output

Return structured results using:

```text
STATUS:
MATCHED | AMBIGUOUS | NOT_FOUND | PAYPAL_LOGIN_REQUIRED | BROWSER_TOOL_UNAVAILABLE

PLATFORM:
PayPal

CARD_DATE:

CARD_AMOUNT:

CARD_CURRENCY:

MERCHANT:

PAYPAL_TRANSACTION_DATE:

PAYPAL_TRANSACTION_ID:

INVOICE_ID:

ORDER_OR_REFERENCE_ID:

PAYPAL_AMOUNT:

PAYPAL_CURRENCY:

PAYMENT_METHOD:

TRANSACTION_STATUS:

FEES:

EVIDENCE_FILE:

SOURCE_URL:

CONFIDENCE:

NOTES:
```

For `AMBIGUOUS`, list only plausible candidates.

For `NOT_FOUND`, report:
- search windows attempted
- amount
- currency
- whether authentication/browser access was healthy

# Example Fast Lookup

User request:

`Find the PayPal transaction for USD 325.00 around May 20, 2026.`

Preferred behavior:
1. focus PayPal Transactions
2. filter May 17-May 23, 2026
3. extract all rows once
4. find USD 325.00 locally
5. open only the plausible candidate
6. extract transaction details
7. save evidence
8. return structured result

Do NOT switch directly to all of 2026.
