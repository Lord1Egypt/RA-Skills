---
name: ve-exchange-rates
description: Get Venezuelan exchange rates - BCV official rate, Binance P2P USDT average, and the gap between them. Use when user asks for Venezuelan dollar rates, brecha cambiaria, dolar BCV, USDT P2P, or exchange rates in Venezuela.
---

# ve-exchange-rates: Venezuelan Exchange Rates

Get current exchange rates for Venezuela:
1. **Tasa BCV** - Official Central Bank rate from the BCV website
2. **Tasa USDT Binance P2P** - Average from P2P market
3. **Brecha cambiaria** - Gap between official and parallel rates

## Usage

Run the wrapper script to get current rates:

```bash
./skills/ve-exchange-rates/scripts/get-rates.sh
```

The shell script is now a thin wrapper around a Python implementation:

```bash
python3 ./skills/ve-exchange-rates/scripts/get_rates.py
```

## Output

The script returns:
- BCV official rate (Bs/USD)
- BCV source used
- BCV "Fecha Valor" extracted from the site
- Warning if the BCV date does not match the expected current run window
- Binance P2P USDT rates (buy/sell/average)
- Gap percentage between BCV and P2P
- Example conversion from 100 USD at BCV rate into USDT at P2P rate

## Data Sources

- **BCV rate**: scraped directly from **bcv.org.ve**
- **BCV validation**: extracts and validates **Fecha Valor** from the BCV page
- **Fallback for BCV**: exchangerate-api.com only if BCV cannot be parsed
- **USDT P2P**: Binance P2P API (`p2p.binance.com`)

## Notes

- BCV is the primary source and should be treated as the authoritative rate
- The skill warns when the BCV "Fecha Valor" does not match today or tomorrow
- P2P rates fluctuate constantly based on market conditions
- Main implementation now lives in Python for readability and easier auditing
- The shell entrypoint is only a thin wrapper that invokes `get_rates.py`
- The implementation uses standard library HTTP requests and `bc` for decimal math formatting compatibility
- If BCV is temporarily unavailable, the skill falls back to a secondary source to preserve functionality
