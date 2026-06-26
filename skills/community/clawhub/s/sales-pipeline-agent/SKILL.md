---
name: sales-pipeline-agent
description: "Manage your B2B sales pipeline end-to-end. Track deals through stages, forecast revenue, log activities, and monitor pipeline health. Weighted forecasting by deal stage. All data stored locally in JSON database. No API keys required."
metadata:
  {
    "openclaw":
      {
        "emoji": "💰",
        "requires": {},
        "pricing": {
          "model": "free",
          "description": "Free to use. Data stored locally on your machine."
        },
      },
  }
---

# Sales Pipeline Agent

An AI-powered agent that manages your B2B sales pipeline using Claude — from first contact to closed deal.

## What It Does

- **Track deals** – store every opportunity with company, contact, value, stage, and close date
- **Pipeline visibility** – weighted forecast, deals by stage, revenue totals
- **Activity logging** – log calls, emails, meetings, demos with outcomes and next steps
- **Stale deal alerts** – surfaces deals with no activity in 14+ days
- **Lead qualification** – AI-scores inbound leads using BANT before they enter the pipeline
- **Outreach drafting** – generates targeted emails for follow-ups, proposals, re-engagement, and close pushes

## Pipeline Stages

```
prospecting (5%) → qualified (20%) → proposal (40%) → negotiation (70%) → closed_won (100%)
                                                                         → closed_lost (0%)
                                                       on_hold (10%)
```

## How to Use

```
"Give me a pipeline summary"
"Add a deal: Acme Corp, $24,000, contact is Sarah Chen, sarah@acme.com, close date June 30"
"What deals are closing this month?"
"Show me stale deals with no activity in 2 weeks"
"Log a call with deal abc123: had a great demo, they want a proposal by Friday"
"Move deal abc123 to negotiation stage"
"Draft a follow-up email for deal abc123"
"Qualify this lead: Globex Corp, they reached out asking about our enterprise tier, 500 employees, need it Q3"
"What are my overdue next actions?"
```

## Running the Agent

The agent script is at `scripts/sales_pipeline_agent.py`. Invoke via this skill or run directly:

```bash
python3 scripts/sales_pipeline_agent.py
```

Or pass a one-shot task:

```bash
python3 scripts/sales_pipeline_agent.py "Give me a pipeline summary"
```

## Tools Available to the Agent

- `add_deal` – add a new deal to the pipeline
- `list_deals` – list deals, filter by stage, value, close date, or staleness
- `get_deal` – get full details for a specific deal
- `update_deal` – update stage, value, close date, notes, or next action
- `log_activity` – log a call, email, meeting, demo, or other touch
- `pipeline_summary` – full pipeline overview with forecast and alerts
- `draft_outreach` – AI-drafted email for follow-up, proposal, re-engage, close push
- `qualify_lead` – AI-scored BANT qualification for inbound leads
- `delete_deal` – permanently remove a deal

## Deal Database

All deals are stored at `~/.openclaw/workspace/sales-pipeline-agent/pipeline.json`. Back it up regularly.

## References

- `references/sales_methodology.md` – BANT, MEDDIC, and pipeline management best practices
- `references/outreach_templates.md` – email templates by stage and situation
