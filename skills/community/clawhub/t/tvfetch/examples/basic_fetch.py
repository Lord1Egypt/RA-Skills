"""
Basic fetch examples — run this to see tvfetch in action.
"""
import tvfetch

# ── 1. Simple fetch — returns a pandas DataFrame ──────────────────────────────
print("=== 1. Fetch BTC/USDT daily (last 30 bars) ===")
result = tvfetch.fetch("BINANCE:BTCUSDT", "1D", bars=30)
print(result)          # FetchResult summary
print(result.df.tail())

# ── 2. Different asset classes ────────────────────────────────────────────────
print("\n=== 2. Fetch EURUSD hourly ===")
forex = tvfetch.fetch("FX:EURUSD", "60", bars=100)
print(forex.df.tail(5))

print("\n=== 3. Fetch Apple stock daily ===")
aapl = tvfetch.fetch("NASDAQ:AAPL", "1D", bars=100)
print(aapl.df.tail(5))

# ── 3. Multiple symbols at once (single connection, much faster) ──────────────
print("\n=== 4. Fetch multiple symbols at once ===")
results = tvfetch.fetch_multi(
    ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "NASDAQ:AAPL", "FX:EURUSD"],
    timeframe="1D",
    bars=30,
)
for sym, r in results.items():
    print(f"  {sym}: {len(r)} bars  ({r.df.index[0].date()} to {r.df.index[-1].date()})")

# ── 4. Export to file ─────────────────────────────────────────────────────────
print("\n=== 5. Export to CSV ===")
btc = tvfetch.fetch("BINANCE:BTCUSDT", "1D", bars=365)
btc.to_csv("btc_daily_1year.csv")
print(f"Saved {len(btc)} bars to btc_daily_1year.csv")

# ── 5. Search for symbols ─────────────────────────────────────────────────────
print("\n=== 6. Search for 'bitcoin' ===")
hits = tvfetch.search("bitcoin", symbol_type="crypto", limit=5)
for h in hits:
    print(f"  {h.symbol:<30} {h.description}")

# ── 6. Use as DataFrame shortcut ──────────────────────────────────────────────
print("\n=== 7. Direct DataFrame shortcut ===")
df = tvfetch.fetch_df("BINANCE:BTCUSDT", "1D", bars=10)
print(df)
