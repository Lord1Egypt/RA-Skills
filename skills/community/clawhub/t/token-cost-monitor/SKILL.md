---
name: token-cost-monitor
description: >
  Monitor OpenClaw API costs in real-time, set budget alerts, and optimize model 
  spending. Track token usage by session and model, get cost optimization tips, 
  and prevent budget overruns. Use when: checking API spending, setting budget 
  alerts, optimizing model costs, analyzing usage trends.
homepage: https://github.com/openclaw/openclaw
metadata:
  openclaw:
    files: ["scripts/*"]
official: false
---

# Token Cost Monitor

Monitor OpenClaw API costs in real-time, set budget alerts, and optimize model spending.

## Why This Matters

**Real user stories:**
- One user spent $18.75 overnight on heartbeat checks asking "Is it daytime yet?"
- Federico Viticci spent $3,600 in a single month
- Regular users report $200/day bills from misconfigured automations

## Quick Commands

**Check current session costs:**
```bash
# View token usage and estimated cost
openclaw /status
openclaw /usage
```

**Set up cost alerts:**
```bash
# Alert when daily spend exceeds $10
echo "Alert if daily_cost > $10"

# Alert when monthly spend exceeds $100
echo "Alert if monthly_cost > $100"
```

## Cost Optimization Strategies

### 1. Model Routing

**Use cheaper models for simple tasks:**
- Claude Haiku: $0.25/1M input tokens (fast, cheap)
- Claude Sonnet: $3/1M input tokens (balanced)
- Claude Opus: $15/1M input tokens (expensive, powerful)

**Routing rules:**
```
Simple queries (weather, facts) → Haiku
Complex analysis → Sonnet
Creative writing → Opus (only if needed)
```

### 2. Context Management

**Reduce token waste:**
- Clear old conversation context regularly
- Don't store tool outputs in context
- Use concise system prompts
- Limit heartbeat frequency

### 3. Heartbeat Optimization

**Common mistake:**
```
❌ Every 30 min: "Is it daytime yet?" → $18.75/night
✅ Every 6 hours: Check emails + calendar → $2/day
```

**Best practices:**
- Combine multiple checks into one heartbeat
- Use longer intervals (4-6 hours)
- Skip nighttime heartbeats (23:00-08:00)
- Track heartbeat costs separately

## Cost Tracking Dashboard

### Daily Cost Breakdown

| Category | Tokens | Cost |
|----------|--------|------|
| Heartbeat checks | 50,000 | $0.50 |
| Web searches | 100,000 | $1.00 |
| Code generation | 200,000 | $2.00 |
| Document analysis | 150,000 | $1.50 |
| **Total** | **500,000** | **$5.00/day** |

### Monthly Projection

```
Daily average: $5.00
Monthly projection: $150.00
Budget limit: $100.00
⚠️ Warning: Will exceed budget by $50
```

## Budget Alerts Setup

### Tier 1: Light User ($10-30/month)
```
Daily limit: $1.00
Alert at: $0.80/day
Actions: Reduce heartbeat frequency, use Haiku more
```

### Tier 2: Regular User ($40-80/month)
```
Daily limit: $2.50
Alert at: $2.00/day
Actions: Optimize context, review model routing
```

### Tier 3: Power User ($100-500/month)
```
Daily limit: $10.00
Alert at: $8.00/day
Actions: Audit all automations, implement strict routing
```

## Cost Reduction Checklist

### Immediate Actions (save 30-50%)
- [ ] Reduce heartbeat frequency to 4-6 hours
- [ ] Route simple queries to Haiku
- [ ] Clear context after completed tasks
- [ ] Disable unnecessary automations

### Medium-term (save 50-70%)
- [ ] Implement model routing rules
- [ ] Optimize system prompts
- [ ] Batch similar tasks together
- [ ] Use caching for repeated queries

### Long-term (save 70-90%)
- [ ] Build cost-aware agent behaviors
- [ ] Implement token budgets per task
- [ ] Use local models for simple tasks
- [ ] Optimize tool output storage

## Monitoring Commands

### Real-time Cost Check
```bash
# Get current session stats
openclaw /status

# Get detailed usage breakdown
openclaw /usage --detailed
```

### Historical Analysis
```bash
# Last 7 days cost trend
echo "Analyze spending trend for past 7 days"

# Identify most expensive tasks
echo "What are my top 5 most expensive task types?"
```

### Anomaly Detection
```bash
# Alert if spending is 2x normal
echo "Alert if hourly_cost > 2 * average_hourly_cost"
```

## Integration Examples

### Slack/Discord Alerts
```bash
# Send daily cost summary to Slack
curl -X POST https://hooks.slack.com/services/YOUR/WEBHOOK/URL \
  -d '{"text": "Daily OpenClaw cost: $5.00 (Budget: $10.00)"}'
```

### Email Reports
```bash
# Send weekly cost report via email
echo "Weekly cost report: $35.00 total, $5.00/day average" | mail -s "OpenClaw Cost Report" user@example.com
```

## Cost Optimization Scripts

### Auto-pause Expensive Sessions
```bash
#!/bin/bash
# Pause session if daily cost exceeds limit

DAILY_LIMIT=10
CURRENT_COST=$(get_current_cost)

if (( $(echo "$CURRENT_COST > $DAILY_LIMIT" | bc -l) )); then
    echo "⚠️ Daily cost ($CURRENT_COST) exceeds limit ($DAILY_LIMIT)"
    echo "Pausing non-essential automations..."
    # Add pause logic here
fi
```

### Model Router
```bash
#!/bin/bash
# Route queries to appropriate model based on complexity

QUERY="$1"
WORD_COUNT=$(echo "$QUERY" | wc -w)

if [ $WORD_COUNT -lt 20 ]; then
    echo "Using Haiku (simple query)"
    MODEL="haiku"
elif [ $WORD_COUNT -lt 100 ]; then
    echo "Using Sonnet (medium complexity)"
    MODEL="sonnet"
else
    echo "Using Opus (complex analysis)"
    MODEL="opus"
fi
```

## Common Cost Pitfalls

### ❌ Mistake: Infinite Loops
```
Agent keeps calling itself → 1000s of API calls → $100+ in hours
```
**Fix:** Implement loop detection and limits

### ❌ Mistake: Storing Tool Outputs
```
Every tool output saved to context → Context grows → Each call costs more
```
**Fix:** Only store essential information

### ❌ Mistake: Wrong Model for Task
```
Using Opus for weather queries → 60x more expensive than needed
```
**Fix:** Implement model routing

### ❌ Mistake: Heartbeat Misconfiguration
```
Heartbeat every 5 minutes → 288 calls/day → $50+/day
```
**Fix:** Use 4-6 hour intervals

## Pricing Reference (2026)

### Anthropic Claude
| Model | Input | Output | Best For |
|-------|-------|--------|----------|
| Haiku | $0.25/1M | $1.25/1M | Simple queries, facts |
| Sonnet | $3/1M | $15/1M | General tasks |
| Opus | $15/1M | $75/1M | Complex analysis |

### OpenAI GPT
| Model | Input | Output | Best For |
|-------|-------|--------|----------|
| GPT-4o Mini | $0.15/1M | $0.60/1M | Simple queries |
| GPT-4o | $2.5/1M | $10/1M | General tasks |
| o1 | $15/1M | $60/1M | Complex reasoning |

### Google Gemini
| Model | Input | Output | Best For |
|-------|-------|--------|----------|
| Flash | $0.075/1M | $0.30/1M | Simple queries |
| Pro | $1.25/1M | $5/1M | General tasks |
| Ultra | $7.5/1M | $30/1M | Complex analysis |

## ROI Calculator

**Calculate if automation is worth it:**

```
Manual task time: 30 minutes
Your hourly rate: $50/hour
Manual cost: $25 per task

Automation cost:
- API calls: $0.50
- Setup time (amortized): $5.00
- Total: $5.50 per task

Savings: $25 - $5.50 = $19.50 per task
ROI: 355%
```

## Updates

- 2026-03-27: Initial release
- Pricing as of March 2026
- Based on real user cost data
