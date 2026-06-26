# Change Visibility

Use this file when the user should be able to clearly perceive what improved.

## Goal

Make terminal UX improvements observable.
Do not leave the user guessing whether a redesign changed anything important.

## Visibility Options

Choose the lightest option that makes the improvement clear.

### 1. Before/after summary

Use for small or local improvements.

Include:

- what the old interaction forced the user to do
- what the new interaction changes
- why the new version reduces confusion, steps, or ambiguity

### 2. Before/after output comparison

Use when help text, result pages, state output, or prompt wording changed.

Show:

- old structure or wording in summary form
- new structure or wording in summary form
- the concrete difference in hierarchy, hints, or status feedback

Avoid dumping huge raw outputs. Summarize only the load-bearing differences.

### 3. Visual mockup or browser comparison

Use when layout, flow, or state presentation is hard to understand in plain text.

Examples:

- wizard redesign
- session run flow comparison
- help page structure comparison
- result card, list, or detail view comparison

If a visual-comparison tool is available, use it.
If not, fall back to a compact text mockup or structured before/after walkthrough.

### 4. Flow comparison

Use when the main improvement is fewer steps or clearer branching.

Show:

- old flow
- new flow
- removed ambiguity
- new recovery or exit path

### 5. Validation-backed visibility

Use when code has already changed.

Show:

- which paths were tested
- which states now exist or are clearer
- which failure or empty states are now covered

## What Counts as a Visible Improvement

A change is visible when the user can point to at least one of:

- a clearer next action
- fewer confusing choices
- better feedback during loading, success, or failure
- more obvious quit, cancel, or confirmation behavior
- cleaner grouping and information hierarchy
- a clearer result or summary page

## Anti-Patterns

- Saying "the UX is improved" with no artifact or comparison
- Listing internal refactors as if they were user-visible UX gains
- Dumping full outputs without highlighting the important differences
