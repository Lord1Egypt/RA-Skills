---
name: sheet-agent
description: "Spreadsheet operations agent for CSV and Excel files: inspect data, detect anomalies, answer business questions, generate reports, and preview edits safely."
---

# Sheet Agent

## One-Line Positioning

**Transform natural language into spreadsheet comprehension, anomaly detection, business insights, and safe rewrite suggestions.**

---

## When to Use

Activate this skill when the user mentions:

- Having AI read or inspect a spreadsheet for problems
- Querying data from CSV/Excel files
- Generating daily reports, weekly reports, or operations summaries
- Modifying a specific record in a spreadsheet (preview first, confirm second)
- Checking for empty values, duplicates, or anomalies in a spreadsheet

---

## Usage

```
/sheet "spreadsheet path" "natural language instruction"
```

Examples:
```
/sheet "~/Desktop/orders.csv" "Which orders haven't been followed up for more than 3 days?"
/sheet "~/Documents/inventory.xlsx" "Check if there are any negative inventory quantities"
/sheet "~/Desktop/orders.csv" "Generate last week's weekly report"
/sheet "~/Desktop/customers.csv" "Change the customer tier in row 8 to VIP"
```

---

## Core Features

### 1. Spreadsheet Reading & Comprehension
- Supports CSV and Excel (.xlsx) files
- Auto-recognizes column names and data types
- Infers business type (orders/inventory/leads/daily report)

### 2. Business Queries (Natural Language to Structured Results)
- "Orders not followed up for more than X days"
- "Orders with amount greater than Y"
- "Find all VIP customers"
- "Sum quantities by sales representative"

### 3. Anomaly Detection
- Empty values (missing data)
- Negative numbers (inventory/quantity columns)
- Duplicate IDs
- Date anomalies (future dates, inconsistent formats)
- Value anomalies (beyond reasonable ranges)

### 4. Daily / Weekly / Operations Summaries
- Auto-detects time range
- Generates structured summary:
  - Overall view (total count, sum, average)
  - Distribution stats (category percentages, top items)
  - Anomaly record list
  - Trend descriptions

### 5. Change Preview (Key Safety Mechanism)
**All changes show a preview first — execute only after user confirmation.**

User says "Change the amount in row 5 to 15000":
-> The agent shows a preview and does NOT write yet
-> If the user replies "confirm", execute the write
-> If the user replies "cancel", do nothing

---

## Output Examples

### Query Results
```
📊 Query Results: 12 leads have not been followed up for more than 3 days

| # | Name | Phone | Entry Date | Days Since |
|---|------|-------|------------|------------|
| 3 | Alex Wang | 138... | 2026-03-25 | 6 days |
| 7 | Leo Zhao | 139... | 2026-03-27 | 4 days |
```

### Anomaly Detection
```
⚠️ Found 4 anomalies:

1. Row 15 [Bluetooth Earbuds]: Inventory = -5 (negative)
2. Row 28 [Phone Case]: Unit price is empty
3. Row 42 [Data Cable]: Inventory = 9999 (suspiciously large)
4. Row 55: Product name is duplicated
```

### Weekly Report
```
📈 Operations Summary — Week 4, March 2026

[Overall View]
- Total orders: 156
- Total sales: ¥128,500
- Average order value: ¥823

[Top 5 Selling Items]
1. Bluetooth Earbuds - 45 units
2. Phone Case - 32 units
...

[Anomalous Orders]
- Refunds: 2 orders
```

### Change Preview
```
📝 Proposed Change Preview:

File: customers.csv
Row: 8
Field: Customer Tier
Old value: Regular
New value: VIP

⚠️ Confirm execution? Reply "confirm" or "cancel"
```

---

## Safety Principles

1. **Read-only by default**: Any operation does not modify files by default
2. **Write only on confirmation**: Write operations require explicit user confirmation
3. **Backup before write**: Automatically back up original file to `backup/` directory
4. **Ask when uncertain**: If column meaning is unclear, proactively ask the user instead of assuming

---

## Limitations

- Recommended maximum of 100,000 rows per operation
- Supports CSV and .xlsx formats
- Version 1 does not handle cross-spreadsheet joins
