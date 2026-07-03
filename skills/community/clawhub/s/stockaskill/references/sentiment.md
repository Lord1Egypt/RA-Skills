# Sentiment Adjustment

The sentiment aggregator (`scripts/sentiment/aggregator.py`) computes an adjustment factor based on:

## Components

| Component | Source | Description |
|-----------|--------|-------------|
| Market breadth | Index data | Advance-decline ratio |
| North-bound flow | 沪股通/深股通 | Net buy for A-shares |
| Guba sentiment | East Money 股吧 | Community sentiment score |

## Adjustment formula

```
adjustment_factor = 0.8 + 0.4 × combined_sentiment_score
```

- `combined_sentiment_score` ranges from 0 (bearish) to 1 (bullish)
- `adjustment_factor` ranges from 0.8 to 1.2
- Final adjusted score = strategy base score × adjustment_factor, clamped to [0, 100]

## Usage

```python
from sentiment.aggregator import SentimentAggregator

sentiment = SentimentAggregator("600519", "A").get_sentiment_report()
# Returns adjustment_factor (0.8-1.2), sources, scores
```

## Note

- Sentiment adjustment only triggers when the combined impact exceeds ±5%
- North-bound flow is A-share only; for HK/US markets, only breadth and news sentiment apply
