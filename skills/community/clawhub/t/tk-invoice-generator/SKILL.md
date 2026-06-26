---
name: invoice-generator
description: Generate professional invoices from project data — line items, tax calculation, payment terms, and formatted output. Supports freelance, agency, and SaaS billing. Tracks outstanding invoices and sends payment reminders.
metadata:
  version: 1.0.0
  author: TKDigital
  category: Business Operations
  tags: [invoice, billing, freelance, payment, accounting, business, finance]
---

# Invoice Generator

Create professional invoices from project data with automatic calculation, payment terms, and tracking.

## What It Does

1. **Invoice Creation** — Generate formatted invoices from simple inputs
2. **Auto-Calculation** — Line items, subtotals, tax, discounts, totals
3. **Payment Terms** — Net 15/30/60, late fees, early payment discounts
4. **Client Management** — Remember client details for repeat invoicing
5. **Outstanding Tracking** — Track unpaid invoices, generate reminders
6. **Multi-Currency** — USD, EUR, GBP, and more

## Usage

### Create an Invoice
```
Create an invoice:

From: [Your business name]
To: [Client name, address]
Invoice #: [Number or auto-generate]
Date: [Today or specific date]
Due: [Net 30 / specific date]

Line items:
1. [Service] — [quantity] × $[rate] 
2. [Service] — [quantity] × $[rate]
3. [Service] — [quantity] × $[rate]

Tax: [rate]% or [none]
Discount: [amount or percentage] or [none]
Currency: USD
Payment method: [Bank transfer / PayPal / Stripe link]
Notes: [Any additional notes]
```

### Quick Invoice from Project
```
Invoice for this project:

Client: [Name]
Project: [Description]
Hours worked: [X hours]
Rate: $[X]/hour
Expenses: [List any]
Payment: Net 30

Generate the invoice with a professional layout.
```

### Monthly Recurring Invoice
```
Generate this month's recurring invoices:

Client A: $2,500/mo retainer (content services)
Client B: $1,500/mo retainer (social media management)
Client C: $500/mo (bot hosting + maintenance)

Include: invoice numbers (sequential), dates, payment terms, totals
```

### Outstanding Invoice Report
```
Here are my issued invoices this month:

INV-001: Client A, $2,500, issued April 1, due April 30
INV-002: Client B, $1,500, issued April 1, due April 15
INV-003: Client C, $800, issued April 5, due May 5

Which are overdue? Draft payment reminder emails for any past due.
```

## Output Format

```
═══════════════════════════════════════════
                  INVOICE
═══════════════════════════════════════════

From: [Your Business]             Invoice #: [INV-XXX]
[Your Address]                    Date: [YYYY-MM-DD]
[Your Email]                      Due: [YYYY-MM-DD]
                                  Terms: [Net 30]

Bill To:
[Client Name]
[Client Address]
[Client Email]

───────────────────────────────────────────
Description              Qty    Rate    Amount
───────────────────────────────────────────
[Service 1]               [X]   $[X]    $[X.XX]
[Service 2]               [X]   $[X]    $[X.XX]
[Service 3]               [X]   $[X]    $[X.XX]
───────────────────────────────────────────
                          Subtotal:     $[X.XX]
                          Tax ([X]%):   $[X.XX]
                          Discount:    -$[X.XX]
                          ─────────────────
                          TOTAL:        $[X.XX]
═══════════════════════════════════════════

Payment Methods:
[Bank details / PayPal / Stripe link]

Notes:
[Additional terms or thank you message]

Late Payment: [X]% monthly interest after due date
```

## Best Practices

- Keep invoice numbers sequential (INV-001, INV-002...)
- Include clear payment instructions
- Send invoices within 24 hours of project completion
- Follow up on overdue invoices at 1, 7, and 14 days past due
- Pair with a cost tracking system for profit calculations

## References

- `references/payment-terms.md` — Standard payment terms explained
- `references/reminder-templates.md` — Follow-up email templates for overdue invoices
