---
name: shopify-auto-invoicing-inventory
description: Lightweight Shopify order invoicing and inventory operations workflow for detecting new orders, preparing invoice-ready billing data, updating stock tables, and producing simple monthly summaries. Use when building a review-first Shopify back-office process, preparing invoice exports from new orders, reconciling stock after sales, or generating easy e-commerce operations reports for a free ClawHub edition.
---

# Shopify Auto Invoicing & Inventory

Run a simple, review-first Shopify operations workflow focused on order detection, invoice preparation, stock updates, and clear monthly reporting.

Keep outputs professional, merchant-friendly, and easy to validate before any external action.

## Workflow

Use this sequence for complete requests:

1. collect store context
2. detect new or relevant orders
3. prepare invoice-ready billing data
4. update stock tables
5. summarize exceptions
6. export a monthly operations report

## 1. Collect store context

Capture the operating brief before producing outputs.

Minimum inputs:

- store name
- currency
- tax regime or VAT note
- invoice numbering rule if provided
- order date range or event trigger
- product SKU source
- current stock source
- desired report month

If details are missing, keep assumptions explicit and conservative.

## 2. Detect new orders

Use Shopify order exports, webhook payloads, user-provided CSV files, or manually reviewed order lists.

Capture these fields whenever possible:

- order_id
- order_name
- created_at
- financial_status
- fulfillment_status
- customer_name
- customer_email
- billing country
- shipping country
- currency
- line items
- SKU
- quantity
- subtotal
- tax
- shipping
- total price

Classify orders into these simple buckets:

- ready_for_invoice
- paid_but_review_needed
- pending_payment
- cancelled_or_ignore

Rules:

- invoice only orders that are paid or explicitly approved
- never invent tax data
- flag missing customer billing fields before invoice generation

## 3. Prepare invoice-ready billing data

Generate structured invoice rows rather than pretending to issue official accounting documents automatically.

For each invoice-ready order, prepare:

- invoice_number or placeholder
- invoice_date
- merchant legal name placeholder
- customer billing name
- customer billing address
- tax identifier if available
- line description
- quantity
- unit price
- tax amount
- total amount
- payment status
- source order reference

Use `references/templates.md` for invoice field structure and merchant-facing language.

If the user asks for a PDF, produce a professional invoice content block or a PDF-ready dataset unless a real PDF renderer is already available.

## 4. Update stock tables

After processing valid orders, create a stock movement view.

Recommended columns:

- sku
- product_title
- variant_title
- opening_stock
- quantity_sold
- quantity_refunded
- net_change
- closing_stock
- low_stock_flag
- reorder_note

Rules:

- subtract sold quantities from stock
- add refunded quantities back only when explicitly confirmed
- flag negative resulting stock as `needs_review`
- flag low stock using the user threshold, otherwise default to 5

Use `scripts/stock_sync.py` to compute a flat stock reconciliation file from inventory and order exports.

## 5. Summarize exceptions

Always produce a short exception section.

Include:

- orders missing billing data
- unpaid orders excluded from invoicing
- orders with missing SKU data
- products with negative or low stock
- tax or currency mismatches

Keep this section concise and actionable.

## 6. Export monthly report

When the user asks for a monthly summary, include:

- total orders processed
- paid orders
- pending-payment orders
- cancelled orders
- invoice-ready orders
- invoiced revenue
- tax total
- units sold
- top SKUs by quantity
- low-stock SKU count

Use `scripts/monthly_ops_report.py` to aggregate order and stock data into a compact CSV summary.

## Output order

For a complete request, produce outputs in this order:

1. operating assumptions
2. order status summary
3. invoice-ready table
4. stock reconciliation table
5. exceptions list
6. monthly report summary

## Ease-of-use standard

Write for non-technical Shopify merchants.

Prefer:

- plain labels
- compact tables or CSV-ready rows
- obvious status names
- clean summaries with next actions

Avoid:

- jargon-heavy accounting language unless requested
- pretending an official invoice was sent when only a draft was prepared
- risky automation claims without source data

## Compliance standard

Operate in a review-first and accounting-aware way.

Use this skill to support:

- order review
- invoice preparation
- stock reconciliation
- monthly reporting

Do not claim legal or tax compliance beyond the data provided. Recommend accountant review when tax treatment is uncertain.

## Community edition note

This free edition focuses on invoice-ready data prep, stock reconciliation, and simple monthly reporting. It intentionally excludes automated payment reminders, advanced PDF workflows, and richer finance automation.

## Resources

Use bundled resources when useful:

- `references/templates.md` for invoice and report templates
- `scripts/invoice_export.py` to convert Shopify-style order JSON into invoice-ready CSV rows
- `scripts/stock_sync.py` to reconcile stock from orders and inventory CSV files
- `scripts/monthly_ops_report.py` to build a simple monthly operations summary
