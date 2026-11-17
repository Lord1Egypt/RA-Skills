---
name: drafting-invoices
description: "Drafts a SuperBooks invoice for a customer, optionally from tracked time, creates the customer if needed, and sends it only after an explicit confirmation naming the invoice and recipient. Use when the user asks to 'invoice Cedar Valley Books for 6 hours of design at $125', 'bill my September hours on Harbor & Pine', 'create an invoice', 'turn my tracked time into an invoice', 'add a new customer', or 'send this invoice'."
---

# Draft an invoice in SuperBooks

Build a correct draft invoice from what the user says or from their tracked time. The draft stays in SuperBooks until the user explicitly asks to send it; sending e-mails the customer.

## Connecting and calling the tools

Every operation in this skill comes from the `superbooks` MCP server, the SuperBooks connector. The server defaults to Code Mode, so the operations below are written as the `external_*` functions you call inside `superbooks:execute_typescript`. On a server set to the per-tool surface, the same operation is listed as `superbooks:<name>` without the `external_` prefix, for example `superbooks:invoices_list`.

- **Only `superbooks:search_tools` and `superbooks:execute_typescript` listed (Code Mode, the default):** call `superbooks:search_tools` first, then call each tool inside `superbooks:execute_typescript` as `external_<tool>` (for example `external_invoices_list`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **Operations listed by name:** call them directly, for example `superbooks:invoices_list`.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `superbooks:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects SuperBooks and approves that scope.
- **No `superbooks` tools at all:** SuperBooks is not connected yet. Install the SuperBooks power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

The `superbooks` MCP server has two tools. Everything below goes through them.

- `superbooks:search_tools`: lists the operations this connection can reach as `declare function external_<name>(...)` signatures. Call it first, for example with the queries `invoice`, `customer`, `tracker`, to get the exact input shapes.
- `superbooks:execute_typescript`: runs a short program calling those `external_*` functions, which are already in scope; never import or redeclare them. The program must `return` its result.

If the connection lists the operations by name instead (the per-tool surface), call them directly without the `external_` prefix.

Operations this skill uses:

- `external_customers_list` and `external_customers_get`: find the customer and their billing details.
- `external_customers_create`: add a customer that does not exist yet.
- `external_tracker_list_projects` and `external_tracker_list_entries`: tracked projects and their time entries (start, stop, description).
- `external_team_get`: the team profile, including its currency.
- `external_invoices_create_draft`: save an invoice with line items and a due date as a draft. Returns the invoice number.
- `external_invoices_get`: read the draft back to confirm totals.
- `external_invoices_send`: e-mail the invoice to the customer and mark it unpaid. Confirm first, every time.

## Workflow

1. In one program, fetch `external_customers_list` and `external_team_get` with `await Promise.all`. If the customer is missing, offer to create one; ask for the name and billing e-mail, then call `external_customers_create`.
2. Build the line items:
   - From the user's words: description, quantity, unit price.
   - From tracked time: find the project with `external_tracker_list_projects`, fetch `external_tracker_list_entries` for the period, total the hours, and show the entries you are billing.
3. Show the draft: customer, line items, subtotal in the team currency, due date (default 30 days unless the user says otherwise).
4. On approval, call `external_invoices_create_draft`. Report the invoice number and that it is a draft the customer has not received.
5. Only if the user asks to send it: restate "Send INV-0007 for $750.00 to billing@cedarvalley.example?" and wait for a yes. Then run `external_invoices_send` on its own, and confirm with `external_invoices_get` that it is unpaid with a `sent_at` time.

## Code Mode pattern

```ts
const [customers, team] = await Promise.all([
  external_customers_list({}),
  external_team_get({}),
]);
return { customers, currency: team.currency };
```

A call that is out of scope or fails throws an `Error` whose message says what went wrong. Wrap it in `try { ... } catch (e) { return String(e) }` and relay the message.

## Rules

- Never call `external_invoices_send` without an explicit confirmation naming the invoice and the recipient in this conversation. Drafting never implies sending, and a send never runs in the same program as other writes.
- Do not invent rates, hours, or tax. Ask when a price or quantity is missing.
- No operation moves money; there is no payment tool.
- Deleting or voiding invoices is not offered here. If the user asks, point them to the SuperBooks app.
