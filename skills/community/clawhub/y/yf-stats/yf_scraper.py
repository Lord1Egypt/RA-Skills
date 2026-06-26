import yfinance as yf
import matplotlib.pyplot as plt
import sys
import argparse

def get_data(ticker_symbol, show_chart=False):
    ticker = yf.Ticker(ticker_symbol)
    
    # Text data
    info = ticker.info
    print(f"Ticker: {ticker_symbol}")
    print(f"Current Price: ${info.get('currentPrice', 'N/A')}")
    print(f"52-Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}")

    # Chart generation
    if show_chart:
        # Fetch 6 months of history
        hist = ticker.history(period="6mo")
        
        plt.figure(figsize=(10, 5))
        plt.plot(hist.index, hist['Close'], label='Close Price', color='#1f77b4')
        plt.title(f"{ticker_symbol} - 6 Month Trend")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        
        # Save as file so the agent can upload it
        filename = f"{ticker_symbol}_chart.png"
        plt.savefig(filename)
        plt.close()
        print(f"\n[CHART GENERATED: {filename}]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ticker", help="Stock ticker symbol")
    parser.add_argument("--chart", action="store_true", help="Generate a price chart")
    args = parser.parse_args()

    get_data(args.ticker.upper(), args.chart)
