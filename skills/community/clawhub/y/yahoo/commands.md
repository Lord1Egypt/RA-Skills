# Yahoo Command Recipes

Run these from the installed skill folder.

## Symbol lookup

```bash
python3 yahoo_search.py "apple"
python3 yahoo_search.py "semiconductor etf"
python3 yahoo_search.py "bitcoin"
```

Use this first when the user gives a company name, theme, ETF nickname, or an ambiguous symbol.

## Single-symbol snapshot

```bash
python3 yahoo_quote.py AAPL
python3 yahoo_quote.py NVDA
python3 yahoo_quote.py BTC-USD
```

Use this for price, daily move, market state, and headline statistics on one instrument.

## Multi-ticker market brief

```bash
python3 yahoo_brief.py AAPL MSFT NVDA AMZN
python3 yahoo_brief.py SPY QQQ IWM DIA
python3 yahoo_brief.py EURUSD=X GBPUSD=X JPY=X
```

Use this to rank movers, compare watchlists, or prep a pre-market and post-market pass.

## Decision workflow

1. Resolve the exact symbol with `yahoo_search.py`.
2. Pull the latest snapshot with `yahoo_quote.py`.
3. Run `yahoo_brief.py` for peers, benchmarks, or a full watchlist.
4. Frame the setup with `thesis-card.md`.
5. Apply `risk-playbook.md` before suggesting urgency or size.
