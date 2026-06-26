# Symbol Resolution

Before placing any order, you need the `universal_symbol_id` for the instrument.
This is SnapTrade's internal ID that uniquely identifies a security + exchange combination.

---

## Step 1: Resolve Ticker → universal_symbol_id

```python
response = snaptrade.reference_data.get_symbols_by_ticker(
    query=ticker,  # e.g. "AAPL", "MSFT", "CNR.TO"
)
symbol = response.body[0]
universal_symbol_id = symbol["id"]
```

**Ticker format (Yahoo Finance convention):**
- NYSE / NASDAQ — no suffix: `AAPL`, `MSFT`, `TSLA`
- TSX — `.TO` suffix: `CNR.TO`, `SHOP.TO`
- Other exchanges — check Yahoo Finance for the correct suffix

---

## Step 2: Confirm with a Quote

After resolving the symbol ID, confirm it and get the latest brokerage quote.
Also use this to double-check you have the right instrument before placing an order.

```python
response = snaptrade.trading.get_user_account_quotes(
    user_id=user_id,
    user_secret=user_secret,
    account_id=account_id,
    symbols=universal_symbol_id,  # comma-separated string for multiple symbols
)
quotes = response.body
# Each quote: symbol (with id), bid_price, ask_price, last_trade_price, bid_size, ask_size
```

---

## Notes

- Quotes from this endpoint may be **delayed** depending on the brokerage
- For real-time prices used in strategy logic (RSI, MACD triggers etc.), use a
  dedicated market data provider such as Polygon.io or Yahoo Finance
- Symbol IDs can change if a stock changes exchanges — do not cache long-term
