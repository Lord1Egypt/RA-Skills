---
name: handling-flaky-changes
description: "Handles flaky or known visual changes in SnapVisor: ignores or un-ignores a change after confirmation, finds flaky tests, and lists the ignored changes for a project. Use when the user asks to 'ignore the date-widget change, it's the flaky clock again', 'which tests are flaky', 'stop flagging this change', 'un-ignore this change', 'show ignored changes', or deal with noisy screenshot diffs."
---

# Flaky and ignored changes in SnapVisor

Silence a single known-noisy change so it stops blocking a build, undo that when needed, and show which tests flake most. Ignoring affects one change; every other diff in the build stays as it is.

## Connecting and calling the tools

Every operation in this skill comes from the `snapvisor` MCP server, the SnapVisor connector. The server defaults to Code Mode, so the operations below are written as the `external_*` functions you call inside `snapvisor:execute_typescript`. On a server set to the per-tool surface, the same operation is listed as `snapvisor:<name>` without the `external_` prefix, for example `snapvisor:listBuilds`.

- **Only `snapvisor:search_tools` and `snapvisor:execute_typescript` listed (Code Mode, the default):** call `snapvisor:search_tools` first, then call each tool inside `snapvisor:execute_typescript` as `external_<tool>` (for example `external_listBuilds`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **Operations listed by name:** call them directly, for example `snapvisor:listBuilds`.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `snapvisor:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects SnapVisor and approves that scope.
- **No `snapvisor` tools at all:** SnapVisor is not connected yet. Install the SnapVisor power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

The `snapvisor` MCP server has two tools: `snapvisor:search_tools` (find operations and their inputs; call it first, for example with `change`, `test`, `ignore`) and `snapvisor:execute_typescript` (run a short program calling the declared `external_*` functions, which are already in scope; the program must `return` its result).

If the connection lists the operations by name instead (the per-tool surface), call them directly without the `external_` prefix.

Operations this skill uses (confirm with `snapvisor:search_tools`):

- `external_listBuildDiffs`: diffs in a build; each carries its `test` and its `change`, whose id is what the ignore operations take.
- `external_ignoreChange` and `external_unignoreChange`: mark one change ignored or restore it, by `changeId`.
- `external_listTests`: tests in a project.
- `external_getTest`: one test with its flakiness metrics for a `metricsPeriod` (`LAST_24_HOURS` up to `LAST_90_DAYS`).
- `external_listTestChanges`: a test's changes; filter with `ignored`.
- `external_listIgnoredChanges`: changes currently ignored in a project.

## Workflow

1. Identify the build and the change the user means. Call `external_listBuildDiffs` and match on the screenshot `name`. If more than one diff matches, list them and ask which one.
2. Before ignoring, fetch `external_getTest` for that diff's test with `metricsPeriod: "LAST_30_DAYS"` so the user sees whether it really flakes.
3. Confirm: "Ignore the change on `checkout/date-widget` in build 42?" On a yes, call `external_ignoreChange` with the change id and report the result.
4. To un-ignore, find the change with `external_listIgnoredChanges` or `external_listTestChanges` with `ignored: "true"`, confirm, then call `external_unignoreChange`.
5. For "which tests are flaky", list the project's tests, fetch `external_getTest` for them in one program with `await Promise.all`, and return them sorted by their flakiness metric. Report the top ones with their numbers.

## Code Mode pattern

```ts
const tests = await external_listTests({ owner, project });
const detail = await Promise.all(
  tests.results.slice(0, 25).map((t) =>
    external_getTest({ owner, project, testId: t.id, metricsPeriod: "LAST_30_DAYS" })
      .catch((e) => ({ id: t.id, error: String(e) })),
  ),
);
return detail;
```

Check the real field names in the `snapvisor:search_tools` declarations before relying on them. Errors read `<CODE>: <details>`.

## Rules

- Ignore one change at a time, each after a confirmation. Never ignore every diff in a build to make it pass.
- Do not approve or reject builds from this skill; hand off to `reviewing-visual-builds`.
- Report only metrics the operations returned. If a test has no flakiness data for the period, say so.
