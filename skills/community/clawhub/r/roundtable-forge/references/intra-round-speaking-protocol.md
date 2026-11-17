# Intra-Round Speaking Protocol

This protocol turns the roundtable from a fixed-schedule debate into a **topic-driven, flowing conversation** where characters respond to each other naturally, including interruptions and follow-ups.

## Core principle

The conversation is organized by **topic segments**, not by rigid rounds. Within a segment, any character may speak more than once, characters may interrupt or ask clarifying questions, and the Conductor decides who speaks next based on speaking intent, role balance, and conversational depth.

## Topic segment

A segment is a unit of discussion around one focused sub-question.

- Each segment has a `focus_question` chosen by the Conductor.
- A segment ends when the question is exhausted, when ideas start repeating, or when the Conductor decides to move to the next sub-question.
- There is **no fixed number of turns per segment**.
- Segments are recorded in `rounds[]` for backward compatibility with the Memory schema.

## Speaking flow

1. The Conductor announces the `focus_question` for the current segment.
2. The Conductor may seed the segment by inviting one or two characters to open.
3. After each speech, every other character may submit a `speaking_intent`:
   - `extend` — wants to build on the last speech
   - `rebut` — wants to oppose or challenge the last speech
   - `question` — wants to ask the last speaker a clarifying question
   - `pivot` — wants to bring the segment to a related but new angle
   - `pass` — has nothing to add right now
4. The Conductor selects the next speaker from the submitted intents.
5. The selected speaker may also **request an interruption** before another character finishes, but the Conductor decides whether to allow it.

## Allowed speech actions

Each speech must declare an `action_type`:

| Action | Meaning | Example |
|--------|---------|---------|
| `independent` | No direct response; opens a new angle | "I want to add something from the AI industry side..." |
| `extend` | Builds on a previous speech | "As Teacher Wang just said, and I would push further..." |
| `rebut` | Opposes fairly, restating first | "I respect X's point, but..." |
| `question` | Asks a clarifying question | "Confucius, when you say 'dao', do you mean...?" |
| `interrupt` | Briefly cuts in to challenge or clarify | "May I interrupt? That assumes..." |

## Interruption rules

- A character may request to interrupt only when the current speech contains a claim they strongly disagree with or a term that needs immediate clarification.
- The interrupting speech must be short (1-2 sentences).
- The Conductor records it with `action_type: interrupt` and `responds_to` the interrupted speech.
- After the interruption, the original speaker may briefly reply, or the Conductor may move on.

## Visibility rules

When a character is about to speak, their prompt packet includes:

- Their own `agent_profile`.
- The current segment's `focus_question`.
- All speeches in the current segment so far, in chronological order.
- A short summary of prior segments.
- The list of current `speaking_intent` submissions (who wants to respond and how).

They do not see speeches that have not happened yet.

## Conductor responsibilities

- Choose `focus_question` for each segment.
- Invite opening speakers or accept spontaneous opening intents.
- Collect speaking intents after every speech.
- Select the next speaker to maximize conversational depth and role balance.
- Prevent domination: if one character has spoken twice in a row or three times in one segment, invite quieter characters.
- Allow interruptions only when they sharpen the debate.
- Move to the next segment when the current one is exhausted or repetitive.
- Write every speech to Memory immediately.

## When to end the roundtable

The Conductor may end the discussion when:

- The user's original question has been explored in sufficient depth and breadth.
- New speeches are mostly repeating prior points.
- The conversation drifts far from the topic.
- A user interjection asks to pause or end.

## Real-time Memory update

After each speech, the Conductor must immediately:

1. Assign a stable `speech_id`.
2. Record `timestamp`.
3. Record `action_type`.
4. Record `responds_to` if applicable.
5. Append the speech to `rounds[n].speeches`.
6. Record any `speaking_intent` objects in `rounds[n].exchange`.
7. Rewrite the Memory file before dispatching the next agent.

## Why this matters

Fixed rounds produce five parallel monologues. Dynamic segments produce a conversation where ideas collide, refine, and evolve in real time — closer to how real scholars actually talk.
