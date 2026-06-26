---
name: test-master-fixed
description: Use when you need a practical testing playbook for turning product or code changes into a clear test strategy, test cases, and execution checklist.
tags: [testing, qa, unit, integration, e2e, coverage, regression, quality]
version: 1.0.1
---

# Test Master

This skill is a documentation playbook, not a standalone CLI or framework.

## When to use

- A feature, bug fix, or refactor needs a structured test plan.
- You want to turn product requirements into concrete test scenarios.
- You need to review coverage across unit, integration, end-to-end, or regression layers.
- You want a concise list of risks, assumptions, and follow-up checks before release.

## Recommended workflow

1. Define the scope.
   Capture the user-facing behavior, systems touched, and anything explicitly out of scope.
2. Map risks.
   Identify high-risk paths first: authentication, payments, data loss, permissions, concurrency, migrations, and integrations.
3. Split the plan by test layer.
   Decide what belongs in unit tests, integration tests, end-to-end tests, and manual exploratory checks.
4. Convert risks into test cases.
   Write clear preconditions, steps, expected results, and edge cases.
5. Review observability.
   Call out logs, metrics, alerts, and failure signals that should be checked during validation.

## Output checklist

- Test scope summary
- Key risks and assumptions
- Coverage by test layer
- Prioritized test cases
- Regression checklist
- Open questions or missing instrumentation

## Guardrails

- Confirm assumptions instead of inventing product behavior.
- Prefer realistic test data and production-like edge cases.
- Mark anything that still needs manual verification.
- If automation is not available, say so clearly instead of implying a tool exists.
