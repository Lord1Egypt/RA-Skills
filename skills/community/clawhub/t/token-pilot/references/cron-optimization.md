# Cron Job Token Optimization

## Model Routing by Task Type

### Light Tasks → Cheapest Model (gemini/haiku/glm)
- Inbox scan (read files, update status)
- Dashboard update (read + summarize)
- Status checks (git status, error count)
- Simple data extraction (parse CSV/JSON)
- Heartbeat checks

**Add `lightContext: true` to skip full workspace injection.**

### Medium Tasks → Mid-tier Model (gpt/sonnet)
- Web search + analysis
- Content drafting
- Code review (read-only)
- Report generation
- Competitor monitoring

### Heavy Tasks → Top Model (opus)
- Morning brief (multi-source synthesis)
- Architecture decisions
- Complex debugging
- Strategy planning

## Prompt Compression for Cron

Bad (verbose prompt wastes input tokens):
```
"Daily growth work: 1. Read the morning brief document and check your inbox for messages. 
2. GEO monitoring which is the highest priority task: use the web_search tool with 2-3 
product category keywords in AI search engines, then record the mention rate and ranking 
position, and update the tracking file at shared/products/richlyva/geo-tracking.md..."
```

Good (compressed, same instruction):
```
"Daily: 1. Read inbox+brief. 2. GEO check: search 2 keywords, update geo-tracking.md. 
3. If time: one community scan. Chinese. Focus GEO if short on time."
```

**Rule: Cron prompts < 300 chars (中文信息密度高，200太短). The agent has SOUL.md for detailed behavior.**

## lightContext Jobs

Jobs that only read/write files and don't need full workspace context:
- Inbox processors
- Dashboard updaters
- Status aggregators
- File parsers

These save ~2000-5000 tokens per execution.

## Schedule Optimization

- Stagger jobs 30min apart to avoid API rate limits
- Use `activeHours` on heartbeat to skip nighttime
- Batch similar checks into fewer jobs
- Disable jobs for products not yet launched

## Cost Estimation

Per cron job execution (approximate):
- lightContext + cheap model: ~2K tokens, minimal cost
- Full context + mid model: ~8K tokens, moderate cost
- Full context + Opus: ~8K tokens, highest cost

10 daily jobs:
- All Opus: ~$1.20/day = **$36/month**
- Optimized mix: ~$0.15/day = **$4.50/month** (88% savings)
