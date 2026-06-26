# Core Review Policy

Use this file for all review modes and all stacks.

## Table of Contents

- [Primary Objective](#primary-objective)
- [Review Order](#review-order)
- [Confidence Filter](#confidence-filter)
- [Severity Guide](#severity-guide)
- [Shared Heuristics](#shared-heuristics)
- [Dead Code Guidance](#dead-code-guidance)
- [Security Baseline](#security-baseline)
- [Source Notes](#source-notes)


## Primary Objective

Find real problems in changed code:

- behavioral regressions
- broken edge cases
- trust-boundary mistakes
- data corruption risks
- resource leaks or concurrency hazards
- missing or misleading tests
- isolated dead code that signals unfinished or abandoned behavior

Do not optimize for issue count. Optimize for correctness.

## Review Order

Review in this order:

1. Correctness
2. Security
3. Data integrity
4. Concurrency and lifecycle
5. Performance and scalability
6. Maintainability

## Confidence Filter

Report only high-confidence findings.

Usually skip:

- pure style disagreements
- speculative architecture advice
- unchanged legacy issues
- warnings already guaranteed by enforced lint/typecheck/build gates
- minor naming or formatting nits unless the repository explicitly requires them

Escalate when:

- the change can break production behavior
- the change weakens auth, validation, escaping, or query safety
- the change can leak secrets or PII
- the change can deadlock, race, block, or leak resources
- the change introduces an untested new path or bug fix with no proof

## Severity Guide

| Severity | Meaning |
|---|---|
| CRITICAL | Security break, data loss, auth bypass, remote exploit path |
| HIGH | Likely bug or operational failure with meaningful impact |
| MEDIUM | Real issue with bounded impact or lower probability |
| LOW | Small maintainability or clarity issue with direct evidence |

## Shared Heuristics

- Prefer one strong finding over five weak ones.
- Read enough surrounding code to verify the claim.
- Mixed refactor + behavior changes increase review risk and should be called out.
- New code paths should usually come with tests near the same change.
- Comments should explain why, not restate obvious code.
- Isolated dead code matters when it preserves stale behavior, unused trust boundaries, or obsolete integration paths.

## Dead Code Guidance

Treat dead code as worth reporting when it is more than a cosmetic unused local:

- orphan modules or handlers with no incoming references
- branches made permanently unreachable by current control flow or feature flags
- unused exports, routes, jobs, or workers that imply abandoned behavior
- obsolete fallback paths that still retain secrets, permissions, or side effects

Usually skip dead-code findings already fully enforced by compiler or linter warnings unless:

- the repository appears not to enforce those warnings
- the dead code is structural, not just a local variable
- the dead code preserves risky behavior or confuses entry-point ownership

## Security Baseline

Across all stacks, look for:

- input crossing trust boundaries without validation
- dynamic query construction with user input
- shell, file, or URL handling based on untrusted input
- secrets, tokens, connection strings, or PII in logs
- auth without authz
- outbound requests without host restrictions or time limits

## Source Notes

These review rules were strengthened using official guidance from:

- Google Engineering Practices: https://google.github.io/eng-practices/review/reviewer/looking-for.html
- OWASP Input Validation Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
- OWASP SQL Injection Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- OWASP Query Parameterization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html
- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- TypeScript `noUnusedLocals`: https://www.typescriptlang.org/tsconfig/noUnusedLocals.html
- TypeScript `allowUnreachableCode`: https://www.typescriptlang.org/tsconfig/allowUnreachableCode.html
- ESLint `no-unused-vars`: https://eslint.org/docs/latest/rules/no-unused-vars
