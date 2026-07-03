---
name: smb-invoice-tracker
version: 1.0.1
author: "NASSER AL-SOLAITTI"
description: "Local invoice tracking ledger with optional LLM-generated reminder text. Add invoices manually, track outstanding/paid status, generate cash flow reports. Use when user says 'track an invoice', 'add an invoice', 'show my outstanding invoices', or 'invoice report'.
permissions:
  - filesystem-write: write invoice and config data to ~/.openclaw/smb-invoice-tracker/
  - env: read MINIMAX_API_KEY from environment (for optional LLM reminder generation)
  - network: send invoice fields (payer name, amount, due date, note) to minimax LLM API when reminder generation is used
privacy: |
  This skill stores invoices locally at ~/.openclaw/smb-invoice-tracker/ — no data leaves your machine by default.
  When MINIMAX_API_KEY is set and reminder text is generated, invoice fields (payer name, amount, due date, note)
  are sent to api.minimax.chat. No Gmail scanning, no WhatsApp, no Stripe, no automated reminders are implemented.
  Gmail, WhatsApp, Stripe, and Telegram features described in v1.0 are planned for v1.1.
---

# SMB Invoice Tracker

## When to use this skill

Activate when the user wants to:
- Add and track invoices manually
- See which invoices are outstanding or overdue
- Generate a cash flow report
- Produce reminder text via LLM (optional, requires MINIMAX_API_KEY)

## Prerequisites

- MINIMAX_API_KEY (optional — only needed for LLM-generated reminder text)
- OpenClaw gateway running

> **Note:** Gmail scanning, WhatsApp reminders, Stripe payment detection, and Telegram digests
> are NOT implemented in v1.0. These are planned for v1.1.

## Workflow

### 1. Add an invoice

```bash
clawhub run smb-invoice-tracker add \
  --payer "Acme Corp" \
  --amount 1500 \
  --currency "USD" \
  --due 2026-07-15 \
  --note "Q2 consulting"
```

### 2. Configure reminder tone (optional)

```bash
clawhub run smb-invoice-tracker configure \
  --tone "polite" \
  --reminder-schedule "T-7,T-1,T+0,T+7"
```

Available tones: `polite`, `friendly`, `firm`.

### 3. List invoices

```bash
# All invoices
clawhub run smb-invoice-tracker list

# Overdue only
clawhub run smb-invoice-tracker list --status outstanding

# Paid only
clawhub run smb-invoice-tracker list --status paid
```

### 4. Generate reminder text (optional LLM)

```bash
clawhub run smb-invoice-tracker send-reminder --id INV-001
# Prints reminder text to stdout — review before sending manually
```

### 5. Mark as paid

```bash
clawhub run smb-invoice-tracker mark-paid --id INV-001
```

### 6. Cash flow report

```bash
clawhub run smb-invoice-tracker report --period week
```

## Outputs

- **Invoice ledger**: stored at `~/.openclaw/smb-invoice-tracker/invoices.json`
- **Reminder text**: printed to stdout (review before sending manually)
- **Reports**: printed to stdout

## What v1.0 actually does

- ✅ Add / list / mark-paid invoices
- ✅ Track outstanding and paid status
- ✅ Cash flow report (outstanding balance, due dates)
- ✅ LLM-generated reminder text (optional, MINIMAX_API_KEY required)
- ❌ Gmail scanning — NOT implemented (v1.1)
- ❌ WhatsApp reminders — NOT implemented (v1.1)
- ❌ Stripe payment detection — NOT implemented (v1.1)
- ❌ Telegram digest — NOT implemented (v1.1)
- ❌ CSV export — NOT implemented (v1.1)

## Cost expectations

- LLM reminder generation: ~$0.001 per invoice (only when MINIMAX_API_KEY is set)
- OpenClaw: free, self-hosted

## Troubleshooting

**Invoice not appearing?**
- Check status: `clawhub run smb-invoice-tracker list`

**LLM reminder not generating?**
- Verify MINIMAX_API_KEY is set in your environment

**Want Gmail / WhatsApp / Stripe integration?**
- These are planned for v1.1. Currently not implemented.
