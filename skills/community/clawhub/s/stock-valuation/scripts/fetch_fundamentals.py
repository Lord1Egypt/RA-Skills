#!/usr/bin/env python3
"""Fetch fundamental data for a ticker using yfinance. Outputs JSON."""
import sys
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: fetch_fundamentals.py TICKER [PEER1 PEER2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        import yfinance as yf
    except ImportError:
        print("ERROR: yfinance not installed. Run with: uv run --with yfinance python3 fetch_fundamentals.py TICKER", file=sys.stderr)
        sys.exit(1)

    tickers = [t.upper() for t in sys.argv[1:]]
    result = {}

    for ticker in tickers:
        t = yf.Ticker(ticker)
        info = t.info
        keys = [
            'shortName','sector','industry','currentPrice','marketCap',
            'trailingPE','forwardPE','trailingEps','forwardEps',
            'priceToBook','enterpriseValue','enterpriseToRevenue','enterpriseToEbitda',
            'totalRevenue','revenueGrowth','grossMargins','operatingMargins','profitMargins',
            'totalCash','totalDebt','bookValue','sharesOutstanding',
            'fiftyTwoWeekHigh','fiftyTwoWeekLow','dividendYield','beta',
            'returnOnEquity','freeCashflow','operatingCashflow',
            'earningsGrowth','revenuePerShare','trailingPegRatio'
        ]
        data = {k: info.get(k) for k in keys if info.get(k) is not None}

        # Quarterly financials
        try:
            qf = t.quarterly_income_stmt
            if qf is not None and not qf.empty:
                quarters = []
                for col in qf.columns[:4]:  # Last 4 quarters
                    q = {'period': str(col.date())}
                    for row in ['Total Revenue','Gross Profit','Operating Income','EBITDA',
                                'Net Income','Diluted EPS','Basic EPS']:
                        if row in qf.index:
                            val = qf.loc[row, col]
                            if val is not None and str(val) != 'nan':
                                q[row] = float(val)
                    quarters.append(q)
                data['quarterly'] = quarters
        except Exception:
            pass

        result[ticker] = data

    print(json.dumps(result, indent=2, default=str))

if __name__ == '__main__':
    main()
