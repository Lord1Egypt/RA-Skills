# Release Note Style

Use this reference after collecting Git history and before drafting final release notes.

## Default Structure

```markdown
# Release Notes: <version or range>

Date: <date if known>
Range: `<from>..<to>`

## Highlights

- <Most important user-facing outcome>

## Added

- <New capability or supported workflow>

## Changed

- <Behavior, UX, performance, or compatibility change>

## Fixed

- <Bug fix with user impact>

## Removed

- <Removed feature, deprecated path, or cleanup with user impact>

## Security

- <Security-relevant fix or hardening>

## Developer Notes

- <Build, test, dependency, API, or internal change useful to maintainers>

## Upgrade Notes

- <Breaking change, migration, config change, or action required>
```

Omit empty sections unless the user asks for a complete changelog template.

## Categorization

- Prefer "Added" for new features, commands, endpoints, UI controls, docs pages, or supported platforms.
- Prefer "Changed" for renamed behavior, refactors with visible impact, performance changes, dependency updates, and compatibility changes.
- Prefer "Fixed" for bug fixes, regressions, crashes, incorrect output, flaky workflows, or data-loss prevention.
- Prefer "Removed" for deleted features, flags, endpoints, files, config keys, or deprecated compatibility paths.
- Prefer "Security" only for explicit security fixes or defensive hardening.
- Prefer "Developer Notes" for tests, CI, linting, build tooling, internal refactors, and maintenance-only changes.

## Writing Rules

- Write for users first, maintainers second.
- Start bullets with strong verbs.
- Collapse noisy commit sequences such as "fix lint", "address review", and "wip" into the actual shipped change.
- Preserve precise names for commands, flags, files, APIs, and config keys.
- Mention uncertainty directly when commit messages are unclear.
- Do not invent impact that is not supported by commits, diffs, or files.
