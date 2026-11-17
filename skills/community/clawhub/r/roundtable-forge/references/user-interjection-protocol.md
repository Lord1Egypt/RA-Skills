# User Interjection Protocol

This file defines how the Conductor handles interruptions from the user mid-discussion.

## Why user interjections matter

A roundtable is not a one-shot answer; it is a live dialogue. The user may want to:

- Ask a clarifying or challenging question.
- Add a new character to the roster.
- Pivot to a related but different question.
- Pause, end, or restart a round.

Each interjection is a routing decision that must preserve the integrity of the Memory file and the continuity of the discussion.

## Interjection shape

Every user interjection is recorded as a record in Memory:

```json
{
  "interjection_id": "user-001",
  "round_number": 2,
  "type": "question | seat_expansion | topic_pivot | pause | end",
  "raw_text": "the user's original message",
  "resolved_into": "the resulting action"
}
```

The `resolved_into` field tells subsequent agents how the interjection was handled.

## Interjection types and resolution rules

### 1. Question

**User intent**: ask a specific question about what was just said.

**Resolution rules**:

1. The Conductor identifies which character agent is being asked. If unclear, ask the user to clarify.
2. The Conductor dispatches only that character agent with the user's question as the focus.
3. The character agent responds in the current round. Do not advance to the next round.
4. Record the interjection with `type: "question"` and `resolved_into: "in-round-answer"`.

### 2. Seat expansion

**User intent**: add a new character mid-discussion.

**Resolution rules**:

1. The Conductor reads [character-selection-guide.md](character-selection-guide.md) and [multi-agent-runtime-protocol.md](multi-agent-runtime-protocol.md) and picks a character that complements the existing roster.
2. The Conductor builds an `agent_profile` for the new character.
3. The Conductor briefly onboards the new agent with the topic and the last round.
4. Let the new agent speak in the next round, or immediately if the user explicitly asks.
5. Record `type: "seat_expansion"` and `resolved_into: "added-character:{name}"`.

### 3. Topic pivot

**User intent**: switch to a different question.

**Resolution rules**:

1. The Conductor freezes the current topic's open questions and consensus into Memory under the old topic.
2. The Conductor initializes a new `topic` field in Memory while keeping the same `roundtable_id`.
3. The Conductor reuses the existing roster if the new topic is in the same domain; otherwise re-evaluates the roster and their agent profiles.
4. Record `type: "topic_pivot"` and `resolved_into: "new-topic:{topic}"`.

### 4. Pause

**User intent**: stop temporarily but resume later.

**Resolution rules**:

1. The Conductor records the current round number, the last speech, and any open questions.
2. Mark Memory with `metadata.paused: true` and `metadata.paused_at`.
3. When the user resumes, load Memory and continue from the next round.

### 5. End

**User intent**: end the roundtable.

**Resolution rules**:

1. The Conductor writes the synthesis (consensus, divergence, open questions).
2. Mark Memory with `metadata.completed: true` and `metadata.completed_at`.
3. Recommend the user to archive the Memory file.

## What never changes

- The disclaimer is still required.
- The Memory file is still the single source of truth.
- Each character agent only sees its own profile and the shared Memory.
- The Conductor remains neutral and never speaks as a character.

## Why this is safe

- All interjections are recorded, so downstream agents can audit the conversation.
- The interjection type is explicit, so the same prompt can be re-evaluated deterministically.
- A topic pivot preserves the old topic in Memory instead of dropping it.
