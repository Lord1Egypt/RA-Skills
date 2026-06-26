# Coding Principles

Behavioral principles for implementation. Load before writing any code.

## When to Use

Auto-loaded by implement.md before writing code. Not a direct trigger.

## Core Principles

| Principle | Description |
|-----------|-------------|
| Simplicity first | Write the simplest code that satisfies the requirement |
| Surgical changes | Modify only what is necessary, leave unrelated code untouched |
| Goal-driven | Every change must trace back to a requirement or acceptance criterion |
| Follow existing patterns | Match the project's conventions exactly. When the `.artifacts/codebase/{area}.md` cache exists for the area, use it for Project Abstractions and Custom Hooks; otherwise read representative files |
| Test first (when tests exist) | If the project has test infrastructure, write the failing test before the implementation |
| Verify before moving on | Run quality gates after each task, fix issues immediately |

## Anti-Patterns

| Anti-Pattern | What It Looks Like | Instead |
|--------------|--------------------|---------|
| Over-engineering | Adding abstractions for one use case | Write concrete code, extract later if needed |
| Premature abstraction | Creating helpers/utils for single callers | Inline the logic, refactor when a pattern emerges |
| Unnecessary refactoring | Cleaning up code outside the task scope | Only touch files listed in the design |
| Speculative features | Adding config options "just in case" | Implement exactly what the spec requires |
| Gold plating | Adding extra error handling, logging, or comments beyond requirements | Match the project's existing level of detail |
| Symptom masking | Wrapping in `try/catch`, returning a fallback default, or silently recovering to make an error stop appearing | Diagnose the root cause (file:line of the first incorrect decision), fix there. If a workaround is genuinely needed, label it in code with the underlying defect and capture a follow-up |

## Decision Framework

Before writing code, ask:

1. Is this change required by a spec requirement?
2. Does the design specify this file/component?
3. Am I following the project's existing pattern for this?
4. Is this the minimal change that satisfies the task?
5. If this is a fix: does it address the root cause (file:line of the
   first incorrect decision), or does it suppress the symptom? If
   suppressing, is it explicitly labeled as a workaround with a
   captured follow-up?

If any answer is "no", reconsider the change.
