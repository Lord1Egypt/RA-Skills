---
name: pr-review
description: Comprehensive pull request review covering code quality, security, performance, and maintainability. Use for any code review task.
triggers:
  - review PR
  - code review
  - review changes
  - review diff
---

# Pull Request Review

Perform a thorough code review covering quality, security, performance, and maintainability.

## Review Checklist

### Code Quality
- Naming: clear, descriptive, consistent with codebase conventions
- Functions: single responsibility, reasonable length (<50 lines)
- Error handling: all failure paths covered, no swallowed exceptions
- Types: proper TypeScript/type annotations where applicable
- DRY: no unnecessary duplication
- Dead code: nothing unused or commented out

### Security (see also: security-review skill)
- No secrets or credentials in code
- Input validation on all user-facing endpoints
- Parameterized queries (no string concatenation for SQL)
- Proper auth/authz checks

### Performance
- N+1 query patterns
- Missing database indexes for new queries
- Unbounded loops or recursive calls
- Large payload responses without pagination
- Missing caching where appropriate

### Testing
- New functionality has tests
- Edge cases covered (empty arrays, null, boundaries)
- Tests are deterministic (no timing dependencies)
- Mocks are appropriate (not over-mocked)

### Maintainability
- Changes are documented (README, comments for complex logic)
- Breaking changes are noted
- Migration path is clear for schema changes
- Dependencies added are justified

## Output Format

Start with a summary:
```
## Review Summary
**Verdict:** APPROVE | REQUEST_CHANGES | COMMENT
**Risk Level:** Low | Medium | High
**Key Findings:** [1-3 sentence summary]
```

Then list findings by category, each with:
- File and line reference
- What the issue is
- Suggested fix (with code when helpful)
- Severity (blocking vs. nit)

End with:
```
## Positive Notes
[Things done well worth calling out]
```
