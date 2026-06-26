---
name: qc-deep-feature-forensics
description: 12-dimensional technical feature attribution engine — compares winner vs loser trade entry conditions using RSI, Bollinger, MACD, volume surge, gap, and more to find what makes winning entries different.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - pip3
    emoji: "\U0001F9EC"
---

# QC Deep Feature Forensics

Go beyond P&L analysis. This skill answers: **"What market microstructure conditions were present when winning trades were entered vs losing trades?"**

## When to use

- "Why do some of my trades win and others lose?"
- "What entry conditions lead to profitable trades?"
- "Run a feature attribution on my backtest"
- "What-if analysis: would filtering out RSI > 70 trades help?"
- After running `qc-order-forensics` for high-level diagnosis, use this for deep-dive

## How it works

```bash
python3 deep_forensics.py <orders.csv>
```

### Pipeline

1. **Order Reconstruction**: Groups raw orders into closed trade pairs (buy group + sell group per contract)
2. **Batch Data Download**: Fetches historical daily OHLCV from Yahoo Finance per ticker (cached to local CSV to avoid re-downloading)
3. **Technical Indicator Pre-computation**: Calculates all 12 indicators on the full ticker history
4. **Feature Extraction**: For each trade, extracts a 12-dimensional feature vector at the entry date
5. **Winner vs Loser Comparison**: Statistical dual-sample comparison with diagnostic interpretation
6. **What-If Simulation**: Tests hypothetical filters and measures their net impact on total P&L

### 12 Feature Factors

| Factor | Description | Format |
|--------|-------------|--------|
| `gap_pct` | Gap open % vs previous close | % |
| `volume_surge` | Volume / 10-day average volume | x |
| `ma5_deviation` | (Close - MA5) / MA5 | % |
| `ma20_deviation` | (Close - MA20) / MA20 | % |
| `volatility_expansion` | Intraday range / 5-day ATR | x |
| `intraday_return` | (Close - Open) / Open | % |
| `rsi_14` | RSI(14) | 0-100 |
| `bb_position` | Position in Bollinger Band (0=lower, 1=upper) | 0-1 |
| `macd_hist_norm` | MACD histogram / Close | ratio |
| `consecutive_up_days` | Count of consecutive up-close days | days |
| `distance_from_20d_high` | (Close - 20d High) / 20d High | % |
| `prev_day_return` | Previous day's return | % |

## Report Output

### Section 1: Feature Mean Comparison (Winners vs Losers)

Table showing each factor's mean for winning vs losing trades, the delta, and a diagnostic interpretation. Example:

```
| Gap Open %    | +3.2% | +1.1% | +2.1% | Winners enter on stronger gaps |
| Volume Surge  | 2.8x  | 1.4x  | +1.4x | Volume confirmation helps      |
```

### Section 2: What-If Filter Analysis

Simulates applying each filter rule to the full trade set and measures:
- How many losers would be avoided
- How many winners would be accidentally killed
- Net impact on total portfolio ROI
- Verdict: Shield (improves total P&L), Toxic (kills outlier wins), or Marginal

Filters tested include: gap > 2%, volume > 2x, below MA20, RSI > 70, BB > 0.95, consecutive up > 3, near 20d high, negative intraday return.

**Combined filter**: Stacks all "Shield" filters and reports the combined effect.

### Section 3: Winner Entry Profile

Statistical percentile ranges (25th-75th) for each factor among winning trades. Defines the "ideal entry environment" envelope.

## Output Files

- `<name>_features.csv` — Full feature matrix for all trades
- `feature_diagnosis.md` — Complete markdown report

## Caching

YFinance data is cached per-ticker in `yfinance_cache/` alongside the orders CSV. Subsequent runs on the same data skip downloads entirely.

## Dependencies

```bash
pip3 install pandas numpy yfinance
```

## Rules

- **Do not modify files in `yfinance_cache/` manually.** The cache uses date-range coverage checks. Corrupted cache files will cause silent data gaps in indicator calculations.
- **Do not change indicator parameters (RSI period, Bollinger window, etc.)** without understanding that all 12 factors are calibrated together. Changing one shifts the entire winner/loser comparison baseline.
- **What-If verdicts ("Shield" vs "Toxic") are based on total portfolio ROI impact, not win rate.** A filter that improves win rate but kills outlier wins is marked "Toxic" because total P&L decreases. Do not override this logic.
- **Internet access is required** on first run for each ticker. Subsequent runs use cached data. If you run in an offline environment, pre-populate the cache directory.
- **Minimum 20 closed trades required** for statistically meaningful feature comparison. With fewer trades, the report will still generate but conclusions are unreliable.
