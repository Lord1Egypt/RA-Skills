---
name: toast
description: Find restaurants that order through Toast (toasttab.com) and read their menus via the toasttab-mcp server — "what can I order on Toast near me", "show the menu at this order.toasttab.com link", "is X out of stock", "does this place have vegetarian options". Requires toasttab-mcp and the ContextMint Bridge browser extension with an order.toasttab.com tab open.
---

# toasttab-mcp

Read-only access to Toast's diner side, relayed through the user's own browser.

## Workflow

1. **Find a restaurant.** `toast_find_restaurants` needs a latitude and longitude. This server has no geocoder, so convert the address or city first. Results list only places open for the dining option at `when` (default: now). An empty result late at night means "closed", not "none exist"; retry with a daytime `when`.
2. **Get its GUID.** Every directory result carries `guid`. For a link the user pasted, call `toast_resolve_restaurant`. Links containing `r-<guid>` or `?guid=` resolve with no network call. An `order.toasttab.com/online/<shortUrl>` link (or a bare shortUrl) is looked up in Toast by its slug.
3. **Read the menu.** `toast_get_menu` with `source`:
   - `online` (default): what can be ordered online.
   - `pos`: the full register menu, often much larger.
   - `both`: merged.

   Use `query` to search, and `include_out_of_stock: false` to hide sold-out items.

## The user's own account

With a signed-in toast.app tab in the bridged browser:

- `toast_list_orders`: order history, newest first. Pass `next_page_token` for older orders.
- `toast_get_order`: a full receipt. It takes `restaurant_guid` + `order_guid` from a `toast_list_orders` row.
- `toast_get_loyalty`: loyalty programs, balances and progress toward rewards.
- `toast_get_wallet`: Toast Cash balance and its units.

On a "not signed in" or "expired" error, ask the user to open or reload toast.app and sign in. Don't retry in a loop. `dining_option` and `status` are Toast's own values. Don't relabel them (an order shown as "Delivery" on toast.app can carry `TAKE_OUT`).

## In context groups

In an mcp-host context group this server joins `food`. Every tool carries a `_meta.mint` hint except `toast_healthcheck`.

- **Canonical read:** `toast_list_orders` answers `whats-new` ("is my order ready?", "anything new on my food orders?"). With `view: "brief"` it answers one line per order: `restaurant (dining option, N items) — <placed, ISO> — <status>`. The lines arrive inside the untrusted-data envelope as `data` (restaurant names are the restaurants' own text), each cut to 120 characters, and a restaurant name that starts with `-- ` or `\` is escaped with one leading `\`. A line starting `-- ` is a note, not an order: `-- none` when there are no orders, `-- error: …` when Toast reported a partial failure beside the orders that did arrive, and `-- more` when older orders exist (call again with `view: "compact"` to get `next_page_token`). It has no subject, because it reads the one signed-in toast.app account. It has no date range either, because Toast pages orders by token.
- Nothing here answers `whats-due` or `whats-on`. Toast has no reservations or due dates. Restaurants, menus, receipts, loyalty and Toast Cash are `lookup` hints, and `toast_graphql` is `other`.
- **A compound ask** like "anything new with dinner, and is my takeout ready?" fans out to every `food` member's canonical `whats-new` read. Toast adds one section of brief order lines.
- This server is browser-bridged. When no bridged browser is connected (ContextMint Bridge with a signed-in toast.app tab), the group reports Toast as "needs your browser open" and does not call it. Ask the user to open the browser, then retry.

## Rules

- Report out-of-stock items as out of stock today, not as removed.
- Prices are dollars (`12.5` = $12.50). Modifier prices are not included.
- `truncated: true` means more items exist. Say so, or raise `limit`.
- On a "no order.toasttab.com tab", "Forbidden" or edge-block error, ask the user to open any restaurant's ordering page on `order.toasttab.com` in their browser and complete any check. Don't retry in a loop.
- `toast_graphql` is for exploration (read-only queries). Correct a query from the validation errors it returns. Don't guess field names repeatedly.
