---
name: trello-orchestrator-runner
description: Run a Trello-backed closed-loop delivery workflow for OpenClaw multi-agent execution. Use when a user says to run tasks from Trello automatically, keep cards moving across workflow lists, enforce manager-only intake, local-first routing, reviewer-gated completion, and retry cycles until accepted or blocked.
---

# Trello Orchestrator Runner

Use deterministic Trello lifecycle control with `trello-workflow-map.json`.

## Inputs required
- `TRELLO_API_KEY`
- `TRELLO_TOKEN`
- `trello-workflow-map.json` in workspace root

## Hard rules
1. Manager-only intake: create/update objective card in `Inbox`.
2. Move flow in order:
   - `Inbox -> Scoped -> Ready -> In Progress (Local|Remote) -> In Review -> Done|Blocked`
3. Local-first routing by default (`In Progress (Local)`).
4. Remote is escalation-only (`In Progress (Remote)`).
5. Never move to `Done` without explicit reviewer ACCEPT against original objective.
6. On reject, move back to active in-progress list and continue loop until ACCEPT or explicit stop/block.

## Required card description fields
Ensure card `desc` includes:
- objective
- acceptance_criteria
- owner_agent
- execution_mode
- escalation_reason
- expected_files_modules
- risk_level
- test_plan
- review_outcome

## Deterministic Trello API patterns
- Create card:
  - `POST /1/cards` with `idList`, `name`, `desc`
- Move list:
  - `PUT /1/cards/{cardId}/idList?value={listId}`
- Add comment:
  - `POST /1/cards/{cardId}/actions/comments` with `text`
- Update desc:
  - `PUT /1/cards/{cardId}` with `desc`

## Execution loop
1. Parse objective.
2. Create/locate epic card in `Inbox`.
3. Scope (planner) -> move to `Scoped`, comment scope summary.
4. Route (manager) -> move to `Ready`, comment local/remote decision.
5. Start builder:
   - local default -> move to `In Progress (Local)`
   - escalation -> move to `In Progress (Remote)`
6. Review -> move to `In Review`, add review findings.
7. Decision:
   - ACCEPT -> set `review_outcome: accepted`, move to `Done`
   - REJECT -> set `review_outcome: rejected`, move back to in-progress and continue
   - BLOCKED -> move to `Blocked` with explicit reason

## Output back to user
Return:
- card id + URL
- current list
- routing mode (local/remote)
- reviewer verdict
- next action
