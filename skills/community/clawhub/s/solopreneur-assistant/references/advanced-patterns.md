# Solopreneur Assistant — Advanced Patterns

## Multi-Business Tracking

If you run multiple businesses or side projects, extend the dashboard:

```markdown
# Business Dashboard

## Business 1: [Name]
| Stream | Monthly Target | MTD Actual | Status |
|--------|---------------|------------|--------|
| ... | ... | ... | ... |

## Business 2: [Name]
| Stream | Monthly Target | MTD Actual | Status |
|--------|---------------|------------|--------|
| ... | ... | ... | ... |

## Combined Metrics
- **Total Revenue MTD:** $X
- **Total Expenses MTD:** $X
- **Net Profit MTD:** $X
```

Add context to your AGENTS.md about which business is the priority, so the agent weights its attention correctly.

---

## Monthly Retrospective

Add to your cron or heartbeat (first of each month):

```markdown
## Monthly Retrospective
1. Read all weekly reviews from last month
2. Read DECISIONS.md entries from last month
3. Compare DASHBOARD.md targets vs actuals
4. Deliver Monthly Retrospective:

# 📈 Monthly Retrospective — [Month Year]

## Revenue vs Target
- Target: $X | Actual: $X | Delta: +/-$X

## Top 3 Wins
## Top 3 Lessons
## Decisions That Paid Off
## Decisions to Revisit
## Next Month's Focus (max 3 goals)
## One Thing to Stop Doing
```

---

## Client/Project Tracker

For service-based solopreneurs, add `business/CLIENTS.md`:

```markdown
# Active Clients

| Client | Project | Status | Due Date | Value | Notes |
|--------|---------|--------|----------|-------|-------|
| ... | ... | In Progress | ... | $X | ... |

## Pipeline
| Lead | Source | Stage | Est. Value | Next Action |
|------|--------|-------|------------|-------------|
| ... | ... | Proposal Sent | $X | Follow up [date] |
```

The agent can reference this for daily briefings and flag overdue items.

---

## Revenue Alerts

Add threshold-based alerts to your AGENTS.md:

```markdown
## Revenue Alerts
When updating or reading DASHBOARD.md:
- If any stream is >20% behind monthly target at mid-month → flag it prominently
- If total revenue exceeds monthly target → celebrate briefly, then suggest stretch goal
- If expenses exceed budget → flag immediately with category breakdown
```

---

## Energy Management

Solo businesses live or die by the founder's energy. Add:

```markdown
## Energy Check
During the daily briefing, consider the human's likely energy level:
- Monday: Fresh start energy — schedule hardest tasks
- Wednesday: Mid-week dip — lighter review/admin tasks  
- Friday: Closing energy — wrap up loose ends, weekly review
- After a long meeting/call: Suggest a break before deep work
- Multiple missed deadlines: Gently check if workload is realistic
```

---

## Automation Audit

Quarterly, the agent should suggest automation opportunities:

```markdown
## Quarterly Automation Audit
Review the last 3 months of daily logs and identify:
1. Tasks the human does repeatedly that could be automated
2. Decisions that follow a clear pattern (candidate for rules/templates)
3. Information the human keeps asking for (candidate for dashboard additions)
4. Time sinks that don't generate revenue (candidate for elimination)

Format: Table with task, frequency, time spent, automation difficulty (easy/medium/hard), suggested solution.
```

---

*More patterns at [theagentledger.com](https://www.theagentledger.com)*
