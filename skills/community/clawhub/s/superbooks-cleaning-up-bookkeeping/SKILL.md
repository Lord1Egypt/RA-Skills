---
name: cleaning-up-bookkeeping
description: "Tidies up SuperBooks transactions and receipts: categorizes or recategorizes transactions, fixes a transaction's category or status, finds uncategorized spending, matches receipts and bills in the inbox to transactions, and finds documents. Use when the user asks to 'categorize last month's transactions', 'match the receipts in my inbox', 'find uncategorized expenses', 'fix this transaction's category', 'reconcile my receipts', or 'find the receipt for this purchase'."
---

# Bookkeeping cleanup in SuperBooks

Work through transactions that need a category or status, and connect receipts to the transactions they belong to. Every change is shown to the user before it is made.

## Connecting and calling the tools

Every operation in this skill comes from the `superbooks` MCP server, the SuperBooks connector. The server defaults to Code Mode, so the operations below are written as the `external_*` functions you call inside `superbooks:execute_typescript`. On a server set to the per-tool surface, the same operation is listed as `superbooks:<name>` without the `external_` prefix, for example `superbooks:invoices_list`.

- **Only `superbooks:search_tools` and `superbooks:execute_typescript` listed (Code Mode, the default):** call `superbooks:search_tools` first, then call each tool inside `superbooks:execute_typescript` as `external_<tool>` (for example `external_invoices_list`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **Operations listed by name:** call them directly, for example `superbooks:invoices_list`.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `superbooks:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects SuperBooks and approves that scope.
- **No `superbooks` tools at all:** SuperBooks is not connected yet. Install the SuperBooks power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

The `superbooks` MCP server has two tools: `superbooks:search_tools` (call it first, for example with `transaction`, `categor`, `inbox`, to get the exact input shapes) and `superbooks:execute_typescript` (run a short program calling the declared `external_*` functions; the program must `return` its result).

If the connection lists the operations by name instead (the per-tool surface), call them directly without the `external_` prefix.

Operations this skill uses:

- `external_transactions_list`: transactions for a period (for example `from: "2026-09-01"`), with amount, merchant and `category_slug`.
- `external_transactions_get`: one transaction in full.
- `external_categories_list`: the team's categories and their slugs. `external_categories_create` adds one the user asks for.
- `external_transactions_update_category`: set a transaction's category by slug.
- `external_transactions_update_status`: set a transaction's workflow status.
- `external_tags_list` and `external_tags_create`: labels the user may want.
- `external_inbox_list`: incoming receipts and bills waiting to be matched.
- `external_inbox_match`: attach an inbox item to a transaction.
- `external_documents_search`, `external_documents_list`, `external_documents_get`: receipts and documents already stored.

## Workflow

1. Agree the period (default: last calendar month). In one program, fetch `external_transactions_list` for it and `external_categories_list` with `await Promise.all`.
2. List the transactions that are uncategorized or that the user flagged. For each, propose a category slug from the category list, based on the merchant and amount.
3. Show the proposals as a table (date, merchant, amount, current category, proposed category) and let the user approve all, some, or edit them.
4. Apply the approved ones in one program: one `external_transactions_update_category` call per transaction, each wrapped so one failure does not hide the others. Report what changed and what failed.
5. For receipts: fetch `external_inbox_list`, pair each item with the transaction of the same amount and a close date, show the pairs, and apply `external_inbox_match` for the ones the user approves.
6. If a category the user wants does not exist, offer to create it with `external_categories_create` first.

## Code Mode pattern

```ts
const approved = [{ id: "txn_1", slug: "design_software" }];
const results = await Promise.all(
  approved.map((t) =>
    external_transactions_update_category({ id: t.id, category_slug: t.slug })
      .then(() => ({ id: t.id, ok: true }))
      .catch((e) => ({ id: t.id, error: String(e) })),
  ),
);
return results;
```

Check the real argument names in the `superbooks:search_tools` declaration before running this.

## Rules

- No change without the user's approval of that specific change. Batches are fine once the user approves the batch.
- Never guess a category slug; use one returned by `external_categories_list`.
- Deleting transactions, receipts, or categories is not offered here. Destructive operations are off by default for the team; do not ask the user to turn them on.
- Each credential is limited to 120 calls a minute. For large batches, work in chunks of about 50 and report progress between them.
