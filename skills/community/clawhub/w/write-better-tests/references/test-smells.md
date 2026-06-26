# Test Smell Reference

Use this when reviewing tests that appear to pass too easily.

## Fast Smell Checks

- Could the old bug still exist while this test passes?
- Is the expected value copied from the new implementation rather than derived from the product contract?
- Does the test mock the boundary it claims to verify?
- Does the test assert helper calls instead of observable behavior?
- Does the fixture contain only the happy path created for this patch?
- Is the assertion weaker than the bug? For example, "returns an array" for a ranking, auth, filtering, or persistence regression.
- Would a maintainer understand the regression from the test name and assertions without reading the PR?
- Did the test fail at least once for the right reason during development?

## Common Anti-Patterns

### Mocking the subject

Bad pattern:

```ts
vi.mock("../search", () => ({
  searchPackages: vi.fn(() => expectedResults),
}));

expect(await renderSearch("foo")).toContain("foo");
```

This proves the mock, not the search behavior.

Better pattern: seed or construct realistic records, call the real search/ranking/filtering boundary, and assert the result ordering or inclusion contract.

### Helper echo

Bad pattern:

```ts
const expected = normalizePackage(input);
expect(await loadPackage(input)).toEqual(expected);
```

If `normalizePackage` is also used by `loadPackage`, the test repeats the implementation. Expected values should be written from the contract or from independent fixtures.

### Snapshot fog

Snapshots are acceptable for stable, broad rendering guardrails, but they are weak for bug fixes. If the change fixes auth, moderation, filtering, counts, config, CLI output, or persistence, assert that behavior directly.

### No-failure assertions

`not.toThrow`, `toBeTruthy`, and "renders without crashing" are useful smoke checks only. They do not prove a concrete regression unless the bug was exactly a crash and the test asserts the triggering input.

## Red-Green Proof Options

Use the cheapest credible proof:

- Run the new test on the parent commit or pre-fix worktree.
- Temporarily revert the implementation hunk, run the test, then restore it.
- Temporarily inject the old condition, stale value, missing guard, or wrong branch and confirm the test fails.
- For CLI/config/filesystem work, run against a temp home that reproduces the old state.

If red proof is not practical because the change is pure refactor, docs-only, or the old environment cannot be reconstructed cheaply, say so and explain what alternative proof was used.

## Strong Regression Shapes

- Bug fix: one test for the failing input and one adjacent non-regression case when the boundary is subtle.
- Security or auth: allowed and denied cases; assert no secret/path/token leakage where relevant.
- Search/filter/ranking: include competing records that would expose wrong inclusion, ordering, or source priority.
- Pagination/counts: include `limit + 1`, empty, exact limit, and overflow when that is the contract.
- CLI/config: use temp directories, explicit environment, and exact stdout/stderr/exit-code assertions only where the CLI contract requires exactness.
- Persistence/migration: assert both written data and read-back behavior, not just that a function was called.
