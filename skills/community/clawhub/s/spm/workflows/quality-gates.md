# Quality Gates — Three-Tier System

## Overview

Three-tier quality enforcement that runs throughout the development lifecycle.

## Tier 1: Always Do (Mandatory)

- Run test suite before any commit
- Follow project naming conventions
- Validate all inputs (security baseline)
- Perform code style checks
- Keep documentation in sync with changes

## Tier 2: Ask First (Require Approval)

- Database schema changes
- Adding new dependencies
- Modifying CI/CD configuration
- Breaking API contracts
- Changing performance-critical paths
- Modifying security-sensitive code

## Tier 3: Never Do (Blocked)

- Commit secrets or credentials
- Edit vendor directories
- Remove failing tests without explicit approval
- Skip code review for complex changes
- Bypass security checks
- Force-push to shared branches without coordination

## Quality Gate Evaluation

After each phase, record in WBS ledger:

```
Quality Gate: [Phase]
- Always Do: ✅ All passed
- Ask First: N/A (no DB changes)
- Never Do: ✅ No violations
- Result: PASS
```
