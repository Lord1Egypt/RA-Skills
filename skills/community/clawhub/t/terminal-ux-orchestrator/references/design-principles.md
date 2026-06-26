# Design Principles

Use these principles to keep terminal interfaces implementable and readable.

## 1. Prefer clarity over decoration

Use spacing, ordering, labels, and grouping before reaching for color, borders, or box art.
If a screen only works because of heavy styling, the structure is probably weak.

## 2. Match interaction cost to task value

- Simple and repeatable tasks should stay command-first.
- Short branching flows work well as prompts or guided steps.
- Persistent context, multiple panes, or keyboard navigation justify a TUI.

Do not increase interaction cost just to make the tool feel more modern.

## 3. Make state legible

Every meaningful state should be distinct in wording and layout, not only color.
A user should be able to tell:

- what the tool is waiting for
- what is happening now
- what succeeded
- what failed
- how to recover or exit

## 4. Keep density intentional

Terminal space is scarce. Reduce noise:

- avoid unnecessary borders
- avoid redundant labels
- avoid large blocks of unstructured text
- keep key hints close to the control they affect

Dense output is acceptable only when scanning speed improves.

## 5. Use color semantically

Treat color as a meaning layer, not decoration:

- neutral for structure and secondary information
- accent for focus or primary actions
- green or equivalent for success
- yellow or equivalent for caution
- red or equivalent for errors or destructive actions

Never rely on color alone to communicate meaning.

## 6. Favor progressive disclosure

Show the minimum needed to move the user forward.
Reveal advanced options, diagnostics, or secondary actions when they become relevant.

## 7. Design around failure paths

Terminal tools are often used in unreliable environments.
Make room for:

- retries
- cancellation
- invalid input correction
- partial success
- resumable work where possible

## 8. Keep copy operational

Write prompts and messages so the user can act immediately:

- say what happened
- say what to do next
- say what will happen if they continue

Avoid decorative or vague language.
