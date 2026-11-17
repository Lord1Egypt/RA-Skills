---
name: reading-financial-reports
description: "Reports how the business is doing from SuperBooks data: profit and loss, revenue, spending by category, burn rate, runway, account balances, top customers, and recurring expenses. Use when the user asks 'how did June to September go', 'what's my runway', 'show my P&L', 'profit and loss this quarter', 'what's my burn rate', 'where am I spending the most', 'who are my top customers', or wants a monthly or quarterly financial summary. Read-only."
---

# SuperBooks financial report

Read the team's reports and turn them into a short, honest summary in the team currency.

## Connecting and calling the tools

Every operation in this skill comes from the `superbooks` MCP server, the SuperBooks connector. The server defaults to Code Mode, so the operations below are written as the `external_*` functions you call inside `superbooks:execute_typescript`. On a server set to the per-tool surface, the same operation is listed as `superbooks:<name>` without the `external_` prefix, for example `superbooks:invoices_list`.

- **Only `superbooks:search_tools` and `superbooks:execute_typescript` listed (Code Mode, the default):** call `superbooks:search_tools` first, then call each tool inside `superbooks:execute_typescript` as `external_<tool>` (for example `external_invoices_list`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **Operations listed by name:** call them directly, for example `superbooks:invoices_list`.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `superbooks:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects SuperBooks and approves that scope.
- **No `superbooks` tools at all:** SuperBooks is not connected yet. Install the SuperBooks power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

The `superbooks` MCP server has two tools: `superbooks:search_tools` (call it first with the query `reports` to get every report's exact input shape) and `superbooks:execute_typescript` (run a short program calling the declared `external_*` functions; the program must `return` its result).

If the connection lists the operations by name instead (the per-tool surface), call them directly without the `external_` prefix.

Operations this skill uses:

- `external_reports_profit_loss`: revenue, expenses and the difference per month, with totals.
- `external_reports_revenue`: revenue over a period.
- `external_reports_spending`: spending broken down by category.
- `external_reports_burn_rate`: monthly net spend.
- `external_reports_runway`: how long the current balance lasts at the current burn.
- `external_reports_balance`: balances over time.
- `external_reports_top_customers`: customers ranked by revenue.
- `external_reports_recurring_expenses`: subscriptions and other repeating costs.
- `external_bank_accounts_list`: connected accounts, to name where balances come from.
- `external_team_get`: the team profile, including its currency.

## Workflow

1. Agree the window (default: the last three full months).
2. Fetch every report the question needs in one program with `await Promise.all`, together with `external_team_get`:
   - Performance: `external_reports_profit_loss`.
   - Cash position: `external_reports_balance`, `external_reports_burn_rate`, `external_reports_runway`.
   - Where money goes: `external_reports_spending`, `external_reports_recurring_expenses`.
   - Where money comes from: `external_reports_revenue`, `external_reports_top_customers`.
3. Present a month-by-month table of revenue, expenses and net, then the totals, then the sections the user asked about.
4. Close with at most three observations drawn from the numbers, such as the largest expense category or a recurring cost that grew.

## Code Mode pattern

```ts
const range = { from: "2026-06-01", to: "2026-09-30" };
const [team, pl, runway, spending] = await Promise.all([
  external_team_get({}),
  external_reports_profit_loss(range),
  external_reports_runway({}),
  external_reports_spending(range),
]);
return { currency: team.currency, pl, runway, spending };
```

Match each report's arguments to its `superbooks:search_tools` declaration. A failing call throws an `Error`; wrap calls in try/catch when the rest should still return.

## Rules

- Only report figures the operations returned, in the team currency. If a report comes back empty for the window, say so.
- This is bookkeeping data, not tax or legal advice. Say so if the user asks what they owe in tax.
- This skill only reads. Nothing is changed, sent, or paid: never call a write or destructive operation such as `external_invoices_send`, `external_transactions_update_category`, or any `*_delete` operation from it.
