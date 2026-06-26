# Triage Guide

When classifying PR review comments, assign one of five categories:

## MUST_FIX
A blocking issue that must be resolved before the PR can merge.

Indicators:
- Reviewer explicitly says "blocking", "must fix", "required"
- Correctness bug or security issue
- Breaks tests or build
- Data loss risk
- Violates project conventions that are explicitly documented

## SHOULD_FIX
Non-blocking but worth addressing in this PR to improve quality.

Indicators:
- Reviewer says "nit", "suggestion", "consider", "ideally"
- Style or readability improvement
- Clear improvement with low risk and small effort
- Would reduce future confusion or maintenance burden

## PARK
Valid concern, but intentionally deferred outside this PR.

Use when:
- The fix requires changes in a different PR or component
- The effort is disproportionate to the PR scope
- It's a known existing issue not introduced by this PR
- You are deferring: create a follow-up issue and reference it in your reply

## OUT_OF_SCOPE
Not applicable to this PR; rejected with explanation.

Use when:
- Comment is based on a misunderstanding
- The suggested approach contradicts project conventions
- The comment refers to code not changed by this PR
- A prior discussion or decision already covers this

## NEEDS_CLARIFICATION
The comment's intent is genuinely ambiguous and acting without confirmation risks implementing the wrong thing.

Use when:
- Multiple valid interpretations exist and they would lead to different code changes
- The reviewer's suggestion is unclear or self-contradictory
- Applying any plausible interpretation without confirmation would be wasteful or risky

Do **not** use as a way to avoid difficult work. Only classify as NEEDS_CLARIFICATION when the ambiguity is real.

---

## Triage Tips

- When in doubt between MUST_FIX and SHOULD_FIX, ask: "Would a reviewer block merge over this?" If yes, MUST_FIX.
- When in doubt between SHOULD_FIX and PARK, ask: "Can this be done safely within this PR's scope?" If yes, SHOULD_FIX.
- When in doubt between SHOULD_FIX and NEEDS_CLARIFICATION, ask: "Can I implement a reasonable interpretation without risking the wrong outcome?" If yes, SHOULD_FIX.
- **Prefer asking over guessing.** A wrong fix wastes review cycles and can introduce regressions. One well-targeted question is cheaper than an incorrect implementation.
- If you need external knowledge (e.g., is this pattern idiomatic in this language/framework?), use Perplexity if available.
- Triage all comments before acting on any. This gives you a full picture before committing to changes.
