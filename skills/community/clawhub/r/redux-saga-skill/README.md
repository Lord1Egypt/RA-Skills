# Redux-Saga Skill

Created by **[Anivar Aravind](https://anivar.net)**

An AI agent skill for writing, testing, and debugging Redux-Saga code with modern best practices.

## The Problem

AI agents often generate outdated or incorrect redux-saga code — missing `yield` on effects, calling async functions directly instead of using `call()`, using `fork` inside `race`, or setting up root sagas that crash entirely when one watcher fails. These are subtle bugs that pass linting but break at runtime.

## This Solution

22 rules with incorrect→correct code examples that teach agents the actual redux-saga API behavior, fork model semantics, and modern Redux Toolkit integration patterns. Each rule targets a specific mistake and shows exactly how to fix it.

## Install

```bash
npx skills add anivar/redux-saga-skill -g
```

Or with full URL:

```bash
npx skills add https://github.com/anivar/redux-saga-skill
```

## Baseline

- redux-saga ^1.4.2
- @reduxjs/toolkit (recommended)
- redux-saga-test-plan ^5.x (for testing rules)
- Jest or Vitest

## What's Inside

### 22 Rules Across 7 Categories

| Priority | Category | Rules | Impact |
|----------|----------|-------|--------|
| 1 | Effects & Yielding | 5 | CRITICAL |
| 2 | Fork Model & Concurrency | 4 | CRITICAL |
| 3 | Error Handling | 2 | HIGH |
| 4 | Testing Patterns | 4 | HIGH |
| 5 | Recipes & Patterns | 3 | MEDIUM |
| 6 | Channels & External I/O | 2 | MEDIUM |
| 7 | RTK Integration | 2 | MEDIUM |

Each rule file contains:
- Why it matters
- Incorrect code with explanation
- Correct code with explanation
- Decision tables and additional context

### 7 Deep-Dive References

| Reference | Covers |
|-----------|--------|
| `effects-and-api.md` | All effect creators, blocking vs non-blocking, pattern matching |
| `fork-model.md` | Attached vs detached forks, error propagation, cancellation semantics |
| `testing.md` | expectSaga, testSaga, providers, matchers, reducer integration |
| `channels.md` | eventChannel, actionChannel, buffers, worker pools |
| `recipes.md` | Throttle, debounce, retry, polling, optimistic updates, batching |
| `anti-patterns.md` | 12 common mistakes with BAD/GOOD examples |
| `troubleshooting.md` | Frozen apps, missed actions, bad stack traces, TypeScript yield types |

## Structure

```
├── SKILL.md                          # Entry point for AI agents
├── AGENTS.md                         # Compiled guide with all rules expanded
├── rules/                            # Individual rules (Incorrect→Correct)
│   ├── effect-*                      # Effects & yielding (CRITICAL)
│   ├── fork-*                        # Fork model & concurrency (CRITICAL)
│   ├── error-*                       # Error handling (HIGH)
│   ├── testing-*                     # Testing patterns (HIGH)
│   ├── recipe-*                      # Common patterns (MEDIUM)
│   ├── channel-*                     # Channels & external I/O (MEDIUM)
│   ├── rtk-*                         # Redux Toolkit integration (MEDIUM)
│   └── troubleshoot-*               # Debugging (LOW)
└── references/                       # Deep-dive reference docs
    ├── effects-and-api.md
    ├── fork-model.md
    ├── testing.md
    ├── channels.md
    ├── recipes.md
    ├── anti-patterns.md
    └── troubleshooting.md
```

## Ecosystem — Skills by [Anivar Aravind](https://anivar.net)

### Testing Skills
| Skill | What it covers | Install |
|-------|---------------|---------|
| [jest-skill](https://github.com/anivar/jest-skill) | Jest best practices — mock design, async testing, matchers, timers, snapshots | `npx skills add anivar/jest-skill -g` |
| [redux-saga-testing](https://github.com/anivar/redux-saga-testing) | Redux-Saga testing — expectSaga, testSaga, providers | `npx skills add anivar/redux-saga-testing -g` |
| [zod-testing](https://github.com/anivar/zod-testing) | Zod schema testing — safeParse, mock data, property-based | `npx skills add anivar/zod-testing -g` |
| [msw-skill](https://github.com/anivar/msw-skill) | MSW 2.0 API mocking — handlers, responses, GraphQL | `npx skills add anivar/msw-skill -g` |

### Library & Framework Skills
| Skill | What it covers | Install |
|-------|---------------|---------|
| [zod-skill](https://github.com/anivar/zod-skill) | Zod v4 schema validation, parsing, error handling | `npx skills add anivar/zod-skill -g` |
| [msw-skill](https://github.com/anivar/msw-skill) | MSW 2.0 handlers, responses, migration | `npx skills add anivar/msw-skill -g` |

### Engineering Analysis
| Skill | What it covers | Install |
|-------|---------------|---------|
| [contributor-codebase-analyzer](https://github.com/anivar/contributor-codebase-analyzer) | Code analysis, annual reviews, promotion readiness | `npx skills add anivar/contributor-codebase-analyzer -g` |

## Author

**[Anivar Aravind](https://anivar.net)** — Building AI agent skills for modern JavaScript/TypeScript development.

## License

MIT
