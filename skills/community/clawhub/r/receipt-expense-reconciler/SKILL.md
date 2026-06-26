---
name: receipt-expense-reconciler
description: Parse receipts and invoices, categorize spend, detect anomalies, and produce tax-ready expense summaries for freelancers and SMB operators.
metadata: {"openclaw":{"emoji":"🧾"}}
---

# Receipt and Expense Reconciler

## Purpose

Turn messy receipts/invoices into clean, auditable expense data.

## Core capabilities

- extract key fields (date, vendor, amount, tax, currency, category hints)
- normalize merchant names
- categorize expenses using rule + confidence model
- detect anomalies (duplicates, outliers, suspicious amounts)
- generate monthly and quarterly tax-ready summaries

## Disclaimer

This skill provides operational/accounting guidance only. It is not legal or tax advice. Always verify with a licensed accountant/tax advisor before filing.

## Workflow

1. Ingest receipts/invoices (PDF/image/text/CSV).
2. Parse and normalize fields.
3. Categorize with confidence score.
4. Flag uncertain and anomalous rows for review.
5. Produce reconciled ledger and summary report.

## Output format

1. Parsed records table
2. Category summary
3. Anomaly report
4. Tax-ready export checklist

## Setup

Read [setup.md](setup.md).

## Examples

See [examples.md](examples.md).

