---
name: swarm-coordinator
description: Coordinate multi-agent swarm execution with a lightweight Pub/Sub protocol, standardized SwarmCommand messages, token-budget control, agent status tracking, negotiation, fallback, and completion gates. Use when building or reviewing multi-agent coordination, swarm execution, task delegation, agent handoff, token quota governance, Redis/in-memory PubSub orchestration, role-based agent teams, or safe parallel AI workflows.
version: "1.1.0"
last_updated: "2026-04-25"
changelog: "ClawHub-ready release: generalized public wording, added execution workflow, safety boundaries, gates, failure handling, validation checklist, and test prompts."
---

# Swarm Coordinator

Swarm Coordinator is a lightweight coordination skill for multi-agent execution. It helps an agent design, validate, and operate a swarm workflow using:

- standardized `SwarmCommand` messages
- Redis or in-memory Pub/Sub coordination
- token-budget governance and downgrade rules
- agent status tracking
- negotiation and conflict resolution
- assignment, completion, and failure notifications

Use it when the task is not “one agent answers once”, but **multiple agents must coordinate without losing control of cost, state, ownership, or completion criteria**.

This skill is intentionally control-oriented: a swarm is only valuable when parallelism improves throughput or quality without causing duplicated work, hidden queue drift, or uncontrolled token spend.

---

## When to Use

Use this skill for:

- multi-agent task delegation or swarm execution
- role-based AI teams, agent crews, or collaborative agent workflows
- Pub/Sub task coordination with Redis or memory queues
- designing a standard command protocol between agents
- assigning roles, budgets, deadlines, and dependencies
- tracking task state across multiple agents
- negotiating conflicts between agents
- enforcing token quota and fallback behavior
- reviewing whether a swarm workflow can converge safely

Do not use it for simple single-agent tasks. If one agent can complete the job directly, avoid swarm overhead.

---

## Core Principle

A swarm is useful only if it improves throughput or quality **without causing coordination chaos**.

Always protect four invariants:

1. **Single task owner** — every task has one accountable owner at a time.
2. **Explicit state** — each command has status, deadline, budget, dependencies, and result.
3. **Bounded cost** — token budget and downgrade rules are part of the protocol.
4. **Verifiable completion** — completion requires artifacts, tests, review, or an explicit result field.

If any invariant is missing, the swarm can drift, duplicate work, or burn tokens.

---

## Default Workflow

### Step 1: Decide whether swarm is justified

Use swarm only when at least one is true:

- task can be split into independent subtasks
- different agents have clearly different roles
- review/verification must be separated from implementation
- latency can be reduced through parallel work
- negotiation is needed because constraints conflict

If not, keep it single-agent.

### Step 2: Define roles and ownership

Specify:

```text
commander / coordinator
executor(s)
reviewer / auditor
monitor / verifier
fallback owner
```

Each task should have one current `assigned_to`. Multiple reviewers are allowed, but multiple executors writing the same artifact are not unless explicitly coordinated.

### Step 3: Create a SwarmCommand

A command must include:

```json
{
  "command_id": "cmd_12345678",
  "timestamp": "2026-04-25T12:00:00Z",
  "sender": {"type": "coordinator", "id": "001"},
  "target": {"type": "developer", "id": "003"},
  "command": {
    "action": "develop",
    "module": "login",
    "requirements": ["JWT auth", "tests"],
    "output_format": "python_code"
  },
  "metadata": {
    "priority": "high",
    "token_budget": 1500,
    "deadline": "2026-04-25T13:00:00Z",
    "dependencies": []
  },
  "negotiation": {
    "allowed": true,
    "timeout": 300
  }
}
```

Prefer using `coordinator/swarm_protocol.py` for deterministic command creation and validation. If your project has its own agent taxonomy, map local role names to the protocol roles instead of hard-coding private labels in prompts.

### Step 4: Validate before publish

Before publishing to Redis or memory queue, validate:

- schema format
- known sender / target role
- priority is one of `low | medium | high | critical`
- token budget is positive and within tier quota
- dependencies exist or are intentionally empty
- deadline is realistic
- completion gate is clear

If validation fails, do not publish. Return validation errors and ask for correction or auto-fix safe fields.

### Step 5: Publish, subscribe, and track state

Use:

```python
from coordinator.pubsub import PubSubCoordinator
from coordinator.swarm_protocol import SwarmProtocol

protocol = SwarmProtocol()
coordinator = PubSubCoordinator(use_redis=True)

command = protocol.create_command(
    agent_type="developer",
    command={"action": "analyze", "module": "performance"},
    priority="high",
    token_budget=2000,
)

valid, errors = protocol.validate_command(command)
if valid:
    coordinator.publish("tasks", command.to_dict())
else:
    print(errors)
```

Track state transitions:

```text
pending → assigned → in_progress → completed / failed / cancelled
```

No command should remain `in_progress` forever. Use deadline or heartbeat timeout to trigger fallback.

### Step 6: Collect result and close the loop

Completion should include:

- `success: true/false`
- output or artifact path
- tests/review/verification result when applicable
- token usage
- failure reason if failed
- next action recommendation

If result is missing required artifacts, mark as incomplete instead of completed.

---

## Token Budget and Downgrade Rules

Use token budget as a control mechanism, not just metadata.

Recommended rules:

| Condition | Action |
|---|---|
| budget remaining > 40% | continue normal execution |
| budget remaining 20-40% | compress context and reduce parallel agents |
| budget remaining < 20% | downgrade model/tier or require coordinator approval |
| budget exceeded | stop publishing new subtasks and request confirmation |
| repeated failure | lower concurrency and route to reviewer/monitor |

For local implementation, use `coordinator/token_budget.py` if available.

---

## Negotiation Rules

Allow negotiation when:

- two agents propose conflicting plans
- deadline and token budget cannot both be satisfied
- a dependency is blocked
- an agent lacks capability or context

Negotiation output should be a decision, not endless discussion:

```json
{
  "decision": "assign_to_developer_then_review_by_auditor",
  "reason": "developer owns implementation; auditor reviews risk",
  "budget_adjustment": 500,
  "deadline_adjustment": null,
  "blocked": false
}
```

If negotiation exceeds timeout, coordinator decides or escalates to human.

---

## Failure Handling

Handle these failures explicitly:

| Failure | Response |
|---|---|
| invalid command | reject before publish; return schema errors |
| target unavailable | reroute to fallback owner |
| dependency blocked | keep pending; notify coordinator |
| budget exceeded | pause or downgrade; do not silently continue |
| deadline missed | mark failed or escalate |
| duplicate owner | choose one owner; cancel duplicate assignment |
| incomplete result | reopen task with missing artifact list |
| repeated failure | reduce concurrency; route to reviewer/monitor |

Never let failures become silent queue drift.

---

## Safety Boundaries

Ask for human confirmation before swarm actions that are:

- destructive: delete data, remove files, reset state
- public: publish, message external users, send email
- costly: paid API calls, high-token parallel execution, cloud deployment
- irreversible: production migrations, permission changes, credential rotation
- ambiguous: unclear task owner, conflicting requirements, missing acceptance criteria

Swarm coordination amplifies mistakes. High-risk actions need stronger gates than single-agent execution.

---

## Output Format

When using this skill, return:

```markdown
## Swarm Plan
- Goal:
- Swarm justified? yes/no + reason
- Agents and roles:
- Ownership model:

## Commands
| command_id | target | action | budget | dependencies | gate |
|---|---|---|---:|---|---|

## Coordination Flow
pending → assigned → in_progress → completed/failed

## Budget / Downgrade
- Total budget:
- Per-agent budget:
- Downgrade trigger:

## Failure / Fallback
- Main risks:
- Fallback owner:
- Escalation condition:

## Verification
- Required artifacts:
- Tests / review:
- Done criteria:
```

For code-facing tasks, also mention which files or APIs to use.

---

## Bundled Resources

Use these resources when needed:

- `coordinator/swarm_protocol.py` — deterministic SwarmCommand creation, validation, assignment, completion, negotiation helpers.
- `schemas/swarm_command.json` — JSON Schema for command validation.
- `tests/test_swarm_protocol.py` — regression tests for protocol behavior.
- `test-prompts.json` — Darwin-style prompts for future skill regression evaluation.

Read or run them when modifying the protocol implementation.

---

## Validation Checklist

Before calling a swarm workflow ready, check:

- [ ] Every task has exactly one current owner.
- [ ] Every command validates against schema.
- [ ] Budget and deadline are explicit.
- [ ] Dependencies are declared.
- [ ] Completion gate is explicit.
- [ ] Failure fallback is defined.
- [ ] High-risk actions require confirmation.
- [ ] Tests or review exist for important outputs.
- [ ] No open-ended negotiation loop remains.

---

## Quality Bar

A good swarm plan should reduce confusion, not add bureaucracy.

It succeeds when:

- agents know exactly what they own
- coordinator can see state and budget
- failures route to a clear fallback
- completion is verifiable
- token use stays bounded
- parallelism improves throughput without oscillation

If the swarm adds agents without improving control, do not use swarm.
