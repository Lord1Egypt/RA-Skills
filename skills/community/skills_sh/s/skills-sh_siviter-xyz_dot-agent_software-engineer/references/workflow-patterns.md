# Workflow Patterns

Detailed patterns and practices for software development workflows.

## Implementation Workflow

- **Atomic changes**: Group related changes together (code + tests)
- **CI verification**: Run CI checks before staging (types, tests, lint)
- **Semantic commits**: Use conventional commit format
- **Stop and ask**: Ask user before adding type ignores, suppressions, or `any` types

## Code Review Workflow

- Review for functionality, code quality, and security
- Check edge cases and error handling
- Verify tests are present and passing
- Ensure code follows project conventions
- Verify CI passes before completion claims

## Testing Workflow

- Write tests before or alongside implementation
- Use appropriate test frameworks for the language
- Test edge cases and error conditions
- Maintain test coverage for critical paths
- Tests go with implementation in atomic commits

## Documentation Workflow

- Update documentation when code changes
- Keep README and AGENT files current and accurate
- Document non-obvious design decisions
- Include examples for complex APIs

## Refactoring Workflow

- Refactor incrementally, not in big bangs
- Maintain test coverage during refactoring
- Preserve functionality while improving structure
- Document significant architectural changes
- E2E tests serve as confirmation gate for internal refactoring