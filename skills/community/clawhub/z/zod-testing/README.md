# Zod Testing

Created by **[Anivar Aravind](https://anivar.net)**

An AI agent skill for testing Zod schemas with Jest and Vitest.

## The Problem

AI agents often write schema tests that only check the happy path, use `parse()` instead of `safeParse()` (crashing instead of failing), test schema internals (`.shape`, `._def`) instead of behavior, or hardcode mock data instead of generating it from the schema. The result: tests that miss regressions and break on harmless refactors.

## This Solution

A focused testing skill covering schema correctness testing, error assertion patterns, mock data generation, snapshot testing with `z.toJSONSchema()`, property-based testing, structural testing, and drift detection — with 14 anti-patterns showing exactly what goes wrong and how to fix it.

## Install

```bash
npx skills add anivar/zod-testing -g
```

Or with full URL:

```bash
npx skills add https://github.com/anivar/zod-testing
```

## Baseline

- zod ^4.0.0
- Jest or Vitest
- TypeScript ^5.5

## What's Inside

### Testing Approaches

| Approach | Type | Use When |
|----------|------|----------|
| `safeParse()` result checking | Correctness | Default — always use safeParse in tests |
| `z.flattenError()` assertions | Error messages | Verifying specific field errors |
| `z.toJSONSchema()` snapshots | Schema shape | Detecting unintended schema changes |
| Mock data generation | Fixtures | Need valid/randomized test data |
| Property-based testing | Fuzz testing | Schemas must handle arbitrary valid inputs |
| Structural testing | Architecture | Verify schemas are only imported at boundaries |
| Drift detection | Regression | Catch unintended schema changes via JSON Schema snapshots |

### Anti-Patterns

14 common testing mistakes with BAD/GOOD code examples:
- Testing schema internals instead of behavior
- Not testing error paths (only happy path)
- Using `parse()` in tests (crashes instead of failing)
- Not testing boundary values (min/max edges)
- Hardcoding mock data instead of generating from schema
- Snapshot testing raw ZodError instead of formatted output
- Not seeding random data generators (flaky tests)
- Not testing at boundaries (schema tests pass but handler doesn't validate)
- No snapshot regression testing (field removal goes unnoticed)
- Testing schema shape but not error observability
- No drift detection workflow (schema changes land without review)

## Structure

```
├── SKILL.md                      # Entry point for AI agents
└── references/
    ├── api-reference.md          # Testing patterns, assertion helpers, mock generation
    └── anti-patterns.md          # Common testing mistakes to avoid
```

## Ecosystem — Skills by [Anivar Aravind](https://anivar.net)

### Testing Skills
| Skill | What it covers | Install |
|-------|---------------|---------|
| [jest-skill](https://github.com/anivar/jest-skill) | Jest best practices — mock design, async testing, matchers, timers, snapshots | `npx skills add anivar/jest-skill -g` |
| [msw-skill](https://github.com/anivar/msw-skill) | MSW 2.0 API mocking — handlers, responses, GraphQL | `npx skills add anivar/msw-skill -g` |
| [redux-saga-testing](https://github.com/anivar/redux-saga-testing) | Redux-Saga testing — expectSaga, testSaga, providers | `npx skills add anivar/redux-saga-testing -g` |

### Library & Framework Skills
| Skill | What it covers | Install |
|-------|---------------|---------|
| [zod-skill](https://github.com/anivar/zod-skill) | Zod v4 schema validation, parsing, error handling | `npx skills add anivar/zod-skill -g` |
| [redux-saga-skill](https://github.com/anivar/redux-saga-skill) | Redux-Saga effects, fork model, channels, RTK | `npx skills add anivar/redux-saga-skill -g` |

### Engineering Analysis
| Skill | What it covers | Install |
|-------|---------------|---------|
| [contributor-codebase-analyzer](https://github.com/anivar/contributor-codebase-analyzer) | Code analysis, annual reviews, promotion readiness | `npx skills add anivar/contributor-codebase-analyzer -g` |

## Author

**[Anivar Aravind](https://anivar.net)** — Building AI agent skills for modern JavaScript/TypeScript development.

## License

MIT
