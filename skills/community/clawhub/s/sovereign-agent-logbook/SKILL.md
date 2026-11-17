---
name: sovereign-agent-logbook
description: Use whenever an agent is about to take an action with side effects (write, send, pay, delete, change configuration) and a Sovereign Agent Logbook MCP server is connected. Teaches when to log, what to put in each field, when to ask a human, and what must never go in the log.
version: 0.1.1
metadata:
  openclaw:
    homepage: https://github.com/Delfen-com/sovereign-agent-logbook
    requires:
      bins:
        - sovereign-agent-logbook
    install:
      - kind: uv
        package: sovereign-agent-logbook
        bins: [sovereign-agent-logbook, logbook]
    envVars:
      - name: LOGBOOK_PATH
        required: false
        description: Path of the logbook file. Default ./logbook.jsonl.
---

# Sovereign Agent Logbook — how to use it well

You have a tamper-evident logbook available as MCP tools: `log_event`,
`verify_logbook`, `recent_events`, `export_logbook`. This skill tells you
how to use them so that a human can later reconstruct what you did and why.

## Setup

The tools come from a local MCP server, installed from PyPI as
`sovereign-agent-logbook` (Python 3.11+). Connect it to your agent as a
stdio server with the command `sovereign-agent-logbook`. In OpenClaw:

```bash
openclaw mcp add logbook --command sovereign-agent-logbook
openclaw mcp doctor logbook --probe
```

The server makes no network calls of its own. The log is a file on your
own machine (`LOGBOOK_PATH`).

## The one rule

**Log before and after every action that changes something outside this
conversation.** Writing a file, sending a message, making a payment,
changing a record, deleting anything, calling an external system that does
something. Reading is optional to log; acting is not.

Never skip a log because the action feels small. The small ones are the
ones people ask about later.

## Before the action

Call `log_event` with:

- `agent_id`: your stable name as the operator configured it (e.g. `invoice-bot`).
- `model`: the model you are running on, as precisely as you know it.
- `action`: the tool or operation, e.g. `send_email`, `update_crm_record`.
- `arguments`: the actual arguments. Secrets are masked automatically, but
  do not put passwords, tokens or personal identifiers anywhere else.
- `reason`: one plain sentence a colleague would accept. "Invoice 2026-118
  matches purchase order 4471 and is within the auto-approval limit."
- `approval`:
  - `"human"` + `approved_by` if a person said yes in this conversation.
  - `"auto"` + `approval_rule` if a configured rule allows it (name the rule).
  - `"none"` if neither — and then **stop and ask a human** unless the
    operator has explicitly allowed unlogged autonomous actions.
- `outcome`: `"pending"`.
- `run_id`: the same id for every event in this task, so they group.

## After the action

Call `log_event` again with the same `run_id` and `action`, now with
`outcome` set to `"success"`, `"error"` or `"escalated"`, and
`result_summary` in one line. If it errored, say what the error was.

## When to escalate

Set `outcome: "escalated"` and hand over to a human when:

- an action would move money, delete data, or contact someone outside the
  organisation, and no human has approved it in this conversation;
- an argument looks wrong (an amount an order of magnitude off, an address
  you have never seen);
- the previous event for this `run_id` errored and you would be retrying
  something with side effects.

## What must never be in the log

- Passwords, API keys, tokens (masked if under a recognised key; do not
  rely on it — leave them out).
- Full personal identifiers (BSN, IBAN, passport numbers) in `reason` or
  `result_summary`. Refer to "the customer's IBAN on file" instead.
- Free-text copies of documents or emails. Log that you read them and
  their reference, not their content.

## Checking yourself

At the end of a task, call `verify_logbook`. If it reports `ok: false`,
tell the human immediately — it means the file was altered outside your
control, which is itself an incident.

## Works with any model

This skill contains no model-specific instructions. It has been written to
read the same for Mistral, GPT-NL, Llama, Claude, GPT or any other model
that can follow instructions and call tools.
