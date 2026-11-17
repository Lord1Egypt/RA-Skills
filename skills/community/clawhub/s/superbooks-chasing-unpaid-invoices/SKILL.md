---
name: chasing-unpaid-invoices
description: "Reviews money owed to the business in SuperBooks: unpaid and overdue invoices, who owes the most, the total outstanding, and an open invoice's details, and drafts a reminder for the user to send. Use when the user asks 'which invoices are unpaid', 'who owes me the most', 'what's overdue', 'how much is outstanding', 'show my accounts receivable', or 'which customers should I chase'. Read-only."
---

# Unpaid invoices in SuperBooks

Give the user a clear picture of receivables: what is open, what is overdue, and who owes what.

## Connecting and calling the tools

Every operation in this skill comes from the `superbooks` MCP server, the SuperBooks connector. The server defaults to Code Mode, so the operations below are written as the `external_*` functions you call inside `superbooks:execute_typescript`. On a server set to the per-tool surface, the same operation is listed as `superbooks:<name>` without the `external_` prefix, for example `superbooks:invoices_list`.

- **Only `superbooks:search_tools` and `superbooks:execute_typescript` listed (Code Mode, the default):** call `superbooks:search_tools` first, then call each tool inside `superbooks:execute_typescript` as `external_<tool>` (for example `external_invoices_list`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **Operations listed by name:** call them directly, for example `superbooks:invoices_list`.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `superbooks:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects SuperBooks and approves that scope.
- **No `superbooks` tools at all:** SuperBooks is not connected yet. Install the SuperBooks power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

The `superbooks` MCP server has two tools: `superbooks:search_tools` (call it first, for example with `invoice`, to get the exact input shapes) and `superbooks:execute_typescript` (run a short program calling the declared `external_*` functions; the program must `return` its result).

If the connection lists the operations by name instead (the per-tool surface), call them directly without the `external_` prefix.

Operations this skill uses:

- `external_invoices_list`: invoices filtered by status (for example `unpaid`), with amounts and due dates.
- `external_invoices_get`: one invoice with line items, customer, totals and `sent_at`.
- `external_customers_get`: contact details for a customer the user wants to follow up with.
- `external_reports_top_customers`: customers ranked by revenue, for context.
- `external_team_get`: the team currency.

## Workflow

1. In one program, fetch `external_invoices_list` with `status: "unpaid"` and `external_team_get` with `await Promise.all`.
2. Split the list into overdue (due date before today) and not yet due. Sort each by amount.
3. Present a table: invoice number, customer, amount, due date, days overdue. Give the totals for overdue and for all open invoices.
4. Group by customer and name the customer with the largest open balance.
5. If the user wants to follow up with a customer, fetch `external_invoices_get` and `external_customers_get` together and draft a short, polite reminder e-mail for the user to send themselves, with invoice number, amount, due date and the customer's billing e-mail.

## Code Mode pattern

```ts
const [open, team] = await Promise.all([
  external_invoices_list({ status: "unpaid" }),
  external_team_get({}),
]);
return { open, currency: team.currency };
```

## Rules

- This skill only reads. SuperBooks has no reminder operation, and `external_invoices_send` is for sending a draft, so never use it to nudge a customer about an invoice already sent.
- Never mark an invoice paid or void it from here: never call `external_invoices_void` or any other write operation. Payments are recorded in the app.
- Use the dates and amounts the operations return. State today's date when you compute days overdue.
