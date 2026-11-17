# Ambiguity pass and stop triggers

Loaded by `/todo-plan` (step 2) and `/todo-add` (step 5) only when a request is not clear from its text and the repository. Part of the `todo` core skill.

**Skip this** when the request and the repo already answer every item below. Most requests need no pass at all.

## Checklist

Read the request against the README, `docs/`, the code and the tests, and note what is still unknown:

- **Undefined terms:** a word the request relies on that nothing in the repo defines ("loyal customer", "stale", "admin").
- **Missing acceptance criteria:** no observable result that would prove the work is done, so no `Done when` can be written.
- **Unstated actors:** who calls it, who may use it, and on whose behalf.
- **Error and boundary cases:** invalid input, empty or maximum values, failures of what it depends on, and what happens then.
- **Out of scope:** nearby work the request might or might not include.

## Stop triggers

Stop before writing `TODO.md`, a plan doc or code when any of these holds:

1. A **business rule**, data shape or boundary behaviour the work depends on is missing.
2. Two or more **incompatible implementations** fit the request, and the repo does not choose between them.
3. The work touches security, and its **authorization** or other security expectations are not stated.

Then ask: one message of at most 3 numbered questions, each with its options and the trade-off of each. Rounds may repeat until the triggers are cleared, at most 3 questions each time. Never guess to avoid asking.

## When the answer has to wait

If the user wants to record the question instead of answering now:

- With a plan doc (existing, or written in this confirmation), add each question as a bullet under its **Open questions**.
- Otherwise, on the user's yes, write the node as `[!]`, with its intended `Done when` and the line `Blocked: open questions: <one line> → n/a (manual) → answer them, then /todo-update <ID> --status ready`.

Questions go only there: never a new section in `TODO.md`, and never into a task's other fields.
