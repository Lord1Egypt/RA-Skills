# Accountant Agent Skill Mastery Guide

Welcome to the Accountant Agent Skill repository! This document serves as the master index for the AI accountant's core knowledge base. It details the purpose of each foundation file, the execution tools, installation instructions, and the initial onboarding flow an agent should use when setting up a new business.

---

## 📚 Core Knowledge Base Files

### 1. `audit_rule.md`
- **What it is for:** Defines preventive, detective, and corrective audit controls.
- **How to use it:** Use as the ultimate gatekeeper before posting any transaction. Enforces the "Maker-Checker" protocol where the agent drafts and the human confirms.
- **What it contains:** Three layers of controls, Golden Audit Checks, anomaly detection, and validation requirements (e.g., preventing unbalanced journals).
- **Why it's important:** Prevents financial data corruption, fraud, and ensures mathematical accuracy before any database write occurs.

### 2. `closing.md`
- **What it is for:** Defines the operational workflows for period-end closures (Monthly, Quarterly, and Yearly).
- **How to use it:** Use to guide the agent through reconciliation checklists before locking a financial period.
- **What it contains:** Step-by-step procedures for capturing, reconciling, adjusting, reviewing, reporting, and locking. Explains how temporary accounts close to retained earnings at year-end.
- **Why it's important:** Certifies financial truth for a given period and legally locks historical records to prevent backdated manipulations.

### 3. `coa.md` (Chart of Accounts)
- **What it is for:** The foundational classification system for all financial buckets.
- **How to use it:** Use to classify every ledger into one of the 5 primary types: Assets, Liabilities, Equity, Income, or Expenses.
- **What it contains:** Definitions of the 5 primary types, normal balance rules (Debit vs. Credit), and the foundational accounting equation (Assets = Liabilities + Equity).
- **Why it's important:** Proper classification dictates how transactions behave and how financial reports are ultimately structured.

### 4. `db.md` & `db_tool.md`
- **What it is for:** Defines the architectural bridge between accounting theory and the actual `better-sqlite3` execution engine.
- **How to use it:** Guides the agent on how to call specific `scripts/` (syscalls) rather than improvising raw SQL.
- **What it contains:** The architecture of the `tool/` directory, schema definitions, transactional requirements (WAL mode), and detailed instructions on how the posting engine works.
- **Why it's important:** Ensures deterministic, low-tool-call operations that safely persist financial data in an ACID-compliant database.

### 5. `general_ledger.md`
- **What it is for:** Explains the hierarchy of Ledgers and Ledger Groups.
- **How to use it:** Use to understand how journal entries accumulate into running balances over time.
- **What it contains:** The distinction between postable ledgers (where transactions happen) and non-postable ledger groups (used only for organization).
- **Why it's important:** Prevents the agent from accidentally posting transactions to summary folders, ensuring granular transaction tracking.

### 6. `journal_entry.md`
- **What it is for:** Teaches the agent how to translate business events into formal double-entry accounting records.
- **How to use it:** Use to map natural language intents to specific Voucher Types (e.g., CR, BP, SE, PE) and apply Debit/Credit logic.
- **What it contains:** The anatomy of a journal entry, voucher type definitions, and examples of translating human speech into balanced journals.
- **Why it's important:** It guarantees that every financial event adheres to the fundamental rule: Total Debits must equal Total Credits.

### 7. `rectification.md`
- **What it is for:** Transaction correction logic for handling mistakes.
- **How to use it:** Use to determine if a mistake can be edited (if still a Draft) or must be reversed/adjusted (if already Posted).
- **What it contains:** Rules for reversing vouchers, adjusting entries, and enforcing the two-stage posting model (Draft -> Preview -> Confirm -> Post).
- **Why it's important:** Enforces an append-only, immutable audit trail. History is never silently overwritten.

### 8. `report_manual.md`
- **What it is for:** Defines the output reporting layer of the accounting system.
- **How to use it:** Use to generate the 12 core reports (Trial Balance, P&L, Balance Sheet, Cash Flow, etc.) dynamically from the ledger.
- **What it contains:** Definitions, generation logic, and example layouts for every critical financial report.
- **Why it's important:** Provides the human owner with visibility into the financial health, liquidity, and profitability of the business.

### 9. `source_document.md`
- **What it is for:** Defines the required evidence that must exist before a transaction is recorded.
- **How to use it:** Use to map physical/digital documents (Invoices, Receipts, Bank Statements) to system Voucher Types.
- **What it contains:** Document definitions and the "Document First, Entry Second" rule.
- **Why it's important:** Ensures that the agent does not fabricate entries without underlying business proof.

### 10. `transaction_language.md`
- **What it is for:** NLP keyword mappings.
- **How to use it:** Use as a dictionary to parse user intent and colloquials into formal accounting commands.
- **What it contains:** Extensive lists of keywords, phrases, and Indian/Global colloquialisms mapped to specific voucher types.
- **Why it's important:** Enables seamless, conversational human-agent interaction without requiring the user to speak in strict accounting terms.

---

## 🛠 Installation & Setup

The actual execution logic resides in the `tool/` directory, powered by Node.js and `better-sqlite3`.

To set up the database and toolset:

```bash
# 1. Navigate to the tool directory
cd tool/

# 2. Install dependencies (better-sqlite3)
npm install

# 3. Initialize the database schema (Creates accounting.db)
node scripts/migrate-schema.js

# 4. Verify database integrity
node scripts/integrity-check.js
```

Once initialized, the system uses the scripts in `tool/scripts/` (e.g., `post-voucher.js`, `generate-report.js`) as the primary interface for all ledger operations.

---

## 🤝 Initial Onboarding: Accountant Initialization Interview

When the Accountant Agent is installed or attached to a new workspace, it should behave like a professional human accountant onboarding a new client. 

Before recording any daily transactions, the agent MUST ask the user the following questions to properly initialize the books:

1. **Business Entity & Reporting Period:**
   > "What is the legal name of the business, and what is your financial year (e.g., April to March or Jan to Dec)?"
2. **Opening Balances (The Transition):**
   > "Are we starting fresh, or do you have an existing Trial Balance / Balance Sheet from a previous system that we need to import as opening balances?"
3. **Cash & Banks:**
   > "What are your primary bank accounts and cash registers? We need to set these up as your core Asset ledgers."
4. **Chart of Accounts (COA) Customization:**
   > "Do you have specific expense/income categories you want to track granularly, or should I initialize a standard Chart of Accounts for your industry?"
5. **Initial Capital (For New Businesses):**
   > "If this is a brand new business, how much initial owner's capital has been introduced, and into which bank or cash account was it deposited?"
6. **Outstanding Dues (Day One AR/AP):**
   > "Are there any pending payables to suppliers or receivables from customers that we need to record on day one to ensure accurate cash flow tracking?"

Once these questions are answered, the agent will use the `tool/` scripts to generate the Opening Entries (`OE`) and establish the initial Trial Balance.
