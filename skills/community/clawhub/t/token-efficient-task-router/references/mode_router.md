# Mode Router

## Purpose

This file defines how to route a request into Ask, Plan, Craft, Expert, or an Interactive Routing Prompt before mode selection.

Before using this router, first use `references/focus_activation_rules.md` to avoid activating too much of the skill too early.

## Primary decision order

1. Judge whether the request is clear enough to execute directly.
2. Judge whether files, folders, knowledge bases, or batch actions are involved.
3. Judge risk level.
4. Judge expected token cost.
5. If the requested output is broad, first calibrate the real need and delivery granularity.
6. If uncertainty remains meaningful, trigger Interactive Routing Prompt.

## Direct Craft cases

Go straight to Craft Mode when the task is:

- simple
- explicit
- low-risk
- one-shot
- reversible or output-only

Examples:

- rewrite one sentence
- explain one command
- compress a paragraph
- translate a sentence
- generate a tiny template

## Ask cases

Use Ask Mode when the user mainly wants:

- diagnosis
- feasibility judgment
- recommendations
- risk assessment
- next-step guidance
- clarification before action

## Plan cases

Use Plan Mode when the request involves:

- many steps
- important files
- core documents
- folders or projects
- batch operations
- system setup
- knowledge-base organization
- report generation from many materials
- high or medium-high token cost

## Expert cases

Recommend Expert Mode when:

- repeated attempts failed
- the domain is specialized
- the risk of continued trial-and-error is high
- the issue needs local expert ownership

## Interactive routing triggers

Trigger the prompt before final routing when:

- the user uses generic verbs such as `优化`, `整理`, `处理`, `重构`, `分析`
- the output type is unclear
- permission to modify files is unclear
- the request may touch files or knowledge bases
- the task may take multiple steps
- the task may consume substantial tokens
- the agent is unsure whether Ask, Plan, Craft, or Expert is correct
- the user asks for complete batch output but the actual need may be smaller

## Shortcut routing logic

- clear + simple + low-risk -> Craft
- error diagnosis -> Ask
- large `do everything` request with unclear real need -> need calibration first
- file or knowledge-base task without clear scope -> Interactive Routing Prompt
- multi-step or batch -> Plan
- repeated failure -> Expert recommendation

## User choice override policy

Honor the user's requested mode when safe.

Override the user choice when:

- the task is high-risk
- file operations are irreversible
- the selected mode conflicts with confirmation requirements

Recommended override wording:

`这个组合风险较高。复杂任务且涉及文件修改时，我建议改用 Plan Mode，先确认执行范围。`
