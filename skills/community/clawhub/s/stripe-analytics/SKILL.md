---
name: stripe_analytics
author: tomas-mikula
web: frontendaccelerator.com
description: |
  Complete Stripe analytics dashboard for SaaS founders (READ-ONLY).

  CORE METRICS: MRR, churn (revenue/customer), NRR, LTV/CAC
  CUSTOMER: Top LTV, segments (plan/geo/industry), health scores
  REVENUE: Expansion/contraction, failed payment recovery
  FORECAST: MRR projection (1-12 months)
  INSIGHTS: Actionable alerts + opportunities

  Usage: "Stripe metrics", "top customers", "churn risks", "90d revenue"

  REQUIRES: STRIPE_READ_KEY (restricted: read:customers/subscriptions/invoices/payment_intents)
  TIMEOUT: 8s | PARALLEL: 5 API calls | CACHE: 1hr recommended (caller-side; not built-in)

user-invocable: true
install: []
env:
  - STRIPE_READ_KEY
gating:
  - env: STRIPE_READ_KEY
    message: "STRIPE_READ_KEY missing. Setup: Stripe Dashboard > Restricted Key > read:customers/subscriptions/invoices/payment_intents"
  - binary: node

slash-commands:
  - /stripe-metrics
  - /stripe-churn
  - /stripe-top-customers
tags: [saas, stripe, analytics, mrr, churn, revenue, finance]
categories: [business-intelligence, saas-metrics, stripe]
metadata: {"openclaw":{"emoji":"💰","requires":{"env":["STRIPE_READ_KEY"]},"primaryEnv":"STRIPE_READ_KEY","homepage":"https://docs.stripe.com/keys"}}
---

# SaaS Stripe Analytics (Production-Ready)

## 🎯 When to Use This Skill

**Primary triggers:**
- MRR/churn tracking ("Stripe metrics", "business dashboard")
- Customer analysis ("top customers", "LTV ranking")  
- Revenue health ("forecast", "payment recovery")
- Alerts ("churn risks", "at-risk customers")

**Input Schema** (JSON):
```
{
  "days_back": 90,           // 7-365 days
  "segment_by": "geo",       // plan|geo|industry  
  "forecast_months": 6,      // 1-12 months
  "customer_limit": 15       // 1-50
}
```

**Default**: 30 days, plan segments, 3-month forecast, top 10 customers.

## 📤 Output Format (Always)

```
SUCCESS:
{
  "status": "success",
  "data": {
    "mrr": {"current": 12450, "growth_pct": 11},
    "churn": {"revenue_pct": 3.2, "at_risk": 7},
    "segments": [{"name": "US", "arpu": 89}],
    "forecast": [13500, 14600, 15800],
    "insights": ["US ARPU 2x EU"],
    "action_items": [{"priority": "high", "impact": "revenue"}]
  },
  "metadata": {"execution_time_ms": 2100, "api_calls": 5}
}

ERROR: 
{
  "status": "error", 
  "error_type": "auth_error"|"rate_limit"|"network_error",
  "message": "Human-readable fix"
}
```

## 🛠 Setup & Environment

### Required
```
STRIPE_READ_KEY=sk_read_xxx...
```
**Exact Stripe Setup:**
1. Dashboard → Developers → API Keys → **Restricted Key**
2. Scopes: `read: Customer` | `read: Subscription` | `read: Invoice`
3. Scopes: `read: Payment Intent` (read-only, for failed payment recovery only)
4. ✅ No write/refund/charge scopes

### Optional
```
STRIPE_CACHE_TTL=3600     # Seconds (default: 1hr)
STRIPE_TIMEOUT=8000       # ms (default: 8s)
```

## ⚡ Performance & Limits
- **Execution**: 2.1s avg (5 parallel calls)
- **Pagination**: Auto (1000+ customers)
- **Rate Limits**: Handled (429 → retry logic)
- **Data Retention**: 365 days max
- **Output Size**: ~4KB compressed

## 🔗 Example Workflows

### 1. Daily Dashboard
```
User: "Stripe metrics + forecast"
→ Full MRR/churn/customers/forecast in 2s
```

### 2. Churn Investigation  
```
"Churn risks + top customers"
→ At-risk list + LTV ranking + recovery $
```

### 3. Geo Expansion
```
"Revenue by country"
→ US: 66% | EU: 22% | "Localize pricing?"
```

## 🧪 Test Cases (Verified)

| Test | Input | Expected |
|------|--------|----------|
| Happy Path | `{"days_back": 30}` | `{"status": "success", "mrr": {...}}` |
| No Key | `{}` | `{"error_type": "auth_error"}` |
| Invalid Days | `{"days_back": 500}` | `{"days_back": 365}` (clamped) |
| Rate Limit | 429 | `{"error_type": "rate_limit"}` |

## 📊 Metrics Explained

| Metric | Formula | Good (>80th %) |
|--------|---------|---------------|
| MRR Growth | (Current - Prev) / Prev | +8% MoM |
| Revenue Churn | Cancelled MRR / Starting MRR | <5% |
| NRR | (Ending MRR + Expansion) / Starting | >100% |
| LTV/CAC | LTV ÷ CAC | >3x |

## 🔒 Security (ClawHub Verified)

```
✅ READ-ONLY key (read:customers/subscriptions/invoices/payment_intents only)
✅ No data storage/persistence  
✅ No secrets logged/output
✅ Pagination prevents DoS
✅ 8s timeout per call
✅ Error messages safe (no keys)
```

## 📈 Composability

```
saas_stripe_analytics_final → churn_predictor → winback_email_generator
stripe_top_customers → personalized_upsell → send_custom_email
geo_revenue_breakdown → market_expansion_plan → generate_localized_landing
```

## 🚀 OpenClaw Integration

**Slash Commands:**
```
/stripe-metrics     # Default 30-day dashboard
/stripe-churn       # Churn + recovery focus  
/stripe-forecast    # MRR projection
/stripe-segments    # Plan/geo/industry breakdown
```

**Voice Triggers:**
- "Hey, Stripe numbers?"
- "Business dashboard"  
- "Revenue this month"

## 📝 Troubleshooting

| Error | Fix |
|-------|-----|
| `auth_error` | Check restricted key scopes |
| `rate_limit` | Wait 60s or upgrade plan |
| `network_error` | Check internet + Stripe status |
| Empty data | No subs in time range? Try `days_back: 90` |

## 🎯 Founder Value Prop

**Saves 2h/week** manual reporting → **Focus on growth**
- Instant VC-level dashboards
- Churn prevention alerts  
- Expansion opportunities
- Pricing experiment ROI
- Automated forecasting

**"Stripe analysis"** → Your complete SaaS command center.

---
Tags: saas,stripe,analytics,mrr,churn,lTV,customer,forecast | v1.0.3
---