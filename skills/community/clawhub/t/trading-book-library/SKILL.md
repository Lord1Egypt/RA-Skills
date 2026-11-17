---
name: trading-book-library
description: Consolidated trading knowledge from 62 books covering technical analysis, quantitative methods, behavioral finance, risk management, and systematic strategies. Use when analyzing markets, developing trading systems, or applying frameworks from classic trading literature.
license: MIT
metadata:
  books: 62
  categories: [technical-analysis, systematic-trading, risk-management, behavioral-finance, quantitative]
---
# Trading Book Library

Condensed wisdom from 62 trading books (17MB, 3M words). Extracted frameworks, principles, and techniques.

## Core Frameworks

### The Turtle Trading System (Turtle Trader, Way of the Turtle)
- **Entry**: 20-day breakout (buy above 20-day high)
- **Exit**: 10-day breakout in opposite direction
- **Position sizing**: ATR-based, risk 1-2% per trade
- **Pyramiding**: Add at 0.5 ATR intervals, max 4 units
- **Principle**: "Trade what you see, not what you think"

### Risk Management (Trading in the Zone, Market Wizards)
- **Core rule**: Never risk more than 1-2% on any single trade
- **R-multiple**: Every trade expressed as risk/reward multiple
- **Expectancy**: (Win% × Avg Win) - (Loss % × Avg Loss)
- **Drawdown management**: Scale down at 20% DD, stop at 30%
- **Principle**: Mark Douglas: "Anything can happen"

### Candlestick Patterns (Beyond Candlesticks, Encyclopedia of Chart Patterns)
- **Reversal**: Hammer, Shooting Star, Engulfing, Morning/Evening Star
- **Continuation**: Three White Soldiers, Rising/Falling Three Methods
- **Indecision**: Doji (Dragonfly, Gravestone, Long-legged)
- **Confirmation**: Always wait for next candle to confirm
- **Principle**: Nison: "The market is a discounting mechanism"

### Volume Price Analysis (Anna Coulling)
- **Key signal**: Volume confirms price — high volume + price move = valid
- **Testing**: Low volume on pullback = healthy, high volume = distribution
- **Climax**: Ultra-high volume + narrow range = exhaustion
- **Principle**: "Volume precedes price"

### Market Wizards Principles (Schwager)
1. **Have a method**: Every wizard had a specific, repeatable edge
2. **Cut losses**: "Losers average losers"
3. **Let winners run**: "It's not whether you're right, it's how much you make when you're right"
4. **Risk management is primary**: Position sizing > entry timing
5. **Discipline over intelligence**: Emotional control beats IQ
6. **Adapt or die**: Markets change, methods must evolve

### Behavioral Finance (Fooled by Randomness, When Genius Failed)
- **Survivorship bias**: We only see the winners, not the thousands who failed
- **Black swans**: Fat tails are real; prepare for the impossible
- **Overconfidence**: Most traders overestimate their edge
- **Principle**: Taleb: "Never cross a river that is on average 4 feet deep"

### Ichimoku Cloud (Trading Ichimoku)
- **Components**: Tenkan-sen (9), Kijun-sen (26), Senkou Span A/B (52)
- **Bullish**: Price above cloud, Tenkan > Kijun, future cloud green
- **Bearish**: Price below cloud, Tenkan < Kijun, future cloud red
- **Kumo twist**: Senkou A crossing B = trend change signal

### Buffett/Graham Value Investing (Intelligent Investor, Buffett Essays)
- **Margin of safety**: Buy below intrinsic value
- **Circle of competence**: Only invest in what you understand
- **Mr. Market**: Use volatility, don't be used by it
- **Long-term**: "Our favorite holding period is forever"

## Key Principles Cross-Referenced

### Position Sizing
| Source | Rule |
|--------|------|
| Turtle | 2% risk per trade, ATR-based sizing |
| Market Wizards | Bet more when conviction is higher |
| Van Tharp | R-multiples, position size = risk / stop distance |

### Stop Loss Placement
| Source | Method |
|--------|--------|
| Technical Analysis | Below support / above resistance |
| Turtle | 2× ATR trailing stop |
| Elder | "SafeZone" — dynamic ATR-based |

### Exit Strategies
| Source | Method |
|--------|--------|
| Turtle | 10-day low breakout |
| Minervini | Moving average crossover + volume climax |
| O'Neil | 20-25% profit target, 8% stop |

## Anti-Patterns to Avoid
1. **Averaging down** (losers average losers — Paul Tudor Jones)
2. **Over-optimization** (curve-fitting to historical data)
3. **Ignoring correlation** (multiple positions in same sector = hidden risk)
4. **Position size drift** (letting winners become oversized)
5. **Revenge trading** (trading to recover losses)
6. **Analysis paralysis** (too many indicators, no action)
7. **Premature profit-taking** (cutting winners short)

## On-Demand Chapter Lookup
The full extracted text (17.65MB, 62 books) is available at:
`C:/Users/ARTHUR~1/AppData/Local/Temp/book_skill_work/full_text.txt`

Use `search_files(pattern="book_name", path="C:/Users/ARTHUR~1/AppData/Local/Temp/book_skill_work")` to find a book's SOURCE header, then `read_file` with offset/limit to stream chapters into context. Each book is marked by its `==== SOURCE: filename.txt ====` header.