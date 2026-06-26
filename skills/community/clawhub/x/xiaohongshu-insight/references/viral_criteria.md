# Xiaohongshu Viral Post Detection Algorithm

## Indexing Criteria

### 1. Low-Follower Viral Posts

**Definition**: Posts from accounts with relatively few followers whose interaction volume significantly exceeds the category average.

**Determination Criteria**:
```
Follower Count < 5,000
AND
Total Engagement > Category Average Engagement × 3
AND
Engagement Rate > 10%
```

**Weight Coefficients**:
| Follower Range | Required Engagement Multiple |
|----------------|----------------------------|
| < 1,000 | 2.0x |
| 1,000 - 3,000 | 2.5x |
| 3,000 - 5,000 | 3.0x |

**Example**:
- Beauty category average engagement: 500
- Blogger has 2,000 followers, post engagement: 1,500
- Determination: 1,500 > 500 × 2.5 = 1,250 ✓ Low-Follower Viral

---

### 2. Periodic High-Engagement Posts

**Definition**: Posts with like growth exceeding 1,000 within 7 days and demonstrating a clear sustained growth trend.

**Determination Criteria**:
```
7-Day Like Growth > 1,000
AND
Consecutive Growth Days >= 3
AND
Average Daily Growth Rate > 15%
```

**Growth Trend Calculation**:
```
Avg Daily Growth Rate = (Today's Likes - Likes 7 Days Ago) / 7 / Likes 7 Days Ago × 100%
```

**Trend Types**:
| Type | Growth Rate | Description |
|------|-------------|-------------|
| Explosive | > 50% | Rapid short-term burst |
| Steady | 15% - 50% | Consistent and stable growth |
| Long-Tail | < 15% | Slow and sustained growth over time |

---

### 3. Single-Day Interaction Spike

**Definition**: Posts with a daily increase in likes + saves + comments exceeding 500.

**Determination Criteria**:
```
Daily Interaction Increase >= 500
OR
Daily Like Increase >= 300
OR
Daily Save Increase >= 200
```

**Spike Levels**:
| Level | Daily Increase | Label |
|-------|----------------|-------|
| S-Level | > 2,000 | Super Viral |
| A-Level | 1,000 - 2,000 | Major Viral |
| B-Level | 500 - 1,000 | Medium Viral |
| C-Level | 300 - 500 | Minor Viral |

---

### 4. Sustained Interaction Growth

**Definition**: Posts with increasing interaction volume for 3 consecutive days, with an average daily growth rate exceeding 20%.

**Determination Criteria**:
```
3 Consecutive Days of Interaction Increase
AND
Average Daily Growth Rate > 20%
AND
Day 3 Interactions > Day 1 Interactions × 1.5
```

**Growth Pattern Detection**:
```python
def detect_growth_pattern(daily_engagement):
    """
    daily_engagement: [day1, day2, day3, ...]
    """
    # Check consecutive increase
    is_increasing = all(daily_engagement[i] < daily_engagement[i+1] 
                        for i in range(len(daily_engagement)-1))
    
    # Calculate growth rates
    growth_rates = [(daily_engagement[i+1] - daily_engagement[i]) / daily_engagement[i] 
                    for i in range(len(daily_engagement)-1)]
    avg_growth_rate = sum(growth_rates) / len(growth_rates)
    
    return is_increasing and avg_growth_rate > 0.20
```

---

## Composite Viral Score

### Scoring Formula

```
Viral Score = Σ (Dimension Score × Weight)

Dimension Weights:
- Low-Follower Viral: 25%
- Periodic High-Engagement: 25%
- Single-Day Spike: 25%
- Sustained Growth: 25%
```

### Score Grading

| Score | Grade | Description |
|-------|-------|-------------|
| 90 - 100 | S-Level | Super Viral, platform-wide recommendation |
| 80 - 89 | A-Level | Major Viral, category trending |
| 70 - 79 | B-Level | Medium Viral, worth attention |
| 60 - 69 | C-Level | Minor Viral, potential |
| < 60 | - | Does not meet viral criteria |

### Dimension Score Calculation

**Low-Follower Viral Score**:
```
Score = min(100, (Actual Engagement / Baseline Engagement) × 50 + 50)
```

**Periodic High-Engagement Score**:
```
Score = min(100, (7-Day Growth / 1000) × 40 + (Growth Rate / 0.15) × 30 + 30)
```

**Single-Day Spike Score**:
```
Score = min(100, (Daily Spike / 500) × 50 + 50)
```

**Sustained Growth Score**:
```
Score = min(100, (Growth Rate / 0.20) × 50 + 50)
```

---

## Category Baseline Values

Different categories have different baseline engagement values:

| Category | Average Engagement | Viral Threshold |
|----------|-------------------|-----------------|
| Beauty & Skincare | 500 | 1,500 |
| Fashion & Styling | 800 | 2,400 |
| Food & Dining | 600 | 1,800 |
| Travel Guides | 400 | 1,200 |
| Home & Lifestyle | 350 | 1,050 |
| Parenting & Childcare | 450 | 1,350 |
| Career & Growth | 300 | 900 |
| Relationships & Psychology | 550 | 1,650 |
| Knowledge & Education | 400 | 1,200 |
| Entertainment & Gossip | 1,200 | 3,600 |

---

## Exclusion Rules

The following posts are excluded from viral indexing:

1. **Violative Content**: Contains sensitive keywords or policy violations
2. **Suspected Manipulation**: Abnormal interaction growth indicative of artificial inflation
3. **Duplicate Content**: Highly similar to existing viral content
4. **Outdated Timeliness**: Posts older than 30 days (unless exhibiting sustained high growth)
5. **Low-Quality Content**: Blurry images or hollow content

---

## Algorithm Update Log

- **v1.0** (2024-01): Initial viral detection algorithm launched
- **v1.1** (2024-03): Added differentiated category baseline values
- **v1.2** (2024-06): Optimized weight coefficients for low-follower viral detection
- **v1.3** (2024-09): Added sustained growth pattern recognition
- **v2.0** (2024-12): Composite scoring system launched