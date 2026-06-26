---
name: srsa-review
description: Use when running Spaced Repetition Systems for AI Agents (SRSA) daily review sessions, grading cards with again/hard/good/easy, and proposing explicit memory add/delete/update actions after each review.
---

# SRSA Review Skill

## Purpose
Use SRSA's command-line workflow to drive efficient agent (you) reviews and turn each review result into actionable memory correction tasks.

## Concept Boundary
- SRSA cards: managed only through `card` and `review` commands in this skill.
- Agent memory system: must be updated explicitly by the agent (add/delete/update), based on reflection.

## What cards need to be generated?
- Actions that have been corrected by the user
- User preferences
- Decision you have hesitated to make
- Others that the user explicitly wants you to remember

## Command Cheat Sheet
```bash
# Print total cards, today's review progress, future due cards and average retrievability
uv run python scripts/main.py status
# Create a new card
uv run python scripts/main.py card new -q "question" -a "answer"
# Override an existing card
uv run python scripts/main.py card override [CARD_ID] -q "question" -a "answer"
# Remove a card
uv run python scripts/main.py card rm [CARD_ID]
# Get a question and its CARD_ID
uv run python scripts/main.py review get-question
# Get the answer and CARD_ID of the current question
uv run python scripts/main.py review get-answer
# Rate the review result, then print historical accuracy, today's review progress and retrievability change
uv run python scripts/main.py review rate [again|hard|good|easy]
```

## Review Loop
Follow this sequence strictly. Do not skip steps:

1. `review get-question`
2. The agent answers from its own memory first (do not view the answer yet).
3. `review get-answer`
4. Compare with the answer, then self-grade with `again/hard/good/easy`.
5. `review rate [RATING]`
6. Use the output's historical correctness and remaining progress to apply the reflection template.
7. Continue to the next card until there are no due cards or the user asks to stop.

## State Constraints
- If did not run `rate`, running `get-question` again will repeat the previous card.
- Running `get-answer` before `get-question` returns an error.
- Running `rate` before `get-answer` returns an error.

## Rating Rules
- again: You could not recall it, or the core facts in your answer were wrong.
- hard: You recalled it, but with clear difficulty and noticeable delay.
- good: You answered correctly with only a brief pause.
- easy: You answered quickly and accurately with no obvious hesitation.

## Reflection Template
After each rating, unless the self-rating is easy, output reflection using this template:

1. Conclusion for this card
- Was the answer correct?
- What were the main errors or hesitation points?

2. Update your memory system (explicit action required)
- Add: If missing key information caused a wrong or slow answer.
- Delete: If interfering memory caused misjudgment.
- Update: If existing memory is inaccurate and needs correction.

3. Challenge the card (optional)
- Is the prompt underspecified or ambiguous?
- Does the reference answer need revision?

4. Next step
- Ask for the next card, or state that the review is finished.

## Output Discipline
- In the `get-question` stage, focus only on the prompt.
- In the `get-answer` stage, focus only on the reference answer.
- In the `rate` stage, do scoring and reflection only; do not rewrite the full question.
- In long review sessions, keep reflections short to control context length.
- When updating memory, you need to explicitly state the action (add/delete/update) on your own memory system. SRSA tracks and schedules cards only. It does not automatically update it.

## End Conditions
End the review when any one condition is met:
- The command output says "No due cards".
- The user explicitly asks to pause or stop.

## Recovery Rules
- If a command returns an error, fix the call order first, then continue.
- If a card is clearly problematic (ambiguous prompt or wrong answer), use the following when needed:
  - `card override [CARD_ID] ...` to revise content
  - `card rm [CARD_ID]` to remove an invalid card
