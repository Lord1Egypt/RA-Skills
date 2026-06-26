---
name: resetcontinue
description: Generate a concise copy-paste session handoff for continuing the current task in a fresh chat after /new or /reset. Use when the user wants to preserve the real task state, current blockers, and immediate next step without carrying over stale context or repeated background explanation. Trigger on direct requests for reset-continue, handoff summary, session handover, or when the user invokes /resetcontinue.
user-invocable: true
---

# Fresh Session Handoff

When invoked, produce a **fresh-session handoff summary** that the user can paste into a new chat after `/new` or `/reset`.

## Goal

- preserve the current task state
- keep only the facts that help the next session continue quickly
- reduce context pollution from long or broken prior threads

## Output contract

- Write in **简体中文** unless the user clearly asks otherwise.
- Output **only** the handoff summary. Do not add an intro like “下面是摘要”.
- Keep it **short, direct, and concrete**.
- Use **8 items or fewer**.
- Prefer bullets or numbered lines.
- No Markdown code fences unless the user explicitly needs a command block.
- Prefer exact facts when available:
  - absolute file paths
  - branch or commit
  - service / room / environment names
  - blocker or error code
  - the immediate next action
- **Never invent missing facts.** If something is unclear, omit it instead of guessing.

## Required sections

Use these sections **when applicable**:

1. 当前任务
2. 已确认结论
3. 已排除问题
4. 当前卡点
5. 下一步动作
6. 重要背景
7. 不要重复做的事
8. 回复要求

## Selection rules

Include only information that meaningfully helps a new session resume fast.

- Keep stable goals, confirmed decisions, constraints, and current scope.
- Keep recent troubleshooting conclusions **only if** they affect the next step.
- Keep unfinished edits, verification status, or pending push/deploy state when relevant.
- Keep approvals, credentials, external dependencies, or user promises that still matter.
- Exclude chit-chat, repeated explanations, and dead exploration unless it should not be retried.
- If the task is already complete, say that clearly and use `下一步动作` for the most useful follow-up.
- If several threads were discussed, summarize only the thread the user is actually carrying forward.

## Quality bar

- The summary should let a new session continue with minimal backtracking.
- The wording should be practical, not essay-like.
- The next agent should be able to tell what to do first within a few seconds of reading it.

## Final line

End with exactly this line:

`新会话请直接接着做，不要从头重复背景。`
