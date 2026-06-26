---
name: x-growth-operator
description: Plan and execute mission-driven X growth operations / 任务驱动的 X 增长运营规划与执行。Use when the user wants to monitor KOL posts, detect emerging discussions, turn briefs or uploaded docs into a growth mission, draft replies or posts, rank opportunities, and execute approved actions with a local audit trail.
version: 1.0.4
metadata:
  openclaw:
    requires:
      env:
        - X_API_KEY
        - X_API_SECRET
        - X_ACCESS_TOKEN
        - X_ACCESS_TOKEN_SECRET
      bins:
        - python3
        - node
        - npm
      config:
        - scripts/.env
    primaryEnv: X_API_KEY
    install:
      - kind: node
        package: commander
      - kind: node
        package: dotenv
      - kind: node
        package: https-proxy-agent
      - kind: node
        package: socks-proxy-agent
---

# X Growth Operator / X 增长运营助手

Use this skill when the user wants a review-first workflow for X operations rather than a generic writing assistant.

## Purpose

Turn a user brief into an X growth mission, infer what the account should watch, find relevant opportunities, draft actions, and execute approved posts with an audit trail.

## Security & Runtime Declaration

- This skill can perform real authenticated X actions only in `x-api` mode and only after explicit approval.
- Required environment variables for real X execution:
  - `X_API_KEY`
  - `X_API_SECRET`
  - `X_ACCESS_TOKEN`
  - `X_ACCESS_TOKEN_SECRET`
- Optional environment variable:
  - `DESEARCH_API_KEY` (needed only for live Desearch search/import)
- Install step required before real execution:
  - `cd scripts && npm install`
- Network targets used by this skill:
  - `https://api.twitter.com`
  - `https://api.x.com`
- Local persistence paths:
  - `data/`
  - `scripts/.env`

## Trigger Conditions

Use this skill when the user asks to:

- operate or grow an X account
- monitor KOLs, keywords, or emerging discussions
- react to breaking events on X
- draft replies, quote posts, or original posts for X
- create or update a mission from a brand brief or uploaded document
- test an autonomous-but-reviewed X growth workflow in OpenClaw

## Workflow

Run these steps in order unless the user explicitly asks for one step only.

1. Build or refresh the mission:

```bash
python3 scripts/ingest_goal.py \
  --doc examples/brand_brief.md \
  --mission data/mission.json
```

You may also pass `--prompt` instead of `--doc`.

The brief can be structured with explicit sections or written as freeform natural language. The parser should infer goals, audience, topics, constraints, CTA, and risk tolerance from either format.

2. Gather opportunities:

```bash
python3 scripts/watch_x.py \
  --mission data/mission.json \
  --input examples/opportunities.json \
  --output data/opportunities_scored.json
```

Import live opportunities with Desearch:

```bash
python3 scripts/import_desearch.py \
  x "your query here" \
  --count 10 \
  --output data/opportunities_from_desearch.json
```

Or run live search all the way to an action plan:

```bash
python3 scripts/live_search_and_plan.py \
  --mission data/mission.json \
  --count 10
```

If `--query` is omitted, derive the search query from mission topics, keywords, and audience.

If the operator is manually surfing X and taking notes, convert those notes first:

```bash
python3 scripts/import_surf_notes.py \
  --notes examples/surf_notes.md \
  --output data/opportunities_from_notes.json
```

3. Draft a recommended action:

```bash
python3 scripts/propose_action.py \
  --mission data/mission.json \
  --opportunities data/opportunities_scored.json \
  --opportunity-id YOUR_OPPORTUNITY_ID \
  --output data/action.json
```

4. Execute only after explicit user approval:

```bash
python3 scripts/execute_action.py \
  --mission data/mission.json \
  --action data/action.json \
  --log data/execution_log.jsonl
```

For `reply` and `quote_post`, execution should run the preflight gate first. It inspects the target tweet's reply settings and blocks likely permission failures before posting.

For real X execution, first install Node dependencies and configure X OAuth credentials, then run:

```bash
python3 scripts/check_env.py --mode execution
python3 scripts/execute_action.py \
  --mission data/mission.json \
  --action data/action.json \
  --log data/execution_log.jsonl \
  --approved \
  --mode x-api
```

5. Build a ranked action plan from the current opportunity set:

```bash
python3 scripts/plan_actions.py \
  --mission data/mission.json \
  --opportunities data/opportunities_scored.json \
  --output data/action_plan.json
```

6. Learn from feedback and refresh memory:

```bash
python3 scripts/review_feedback.py \
  --mission data/mission.json \
  --feedback examples/feedback.json \
  --memory data/memory.json \
  --output data/feedback_report.json
```

7. Run the whole cycle in one command when testing:

```bash
python3 scripts/run_cycle.py \
  --doc examples/brand_brief.md \
  --opportunities examples/opportunities.json \
  --feedback examples/feedback.json
```

## Rules

- Default to review mode. Do not execute posts or replies until the user clearly approves the final action.
- For `reply` and `quote_post`, honor the interaction preflight result unless the user explicitly chooses to bypass it.
- If the user provides a document, parse it into mission fields first instead of drafting content immediately.
- Treat the mission as the source of truth for content direction. Do not assume the account is about OpenClaw, agents, or developer tools unless the user brief says so.
- If no live X source is available, operate on imported JSON opportunities and keep the workflow moving.
- Prefer replies and quote posts over net-new posts when the opportunity is time-sensitive.
- Downrank or reroute interaction ideas when thread structure or reply settings suggest a likely permission failure.
- Reject actions that conflict with mission constraints, banned topics, or risk thresholds.
- When confidence is low, recommend `observe` instead of forcing an action.
- Persist what worked. Use `data/memory.json` to carry forward successful angles, source accounts, and action types.
- Treat `auto` execution as future work. This skill is review-first.
- Real X execution requires `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, and `X_ACCESS_TOKEN_SECRET`.

## Resources

- `examples/brand_brief.md`: sample source document for mission ingestion
- `examples/freeform_brief.md`: sample freeform brief for mission ingestion
- `examples/opportunities.json`: sample X opportunities for local testing
- `examples/feedback.json`: sample outcome data for memory updates
- `examples/surf_notes.md`: sample manual browser-surf notes
- `examples/desearch_query.txt`: sample live search query
- `references/mission-schema.md`: field meanings and scoring rules
- `scripts/.env.example`: example execution environment file

## Outputs

- `data/mission.json`: structured mission for later turns
- `data/opportunities_scored.json`: ranked opportunities with reasons
- `data/action_plan.json`: ranked next actions for the current cycle
- `data/action.json`: one reviewed action proposal
- `data/execution_log.jsonl`: append-only execution history
- `data/memory.json`: persistent learned patterns and historical outcomes
