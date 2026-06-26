# Stock Watchlist

Edit rows inside the marker block. Keep the table header unchanged.

Recommended workflow:
- Add rows manually in this file, then run `watchlist sync`.
- Use `watchlist add` when you want the script to resolve a query for you.
- Keep `symbol` and `quote_id` after sync so later quote requests stay stable.

<!-- stock-watchlist:start -->
| query | symbol   | quote_id | name | cost_price | quantity | note |
| ----- | -------- | -------- | ---- | ---------- | -------- | ---- |
<!-- stock-watchlist:end -->
