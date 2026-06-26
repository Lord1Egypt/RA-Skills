Review the entire app for bugs, regressions, edge cases, security issues, data consistency problems, UX/state bugs, performance risks, and testing gaps. Treat this as a code review.

Prioritize findings by severity (critical / high / medium / low / nit), include file/line references for every finding, list open questions and assumptions you had to make, and mention what you verified with typecheck, lint, and tests (and what you couldn't verify).

Be concrete. Prefer "auth.ts:42 — SQL query concatenates user input, vulnerable to injection" over "watch out for SQL injection". If something looks wrong but you're not sure, say so and explain what you'd need to confirm it.

Structure the output as:

## Summary
One-paragraph overview: overall health, biggest concerns, what's solid.

## Critical
Issues that break things, lose data, or expose security holes. Each: file:line, what's wrong, why it matters, suggested fix.

## High
Bugs, regressions, meaningful edge cases.

## Medium
Code quality issues that will bite later — error handling gaps, fragile patterns, missing validation.

## Low / Nits
Style, naming, minor improvements.

## Testing gaps
What should be tested but isn't. What existing tests might miss.

## Open questions & assumptions
What you weren't sure about. What you assumed. What the author should confirm.

## Verification performed
What you ran (typecheck, lint, tests) and the results. What you couldn't run and why.
