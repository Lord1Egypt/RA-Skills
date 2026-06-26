# Sentiment Analysis Workflow

Complete workflow for conducting sentiment analysis using the Verosight API.

## Step 1: Authentication

```bash
# Set your API key
export VEROSIGHT_API_KEY="vlt_live_YOUR_KEY"

# Get JWT token (valid 24h)
JWT=$(curl -s -X POST "https://api.verosight.com/v1/auth/token" \
  -H "X-API-Key: $VEROSIGHT_API_KEY" | jq -r '.token')

# Verify token works
curl -s "https://api.verosight.com/v1/account/balance" \
  -H "Authorization: Bearer $JWT"
```

## Step 2: Get Sentiment Data

```bash
curl -s "https://api.verosight.com/v1/analytics/sentiment?query=KEYWORD&sources=x,instagram,tiktok&days=7" \
  -H "Authorization: Bearer $JWT" | jq .
```

### Response Fields

| Field | Description |
|-------|-------------|
| `positive` / `negative` / `neutral` | Post counts by sentiment |
| `positive_pct` / `negative_pct` / `neutral_pct` | Percentage breakdown |
| `weighted_positive_pct` / `weighted_negative_pct` | Engagement-weighted percentages |
| `sample_positive` / `sample_negative` | Sample posts with engagement data |
| `sample_independent_negative` | Social media comments with negative sentiment |
| `post_positive` / `post_negative` / `post_neutral` | Post-level sentiment counts |
| `thread_positive` / `thread_negative` | Thread-level sentiment counts |
| `independent_positive` / `independent_negative` | Independent comment sentiment |

## Step 3: Get Volume Trend

```bash
curl -s "https://api.verosight.com/v1/analytics/volume?query=KEYWORD&days=7" \
  -H "Authorization: Bearer $JWT" | jq .
```

Returns daily breakdown of posts and comments by platform.

## Step 4: Get High-Engagement Posts

```bash
# Negative posts from X
curl -s "https://api.verosight.com/v1/posts?query=KEYWORD&sources=x&sentiment=negative&limit=15&days=7" \
  -H "Authorization: Bearer $JWT" | jq .

# All posts from specific platforms
curl -s "https://api.verosight.com/v1/posts?query=KEYWORD&sources=x,threads&limit=20&days=7" \
  -H "Authorization: Bearer $JWT" | jq .
```

## Step 5: Compile Report

Use the following structure for your report:

### Report Template

```markdown
# 🔍 SDV REPORT
## Keyword: "[KEYWORD]"
**Period:** [START] – [END] | **Sources:** [PLATFORMS]

---

## 📊 SENTIMENT OVERVIEW

| Sentiment | Count | % | Weighted |
|-----------|-------|---|----------|
| Positive  | X     | X%| X%       |
| Negative  | X     | X%| X%       |
| Neutral   | X     | X%| X%       |

**Status:** [CRITICAL / HIGH / MEDIUM / LOW]

## 📈 VOLUME TREND

| Date | Posts | Change |
|------|-------|--------|
| Day 1| X     | -      |
| Day 2| X     | +X%    |

## 🔴 TOP NEGATIVE NARRATIVES

1. **[Narrative title]** — @account (Platform, X likes, X shares)
   - Full quote or summary

2. **[Narrative title]** — @account (Platform, X likes)
   - Full quote or summary

## 🟢 TOP POSITIVE NARRATIVES

1. **[Narrative title]** — @account (Platform, X likes)
   - Full quote or summary

## 👤 VOCAL ACCOUNTS (Negative)

| Account | Platform | Engagement | Narrative |
|---------|----------|------------|-----------|
| @user1  | X        | 500 likes  | Topic A   |
| @user2  | Threads  | 200 likes  | Topic B   |

## 📡 PLATFORM BREAKDOWN

| Platform | Volume | % | Engagement | Dominant Sentiment |
|----------|--------|---|------------|-------------------|
| News Portal | X | X% | Low | Factual |
| X (Twitter) | X | X% | Medium | Opinion/criticism |
| Threads     | X | X% | HIGH | Emotional/viral |

## 💡 INSIGHTS

1. [Key finding about sentiment trend]
2. [Key finding about narrative shift]
3. [Key finding about platform dynamics]

## ⚠️ PREDICTIONS (48h)

| Risk | Probability | Impact | Trigger | Timeline |
|------|-------------|--------|---------|----------|
| Volume spike | High | High | Event X | 0-24h |
| Narrative shift | Medium | Medium | Statement Y | 24-48h |

## 📋 RECOMMENDATIONS

### Immediate (0–24h)
- Action 1
- Action 2

### Short-term (1–7 days)
- Action 3
- Action 4

### Medium-term (1–4 weeks)
- Action 5
- Action 6
```

## Interpreting Results

### Sentiment Status Levels

| Status | Negative % | Weighted Neg | Action |
|--------|-----------|--------------|--------|
| CRITICAL | >50% | >60% | Immediate crisis response |
| HIGH | 30-50% | 40-60% | Active monitoring + counter-narrative |
| MEDIUM | 15-30% | 20-40% | Regular monitoring |
| LOW | <15% | <20% | Passive monitoring |

### Bot Detection Indicators

- Same account posting multiple times about one topic
- Identical content across different accounts
- New accounts with abnormally high posting frequency
- Coordinated timing (posts within minutes of each other)
- Low follower count with high post count

### Engagement Benchmarks (Indonesian social media)

| Metric | Low | Medium | High | Viral |
|--------|-----|--------|------|-------|
| Likes (X) | <10 | 10-100 | 100-1K | >1K |
| Likes (Threads) | <5 | 5-50 | 50-500 | >500 |
| Views (X) | <1K | 1K-10K | 10K-100K | >100K |
| Shares | <5 | 5-50 | 50-500 | >500 |
