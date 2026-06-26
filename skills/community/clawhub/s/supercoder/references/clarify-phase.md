# Phase 3: Clarify

Ask targeted technical questions based on codebase findings. The questions here are about how to implement it — architectural choices, pattern conflicts, compatibility concerns.

## What to Communicate

After getting the user's answers, present:

- **Refined scope** — updated in/implicit/out boundaries
- **Refined acceptance criteria** — updated based on answers
- **Key decisions** — each decision, the user's answer, and how it changes the approach

## Context to Preserve

Before finishing, make sure the conversation retains: the refined intent, the updated acceptance criteria count, and the top decisions with their impact.

## Principle

Good technical questions are specific and grounded in the codebase. Compare:

- Weak: "What payment methods do you want?" (generic, no context)
- Strong: "The codebase has WechatPay and AliPay adapters in `src/payments/adapters/`. Should new methods follow this adapter pattern, or refactor to a plugin architecture?" (specific, references actual code, offers concrete options)

## Steps

1. TaskUpdate — set Phase 3 to `in_progress`.
2. Generate up to 8 prioritized questions. For each question, state the ambiguity clearly, reference specific code or files that create it, and offer 2–3 concrete options where possible.

   Prioritize questions that:
   1. Block architectural decisions (highest priority)
   2. Affect the scope of work significantly
   3. Resolve conflicting interpretations
   4. Clarify technical edge cases

3. Present to user — use AskUserQuestion, up to 4 questions per batch. Each question gets a clear header, the context, and 2–3 options with descriptions.
4. Incorporate answers — present updated scope and acceptance criteria.
5. Preserve context for downstream phases.
6. TaskUpdate — set Phase 3 to `completed`.

## Rollback

If clarification reveals insufficient exploration: set Phase 2 back to `pending`, specify what areas need exploration.
