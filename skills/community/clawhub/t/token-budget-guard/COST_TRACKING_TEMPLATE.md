# Cost Tracking Template

A practical template for tracking token usage and costs across your AI-powered projects.

## Budget Tracking Table

| Date | Model | Prompt Tokens | Completion Tokens | Total Tokens | Cost (USD) | Category | Notes |
|------|-------|--------------|-------------------|-------------|-----------|----------|-------|
| 2026-01-15 | gpt-4 | 12,400 | 3,200 | 15,600 | $0.78 | Development | Code review session |
| 2026-01-15 | gpt-3.5-turbo | 45,000 | 8,200 | 53,200 | $0.05 | Batch | Document summarization |
| 2026-01-16 | gpt-4 | 8,600 | 2,100 | 10,700 | $0.54 | Development | Debug session |
| 2026-01-16 | claude-3 | 22,000 | 6,500 | 28,500 | $0.43 | Research | Literature analysis |
| 2026-01-17 | gpt-4 | 31,000 | 9,400 | 40,400 | $2.02 | Production | API endpoint - chatbot |
| | | | | **Weekly Total** | **$3.82** | | |

### Column Guide

- **Model** — Full model identifier (pricing varies by model)
- **Prompt Tokens** — Input tokens sent to the API
- **Completion Tokens** — Output tokens received
- **Cost (USD)** — Calculated from your provider's pricing sheet
- **Category** — `Development`, `Production`, `Research`, `Batch`, `Testing`, `Other`
- **Notes** — Brief description of what the session accomplished

## Cost Calculation Reference

### OpenAI Pricing (as of 2026-01)

| Model | Input (per 1K tokens) | Output (per 1K tokens) |
|-------|----------------------|------------------------|
| gpt-4 | $0.03 | $0.06 |
| gpt-4-turbo | $0.01 | $0.03 |
| gpt-3.5-turbo | $0.001 | $0.002 |
| gpt-4o | $0.005 | $0.015 |

### Anthropic Pricing (as of 2026-01)

| Model | Input (per 1K tokens) | Output (per 1K tokens) |
|-------|----------------------|------------------------|
| claude-3-opus | $0.015 | $0.075 |
| claude-3-sonnet | $0.003 | $0.015 |
| claude-3-haiku | $0.00025 | $0.00125 |

> **Tip:** Always verify current pricing on provider websites. Prices change frequently.

## Usage Patterns

### Pattern 1: Development Sprints

During active development, costs spike. Plan for it.

```
Week 1 (feature dev):  ~$8-15/day
Week 2 (testing):      ~$3-5/day
Week 3 (polish):       ~$2-4/day
```

**Mitigation:** Use cheaper models for boilerplate and syntax fixes. Reserve expensive models for architecture and complex logic.

### Pattern 2: Production API

Steady-state costs tied to user traffic.

```
Baseline:    ~$5-20/day (low traffic)
Growth:      ~$50-200/day (moderate traffic)
Scale:       ~$500+/day (high traffic)
```

**Mitigation:** Implement caching, shorter system prompts, and model routing (cheap model first, escalate on failure).

### Pattern 3: Batch Processing

Periodic large jobs (document processing, embeddings, analysis).

```
Per batch:   ~$2-50 depending on volume
Frequency:   Daily/Weekly
```

**Mitigation:** Pre-filter inputs, use streaming to catch errors early, chunk large documents.

### Pattern 4: Research & Exploration

Unpredictable costs during exploration phases.

```
Typical:     ~$10-30/session
Risk:        Can spike to $100+ without limits
```

**Mitigation:** Set hard token limits per session. Log all queries. Review spending daily.

## Monthly Budget Template

```yaml
monthly_budget:
  total: $200
  allocations:
    development: $60    # 30%
    production_api: $80  # 40%
    research: $30        # 15%
    batch: $20           # 10%
    buffer: $10          # 5%
  
  alerts:
    - threshold: 50%
      action: log_warning
    - threshold: 80%
      action: notify_team
    - threshold: 95%
      action: rate_limit_cheaper_model
    - threshold: 100%
      action: block_non_essential
```

## Cost Optimization Checklist

- [ ] **Model selection** — Are you using the cheapest model that meets quality requirements?
- [ ] **Prompt length** — Can system prompts be shortened without losing effectiveness?
- [ ] **Caching** — Are identical queries being cached instead of re-sent?
- [ ] **Batching** — Can multiple small requests be combined into one?
- [ ] **Streaming** — Are you using streaming to detect early termination opportunities?
- [ ] **Token counting** — Are you counting tokens before sending to avoid oversized requests?
- [ ] **Temperature** — Is temperature set appropriately? Lower = more deterministic = fewer retries.
- [ ] **Max tokens** — Are you setting `max_tokens` to avoid runaway completions?
- [ ] **Fallback routing** — Do you route to cheaper models when quality allows?
- [ ] **Usage monitoring** — Do you have automated cost alerts set up?

## Quick Estimation Formula

```
estimated_cost = (prompt_tokens × input_price + completion_tokens × output_price) / 1000

daily_budget = monthly_budget / 30
tokens_available = daily_budget / (weighted_avg_price_per_1k_tokens)
```

## Integration with token-budget-guard

This template pairs with the `token-budget-guard` rules:

1. **Before a session** — Estimate cost using the formula above
2. **During a session** — Track actual token counts
3. **After a session** — Log actual vs estimated in the tracking table
4. **Weekly review** — Compare against monthly budget allocation
5. **Monthly review** — Adjust allocations based on actual usage patterns
