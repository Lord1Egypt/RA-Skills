# Roundtable State Machine

This file defines the explicit **state machine** that governs a roundtable's lifecycle. Every roundtable has exactly one `state` at any moment, written to the top-level `state` field in Memory. State transitions are recorded in `state_log` so the discussion is fully auditable.

> **Why a state machine:** before v2.5.0, a roundtable's progress was implicit in `rounds[]` length and `metadata.completed` flag. This made it impossible to recover a paused session, validate that handoff cards were generated at the right moment, or detect illegal transitions. The state machine makes progress explicit and machine-checkable.

## States

| State | Meaning | When entered |
|-------|---------|--------------|
| `init` | Memory is initialized, characters seated, no round dispatched yet. | After step 5 (Initialize Memory). |
| `round_open` | A round is in progress; characters may speak. | After Conductor dispatches the first focus question. |
| `handoff_pending` | The current round's speeches are complete; handoff card is being generated and depth assessment is evaluated. | After Conductor writes the last speech of a round. |
| `handoff_consumed` | The next round's first speech has consumed the previous handoff card. | After the first speech of the new round references the handoff card. |
| `paused` | User paused the discussion via an interjection. No round is in progress. | When a `pause` interjection is recorded. |
| `resumed` | User unpaused; about to enter `round_open` for the next round. | When a `pause` interjection is resolved. |
| `synthesizing` | All rounds are done; Conductor is populating `synthesis`. | After the last round's handoff card is consumed. |
| `completed` | Memory is finalized; output is rendered. | After synthesis is written and output contract lint passes. |

`init` and `round_open` are mutually exclusive terminal-like entry points. `completed` is the only true terminal state.

## Transition rules

The following transitions are legal. Any other transition is an error caught by [lint_memory.py](../scripts/lint_memory.py).

```
init
  ├─→ round_open              (first focus question dispatched)
  └─→ completed               (zero-round roundtable, edge case)

round_open
  ├─→ handoff_pending         (last speech of current round written)
  ├─→ paused                  (pause interjection arrives)
  └─→ synthesizing            (no more rounds scheduled)

handoff_pending
  ├─→ handoff_consumed        (next round's first speech references handoff card)
  ├─→ round_open              (next round's first speech is dispatched)
  └─→ paused                  (pause interjection arrives before next round)

handoff_consumed
  └─→ round_open              (transition into active round)

paused
  └─→ resumed                 (user resumes)

resumed
  ├─→ round_open              (next round starts)
  └─→ synthesizing            (no more rounds scheduled)

synthesizing
  └─→ completed               (synthesis written, output contract lint passes)
```

Illegal transitions (caught by lint):

- `completed` → anything (terminal)
- `paused` → `round_open` (must go through `resumed` first)
- `resumed` → `paused` (cannot pause while resuming)
- `init` → `handoff_pending` (must go through `round_open` first)
- Skipping `handoff_pending` (any `round_open` → `round_open` transition that does not pass through handoff generation)

## Memory fields

### Top-level `state`

```json
{
  "state": "round_open"
}
```

Values must come from the states table above. Lint rejects anything else with `STATE_INVALID`.

### Top-level `state_log`

```json
{
  "state_log": [
    {
      "from": "init",
      "to": "round_open",
      "trigger": "first_focus_question_dispatched",
      "at": "2026-06-22T10:05:00Z",
      "round_number": 1
    }
  ]
}
```

Each transition records:

| Field | Required | Description |
|-------|----------|-------------|
| `from` | yes | Previous state. Empty string for the first log entry. |
| `to` | yes | New state. |
| `trigger` | yes | Human-readable reason. Free text, but stable triggers are recommended (see below). |
| `at` | yes | ISO 8601 timestamp. |
| `round_number` | recommended | The round that owns this transition. Omit for non-round transitions (e.g. `init` → `round_open`). |

### Stable trigger tokens

To make the state_log queryable, the `trigger` field should use one of these stable tokens when applicable:

| Token | Transition |
|-------|------------|
| `first_focus_question_dispatched` | `init` → `round_open` |
| `last_speech_written` | `round_open` → `handoff_pending` |
| `next_round_dispatched` | `handoff_pending` → `round_open` |
| `handoff_card_consumed` | `handoff_pending` → `handoff_consumed` |
| `user_pause_interjection` | `*` → `paused` |
| `user_resume` | `paused` → `resumed` |
| `user_continuation_selected` | `paused` → `round_open` (via resumed) |
| `synthesis_started` | `*` → `synthesizing` |
| `depth_assessment_continue` | `handoff_pending` → `handoff_consumed` (depth signals present, continuing) |
| `depth_assessment_passed` | `handoff_pending` → `synthesizing` (depth signals absent, entering synthesis) |
| `output_contract_lint_passed` | `synthesizing` → `completed` |

## Relationship to handoff cards

The state machine and the handoff card protocol ([handoff-card-protocol.md](handoff-card-protocol.md)) work together:

1. A round ends → state transitions to `handoff_pending`.
2. Conductor writes `rounds[round_number].handoff_card` while in `handoff_pending`.
3. The next round's first speech must reference the handoff card → state transitions to `handoff_consumed` → `round_open`.
4. If the next round's first speech does not reference the card, the lint warns `HANDOFF_NOT_CONSUMED` and the Conductor should regenerate the card or rewrite the focus question.

A handoff card is mandatory when `metadata.enforce_handoff_cards` is true (the default). Lint enforces this.

## Relationship to other protocols

- **Continuation**: when a user picks a `next_step`, the roundtable state is `paused` → `resumed` → `round_open`, and the new round's first handoff card references the previous synthesis.
- **User interjection**: any `pause` / `topic_pivot` / `seat_expansion` interjection drives a `paused` transition. The `pause` interjection is the only one that drives `paused`; others drive a state change within `round_open`.
- **Output contract**: a roundtable cannot enter `completed` unless `lint_output_contract()` reports 0 errors.

## Lint enforcement

[lint_memory.py](../scripts/lint_memory.py) provides three related checks:

- `lint_state_machine()`: validates `state` is a known state, validates each `state_log` entry, validates that every transition is legal.
- `lint_handoff_cards()`: validates that handoff cards exist when `enforce_handoff_cards` is true, validates handoff card field completeness, validates that the next round's first speech references the card.
- `lint_versioned_contract()`: validates `contract_version` is present and well-formed, and is compatible with `version` and `metadata.protocol_version`.

These are warning-level when `metadata.enforce_handoff_cards` is `false` (legacy mode), and error-level when it is `true` (the default for new roundtables).
