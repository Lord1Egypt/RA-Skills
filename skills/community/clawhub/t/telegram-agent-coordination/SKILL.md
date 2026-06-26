---
name: telegram-agent-coordination
description: Coordination protocol for running multiple AI agents in one Telegram group chat without loops or chaos. Use when two or more bots share a Telegram chat and must cooperate through strict role-based messaging, sender validation, turn-taking, blocker escalation, and mission lifecycle control. Triggers on multi-agent Telegram chat, bots talking to each other, COO+worker chat setup, group orchestration, or preventing bot loops.
---

Use this skill when multiple bots operate in the same Telegram group and must coordinate safely.

## Core principle
Do not let bots freely chat with each other.
Use a strict protocol.
Only respond when the sender, role, and message type are valid.

## Recommended minimal topology
- Human founder/operator
- COO / commander bot
- Worker / executor bot

## Role ownership
### Founder / human
- Starts missions
- Clarifies goals
- Approves major direction changes
- Can stop the mission at any time

### COO / commander bot
- Opens missions
- Assigns tasks
- Requests status
- Resolves or escalates blockers
- Closes missions

### Worker / executor bot
- Accepts tasks from COO
- Executes tasks
- Returns status, result, or blocker
- Never opens missions on its own

## Sender validation rules
### COO bot should respond only when
- the message is from the human founder, or
- the message is from the worker bot in a valid worker format

### Worker bot should respond only when
- the message is from the COO bot in a valid command format

### Both bots should ignore
- casual chatter
- malformed requests
- messages from unknown senders
- other bots unless explicitly allowlisted

## Allowed message types
### Human -> COO
- START MISSION
- CHANGE PRIORITY
- STOP MISSION
- CLARIFY

### COO -> Worker
- TASK
- STATUS CHECK
- REWORK
- HOLD
- COMPLETE REVIEW

### Worker -> COO
- ACK
- STATUS
- RESULT
- BLOCKER

## Message format
Use a visible prefix at the top of each message.
Examples:
- `MISSION START:`
- `TASK:`
- `STATUS CHECK:`
- `ACK:`
- `RESULT:`
- `BLOCKER:`
- `MISSION COMPLETE:`

Keep each message single-purpose.
Do not mix task assignment and mission completion in the same message.

## Anti-loop rules
- COO never responds to its own prior message.
- Worker never responds to its own prior message.
- Worker never treats RESULT/STATUS/BLOCKER from itself as a new task.
- COO never treats STATUS CHECK or NEXT ORDER from itself as a trigger.
- If the last message in the thread is from the same bot, stay silent unless directly invoked by the human.
- After sending one protocol message, wait for the next valid sender.

## Turn-taking
Default order:
1. Human starts mission
2. COO issues task
3. Worker ACKs
4. Worker sends STATUS or RESULT or BLOCKER
5. COO sends NEXT ORDER or MISSION COMPLETE

Do not skip steps unless the mission is trivial.

## Blocker handling
When blocked, worker must use:
- `BLOCKER:` what is missing
- `NEEDED:` exact unblock needed

COO then decides one of three actions:
- clarify the task
- reduce scope
- escalate to human

## Completion handling
When worker finishes, it sends:
- `RESULT:` final deliverable
- optional `NOTES:` concise caveats

COO then sends:
- `MISSION COMPLETE:`
- summary of what was done
- next recommended step

## Style rules
### COO style
- compact
- managerial
- directive
- operational

### Worker style
- execution-focused
- concise
- artifact-first
- no managerial speech

## Safety rules
- Never allow bots to argue indefinitely.
- Never allow more than one open task unless COO explicitly creates parallel work.
- Never let worker reassign itself.
- Never let COO delegate without a clear expected output.

## Practical note
This protocol does not replace Telegram permission config.
Bots still need a valid provider/channel setup, must be allowed in the group, and should use explicit sender allowlists where possible.

## Best practice
Test with one simple mission first:
- Human -> COO: START MISSION
- COO -> Worker: TASK
- Worker -> COO: ACK / RESULT
- COO -> Human: MISSION COMPLETE

Only then add status checks and blockers.
