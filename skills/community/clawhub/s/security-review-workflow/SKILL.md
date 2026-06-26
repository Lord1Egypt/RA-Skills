---
name: "security_review_workflow"
description: "Use when the current branch or PR needs a focused security review that minimizes false positives and only reports concrete, exploit-relevant issues."
---


# Security Review Workflow

Use this skill for focused security review of branch or PR changes.

## Workflow
1. Collect git status, changed files, commit list, and full diff against the target base.
2. Research the codebase's existing security patterns.
3. Inspect only newly introduced attack surfaces in the diff.
4. Filter out speculative, low-signal, or excluded finding classes.
5. Report only concrete, actionable findings with file, severity, exploit path, and recommendation.

## Guardrails
- Minimize false positives aggressively.
- Ignore general code review comments that are not security issues.
- Prefer fewer high-confidence findings over noisy coverage.

## Example Requests
- Review this branch only for concrete security bugs.
- Find high-confidence vulnerabilities in the current diff and ignore noise.

## Inputs
- Diff against base
- Changed files
- Relevant security context

## Outputs
- High-signal security findings
- Severity and exploit path
- Fix recommendations

## Success Criteria
- Only concrete issues are reported.
- False positives are aggressively filtered.
- Each finding is actionable.

## Non-Goals
- General style review
- Speculative low-confidence security commentary

## Source Provenance
Derived from `src/commands/security-review.ts`.
