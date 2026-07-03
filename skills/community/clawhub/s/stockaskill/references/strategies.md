# Strategy System

6 quantitative strategies with weighted voting. Final signal computed as weighted vote across strategies.

## Strategy weights (from config.py)

| Strategy | Weight | Logic |
|----------|:---:|-------|
| Multi-Factor | 30% | 7-factor composite, >=70=BUY, <=30=SELL |
| Deep Value | 25% | PE<25th%, PB<1.5, yield>3%, F-Score>=6 |
| GARP | 20% | PEG<1, ROE>15%, revenue growth>10% |
| MA Trend | 15% | MA5/10/20/60 alignment, golden/death cross |
| Contrarian | 10% | Oversold>15% from 60d high, low valuation |
| Alpha Momentum | 15% | Momentum(30%)+LowVol(28%)+Quality(21%)+Value(14%)+Growth(7%) |

## Final signal

- **BUY** if weighted score >= 65
- **SELL** if weighted score <= 35
- **HOLD** otherwise

## Enhanced Momentum weights (from config.py: enhanced_weights)

| Factor | Weight |
|--------|:---:|
| Momentum | 35% |
| Quality | 20% |
| Low Vol | 18% |
| Value | 17% |
| Growth | 10% |

## Core-Satellite Enhanced variant

When the user mentions "enhanced" or "core-satellite":
- **ETF core** (40% total): 沪深300 (17%), 创业板 (12%), 科创50 (11%)
- **Alpha momentum satellite** (60% total): Top 3 stocks by enhanced score, 20% each
- Uses enhanced weights (above) instead of standard factor weights

The exact current weights live in `scripts/config.py`. Check there if weights need verification.
