# Implementation Workflow

Unified workflow for implementing code changes with quality gates and atomic commits.

## Workflow Pattern Detection

Before implementing, check for existing workflow patterns in the repository and your skills, the worklow pattern should be superseeded by these.

### Spec-First Workflow
- Look for `docs/` or `specs/` directories with specifications
- Check for spec files in project structure
- Follow spec → implement pattern if present, superseed to specific skills on this

### Test-Driven Development (TDD)
- Check if tests are written before implementation
- Look for test-first patterns in codebase
- Follow test → implement → refactor cycle if present

### Other Structured Workflows
- Check for plan files or structured documentation
- Look for workflow indicators in README.md or AGENTS.md
- Follow existing patterns and skills when detected

## Implementation Process

### 1. Atomic Changes

Group related changes together:
- Implementation code + tests
- Feature + related refactoring
- Fix + test for fix

Each atomic change should:
- Pass type checking
- Pass all tests
- Pass linting
- Be self-consistent

### 2. CI Verification

Before staging any changes:
1. Run CI checks (types, tests, lint)
2. Prefer single CI command if available
3. If checks fail, stop and report
4. Only proceed when all checks pass

### 3. Atomic Commits

After CI passes:
1. Stage atomic changes
2. Suggest semantic commit message
3. Confirm with user
4. Commit after approval
5. Continue to next atomic change

## Stop and Ask

Stop and ask user before:
- Adding type ignores or suppressions
- Using `any` type or type escapes
- Uncertain how to proceed
- Requirements unclear
- Better approach needs confirmation

## Backward Compatibility

- **Public interfaces**: Consider backward compatibility for APIs, libraries
- **Internal refactoring**: Unit, integration, and E2E tests serve as confirmation gate
- **Greenfield**: No backward compatibility needed unless directed

## Automation

If user requests "continue to X":
- Proceed with atomic commits automatically
- Resume asking when X point reached
- X can be: file, feature, test passing, etc.

## Integration

This workflow integrates with:
- CI verification before commits
- Semantic commit messages
- Test-first development when present
- Spec-first development when present
- Code review practices
