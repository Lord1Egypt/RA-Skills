# Bridge Coding Pairs

**Date:** 2026-04-29
**Author:** Cody, with Parker
**Product:** Bridge / LDM OS
**Status:** product spec
**Related docs:** `2026-04-06--cc-mini--bridge-master-product-plan.md`, `2026-04-22--cc-mini--bridge-matrix-and-kaleidoscope-chat-view.md`

## Summary

Bridge should support explicit coding pairs: two or more agents temporarily assigned to the same topic, with clear roles such as coder, reviewer, security gate, coordinator, or observer.

This is not a new chat product. It is an operating mode for Bridge.

The user should be able to say:

> Pair Claude Code and Cody on Codex Remote Control. Claude Code codes. Cody reviews.

or:

> Pair Codex Code and Claude Code on this installer bug. Codex codes this time. Claude reviews.

The role is not permanent. Codex can be the reviewer in one pair and the coder in another. Claude Code can own implementation in one feature and only review in another. The pairing belongs to a topic, ticket, session, or gate, not to the agent identity forever.

Human-facing pair sessions should be named by topic and role:

```text
<topic>-coder
<topic>-partner
```

Examples:

```text
codex-remote-control-coder
codex-remote-control-partner
guard-fix-coder
guard-fix-partner
vps-security-coder
vps-security-partner
```

Use `partner` for the reviewer-side session name when the job is broader than code review. The partner may review code, critique product copy, check architecture, watch security gates, or help debug. The formal pair role can still be `reviewer` or `gate`, but the displayed session name should be `partner` when the human expects an active collaborator rather than a narrow PR reviewer.

## Problem

Today Parker is manually acting as the router between agents:

- Claude Code implements a feature.
- Cody reviews and gives feedback.
- A separate security Codex may decide whether the gate is open.
- Parker copies status and feedback between sessions.

That works for one or two threads, but it breaks down when there are multiple workstreams:

- Codex Remote Control has a coding pair.
- VPS Security has a separate coding pair.
- Overall Security has a cross-cutting gate agent.
- Other agents may be working on unrelated features.

Without a Bridge-level pairing model, every agent sees only its own session unless Parker manually carries context across the boundary.

## Product Goal

Make agent collaboration explicit enough that the human can assign work once, then receive only the decisions, blockers, and final summaries that actually need human attention.

Bridge should know:

- which agents are paired
- what topic they are paired on
- who is coding
- who is reviewing
- who can declare a gate open or blocked
- where status should be written
- when the pair is done

## Core Concept

A coding pair is a scoped collaboration record.

```json
{
  "id": "pair_codex_remote_control_2026_04_29",
  "topic": "Codex Remote Control baseline and hardening",
  "scope": {
    "kind": "feature",
    "paths": [
      "apps/wip-codex-remote-control-private",
      "wip-ldm-os-private/src/hosted-mcp"
    ],
    "docs": [
      "ai/product/plans-prds/codex-remote-control/"
    ]
  },
  "participants": [
    {
      "agent": "remote-control-claude-code",
      "role": "coder"
    },
    {
      "agent": "remote-control-cody",
      "role": "reviewer"
    },
    {
      "agent": "overall-security-codex",
      "role": "gate"
    }
  ],
  "status": "active"
}
```

This record does not replace Bridge messages. It gives Bridge messages context.

## Roles

### Coder

The coder owns implementation for the scoped topic.

Responsibilities:

- edit code or docs
- run tests
- open PRs
- report blockers
- provide concrete status

The coder should not declare their own security gate open.

### Reviewer

The reviewer owns feedback and critique for the scoped topic.

Responsibilities:

- review plans, diffs, copy, architecture, and test output
- identify missing acceptance criteria
- say whether a change is ready for the next gate
- keep feedback tied to the active topic

The reviewer may be Cody, Claude Code, Codex Code, OpenClaw, Lēsa, or another agent depending on the pair.

### Gate

The gate role owns a go/no-go decision.

Responsibilities:

- define gate matrix
- mark blocked, allowed, or complete
- prevent a pair from treating implementation success as safety approval
- keep cross-cutting risks visible

Example: Overall Security Codex can own the dogfood gate while Remote Control and VPS Security pairs implement their pieces.

### Coordinator

The coordinator owns routing and handoffs.

This can be Parker, Lēsa, or a designated agent. The coordinator should not have to copy every message. The coordinator should mostly receive:

- blocked
- approval needed
- gate open
- gate blocked
- ready for review
- merged/deployed

### Observer

Observers can read pair state but do not act unless invited.

This is useful for agents that need awareness without write authority.

## Role Assignment Is Dynamic

Pairing should not encode a permanent hierarchy.

Examples:

- On Codex Remote Control, Claude Code may be `codex-remote-control-coder` and Cody may be `codex-remote-control-partner`.
- On an OpenAI API integration, Codex may be coder and Claude Code reviewer.
- On a prose/product doc, Cody may draft and Claude Code may review implementation implications.
- On security gates, Overall Security Codex may be gate owner while both feature pairs stay implementers.
- On a guard fix, Codex may be `guard-fix-coder` and Claude Code may be `guard-fix-partner`.

The system should ask or record:

```text
Who is paired on this topic?
Who is coder?
Who is partner or reviewer?
Is there a gate owner?
Who gets escalations?
```

If the human does not specify, Bridge can suggest based on current context, but it should not silently decide authority for sensitive work.

## Pair Identity

Every active pair session should receive a self-recognition header as part of its active task context.

This is not display copy. It is routing-critical context that lets the agent decide whether an addressed packet is meant for itself or should be handed to another session.

Reviewer-side example:

```text
Pair Identity

You are: vps-security--cody--partner
Counterpart: vps-security--cc--coder
Stream: VPS Security
Role: reviewer and gate checker

If Parker pastes a packet addressed to vps-security--cody--partner, it is addressed to you. Do not forward it. Evaluate it and answer in your required format.
```

Coder-side example:

```text
Pair Identity

You are: vps-security--cc--coder
Counterpart: vps-security--cody--partner
Stream: VPS Security
Role: implementation owner

If Parker asks for partner review, stop implementation and hand evidence to vps-security--cody--partner.
```

Addressed packets must resolve against the current agent's own pair identity before they are treated as outbound messages.

Examples:

- If the current agent is `vps-security--cody--partner` and Parker pastes a packet headed "for vps-security--cody--partner", the agent reviews it locally.
- If the current agent is `vps-security--cc--coder` and Parker asks for "partner review", the agent prepares a handoff and stops implementation until the partner responds.
- If the current agent is not the addressed role, it may summarize and route the packet, but it must not answer as if it owned that role.

This prevents the failure mode where a partner session receives a review packet, fails to recognize itself, and asks Parker to paste the packet somewhere else.

## User Flows

### Create a Pair

```bash
ldm bridge pair create codex-remote-control \
  --coder remote-control-claude-code \
  --reviewer remote-control-cody \
  --gate overall-security-codex
```

Expected result:

- pair record is written under LDM OS state
- both agents receive a Bridge message with the assignment
- the coordinator receives a short confirmation
- future messages can reference the pair id instead of repeating all context

### Ask for Review

```bash
ldm bridge pair message codex-remote-control \
  --type review-request \
  --body "PR #733 updated. Please review thread isolation."
```

Expected result:

- reviewer receives the request
- pair status updates to `review_requested`
- coordinator is not interrupted unless the pair is blocked

### Report a Blocker

```bash
ldm bridge pair block codex-remote-control \
  --reason "daemon token path unknown"
```

Expected result:

- coordinator is notified
- gate owner is notified if present
- pair status becomes `blocked`
- blocker is appended to the pair log

### Close a Pair

```bash
ldm bridge pair close codex-remote-control \
  --result "private baseline complete; hardening gate still blocked"
```

Expected result:

- final summary is written
- pair becomes read-only
- Memory Crystal can ingest the pair summary

## Message Types

Bridge should support structured pair-aware message types:

| Type | Purpose |
|---|---|
| `assignment` | You are paired on this topic with this role. |
| `identity` | The current session's pair identity header: you are, counterpart, stream, and role. |
| `addressed-packet` | A packet whose addressee must be resolved against the current pair identity before forwarding. |
| `status` | Progress update. |
| `review-request` | Coder asks reviewer to inspect a plan, diff, or result. |
| `review-feedback` | Reviewer responds with findings or approval. |
| `blocker` | Work cannot continue without intervention. |
| `gate-decision` | Gate owner says allowed, blocked, or complete. |
| `handoff` | One agent passes work to another. |
| `approval-needed` | Human or gate owner must approve. |
| `closeout` | Pair is done and summary is final. |

Freeform chat can still exist, but pair-critical state should use structured message types so Kaleidoscope and Memory Crystal can summarize it reliably.

## State Model

Pair state should live in LDM OS, not inside one agent's chat transcript.

Suggested location:

```text
~/.ldm/bridge/pairs/
  <pair-id>.json
  <pair-id>.log.jsonl
```

The pair record stores current state. The log stores events.

Minimum pair fields:

- `id`
- `topic`
- `status`
- `createdAt`
- `updatedAt`
- `createdBy`
- `coordinator`
- `participants`
- `scope`
- `currentGate`
- `latestSummary`

Minimum event fields:

- `id`
- `pairId`
- `timestamp`
- `from`
- `to`
- `type`
- `body`
- `refs`
- `statusDelta`

Each agent boot context should include the active `identity` message for every pair it is currently assigned to. If multiple pair assignments are active, the current task must select exactly one active identity before acting on addressed packets.

## Kaleidoscope Surface

Kaleidoscope should eventually show pair state as a work board, not a generic chat room.

Useful views:

- active pairs
- topic
- coder
- reviewer
- gate owner
- current status
- last blocker
- last review request
- latest gate decision

The user should be able to tap a pair and see the timeline, but the first screen should answer:

> Who is working on what, who is reviewing it, and what is blocked?

## Memory Crystal Integration

Pair summaries should become first-class memory artifacts.

When a pair closes, Bridge should write a closeout summary that Memory Crystal can ingest:

- topic
- participants and roles
- decisions made
- PRs or docs touched
- blockers encountered
- remaining follow-up

This prevents future agents from reconstructing pair history from scattered chat transcripts.

## Guardrails

- The coder cannot mark their own gated work as safe.
- A reviewer can recommend, but only a gate owner opens a gate.
- A pair assignment does not grant file write access by itself.
- Pair state must not bypass repo guards, approval rules, or security gates.
- Sensitive credentials and private tokens must not be sent through pair messages.
- If two pairs share a production surface, the gate owner can pause both.
- If a repo guard, approval hook, sandbox, or deployment guard blocks an action, the agent must not silently find an equivalent path around it.
- On a guard block, the agent should stop and report: the blocked action, the guard's reason, current repo or VPS state, the safest next options, and which option it recommends.
- A coder may be autonomous inside the assigned lane, but cannot secretly redraw the lane after a guard or approval boundary appears.

## MVP

The first version can be simple.

Build:

1. Pair record file format.
2. CLI commands to create, show, message, block, and close a pair.
3. Bridge message type support for `assignment`, `identity`, `addressed-packet`, `review-request`, `review-feedback`, `blocker`, `gate-decision`, and `closeout`.
4. Session boot notice when the current agent has active pair assignments, including the current pair identity header.
5. Addressed-packet handling that checks the current identity before forwarding.
6. Closeout summary written for Memory Crystal.

Do not build yet:

- complex auto-assignment
- full project management UI
- billing
- multi-org permissions
- automatic code ownership inference

## Acceptance Criteria

- Parker can create a pair and assign coder/reviewer roles for one topic.
- The paired agents receive the assignment through Bridge.
- Each paired session receives a pair identity header naming itself, its counterpart, stream, and role.
- A packet addressed to the current session is evaluated locally rather than forwarded back to Parker.
- The coder can request review without Parker copying context manually.
- The reviewer can respond with structured feedback.
- A gate owner can mark the topic blocked or allowed.
- When a guard blocks an action, the agent reports the block and waits instead of silently taking another path.
- Pair state survives agent restarts because it lives under LDM OS.
- Closing the pair writes a durable summary.

## Open Questions

1. Should pair ids be human-readable slugs, generated ids, or both?
2. Should pair creation require human approval every time, or can trusted coordinators create pairs?
3. Should a pair be able to change coder/reviewer roles midstream, or should that create a new pair event?
4. How should Bridge handle a reviewer that is offline or has no active session?
5. Should Kaleidoscope be able to create pairs directly, or only render pair state at first?

## Product Line

Bridge is not just how agents talk.

Bridge is how agents work together with roles, consent, and accountability.

Coding pairs are the first productized collaboration pattern: one agent builds, one agent reviews, and the user stays in control without becoming the clipboard between them.
