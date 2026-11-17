# Roundtable Protocol

This file defines the running rules for a roundtable discussion.

## Roles

- **Conductor**: the coordinator agent. It does not speak as a character. It sets focus questions, decides who speaks next, dispatches character agents, collects outputs, updates Memory in real time, and decides when to expand seats or stop.
- **Character agents**: independent agents, each with its own `agent_profile`. They speak only from their own perspective and can see prior speeches in the current segment.

## Topic segment structure

A roundtable is organized as a series of **topic segments**, not fixed rounds. Each segment explores one focused sub-question derived from the main topic.

Each segment has three parts:

1. **Focus question**: a single sub-question written by the Conductor.
2. **Speeches**: the Conductor invites an opening speaker, then selects subsequent speakers from the `speaking_intent` submissions made after each speech. Each agent receives a prompt packet that includes the focus question, prior segments, and **all speeches already given in the current segment**. The agent may extend, rebut, question, interrupt, or speak independently. See [intra-round-speaking-protocol.md](intra-round-speaking-protocol.md).
3. **Exchange**: the segment may include brief interruptions, clarifying questions, and follow-up replies.

There is **no fixed number of speeches per segment**. A segment ends when the sub-question is exhausted, when ideas start repeating, or when the Conductor decides to move on.

Limit each speech to 150–250 words. Limit each interruption or exchange reply to 50–100 words.

## Real-time Memory update

After every speech, the Conductor must:

1. Assign a stable `speech_id`.
2. Record `timestamp`, `character_id`, `content`, `key_points`, `action_type`, and optional `responds_to`.
3. Append the speech to `rounds[n].speeches`.
4. Record any `speaking_intent` or `interrupt` objects in `rounds[n].exchange`.
5. Rewrite the Memory file before dispatching the next character.

This ensures every subsequent agent reads from the latest shared state.

## Speaker selection

The Conductor does not pre-assign a full speaking order. Instead:

1. Open the segment by inviting one or two characters whose perspectives are most relevant.
2. After each speech, collect `speaking_intent` from every other character.
3. Choose the next speaker based on:
   - Conversational depth: prefer intents that challenge, clarify, or extend the last speech.
   - Role balance: avoid letting one character speak twice in a row or three times in one segment.
   - User interest: prioritize angles the user is likely to care about.
4. Allow brief interruptions only when they sharpen the debate.

Record the actual sequence in `rounds[n].speaking_order` after the segment ends.

## Runtime-aware dispatch

- `single_backend_multi_session`: invoke character agents sequentially, each with its own system prompt and the latest Memory.
- `real_subagent_runtime`: spawn each character as an independent subagent via the host's `Task` tool. The Conductor dispatches subagents one at a time after the first speech so that every agent sees only speeches that have already been written to Memory.
- `soft_orchestration_only`: only if the host cannot support independent sessions, generate all speeches in one backend call while explicitly separating character voices.

## Seat expansion triggers

Add a new character only when one of the following is true:

- The discussion touches a discipline no current character represents.
- The user explicitly asks for a specific perspective.
- A methodological conflict appears that needs a mediator or a third lens.
- A follow-up question requires domain expertise absent from the current roster.

When adding a seat:

1. Build an `agent_profile` for the new character.
2. Name the new character and explain why they are being invited.
3. Briefly onboard them by summarizing the current topic and the last segment.
4. Let them speak in the next segment.

## Dynamic round budget

The roundtable does not use a fixed round count. Instead, the Conductor evaluates problem complexity at capture time and sets a `round_budget` in `metadata`. At each `handoff_pending` state, the Conductor runs a depth assessment to decide whether to continue or synthesize.

### Complexity tiers

| Tier | Typical round budget | When to use |
|------|----------------------|-------------|
| `simple` | 2 | Single-domain factual question, quick consensus achievable |
| `medium` | 3–4 | Multi-perspective trade-off, moderate depth needed |
| `complex` | 5–6 | Multi-stakeholder conflict, deep root-cause, or cross-discipline synthesis |
| `open_exploration` | 6–8 | Open-ended exploration, no predetermined answer, divergent creativity |

The Conductor infers the tier from the question's scope, stakeholder diversity, and whether the answer is convergent or divergent. The user may override the tier explicitly.

### Per-round depth assessment

At each `handoff_pending` state, the Conductor checks four signals:

1. **Unresolved questions**: `handoff_card.unresolved_questions` is non-empty and answerable in a follow-up round.
2. **Missing perspectives**: a discipline relevant to the topic has no seated representative yet.
3. **Open disagreements**: characters have `rebut` or `question` actions that were not resolved within the round.
4. **User engagement**: the user has asked follow-up questions or interjected to expand scope.

### Continue/stop decision tree

- If `current_round < round_budget.min` → **continue** (minimum depth not yet reached)
- If `round_budget.min <= current_round < round_budget.max` → check depth signals:
  - Any signal true → **continue**
  - All signals false → **enter synthesis**
- If `current_round >= round_budget.max` → **enter synthesis** (unless the user explicitly requests more rounds)

The user can always override: requesting more rounds extends the budget; requesting fewer triggers synthesis.

## Stop conditions

Stop the discussion when:

- The user says they have enough.
- The discussion has converged on consensus or clearly documented divergence.
- No new substantive points appear after several turns.
- The user asks to move to synthesis or export.

## Tone rules

- Characters may disagree but must stay respectful.
- Avoid straw-manning: when disagreeing, restate the other position fairly.
- Distinguish factual claims from speculative or value-based claims.
- The Conductor remains neutral and never speaks in the first person as a character.
