# Redux-Saga Testing

Created by **[Anivar Aravind](https://anivar.net)**

An AI agent skill for writing tests for Redux Sagas using redux-saga-test-plan. Works with Jest and Vitest.

## The Problem

AI agents often write saga tests that are brittle (asserting exact effect order when it doesn't matter), miss provider setup (causing tests to hit real APIs), or use manual generator stepping when `expectSaga` would be simpler and more maintainable. The result: tests that break on harmless refactors and pass when they shouldn't.

## This Solution

A focused testing skill covering `expectSaga` (integration), `testSaga` (unit), providers, matchers, and reducer integration — with 12 anti-patterns showing exactly what goes wrong and how to fix it.

## Install

```bash
npx skills add anivar/redux-saga-testing -g
```

Or with full URL:

```bash
npx skills add https://github.com/anivar/redux-saga-testing
```

## Baseline

- redux-saga-test-plan ^5.x
- redux-saga ^1.4.2
- Jest or Vitest

## What's Inside

### Testing Approaches

| Approach | Type | Use When |
|----------|------|----------|
| `expectSaga` | Integration | Default choice — order-independent, async, assertions on effects and state |
| `testSaga` | Unit | Effect ordering matters (e.g., must `select` before `call`) |
| `runSaga` | Manual | Need full store integration or custom middleware |

### Providers

| Provider Type | Purpose |
|---------------|---------|
| Static providers | Map effect → return value (simple, covers most cases) |
| Dynamic providers | Custom logic per effect type (conditional mocking) |
| Partial matchers | `matchers.call.fn(apiFn)` — match by function regardless of args |

### Anti-Patterns

12 common testing mistakes with BAD/GOOD code examples:
- Asserting effect order in integration tests
- Missing providers for API calls
- Not awaiting `expectSaga` (test always passes)
- Testing implementation instead of behavior
- Ignoring error paths and cancellation

## Structure

```
├── SKILL.md                      # Entry point for AI agents
└── references/
    ├── api-reference.md          # Complete expectSaga, testSaga, providers, matchers API
    └── anti-patterns.md          # 12 common testing mistakes to avoid
```

## Ecosystem — Skills by [Anivar Aravind](https://anivar.net)

### Testing Skills
| Skill | What it covers | Install |
|-------|---------------|---------|
| [jest-skill](https://github.com/anivar/jest-skill) | Jest best practices — mock design, async testing, matchers, timers, snapshots | `npx skills add anivar/jest-skill -g` |
| [zod-testing](https://github.com/anivar/zod-testing) | Zod schema testing — safeParse, mock data, property-based | `npx skills add anivar/zod-testing -g` |
| [msw-skill](https://github.com/anivar/msw-skill) | MSW 2.0 API mocking — handlers, responses, GraphQL | `npx skills add anivar/msw-skill -g` |

### Library & Framework Skills
| Skill | What it covers | Install |
|-------|---------------|---------|
| [zod-skill](https://github.com/anivar/zod-skill) | Zod v4 schema validation, parsing, error handling | `npx skills add anivar/zod-skill -g` |
| [redux-saga-skill](https://github.com/anivar/redux-saga-skill) | Redux-Saga effects, fork model, channels, RTK | `npx skills add anivar/redux-saga-skill -g` |
| [msw-skill](https://github.com/anivar/msw-skill) | MSW 2.0 handlers, responses, migration | `npx skills add anivar/msw-skill -g` |

### Engineering Analysis
| Skill | What it covers | Install |
|-------|---------------|---------|
| [contributor-codebase-analyzer](https://github.com/anivar/contributor-codebase-analyzer) | Code analysis, annual reviews, promotion readiness | `npx skills add anivar/contributor-codebase-analyzer -g` |

## Author

**[Anivar Aravind](https://anivar.net)** — Building AI agent skills for modern JavaScript/TypeScript development.

## License

MIT
