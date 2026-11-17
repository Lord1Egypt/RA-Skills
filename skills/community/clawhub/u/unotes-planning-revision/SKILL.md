---
name: planning-revision
description: "Builds a revision plan from the user's uNotes flashcard decks, quizzes, study streak, and monthly quota. Use when the user asks 'what should I revise', 'which flashcards do I have', 'which quizzes are on my courses', 'how long is my study streak', 'did I study today', 'make a revision plan for my exam', or 'how much uNotes quota is left'. Read-only."
---

# uNotes revision check

Read the user's own study data and turn it into a short, actionable revision plan.

## Connecting and calling the tools

Every tool in this skill comes from the `unotes` MCP server, the uNotes connector, and is written here as `unotes:<tool>`.

- **Tools listed by name (how uNotes serves them today):** call them directly, for example `unotes:search_library`.
- **Only `unotes:search_tools` and `unotes:execute_typescript` listed (Code Mode):** call `unotes:search_tools` first, then call each tool inside `unotes:execute_typescript` as `external_<tool>` (for example `external_search_library`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `unotes:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects uNotes and approves that scope.
- **No `unotes` tools at all:** uNotes is not connected yet. Install the uNotes power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

- `unotes:list_my_flashcards`: the user's flashcard decks with title, subject, status, card count, course, and URL.
- `unotes:list_my_quizzes`: quizzes on the user's courses with question count and duration.
- `unotes:get_study_streak`: current streak days, longest streak, whether they studied today, and earned badges.
- `unotes:get_quota_status`: plan tier and per-feature quota rows (`used`, `limit`, `remaining`, `resetsAt`). A `null` limit means unlimited.

## Workflow

1. Call `unotes:get_study_streak`, `unotes:list_my_flashcards`, and `unotes:list_my_quizzes`.
2. Group the decks and quizzes by course. Show one line per course: decks (with card counts) and quizzes (with question counts).
3. Report the streak in one sentence. If `studiedToday` is false, say so and point at the smallest deck or shortest quiz as a quick session.
4. If the user mentions an upcoming exam, put that course first and list its decks and quizzes as the plan for the days left.
5. If the user asks about quota, call `unotes:get_quota_status` and list each feature as used out of limit, with the reset date. Reading quota never uses any.

## Rules

- All four tools read only the signed-in account. No tool takes a user id; never try to read another person's data.
- This connector has no write tools, so this skill never changes anything. It cannot create decks or quizzes, record study sessions, or change the streak. Those happen in the uNotes app.
- Report only what the tools return. Do not invent scores or progress percentages; the tools do not return them.
- Do not make plan or price recommendations from the quota data.
