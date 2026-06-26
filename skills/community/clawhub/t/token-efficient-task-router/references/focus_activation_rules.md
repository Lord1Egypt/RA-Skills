# Focus Activation Rules

## Purpose

This file prevents the skill from activating too broadly before the task is precisely focused.

The problem it solves:

- too many skill branches may be conceptually relevant
- the agent starts loading and explaining too much too early
- token cost rises before the task is even properly scoped

## Core rule

Before loading detailed mode instructions, choose the smallest useful focus bundle.

Activate:

- one primary focus
- optionally one secondary assist focus

Do not activate the whole skill by default.

## Primary focus bundles

### `route-only`

Use when the task is still unclear and the immediate job is only to route.

Load:

- `references/mode_router.md`
- `references/interactive_routing.md`

### `ask-diagnose`

Use when the user mainly wants explanation, diagnosis, feasibility, or next-step advice.

Load:

- `references/ask_mode.md`
- `references/risk_levels.md`

### `plan-safe-execution`

Use when the task may change files, touch many materials, or involve multiple steps.

Load:

- `references/plan_mode.md`
- `references/file_safety_rules.md`

### `craft-quick-output`

Use when the task is clear, small, and low-risk.

Load:

- `references/craft_mode.md`

### `expert-escalation`

Use when repeated failure or specialist depth is the main issue.

Load:

- `references/expert_mode.md`

### `risk-check`

Use when the user mainly asks whether something is risky.

Load:

- `references/risk_levels.md`
- `references/file_safety_rules.md`

### `need-calibration`

Use when the user asks for a large or complete result but the real underlying need may be smaller.

Load:

- `references/need_calibration.md`
- `references/progressive_delivery_rules.md`

### `knowledge-scope`

Use when the task is about selecting how much of a knowledge base to inspect.

Load:

- `references/interactive_routing.md`
- `references/token_budget_modes.md`

### `ima-lite`

Use when the task is happening in iMA Copilot and the answer must stay short, stable, and explicit.

Load:

- `references/ima_copilot_adaptation.md`
- `references/ima_copilot_runtime_protocol.md`

### `workbuddy-file`

Use when the task happens in WorkBuddy and touches local files or folders.

Load:

- `references/workbuddy_adaptation.md`
- `references/file_safety_rules.md`

### `codebuddy-code`

Use when the task happens in CodeBuddy and touches code files, tests, bugfixes, or refactors.

Load:

- `references/codebuddy_adaptation.md`
- `references/file_safety_rules.md`

## Secondary assist bundles

Use a secondary bundle only if it materially improves safety or scope control.

Good examples:

- `route-only` + `ima-lite`
- `plan-safe-execution` + `workbuddy-file`
- `ask-diagnose` + `risk-check`
- `knowledge-scope` + `ima-lite`
- `need-calibration` + `ima-lite`
- `need-calibration` + `workbuddy-file`
- `ask-diagnose` + `codebuddy-code`
- `plan-safe-execution` + `codebuddy-code`
- `need-calibration` + `codebuddy-code`

Avoid loading three or more bundles unless the task genuinely requires it.

## Fast selection logic

1. If unclear: start with `route-only`
2. If simple and explicit: use `craft-quick-output`
3. If diagnostic: use `ask-diagnose`
4. If file or batch work: use `plan-safe-execution`
5. If in iMA: add `ima-lite` only when relevant
6. If in WorkBuddy file tasks: add `workbuddy-file`
7. If in CodeBuddy and code scope is unclear: add `codebuddy-code`
8. If the user asks for complete or batch delivery but the real need is unclear: use `need-calibration`
9. If knowledge-base scope is the main issue: use `knowledge-scope`
10. If repeated failure dominates: use `expert-escalation`

## Anti-bloat rule

Do not load all four mode files just because the skill contains four modes.

Do not load:

- `expert_mode.md` for a simple rewrite
- `plan_mode.md` for a single low-risk sentence edit
- `craft_mode.md` for a pure diagnosis task
- every platform adaptation file in one reply
- the whole repository for a small CodeBuddy bugfix

## Output discipline

If the focus is only routing, output only routing.

If the focus is only risk checking, output only risk judgment and next step.

If the focus is only knowledge scope, do not drift into full report generation.

If the focus is need calibration, do not jump into full delivery before the user confirms the needed granularity.
