# Exporting Reviews

Export reviews to markdown for documentation, sharing, or archival.

## Basic Export

```bash
# Export the most recent review
npx githuman export last

# Export a specific review by ID
npx githuman export abc123
```

## Save to File

```bash
# Save to a specific file
npx githuman export last -o review.md

# Save with a descriptive name
npx githuman export last -o reviews/feature-auth-review.md
```

## Export Format

The exported markdown includes:

- Review metadata (date, status, files)
- List of all changed files
- Inline comments and their status
- Suggestions and whether they were applied
- Associated todos

Example output:

```markdown
# Code Review - 2024-01-15

**Status**: Approved
**Files**: 5 changed

## Files Changed
- src/auth/login.ts
- src/auth/logout.ts
- tests/auth.test.ts

## Comments

### src/auth/login.ts:42
> Consider adding rate limiting here
Status: Resolved

### src/auth/login.ts:67
> Suggestion: Use optional chaining
Status: Applied
```

## Use Cases

1. **Documentation** - Keep a record of why changes were made
2. **Team sharing** - Share reviews with team members not using GitHuman
3. **Audit trail** - Maintain history of code review decisions
4. **Learning** - Review past feedback to improve code quality over time
