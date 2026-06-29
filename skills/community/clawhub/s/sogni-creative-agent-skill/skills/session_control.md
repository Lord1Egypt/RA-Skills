---
name: session_control
description: Turn-control markers the model uses to end its turn cleanly.
always_loaded: true
tool_names:
  - ask_clarifying_question
  - finalize_response
---

# Session control

Semantic-marker tools the model uses to signal *intent* about the current turn — not to execute creative work. The host treats either call as the end of the tool loop.

## Tools

- `ask_clarifying_question {question, reason?}` — model needs more user input. The host stops the loop and surfaces the question.
- `finalize_response {outcome, summary?}` — the turn is complete. The host stops the loop and uses the summary as the assistant message.

## Constraints

- Do not call any other tool after `ask_clarifying_question` or `finalize_response` — both end the turn.
- Call `finalize_response` exactly once per turn at the end. If a tool just surfaced a question to the user, prefer `outcome="asked_user"`.
