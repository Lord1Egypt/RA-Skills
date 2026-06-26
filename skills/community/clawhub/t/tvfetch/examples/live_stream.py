"""
Live price streaming example — streams BTC, ETH, and EURUSD for 30 seconds.
"""
import tvfetch

def on_update(bar: tvfetch.LiveBar) -> None:
    direction = "+" if bar.change >= 0 else "-"
    print(
        f"{bar.symbol:<22}  {bar.close:>12.4f}  "
        f"{bar.change_pct:>+7.2f}%  "
        f"vol={bar.volume:>10.4f}  "
        f"{bar.timestamp.strftime('%H:%M:%S')} {direction}"
    )

print("Streaming live prices for 30 seconds...\n")
tvfetch.stream(
    ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "FX:EURUSD"],
    on_update=on_update,
    timeframe="1",
    duration=30,
)
print("\nDone.")
