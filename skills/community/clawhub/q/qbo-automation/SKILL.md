---
name: qbo-automation
description: >
  QuickBooks Online automation: chart of accounts setup, bank rule configuration,
  recurring transaction templates, reconciliation workflows, and journal entry generation.
  Use when a user needs to configure or automate QBO accounting operations. Domain-specific
  accounting knowledge included. NOT for tax filing, payroll processing, or direct QBO
  OAuth setup (use qbo-to-tax-bridge for tax mapping, and a separate auth skill for OAuth).
metadata:
  openclaw:
    requires:
      bins: []
    tags:
      - accounting
      - quickbooks
      - finance
      - automation
      - bookkeeping
---

# QBO Automation Skill

Automates QuickBooks Online operations: chart of accounts, bank rules, recurring transactions,
reconciliation, and journal entries. Backed by accounting domain knowledge.

---

## Prerequisites

- QBO account with admin or accountant access
- QBO API credentials (Client ID, Client Secret, Refresh Token) stored in environment:
  - `QBO_CLIENT_ID`
  - `QBO_CLIENT_SECRET`
  - `QBO_REFRESH_TOKEN`
  - `QBO_REALM_ID` (Company ID)
- Node.js or Python environment for API calls (or use QBO's web UI with guided steps below)

---

## 1. Chart of Accounts Setup

### Standard Account Hierarchy (US Small Business)

```
ASSETS
  1000  Checking Account              (Bank)
  1010  Savings Account               (Bank)
  1100  Accounts Receivable           (Accounts Receivable)
  1200  Inventory Asset               (Other Current Asset)
  1500  Computer Equipment            (Fixed Asset)
  1510  Accumulated Depreciation      (Fixed Asset)

LIABILITIES
  2000  Accounts Payable              (Accounts Payable)
  2100  Credit Card                   (Credit Card)
  2200  Payroll Liabilities           (Other Current Liability)
  2300  Sales Tax Payable             (Other Current Liability)
  2700  Notes Payable                 (Long Term Liability)

EQUITY
  3000  Owner's Equity                (Equity)
  3100  Owner's Draw                  (Equity)
  3200  Retained Earnings             (Equity)

INCOME
  4000  Services Revenue              (Income)
  4100  Product Sales                 (Income)
  4200  Other Income                  (Other Income)

COST OF GOODS SOLD
  5000  Cost of Goods Sold            (Cost of Goods Sold)

EXPENSES
  6000  Advertising & Marketing       (Expense)
  6010  Bank Charges & Fees           (Expense)
  6020  Dues & Subscriptions          (Expense)
  6030  Insurance                     (Expense)
  6040  Meals & Entertainment         (Expense)
  6050  Office Supplies               (Expense)
  6060  Professional Fees             (Expense)
  6070  Rent or Lease                 (Expense)
  6080  Utilities                     (Expense)
  6090  Vehicle Expense               (Expense)
  6100  Travel                        (Expense)
  6200  Payroll Expenses              (Expense)
  6300  Depreciation                  (Expense)
```

### QBO API — Create Account (Python/requests)

```python
import requests, json, base64, os

def get_access_token():
    """Exchange refresh token for access token."""
    credentials = base64.b64encode(
        f"{os.environ['QBO_CLIENT_ID']}:{os.environ['QBO_CLIENT_SECRET']}".encode()
    ).decode()
    resp = requests.post(
        "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer",
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "refresh_token",
            "refresh_token": os.environ["QBO_REFRESH_TOKEN"]
        }
    )
    return resp.json()["access_token"]

def create_account(access_token, realm_id, name, account_type, account_sub_type, acct_num=None):
    """Create a QBO account."""
    payload = {
        "Name": name,
        "AccountType": account_type,
        "AccountSubType": account_sub_type
    }
    if acct_num:
        payload["AcctNum"] = acct_num
    resp = requests.post(
        f"https://quickbooks.api.intuit.com/v3/company/{realm_id}/account",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        json=payload
    )
    return resp.json()

# Example: Create a new expense account
token = get_access_token()
realm = os.environ["QBO_REALM_ID"]
result = create_account(token, realm,
    name="Software Subscriptions",
    account_type="Expense",
    account_sub_type="OtherMiscellaneousExpense",
    acct_num="6025"
)
print(result)
```

### Bulk Account Import (CSV → QBO)

QBO supports bulk import via **Accountant Toolbox > Chart of Accounts > Import**.

CSV format:
```csv
Account Name,Type,Detail Type,Account Number,Description,Balance
Checking Account,Bank,Checking,1000,Main operating account,0
Accounts Receivable,Accounts receivable,Accounts Receivable (A/R),1100,,0
Software Subscriptions,Expense,Other Miscellaneous Service Cost,6025,SaaS tools,,
```

---

## 2. Bank Rules Configuration

Bank rules auto-categorize imported bank/credit card transactions.

### Rule Types
- **Category Rules** — assign account + class/location
- **Split Rules** — divide transaction across multiple accounts
- **Vendor Rules** — auto-assign payee name

### QBO UI Steps (no API — bank rules not in QBO API v3)

1. Go to **Banking > Rules > New rule**
2. Set:
   - Rule name: descriptive (e.g., "AWS Monthly Charges")
   - Apply to: Money out / Money in
   - Bank account: select account
   - Conditions:
     - `Description` **contains** `AMAZON WEB SERVICES`
   - Then:
     - Category: `Software Subscriptions (6025)`
     - Payee: `Amazon Web Services`
     - Class (if tracking): `Operations`
3. Save and run rule against unreviewed transactions

### Common Bank Rule Templates

| Rule Name | Condition | Category | Notes |
|-----------|-----------|----------|-------|
| AWS Charges | Description contains "AMAZON WEB SERVICES" | Software Subscriptions | |
| Stripe Payouts | Description contains "STRIPE" + Money In | Services Revenue | |
| Payroll - Gusto | Description contains "GUSTO" | Payroll Expenses | |
| Rent | Description contains "ACH RENT" | Rent or Lease | |
| Google Ads | Description contains "GOOGLE ADS" | Advertising & Marketing | |
| Bank Fee | Description contains "SERVICE FEE" | Bank Charges & Fees | |
| Owner Draw | Description contains "OWNER DRAW" | Owner's Draw | Equity |

### Split Rule Example (Mixed Expense)

- Rule: "Office & Meals Split"
- Condition: Payee is `Costco`
- Split:
  - 60% → Office Supplies (6050)
  - 40% → Meals & Entertainment (6040)

---

## 3. Recurring Transaction Templates

### Recurring Bill Template (API)

```python
def create_recurring_transaction(access_token, realm_id):
    """Create a monthly recurring bill template."""
    payload = {
        "RecurDataRef": {
            "type": "Bill",
        },
        "RecurType": "Scheduled",
        "ScheduleInfo": {
            "StartDate": "2026-01-01",
            "NextDate": "2026-04-01",
            "EndDate": None,
            "NumRemaining": None,
            "RecurFrequency": "Monthly",
            "IntervalType": "Monthly",
            "MaxOccurrences": None
        },
        "Name": "Monthly Rent - 123 Main St",
        "Active": True,
        "VendorRef": {"value": "VENDOR_ID_HERE"},
        "Line": [
            {
                "DetailType": "AccountBasedExpenseLineDetail",
                "Amount": 3500.00,
                "AccountBasedExpenseLineDetail": {
                    "AccountRef": {"value": "ACCOUNT_ID_FOR_RENT"}
                }
            }
        ]
    }
    resp = requests.post(
        f"https://quickbooks.api.intuit.com/v3/company/{realm_id}/recurringtransaction",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        json=payload
    )
    return resp.json()
```

### Common Recurring Templates

| Template | Type | Frequency | Amount | Account |
|----------|------|-----------|--------|---------|
| Office Rent | Bill | Monthly | Fixed | Rent or Lease |
| AWS | Bill | Monthly | Variable | Software Subscriptions |
| Liability Insurance | Bill | Monthly | Fixed | Insurance |
| Owner's Draw | Check | Bi-weekly | Fixed | Owner's Draw |
| Depreciation Entry | Journal Entry | Monthly | Calculated | Depreciation |

### Depreciation Journal Entry (Straight-Line)

Monthly entry template:
```
DEBIT  Depreciation Expense (6300)    $[amount]
CREDIT Accumulated Depreciation (1510) $[amount]
Memo: Monthly depreciation - [asset name]
```

---

## 4. Reconciliation Workflows

### Monthly Reconciliation Checklist

1. **Gather statements** — Download bank/CC statements for the period
2. **Review unreviewed transactions** — Banking > For Review; categorize all
3. **Run reconciliation** — Accounting > Reconcile > select account
4. **Match ending balance** to bank statement
5. **Investigate discrepancies**:
   - Duplicate transactions
   - Missing transactions (manually add)
   - Wrong amounts (edit/split)
   - Timing differences (outstanding checks/deposits)
6. **Finish reconciliation** — generate reconciliation report
7. **Document** — save PDF of reconciliation report

### Reconciliation Discrepancy Quick-Fix Guide

| Discrepancy | Likely Cause | Fix |
|-------------|--------------|-----|
| $X off exactly | Transposition error | Search for transposed digits |
| Amount doubled | Duplicate import | Delete duplicate |
| Amount missing | Manual transaction needed | Add from source doc |
| Off by fraction | Rounding | Check bank rounding rules |
| Persistent gap | Beginning balance wrong | Correct prior period |

### API: Fetch Unreconciled Transactions

```python
def get_unreconciled_transactions(access_token, realm_id, account_id, start_date, end_date):
    """Query unreconciled transactions for reconciliation."""
    query = f"""
        SELECT * FROM Purchase
        WHERE AccountRef = '{account_id}'
        AND TxnDate >= '{start_date}'
        AND TxnDate <= '{end_date}'
        AND Cleared = 'false'
        ORDERBY TxnDate ASC
        MAXRESULTS 1000
    """
    resp = requests.get(
        f"https://quickbooks.api.intuit.com/v3/company/{realm_id}/query",
        headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},
        params={"query": query}
    )
    return resp.json()
```

---

## 5. Journal Entry Generation

### Standard Journal Entry Template

```python
def create_journal_entry(access_token, realm_id, txn_date, memo, lines):
    """
    Create a QBO journal entry.
    
    lines: list of dicts with keys:
      - account_id: QBO account ID
      - posting_type: "Debit" or "Credit"
      - amount: float
      - description: str (optional)
    """
    line_items = []
    for i, line in enumerate(lines):
        line_items.append({
            "Id": str(i + 1),
            "Description": line.get("description", memo),
            "Amount": line["amount"],
            "DetailType": "JournalEntryLineDetail",
            "JournalEntryLineDetail": {
                "PostingType": line["posting_type"],
                "AccountRef": {"value": line["account_id"]}
            }
        })
    
    payload = {
        "TxnDate": txn_date,
        "PrivateNote": memo,
        "Line": line_items
    }
    
    resp = requests.post(
        f"https://quickbooks.api.intuit.com/v3/company/{realm_id}/journalentry",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        json=payload
    )
    return resp.json()

# Example: Record depreciation
entry = create_journal_entry(
    access_token=token,
    realm_id=realm,
    txn_date="2026-03-31",
    memo="March 2026 Depreciation",
    lines=[
        {"account_id": "DEPR_EXPENSE_ID", "posting_type": "Debit", "amount": 250.00},
        {"account_id": "ACCUM_DEPR_ID", "posting_type": "Credit", "amount": 250.00}
    ]
)
```

### Common Journal Entry Templates

**Accrued Revenue**
```
DEBIT  Accounts Receivable (1100)   $X
CREDIT Services Revenue (4000)       $X
Memo: Accrue revenue for [client] - [period]
```

**Prepaid Expense Recognition**
```
DEBIT  Insurance Expense (6030)     $X
CREDIT Prepaid Insurance (1200)      $X
Memo: Recognize prepaid insurance - [month]
```

**Owner Investment**
```
DEBIT  Checking Account (1000)      $X
CREDIT Owner's Equity (3000)         $X
Memo: Owner capital contribution [date]
```

**Crypto Asset Purchase (On-Chain)**
```
DEBIT  Crypto Assets (1201)         $X   [at cost basis in USD]
CREDIT Checking Account (1000)       $X
Memo: Purchased [X ETH] at $[price] on [date] - TxHash: [0x...]
```

---

## 6. Reporting & Queries

### Useful QBO Queries (SQL-like)

```python
def run_qbo_query(access_token, realm_id, sql):
    resp = requests.get(
        f"https://quickbooks.api.intuit.com/v3/company/{realm_id}/query",
        headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},
        params={"query": sql}
    )
    return resp.json()

# Trial Balance components - fetch all accounts with balances
accounts = run_qbo_query(token, realm,
    "SELECT * FROM Account WHERE CurrentBalance != '0' ORDERBY AccountType ASC MAXRESULTS 200"
)

# Unpaid invoices (AR aging)
ar = run_qbo_query(token, realm,
    "SELECT * FROM Invoice WHERE Balance > '0' ORDERBY DueDate ASC MAXRESULTS 200"
)

# Monthly P&L check — all transactions this month
txns = run_qbo_query(token, realm,
    "SELECT * FROM Transaction WHERE TxnDate >= '2026-03-01' ORDERBY TxnDate ASC MAXRESULTS 1000"
)
```

---

## Negative Boundaries — When NOT to Use This Skill

- **Tax filing** — use `qbo-to-tax-bridge` for IRS schedule mapping and tax workpaper generation
- **Payroll processing** — QBO Payroll and Gusto have dedicated APIs; this skill doesn't cover payroll runs or W-2/1099 filing
- **OAuth setup** — Getting QBO Client ID/Secret and initial token exchange requires a separate auth flow; this skill assumes credentials already exist
- **Multi-entity consolidations** — Each QBO realm is separate; consolidation across entities requires a dedicated reporting layer
- **Audit-level assurance** — This produces bookkeeping outputs; CPA review and sign-off are required for audit-level work
- **Non-QBO accounting software** — Xero, FreshBooks, Wave, Sage have different APIs; this skill is QBO-specific
- **Real-time inventory management** — QBO inventory has limitations; dedicated WMS systems (Fishbowl, etc.) are better for complex inventory

---

## Environment Variables Reference

```bash
export QBO_CLIENT_ID="your_client_id"
export QBO_CLIENT_SECRET="your_client_secret"
export QBO_REFRESH_TOKEN="your_refresh_token"
export QBO_REALM_ID="your_company_id"

# Sandbox vs Production
export QBO_BASE_URL="https://quickbooks.api.intuit.com"  # Production
# export QBO_BASE_URL="https://sandbox-quickbooks.api.intuit.com"  # Sandbox
```

---

## Quick Reference — QBO Account Types & Sub-Types

| Account Type | Common Sub-Types |
|---|---|
| Bank | Checking, Savings, MoneyMarket |
| Accounts Receivable | AccountsReceivable |
| Other Current Asset | Prepaid Expenses, UndepositedFunds |
| Fixed Asset | Machinery, FurnitureAndFixtures, Vehicles |
| Accounts Payable | AccountsPayable |
| Credit Card | CreditCard |
| Other Current Liability | DirectDepositPayable, SalesTaxPayable |
| Long Term Liability | NotesPayable, OtherLongTermLiabilities |
| Equity | OpeningBalanceEquity, OwnersEquity, RetainedEarnings |
| Income | SalesOfProductIncome, ServiceFeeIncome |
| Cost of Goods Sold | SuppliesMaterialsCogs |
| Expense | AdvertisingPromotional, Insurance, RentOrLeaseOfBuildings |
| Other Income | OtherMiscellaneousIncome |
| Other Expense | Depreciation, OtherMiscellaneousExpense |
