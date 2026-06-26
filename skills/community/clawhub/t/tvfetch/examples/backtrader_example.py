"""
Backtrader integration example.
Fetches BTC daily data from TradingView and runs a simple SMA crossover strategy.

Install: pip install backtrader
"""
import tvfetch
from tvfetch import exporters

try:
    import backtrader as bt
except ImportError:
    print("Install backtrader first:  pip install backtrader")
    raise


class SmaCross(bt.Strategy):
    params = dict(fast=10, slow=30)

    def __init__(self):
        self.fast = bt.ind.SMA(period=self.p.fast)
        self.slow = bt.ind.SMA(period=self.p.slow)
        self.cross = bt.ind.CrossOver(self.fast, self.slow)

    def next(self):
        if self.cross > 0 and not self.position:
            self.buy()
        elif self.cross < 0 and self.position:
            self.sell()


# Fetch data from TradingView
print("Fetching BTCUSDT 1D data...")
result = tvfetch.fetch("BINANCE:BTCUSDT", "1D", bars=500)
print(f"Got {len(result)} bars: {result}")

# Convert to backtrader feed
feed = exporters.to_backtrader(result)

# Run the strategy
cerebro = bt.Cerebro()
cerebro.adddata(feed)
cerebro.addstrategy(SmaCross)
cerebro.broker.setcash(10_000)
cerebro.broker.setcommission(0.001)

print(f"\nStarting portfolio: ${cerebro.broker.getvalue():,.2f}")
cerebro.run()
print(f"Final portfolio:    ${cerebro.broker.getvalue():,.2f}")
