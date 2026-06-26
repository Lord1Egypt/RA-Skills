# Zod Skill

Created by **[Anivar Aravind](https://anivar.net)**

An AI agent skill for writing, validating, and debugging Zod v4 schemas with modern best practices.

## The Problem

AI agents often generate outdated Zod v3 patterns — `z.string().email()` instead of `z.email()`, `z.nativeEnum()` instead of `z.enum()`, `required_error` instead of the `error` parameter — and miss critical parsing pitfalls like using `parse()` instead of `safeParse()`, forgetting `parseAsync` for async refinements, or assuming `z.object()` preserves unknown keys. These produce schemas that compile but silently misbehave at runtime.

## This Solution

27 rules with incorrect→correct code examples that teach agents Zod v4's actual API behavior, schema design patterns, error handling, architectural placement, observability, and TypeScript integration. Each rule targets a specific mistake and shows exactly how to fix it.

## Install

```bash
npx skills add anivar/zod-skill -g
```

Or with full URL:

```bash
npx skills add https://github.com/anivar/zod-skill
```

## Baseline

- zod ^4.0.0
- TypeScript ^5.5

## What's Inside

### 27 Rules Across 9 Categories

| Priority | Category | Rules | Impact |
|----------|----------|-------|--------|
| 1 | Parsing & Type Safety | 3 | CRITICAL |
| 2 | Schema Design | 4 | CRITICAL |
| 3 | Refinements & Transforms | 3 | HIGH |
| 4 | Error Handling | 3 | HIGH |
| 5 | Performance & Composition | 3 | MEDIUM |
| 6 | v4 Migration | 3 | MEDIUM |
| 7 | Advanced Patterns | 3 | MEDIUM |
| 8 | Architecture & Boundaries | 3 | CRITICAL/HIGH |
| 9 | Observability | 2 | HIGH/MEDIUM |

Each rule file contains:
- Why it matters
- Incorrect code with explanation
- Correct code with explanation
- Decision tables and additional context

### 9 Deep-Dive References

| Reference | Covers |
|-----------|--------|
| `schema-types.md` | All primitives, string formats, numbers, enums, dates, files, JSON |
| `parsing-and-inference.md` | parse, safeParse, parseAsync, z.infer, z.input, coercion |
| `objects-and-composition.md` | object/strict/loose, pick, omit, partial, recursive, unions, tuples |
| `refinements-and-transforms.md` | refine, superRefine, transform, pipe, defaults, catch |
| `error-handling.md` | ZodError, flattenError, treeifyError, error customization, i18n |
| `advanced-features.md` | Codecs, branded types, JSON Schema, registries, Standard Schema |
| `anti-patterns.md` | 14 common mistakes with BAD/GOOD examples |
| `boundary-architecture.md` | Where Zod fits: Express, tRPC, Next.js, React Hook Form, env, external APIs |
| `linter-and-ci.md` | ESLint rules, CI schema snapshots, unused schema detection, circular deps |

## Structure

```
├── SKILL.md                          # Entry point for AI agents
├── AGENTS.md                         # Compiled guide with all rules expanded
├── rules/                            # Individual rules (Incorrect→Correct)
│   ├── parse-*                       # Parsing & type safety (CRITICAL)
│   ├── schema-*                      # Schema design (CRITICAL)
│   ├── refine-*                      # Refinements & transforms (HIGH)
│   ├── error-*                       # Error handling (HIGH)
│   ├── perf-*                        # Performance & composition (MEDIUM)
│   ├── migrate-*                     # v4 migration (MEDIUM)
│   ├── pattern-*                     # Advanced patterns (MEDIUM)
│   ├── arch-*                        # Architecture & boundaries (CRITICAL/HIGH)
│   └── observe-*                     # Observability (HIGH/MEDIUM)
└── references/                       # Deep-dive reference docs
    ├── schema-types.md
    ├── parsing-and-inference.md
    ├── objects-and-composition.md
    ├── refinements-and-transforms.md
    ├── error-handling.md
    ├── advanced-features.md
    ├── anti-patterns.md
    ├── boundary-architecture.md
    └── linter-and-ci.md
```

## Ecosystem — Skills by [Anivar Aravind](https://anivar.net)

### Testing Skills
| Skill | What it covers | Install |
|-------|---------------|---------|
| [jest-skill](https://github.com/anivar/jest-skill) | Jest best practices — mock design, async testing, matchers, timers, snapshots | `npx skills add anivar/jest-skill -g` |
| [zod-testing](https://github.com/anivar/zod-testing) | Zod schema testing — safeParse, mock data, property-based | `npx skills add anivar/zod-testing -g` |
| [msw-skill](https://github.com/anivar/msw-skill) | MSW 2.0 API mocking — handlers, responses, GraphQL | `npx skills add anivar/msw-skill -g` |
| [redux-saga-testing](https://github.com/anivar/redux-saga-testing) | Redux-Saga testing — expectSaga, testSaga, providers | `npx skills add anivar/redux-saga-testing -g` |

### Library & Framework Skills
| Skill | What it covers | Install |
|-------|---------------|---------|
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
