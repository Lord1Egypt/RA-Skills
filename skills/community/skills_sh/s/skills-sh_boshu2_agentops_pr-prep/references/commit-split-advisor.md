# Commit Split Advisor

Guidelines for splitting a PR into logical, well-ordered commits.

## Commit Ordering Rules

Apply commits in this order (earlier layers first):

1. **Infrastructure / migrations** -- schema changes, config files, build system
2. **Models / services** -- domain logic, data structures, shared libraries
3. **Controllers / views** -- API endpoints, CLI commands, UI components
4. **Tests** -- test files that pair with the code in the same commit (see below)
5. **VERSION / CHANGELOG** -- version bumps, release notes, documentation updates

## Key Principles

### Each Commit Must Be Independently Valid

- No broken imports -- every file referenced must exist at that point in history.
- The project must build (and ideally pass tests) after each commit.
- If a model and its test are tightly coupled, they belong in the **same** commit.

### Small Diffs Get a Single Commit

If the total diff is **< 50 lines** across **< 4 files**, a single commit is fine.
Splitting a tiny change into multiple commits adds noise without clarity.

### Grouping Heuristics

- A new struct/type and its unit test go together.
- A migration and the code that depends on the new schema go together.
- Pure refactors (renames, moves) are their own commit, separate from behavior changes.
- Formatting / lint fixes are their own commit, never mixed with logic.

## Output Format

When suggesting a split, produce a numbered list:

```
Commit 1: Add user model and migration
  files: db/migrations/003_users.sql, models/user.go, models/user_test.go

Commit 2: Add user API endpoints
  files: handlers/user.go, handlers/user_test.go, routes.go

Commit 3: Update CHANGELOG
  files: CHANGELOG.md, VERSION
```

Each entry names the commit message and lists the files that belong in it.
