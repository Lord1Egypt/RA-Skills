# Sentiment Analysis for Xiaohongshu Posts

## Overview

Xiaohongshu (小红书) posts are unstructured user-generated content. Sentiment analysis helps extract restaurant quality signals from these posts.

## Simplified Approach (Current Implementation)

The skill uses a keyword-based sentiment scoring system:

### Positive Keywords (+1)
```
好吃, 美味, 推荐, 值得, 喜欢, 棒, 赞, 完美, 正宗, 新鲜,
环境好, 服务好, 性价比, 回购, 打卡, 必吃, 太好吃了
```

### Negative Keywords (-1)
```
难吃, 失望, 差评, 不推荐, 避雷, 贵, 服务差, 态度差,
不好吃, 没什么, 普通, 一般, 就那样, 不会再来了
```

### Neutral Keywords (0)
```
还行, 可以, 试试, 感觉, 似乎, 差不多
```

## Scoring Formula

```
sentiment_score = (positive_count - negative_count) / total_mentions
```

Range: -1.0 (very negative) to 1.0 (very positive)

## Example Calculation

Post: "这家日料店太好吃了！环境很好，服务也很热情，就是有点贵。值得推荐！"

- Positive: 太好吃了, 很好, 热情, 值得, 推荐 (5)
- Negative: 贵 (1)
- Total mentions: 6

```
sentiment_score = (5 - 1) / 6 = 0.67
```

Result: Moderately positive (0.67)

## Advanced Approaches (Future Enhancement)

### 1. Machine Learning Models

**SnowNLP** (Chinese NLP library)
```python
from snownlp import SnowNLP

text = "这家餐厅太好吃了！"
s = SnowNLP(text)
sentiment = s.sentiments  # 0-1, higher is more positive
```

**Pros**: More accurate, understands context
**Cons**: Requires additional dependency, slower

### 2. Aspect-Based Sentiment Analysis

Extract sentiment for specific aspects:

```
Food:     好吃, 新鲜, 正宗 → +0.8
Service:  服务好, 热情 → +0.6
Price:    有点贵, 性价比高 → -0.2
Atmosphere: 环境很好 → +0.7
```

Weighted average:
```
overall_sentiment = (food × 0.4) + (service × 0.2) +
                   (price × 0.2) + (atmosphere × 0.2)
```

### 3. Emoji Analysis

Xiaohongshu posts often contain emojis:

| Emoji | Sentiment | Weight |
|-------|-----------|--------|
| 😋, 😍, 👍 | Positive | +0.3 |
| 😔, 😡, 👎 | Negative | -0.3 |
| 😐, 🤔 | Neutral | 0 |

## Integration with Recommendation Score

Sentiment score is used in two ways:

### 1. Consistency Calculation
```
sentiment_alignment = (sentiment_score + 1) / 2  # Normalize to 0-1
```

Used to verify if Dianping ratings match Xiaohongshu sentiment.

### 2. Quality Filter
Posts with sentiment < 0.0 (negative) are excluded from aggregation.

## Implementation Notes

### Current State
The skill currently uses a simplified keyword-based approach for:
- Speed (no ML model loading)
- Simplicity (no heavy dependencies)
- Explainability (clear which keywords triggered)

### When to Upgrade
Consider ML-based sentiment analysis when:
- Processing >1000 posts per day
- Need higher accuracy (>85%)
- Building production system
- Have GPU resources available

### Recommended Libraries

**For Simple Scoring** (Current):
```python
# No external libraries needed
# Pure Python keyword matching
```

**For ML-Based** (Future):
```bash
pip install snownlp jieba
```

```python
from snownlp import SnowNLP
import jieba

text = "这家餐厅太好吃了！"
s = SnowNLP(text)
print(s.sentiments)  # 0.93 (very positive)

# Aspect-based (requires training)
keywords = jieba.cut(text)
# Classify each keyword into food/service/price/atmosphere
```

## Limitations

1. **Sarcasm Detection**
   - "这服务'真好'啊" (sarcastic) → Misses negativity
   - ML models also struggle with this

2. **Context Dependence**
   - "有点贵" is negative but mild
   - "太贵了" is strongly negative
   - Current approach treats both equally

3. **Regional Slang**
   - Xiaohongshu users use platform-specific slang
   - Slang changes over time
   - Requires periodic keyword list updates

## Testing

Validate sentiment analysis by manually scoring 20-30 posts and comparing:

```python
posts = [
    {"text": "太好吃了！", "expected": 0.9, "actual": 0.8},
    {"text": "一般般吧", "expected": 0.2, "actual": 0.1},
    # ...
]

accuracy = sum(1 for p in posts
              if abs(p['expected'] - p['actual']) < 0.2) / len(posts)

print(f"Accuracy: {accuracy * 100:.1f}%")
```

Target: >75% accuracy with simplified approach

## Resources

- **SnowNLP Documentation**: https://github.com/isnowfy/snownlp
- **Jieba (Chinese Word Segmentation)**: https://github.com/fxsjy/jieba
- **Chinese Sentiment Analysis**: Research papers on social media sentiment in Chinese

**Last Updated**: 2026-02-09
