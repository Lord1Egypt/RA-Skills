---
name: tirosman-demo
version: 0.2.0
description: Drive the TirOSMAN autonomous multi-agent demo (5 projects × 150 tasks, Jira-like lifecycle, QA approval) from any MCP-aware client.
mcp:
  url: http://localhost:8000/mcp
  transport: http
  auth:
    type: bearer
    env: TIROSMAN_MCP_API_KEY
tools:
  - demo_estimate
  - demo_start
  - demo_run
  - demo_status
  - demo_board
  - demo_reset
  - demo_qa_approve
  - demo_qa_reject
---

# TirOSMAN Demo Mode

Multi-agent demo powered by the real NVIDIA adapter (meta/llama-3.1-405b-instruct).
Five concurrent projects × 30 tasks each × agent roles (pm, dev, frontend, qa, ceo),
stored in Postgres with RLS, ticked through a Jira-like lifecycle:
`backlog → analysis → in_progress → code_review → qa → done`.

## When to use

- User says "start the TirOSMAN demo" / "kick off the 150-task run" / "show the Jira board."
- User wants a cost preview before burning NVIDIA tokens.
- User needs to approve or reject QA-blocked tasks.
- User wants to wipe every demo-generated task and start over.

## Call order

1. `demo_estimate` first — returns projected tokens + cost, zero DB writes. Use it to confirm intent.
2. `demo_start(company_id, auto_run=True)` — creates tasks AND kicks off the batch executor. Pass `auto_run=False` if you want a confirm step before burning tokens.
3. `demo_run(company_id, projects?)` — resume execution when `auto_run=False`, after QA approvals, or after an interruption. Idempotent.
4. Poll `demo_status(company_id)` until all tasks are `done`/`failed`/`qa`.
5. If any task lands in `qa`, use `demo_qa_approve` or `demo_qa_reject`, then `demo_run` again to push it through.
6. `demo_board(company_id, project?)` for the visual column layout.
7. `demo_reset(company_id)` wipes everything the demo created.

## Notes

- `demo_start` only creates the rows. The batch executor runs inside TirOSMAN via FastAPI BackgroundTasks, triggered by `POST /api/companies/{id}/demo-mode`. If you called `demo_start` directly over MCP, the UI "advance" button or the HTTP endpoint has to drive execution.
- Task-status events are also POSTed to `$TIROSMAN_DEMO_WEBHOOK_URL` if set. Downstream webhook plugins (n8n, Zapier, Slack) see every transition in real time.
- Estimates are static — they do not change as tasks run.

## Failure modes

- No agents on the company → `demo_start` returns `started=false` with an explanation.
- Invalid `company_id` → tools surface a 404 from the HTTP layer.
- MCP bearer missing when `TIROSMAN_MCP_API_KEY` is set server-side → 401.
