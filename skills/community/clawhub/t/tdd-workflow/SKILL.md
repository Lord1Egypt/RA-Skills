---
name: tdd-workflow
description: "Test-driven development workflow enforcing 80%+ code coverage with unit, integration, and E2E tests. Write tests first, validate RED state, implement minimally, validate GREEN, then refactor. Use when writing features, fixing bugs, or refactoring. Trigger phrases: write tests, TDD, test-driven, feature implementation, bug fix. Adapted from everything-claude-code by @affaan-m (MIT)"
metadata: {"clawdbot":{"emoji":"✅","requires":{"bins":["npm","git"],"env":[]},"os":["darwin","linux","win32"]}}
---

# Test-Driven Development Workflow

Ensure all code development follows TDD principles with 80%+ code coverage.

## When to Activate

- Writing new features or functionality
- Fixing bugs or issues
- Refactoring existing code
- User says "write tests", "add specs", "how should I test this"

## Quick Start

1. Write user journey in acceptance-test format ("As a [role], I want...")
2. Generate test cases (happy path + edge cases + errors)
3. Run tests → verify RED state (must fail before implementation)
4. Implement minimal code to make tests pass → GREEN state
5. Refactor while keeping tests green
6. Verify 80%+ coverage achieved

## Key Concepts

- **Tests before code** — Write tests first, then implementation
- **RED-GREEN-REFACTOR** — Fail → Pass → Improve (no exceptions)
- **80% coverage minimum** — Unit, integration, and E2E combined
- **Unit-level isolation** — Mock dependencies, test behavior not implementation
- **Independent tests** — No test ordering dependencies; each can run solo

## Common Usage

Most frequent patterns:
- Unit tests for functions and components
- Integration tests for API endpoints and database operations
- E2E tests for critical user flows
- Edge case and error path testing
- Fast execution (unit tests < 50ms each)

## References

- `references/workflow-steps.md` — Detailed 7-step TDD cycle with git checkpoints
- `references/patterns-and-best-practices.md` — Test patterns, common mistakes, success metrics
