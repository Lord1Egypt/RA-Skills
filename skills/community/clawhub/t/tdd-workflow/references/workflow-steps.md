# TDD Workflow Steps

## Step 1: Write User Journeys

```text
As a [role], I want to [action], so that [benefit]

Example:
As a user, I want to search for markets semantically,
so that I can find relevant markets even without exact keywords.
```

## Step 2: Generate Test Cases

For each user journey, create comprehensive test cases covering happy path, edge cases, and errors.

## Step 3: Run Tests (RED gate)

```bash
npm test  # or appropriate test runner
```

**Tests MUST fail before implementation.** This is mandatory. Before modifying business logic:

- The test must compile/run successfully
- The test must execute and produce RED result
- The failure must be caused by the intended missing implementation (not unrelated syntax errors)

Create a git checkpoint commit after RED validation:

```bash
git commit -m "test: add reproducer for <feature or bug>"
```

## Step 4: Implement Code

Write minimal code to make tests pass. Don't over-engineer.

## Step 5: Run Tests (GREEN gate)

```bash
npm test  # Re-run the same test target
```

Tests should now pass. Only after GREEN validation may refactoring proceed.

Create a git checkpoint commit:

```bash
git commit -m "fix: <feature or bug>"
```

## Step 6: Refactor

Improve code quality while keeping tests green:
- Remove duplication
- Improve naming
- Optimize performance
- Enhance readability

Create a final checkpoint commit:

```bash
git commit -m "refactor: clean up after <feature or bug> implementation"
```

## Step 7: Verify Coverage

```bash
npm run test:coverage
# Verify 80%+ coverage achieved
```
