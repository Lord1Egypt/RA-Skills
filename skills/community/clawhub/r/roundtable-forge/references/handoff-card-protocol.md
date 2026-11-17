# Handoff Card Protocol

This file defines the **handoff card** mechanism. A handoff card is a compact summary the Conductor writes at the end of each round so that the next round's characters can pick up the discussion with full context. It is the contract layer between rounds.

> **Why handoff cards:** before v2.5.0, context flowed between rounds through the Conductor's own memory or implicit narrative. When a new character joined, when the user paused for a day, or when a continuation roundtable was spun up from a Memory file, the context was often partial. Handoff cards make the handoff explicit, machine-checkable, and re-readable by any future participant.

## When handoff cards are required

A handoff card is required for every round except the last, when `metadata.enforce_handoff_cards` is `true` (the default for new roundtables). For the **last round**, the round's contribution flows directly into `synthesis`; a handoff card is optional.

When `metadata.enforce_handoff_cards` is `false` (legacy mode), handoff cards are recommended but not enforced; the lint reports them as warnings rather than errors.

## Card structure

The card is stored in `rounds[].handoff_card` (a sub-object of the round that produced it):

```json
{
  "card_id": "hc-001",
  "from_round": 1,
  "to_round": 2,
  "generated_at": "2026-06-22T10:05:00Z",
  "summary": "一句话总结上轮核心结论",
  "key_takeaways": [
    "上轮共识要点 1",
    "上轮共识要点 2"
  ],
  "unresolved_questions": [
    "上轮未解决问题 1"
  ],
  "consumed_by": [
    "speech_id 列表，下一轮中引用本卡 id 的发言"
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `card_id` | yes | Stable unique id. Use `hc-001`, `hc-002`, ... |
| `from_round` | yes | The round that produced this card. |
| `to_round` | recommended | The round expected to consume this card. Omit for the last round. |
| `generated_at` | yes | ISO 8601 timestamp. |
| `summary` | yes | One-sentence summary, 20–80 字. Must be non-empty. |
| `key_takeaways` | yes | Array of 1–5 strings, each 10–60 字. May be empty only for the last round. |
| `unresolved_questions` | recommended | Array of 0–5 strings. May be empty. Also serves as a core signal for round continuation decisions (see [roundtable-protocol.md](roundtable-protocol.md) § Dynamic round budget). |
| `consumed_by` | recommended | Array of `speech_id` values that explicitly cited the card. Populated post-hoc as the next round plays out. |

## Generation rules

The Conductor generates the handoff card while in state `handoff_pending` (see [state-machine.md](state-machine.md)). The card is written **after** the last speech of the round is committed to Memory.

Generation rules:

1. `summary` must paraphrase the round's main claim, not just copy a speech. It is the Conductor's voice, not a character's.
2. `key_takeaways` must be **structural** — actionable points a new character can build on. Avoid generic phrases like "讨论很深入".
3. `unresolved_questions` must be **answerable** in a follow-up round. If a question is too vague, drop it.
4. `card_id` follows the pattern `hc-` + 3-digit zero-padded index. Cards are ordered by `from_round`.
5. Length: `summary` is one sentence, not a paragraph. Cards are designed to be readable in 10 seconds.

## Consumption rules

The next round's **first speech** must consume the previous round's handoff card. Consumption means:

1. The speech's `content` explicitly references the `card_id` (e.g., "基于 hc-001 的结论...").
2. The speech's `responds_to` field optionally points to the previous round's host summary, but **must** also reference the card id in the prompt context.

The Conductor is responsible for:

1. Including the previous round's handoff card in the prompt context of the next round's first character.
2. Verifying that the response references the card.
3. Adding the response's `speech_id` to `consumed_by`.
4. Transitioning state to `handoff_consumed` (see [state-machine.md](state-machine.md)) when at least one speech in the new round cites the card.

If a character fails to reference the card, the Conductor should either:

- Regenerate the card with a clearer summary and re-dispatch the speech.
- Log a `HANDOFF_NOT_CONSUMED` lint warning (not a hard error, because character creativity should not be blocked by handoff mechanics).

## Relationship to continuation

When a user picks a `next_step` from `synthesis.next_steps` and continues the roundtable:

1. The state machine transitions through `paused` → `resumed` → `round_open`.
2. The new round's first handoff card is built from the previous `synthesis.consensus` and `synthesis.open_questions`, not from a round's speeches. Set `to_round` to the new round's number and `summary` to the synthesis's headline.

This is what makes continuation portable: the handoff card is the bridge between the original roundtable and the continuation.

## Relationship to discussion structures

Handoff cards work the same way across all discussion structures (`standard`, `six_hats`, `delphi`, `world_cafe`, `fishbone`). For structured methods:

- `six_hats`: when a full hat sequence is one round, the card summarizes the hat sequence, not each hat.
- `delphi`: the card summarizes the independent + feedback phases, since convergence becomes the synthesis.
- `world_cafe`: the card summarizes one rotation, since each rotation may be one round. The host summary speech is the natural anchor.
- `fishbone`: the card summarizes one phase (e.g., `cross_review`), since each phase is one round.

## Lint enforcement

[lint_memory.py](../scripts/lint_memory.py) provides `lint_handoff_cards()`:

- ERROR: a non-last round is missing `handoff_card` when `enforce_handoff_cards` is `true`.
- WARNING: a non-last round's handoff card is missing `consumed_by` (i.e., the next round did not cite the card).
- WARNING: `summary` is empty or too long (> 200 字).
- WARNING: `key_takeaways` has more than 5 items or any item longer than 100 字.
- WARNING: `card_id` is not unique across the roundtable.

When `enforce_handoff_cards` is `false`, all the above are warnings.
