# UI Intent Contract

Produce a contract proportionate to the change. A local component adjustment may
need only a few rows; a new page or flow needs the full structure.

## Contents

- [Status Vocabulary](#status-vocabulary)
- [Compact Contract](#compact-contract)
- [Full Contract](#full-contract)
- [Contract Quality](#contract-quality)

## Status Vocabulary

- `CONFIRMED`: directly stated or selected by the user
- `INFERRED`: derived from cited repository or artifact evidence
- `PROPOSED`: recommended by the agent and reversible
- `OPEN`: material uncertainty that still needs a decision or is blocked

## Compact Contract

Use this form for a small, convention-led change:

```markdown
## UI Intent Contract

- Goal:
- Existing pattern to inherit:
- Material change:
- States and responsive impact:
- Deliberate deviation:

| Decision | Status | Basis | Observable result |
|---|---|---|---|

| Acceptance scenario | Evidence |
|---|---|
```

## Full Contract

Use this form for a new page, flow, or materially ambiguous change:

```markdown
## UI Intent Contract

### Product Intent

- User and context:
- Primary job:
- Primary action:
- First-view hierarchy:
- Constraints:
- Anti-goals:

### Decision Record

| ID | Decision | Status | Basis | Observable result |
|---|---|---|---|---|

### Repository Inheritance

| UI need | Existing evidence | Reuse action | Deviation and reason |
|---|---|---|---|

### Structure and Interaction

- Page regions and reading order:
- Action hierarchy:
- Content density and grouping:
- Navigation or disclosure:
- Feedback and recovery:

### States and Viewports

| State or viewport | Expected behavior | Priority |
|---|---|---|

Cover only material states, including loading, empty, error, permission,
disabled, partial, success, long content, narrow, and wide where applicable.

### Accessibility

- Semantics and labels:
- Keyboard and focus:
- Contrast and non-color cues:
- Reduced motion or assistive behavior:

### Acceptance

| Scenario | Viewport or state | Action | Observable oracle | Evidence |
|---|---|---|---|---|

### Open Decisions

| Decision | Why it matters | Owner or blocking evidence |
|---|---|---|
```

## Contract Quality

The contract is ready when:

- decisions describe observable outcomes, not only adjectives
- every repository-inheritance claim cites a concrete source
- unsupported product or visual choices remain labeled `PROPOSED` or `OPEN`
- component reuse is semantic and compatible
- relevant error, content-stress, and responsive behavior is explicit
- acceptance criteria can distinguish a plausible wrong implementation
- no material `OPEN` item is hidden inside implementation prose

Do not fill sections with "N/A" mechanically. Omit immaterial sections for a
small change and explain any material evidence that is blocked.
