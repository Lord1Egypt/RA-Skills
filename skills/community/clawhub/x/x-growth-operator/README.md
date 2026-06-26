# X Growth Operator

`X Growth Operator` is an OpenClaw-style skill for running review-first X growth workflows.

It turns a user brief into a structured mission, derives what to watch from that mission, pulls live opportunities from X, ranks them, drafts posts or interactions, and can execute approved actions through official X OAuth credentials.

## What It Does

- Parse a brief or prompt into a reusable mission
- Infer the operating focus from the user's goals, topics, audience, and constraints
- Pull opportunities from Desearch, sample JSON, or manual surf notes
- Score opportunities for relevance, urgency, and risk
- Draft `post`, `reply`, or `quote_post` actions
- Execute approved actions through the official X API
- Persist an audit trail and lightweight memory loop

## Skill Layout

- `SKILL.md`: skill entrypoint and operating rules
- `agents/openai.yaml`: UI metadata
- `core/`: reusable mission, scoring, drafting, execution, storage, planning, and feedback modules
- `scripts/`: workflow, scoring, and execution scripts
- `references/`: mission schema and scoring reference
- `examples/`: sample briefs, notes, and opportunity data

## Install

Clone the repo or drop the packaged skill folder into your local skills directory.

Install Node dependencies:

```bash
cd scripts
npm install
```

Create `scripts/.env` from `scripts/.env.example` and fill:

- `X_API_KEY`
- `X_API_SECRET`
- `X_ACCESS_TOKEN`
- `X_ACCESS_TOKEN_SECRET`
- `DESEARCH_API_KEY` (optional; only needed for live Desearch search/import)

If you need a proxy for X, also set:

- `HTTP_PROXY`
- `HTTPS_PROXY`
- `ALL_PROXY`
- `NO_PROXY`

## Security & Runtime Notes

- Real posting is only performed in `--mode x-api` and still requires explicit approval in the workflow.
- Required env vars for real X execution:
  - `X_API_KEY`
  - `X_API_SECRET`
  - `X_ACCESS_TOKEN`
  - `X_ACCESS_TOKEN_SECRET`
- Optional env var:
  - `DESEARCH_API_KEY` (only for live Desearch search/import)
- Runtime install step:
  - `cd scripts && npm install`
- Network targets:
  - `https://api.twitter.com`
  - `https://api.x.com`
- The X CLI performs direct HTTPS requests from Node (no shell command execution).

## Quick Start

Build a mission:

```bash
python3 scripts/ingest_goal.py \
  --doc examples/brand_brief.md \
  --mission data/mission.json
```

Freeform briefs also work:

```bash
python3 scripts/ingest_goal.py \
  --doc examples/freeform_brief.md \
  --mission data/mission.json
```

Chinese freeform briefs are also supported:

```bash
python3 scripts/ingest_goal.py \
  --doc examples/freeform_brief_zh.md \
  --mission data/mission.json
```

Search live X and build a ranked plan from the mission:

```bash
python3 scripts/live_search_and_plan.py \
  --mission data/mission.json \
  --count 10
```

You can still override the query manually with `--query`, but the default path is mission-driven.

Draft one action:

```bash
python3 scripts/propose_action.py \
  --mission data/mission.json \
  --opportunities data/opportunities_scored.json \
  --opportunity-id YOUR_OPPORTUNITY_ID \
  --output data/action.json
```

Execute an approved action:

```bash
python3 scripts/execute_action.py \
  --mission data/mission.json \
  --action data/action.json \
  --log data/execution_log.jsonl \
  --approved \
  --mode x-api
```

For `reply` and `quote_post`, execution now runs a preflight check first to inspect the target tweet's reply settings and block likely 403s before posting.

## Review Dashboard

Run the local review app:

```bash
python3 app/server.py
```

Then open:

`http://127.0.0.1:8787`

The dashboard reads the current contents of `data/` and shows:

- mission
- ranked action plan
- current proposed action
- memory signals
- scored opportunities
- recent execution log
- generated state files

It also provides a minimal review loop:

- draft an action from ranked opportunities
- run interaction preflight on the current action
- execute the current action in `dry-run` or `x-api` mode
- switch dashboard language between English and Chinese

## Current Status

What works today:

- Mission ingestion
- Live X search through Desearch
- Opportunity scoring and action planning
- Approved original post execution through X OAuth
- Local execution logs and memory updates

Current limits:

- `reply` and `quote_post` can be rejected by X conversation permissions
- Opportunity filtering is still tuned for review-first operation, not full autonomy
- The example files are OpenClaw-themed demo data; the live workflow is driven by the user's own mission
- The plan stage now downranks `reply` and `quote_post` targets that already look permission-constrained

## Package The Skill

Build a clean bundle without secrets or generated state:

```bash
python3 scripts/build_skill_bundle.py
```

This writes:

`dist/x-growth-operator-skill.zip`

For ClawHub publishing (EN + 中文), use:

- `docs/clawhub_publish_bilingual.md`

## Next

The roadmap for turning this skill into a larger product is in `ROADMAP.md`.
