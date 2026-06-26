---
name: sentiment-bot
description: Analyze sentiment of text or URLs. Supports batch analysis, emotion detection, comparative and trend analysis.
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "🎭"
    homepage: https://aiprox.dev
    requires:
      env:
        - AIPROX_SPEND_TOKEN
---

# Sentiment Bot

Analyze sentiment in text or fetched URLs. Detects emotions, scores intensity, and explains reasoning. Supports batch analysis of up to 10 texts, comparative analysis across multiple inputs, and trend analysis for chronological content. Context-aware framing for social media, news, reviews, and general content.

## When to Use

- Monitoring social media posts for brand sentiment
- Analyzing news articles for tone and editorial framing
- Comparing sentiment across multiple texts or sources
- Tracking sentiment trends over a batch of content
- Analyzing product or service reviews

## Usage Flow

1. Provide `text` (raw string) or `url` (fetched and analyzed), or a `texts` array for batch mode
2. Optionally set `mode`: `single` (default) or `batch`
3. Optionally set `context`: `general` (default), `social`, `news`, or `review` — adjusts how sentiment is framed
4. Use `task` to drive analysis framing — mention "compare" or "vs" for comparative mode, "trend" for trend analysis
5. AIProx routes to the sentiment-bot agent
6. Returns sentiment, score, magnitude, emotions, reasoning, and confidence

## Security Manifest

| Permission | Scope | Reason |
|------------|-------|--------|
| Network | aiprox.dev | API calls to orchestration endpoint |
| Env Read | AIPROX_SPEND_TOKEN | Authentication for paid API |

## Make Request — Single

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -H "X-Spend-Token: $AIPROX_SPEND_TOKEN" \
  -d '{
    "text": "Can't believe they shipped this broken update lmao, every single time 🙄",
    "context": "social"
  }'
```

### Response — Single

```json
{
  "sentiment": "negative",
  "score": 0.18,
  "magnitude": 0.82,
  "emotions": ["frustration", "sarcasm", "disappointment"],
  "reasoning": "Strong negative sentiment expressed through sarcasm ('lmao'), eye-roll emoji, and repeated frustration ('every single time'). The casual social register amplifies the critical tone.",
  "confidence": "high",
  "mode": "single",
  "context": "social"
}
```

## Make Request — Batch

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -H "X-Spend-Token: $AIPROX_SPEND_TOKEN" \
  -d '{
    "texts": [
      "Absolutely love the new interface, so much faster!",
      "It is fine I guess, nothing special",
      "Third outage this month. Done with this service."
    ],
    "mode": "batch",
    "context": "review"
  }'
```

### Response — Batch

```json
{
  "results": [
    {"index": 0, "sentiment": "positive", "score": 0.91, "magnitude": 0.85, "emotions": ["joy", "enthusiasm"], "reasoning": "Enthusiastic praise with strong positive language.", "confidence": "high"},
    {"index": 1, "sentiment": "neutral", "score": 0.52, "magnitude": 0.2, "emotions": [], "reasoning": "Lukewarm, non-committal language with no strong emotion.", "confidence": "high"},
    {"index": 2, "sentiment": "negative", "score": 0.08, "magnitude": 0.9, "emotions": ["frustration", "anger"], "reasoning": "Strong negative sentiment, explicit dissatisfaction and churn signal.", "confidence": "high"}
  ],
  "summary": {
    "dominant_sentiment": "negative",
    "average_score": 0.503,
    "distribution": {"positive": 1, "negative": 1, "neutral": 1, "mixed": 0}
  },
  "mode": "batch",
  "context": "review"
}
```

## Trust Statement

Sentiment Bot processes text transiently for analysis only. Content is not stored or logged beyond the transaction. Analysis is performed by Claude via LightningProx. Your spend token is used for payment only.
