---
name: tdd
description: Test-driven development with red-green-refactor loop and de-sloppify pattern. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or asks for test-first development. Includes cleanup pass for removing test/code slop.
---

# Test-Driven Development

## Philosophy

**Core principle**: Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe _what_ the system does, not _how_ it does it. A good test reads like a specification - "user can checkout with valid cart" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation. They mock internal collaborators, test private methods, or verify through external means (like querying a database directly instead of using the interface). The warning sign: your test breaks when you refactor, but behavior hasn't changed. If you rename an internal function and tests fail, those tests were testing implementation, not behavior.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Anti-Pattern: Horizontal Slices

**DO NOT write all tests first, then all implementation.** This is "horizontal slicing" - treating RED as "write all tests" and GREEN as "write all code."

This produces **crap tests**:

- Tests written in bulk test _imagined_ behavior, not _actual_ behavior
- You end up testing the _shape_ of things (data structures, function signatures) rather than user-facing behavior
- Tests become insensitive to real changes - they pass when behavior breaks, fail when behavior is fine
- You outrun your headlights, committing to test structure before understanding the implementation

**Correct approach**: Vertical slices via tracer bullets. One test → one implementation → repeat. Each test responds to what you learned from the previous cycle. Because you just wrote the code, you know exactly what behavior matters and how to verify it.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

## Workflow

### 1. Planning

Before writing any code:

- [ ] Confirm with user what interface changes are needed
- [ ] Confirm with user which behaviors to test (prioritize)
- [ ] Identify opportunities for [deep modules](deep-modules.md) (small interface, deep implementation)
- [ ] Design interfaces for [testability](interface-design.md)
- [ ] List the behaviors to test (not implementation steps)
- [ ] Get user approval on the plan

Ask: "What should the public interface look like? Which behaviors are most important to test?"

**You can't test everything.** Confirm with the user exactly which behaviors matter most. Focus testing effort on critical paths and complex logic, not every possible edge case.

### 2. Tracer Bullet

Write ONE test that confirms ONE thing about the system:

```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
```

This is your tracer bullet - proves the path works end-to-end.

### 3. Incremental Loop

For each remaining behavior:

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

Rules:

- One test at a time
- Only enough code to pass current test
- Don't anticipate future tests
- Keep tests focused on observable behavior

### 4. Refactor

After all tests pass, look for [refactor candidates](refactoring.md):

- [ ] Extract duplication
- [ ] Deepen modules (move complexity behind simple interfaces)
- [ ] Apply SOLID principles where natural
- [ ] Consider what new code reveals about existing code
- [ ] Run tests after each refactor step

**Never refactor while RED.** Get to GREEN first.

## Checklist Per Cycle

```
---

## The De-Sloppify Pattern

**An add-on pattern for TDD workflows.** Add a dedicated cleanup/refactor step after each implementation phase.

### The Problem

When you implement with TDD, LLMs take "write tests" too literally:
- Tests that verify TypeScript's type system works (testing `typeof x === 'string'`)
- Overly defensive runtime checks for things the type system already guarantees
- Tests for framework behavior rather than business logic
- Excessive error handling that obscures the actual code

### Why Not Negative Instructions?

Adding "don't test type systems" or "don't add unnecessary checks" to the implementer prompt has downstream effects:
- The model becomes hesitant about ALL testing
- It skips legitimate edge case tests
- Quality degrades unpredictably

### The Solution: Separate Pass

Instead of constraining the implementer, let it be thorough. Then add a focused cleanup agent:

```bash
# Step 1: Implement (let it be thorough)
claude -p "Implement the feature with full TDD. Be thorough with tests."

# Step 2: De-sloppify (separate context, focused cleanup)
claude -p "Review all changes in the working tree. Remove:
- Tests that verify language/framework behavior rather than business logic
- Redundant type checks that the type system already enforces
- Over-defensive error handling for impossible states
- Console.log statements
- Commented-out code

Keep all business logic tests. Run the test suite after cleanup to ensure nothing breaks."
```

### In a Loop Context

```bash
for feature in "${features[@]}"; do
  # Implement
  claude -p "Implement $feature with TDD."

  # De-sloppify
  claude -p "Cleanup pass: review changes, remove test/code slop, run tests."

  # Verify
  claude -p "Run build + lint + tests. Fix any failures."

  # Commit
  claude -p "Commit with message: feat: add $feature"
done
```

### Key Insight

> Rather than adding negative instructions which have downstream quality effects, add a separate de-sloppify pass. Two focused agents outperform one constrained agent.

### De-Sloppify Checklist

```markdown
## Cleanup Pass Checklist

### Tests to Remove
- [ ] Tests verifying language features (TypeScript types, JS prototypes)
- [ ] Tests verifying framework behavior (React rendering, Next.js routing)
- [ ] Tests for impossible states (already prevented by type system)
- [ ] Duplicate test coverage (same scenario tested multiple ways)

### Code to Remove
- [ ] Redundant type guards after TypeScript checks
- [ ] Unnecessary runtime validations
- [ ] Console.log statements
- [ ] Commented-out code
- [ ] Dead code (unused functions/imports)

### What to Keep
- [ ] Business logic tests
- [ ] Integration tests
- [ ] Edge case handling for real scenarios
- [ ] Security validations
```

---

*Two focused agents outperform one constrained agent.*
