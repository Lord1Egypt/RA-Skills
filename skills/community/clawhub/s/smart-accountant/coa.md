# coa.md
# Skill Knowledge File: Chart of Accounts (COA) Foundations
# Purpose:
# Provide foundational accounting knowledge for an Accountant Agent.
# This file teaches account classification and normal balance behavior.
# Use as domain reference before journal logic or transaction posting.

---

# 1. CORE CONCEPT

## What is a Chart of Accounts (COA)

A Chart of Accounts is the master list of all accounts used by a business to classify and track financial transactions.

Think of it as categorized buckets where every transaction must belong.

Every account must be classified under exactly one of five primary account types:

1. Asset
2. Liability
3. Equity
4. Income
5. Expense

---

# 2. FIVE PRIMARY ACCOUNT TYPES

## 2.1 Assets

Definition:
Resources owned or controlled by the business that provide value.

Examples:
- Cash
- Bank
- Inventory
- Accounts Receivable
- Machinery
- Furniture
- Deposits

Nature:
- Normal balance: Debit

Rules:
- Increases with Debit
- Decreases with Credit

---

## 2.2 Liabilities

Definition:
Amounts the business owes to others.

Examples:
- Accounts Payable
- Loans
- Taxes Payable
- Accrued Expenses

Nature:
- Normal balance: Credit

Rules:
- Increases with Credit
- Decreases with Debit

---

## 2.3 Equity

Definition:
Owner’s residual interest in the business.

Formula:
Assets = Liabilities + Equity

Examples:
- Owner Capital
- Retained Earnings
- Partner Capital

Nature:
- Normal balance: Credit

Rules:
- Increases with Credit
- Decreases with Debit

---

## 2.4 Income (Revenue)

Definition:
Money earned by business operations.

Examples:
- Sales
- Service Revenue
- Commission Income

Nature:
- Normal balance: Credit

Rules:
- Increases with Credit
- Decreases with Debit

Important:
Income is normally credit.

---

## 2.5 Expenses

Definition:
Costs incurred to operate and earn income.

Examples:
- Rent
- Salaries
- Utilities
- Office Expenses

Nature:
- Normal balance: Debit

Rules:
- Increases with Debit
- Decreases with Credit

Important:
Expenses are normally debit.

---

# 3. NORMAL BALANCE REFERENCE

Use this as default classification rule:

| Account Type | Normal Balance |
|------------|----------------|
| Asset      | Debit          |
| Expense    | Debit          |
| Liability  | Credit         |
| Equity     | Credit         |
| Income     | Credit         |

Memory aid:

DEALER

D = Drawings
E = Expenses
A = Assets

L = Liabilities
E = Equity
R = Revenue

Debit:
- Drawings
- Expenses
- Assets

Credit:
- Liabilities
- Equity
- Revenue

---

# 4. IMPORTANT DISTINCTION:
# ACCOUNT TYPE vs BALANCE SIDE

Critical rule:

Do not confuse account type with current balance side.

Example:
An Asset account may occasionally show a credit balance.
This does NOT change the account into a Liability.

Example:
Accounts Receivable with credit balance may indicate:
- customer advance
- overpayment
- abnormal balance
- adjustment

It remains an Asset-type account.

Likewise:

A Liability account may carry debit balance in special cases.
This does NOT make it an Asset account.

Rule:
Account classification does not change because balance flips.

Only the balance may be abnormal.

---

# 5. ACCOUNTING EQUATIONS

Primary equation:

Assets = Liabilities + Equity

Profit equation:

Profit = Income - Expenses

These relationships must be treated as foundational accounting laws.

---

# 6. SAMPLE CHART OF ACCOUNTS STRUCTURE

Typical coding structure:

1000 Assets
 1100 Cash
 1200 Bank
 1300 Receivables
 1400 Inventory

2000 Liabilities
 2100 Payables
 2200 Loans

3000 Equity
 3100 Owner Capital

4000 Income
 4100 Sales

5000 Expenses
 5100 Rent
 5200 Salary

Rule:
Account numbering may vary by organization.

---

# 7. AGENT CLASSIFICATION RESPONSIBILITY

When analyzing a transaction, first determine:

Step 1:
Identify affected accounts.

Step 2:
Classify each account into one of:
- Asset
- Liability
- Equity
- Income
- Expense

Step 3:
Apply normal balance rules.

Step 4:
Only after classification proceed to debit/credit posting.

Never post entries before classification.

Classification comes before journal logic.

---

# 8. VALIDATION RULES FOR AGENT

Always enforce:

- Every account must have one primary type.
- Every account should have defined normal balance.
- Flag abnormal balances separately.
- Do not reclassify account type because balance changes.
- Income should normally be credit.
- Expense should normally be debit.
- Assets normally debit.
- Liabilities normally credit.
- Equity normally credit.

---

# 9. AGENT OUTPUT EXPECTATION

When asked about an account, respond in this structure:

Account:
Type:
Normal Balance:
Increases By:
Decreases By:
Notes:

Example:

Account: Cash
Type: Asset
Normal Balance: Debit
Increases By: Debit
Decreases By: Credit
Notes: Resource owned by business.

---

# 10. SCOPE LIMIT

This file covers only:
- Chart of Accounts
- Account classification
- Normal balances

This file does NOT cover:
- Journal entries
- Double-entry posting logic
- Trial balance
- Financial statements
- Tax rules

Those belong in separate skill knowledge files.

Suggested future files:
- journal_entries.md
- debit_credit_rules.md
- reconciliation.md
- financial_statements.md

---
End of coa.md
