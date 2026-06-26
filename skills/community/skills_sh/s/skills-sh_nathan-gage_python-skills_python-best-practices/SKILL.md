---
name: python-best-practices
description: Python software engineering guidelines from real PR review patterns. This skill should be used when writing, reviewing, or refactoring Python code — especially dataclasses, service interfaces, error handling, and type annotations. Triggers on tasks involving Python modules, API design, data modeling, type safety, exception handling, or refactoring for maintainability.
license: MIT
metadata:
  author: python-best-practices
  version: "1.3.0"
  pythonVersion: ">=3.11"
---

# Python Best Practices

Guidelines for writing and reviewing Python. 70 rules across 8 categories, prioritized by impact.

A rule match is a signal, not a verdict. Most rules are design preferences for new code, not bugs to fix across the repo — check the rule's impact level before flagging in review or refactoring stable code.

## When to Apply

- Writing new Python modules, functions, classes, or data models
- Reviewing code for correctness or type safety
- Refactoring patterns in code that's being edited anyway

Avoid applying these rules as a blanket sweep across stable code — the churn rarely pays off.

## Impact Levels

- `CRITICAL` — prevents a real bug class (data corruption, swallowed cancellations, insecure defaults). Fix when found.
- `HIGH` — meaningful correctness or maintainability win. Worth fixing in most contexts.
- `MEDIUM` — good practice; clarity or drift prevention. Apply to new code; don't churn stable code.
- `LOW-MEDIUM` / `LOW` — style or micro-optimizations. Apply opportunistically.

## Python Version Baseline

Rules assume Python 3.11+. Rules depending on higher versions call it out inline:

- `warnings.deprecated()` — 3.13+
- `zoneinfo` — 3.9+
- Union types in `isinstance()` — 3.10+
- `assert_never` — 3.11+ (backport via `typing_extensions`)

Rules tagged `applicability:pydantic` are Pydantic-specific.

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Data Modeling | HIGH | `data-` |
| 2 | Error Handling | MEDIUM-HIGH | `error-` |
| 3 | Type Safety | MEDIUM-HIGH | `types-` |
| 4 | API Design | MEDIUM | `api-` |
| 5 | Code Simplification | LOW-MEDIUM | `simplify-` |
| 6 | Performance | LOW-MEDIUM | `perf-` |
| 7 | Naming | LOW-MEDIUM | `naming-` |
| 8 | Imports & Structure | LOW | `imports-` |

Section impact is a typical-case label; individual rules range one level above or below — check the rule file.

## Quick Reference

### Data Modeling (`data-`)

- `data-mutable-defaults` — Never `def f(items=[])`; use `None` + body construction or `default_factory`
- `data-derive-dont-store` — Compute booleans from state; don't cache flags that mirror each other
- `data-mutation-contract` — Mutate OR return; not both
- `data-aware-datetimes` — Timezone-aware `datetime.now(timezone.utc)`; `utcnow()` is deprecated
- `data-discriminated-unions` — Tag variants instead of optional-field bags
- `data-explicit-variants` — Concrete classes per mode beat `is_thread` / `is_edit` flags
- `data-phased-composition` — Group co-present optionals into one nested optional
- `data-encapsulate-mutable-state` — Trap mutable state in the narrowest clear scope
- `data-sentinel-when-none-is-valid` — Private sentinel when `None` is a meaningful value
- `data-newtype-for-ids` — `NewType('UserId', str)` so IDs aren't interchangeable
- `data-delete-dead-variants` — Remove union arms that aren't constructed

### Error Handling (`error-`)

- `error-specific-exceptions` — Catch specific types; never bare `except:` or `except BaseException:` (breaks Ctrl-C and async cancellation); `except Exception:` is cancellation-safe on 3.8+
- `error-context-managers` — `with` / `async with` for files, locks, sessions
- `error-assert-debug-only` — `assert` vanishes under `-O`; not for runtime contracts
- `error-validate-at-boundaries` — Fail fast at system edges before expensive work
- `error-trust-validated-state` — Trust immutable, locally-constructed state
- `error-consolidate-try-except` — Merge blocks with the same catch and handling
- `error-assert-never-exhaustiveness` — `typing.assert_never` for exhaustiveness
- `error-raise-from-for-chains` — `raise NewErr(...) from original` to preserve causality
- `error-inherit-base-exceptions` — New exceptions inherit existing bases for compatibility
- `error-log-exception-context` — `logger.exception(...)` inside `except`; keep the traceback in the log
- `error-repr-in-messages` — `f"tool {name!r}"` for identifiers in error text

### Type Safety (`types-`)

- `types-fix-errors-not-ignore` — Fix type errors; `# type: ignore` is a last resort
- `types-avoid-any` — Protocols, TypeVars, unions over `Any`
- `types-typeddict-over-dict-any` — `TypedDict` / dataclass when structure is known
- `types-literal-for-fixed-sets` — `Literal["a", "b"]` for fixed strings
- `types-fix-types-not-cast` — Fix the definition; `cast()` only when runtime genuinely narrows
- `types-isinstance-for-narrowing` — `isinstance()` over `hasattr` / `type(x).__name__`
- `types-narrow-to-runtime-reality` — Annotations match what control flow actually allows
- `types-trust-the-checker` — Drop runtime checks the types already enforce
- `types-remove-redundant-optional` — Drop `| None` when values are guaranteed present
- `types-type-checking-imports` — `if TYPE_CHECKING:` for optional or heavy imports

### API Design (`api-`)

- `api-required-before-optional` — Required fields before optional (Python enforces this)
- `api-keyword-only-params` — `*` marker for optional/config params
- `api-no-boolean-flag-params` — `Literal` / `Enum` over `True, False` soup
- `api-immutable-transforms` — Return new collections; don't mutate inputs
- `api-model-cohesion` — Flat models; no duplicate or single-key-wrapped fields
- `api-underscore-for-private` — `_prefix` for internals; exclude from `__all__`
- `api-deprecated-aliases` — `warnings.deprecated()` (3.13+) for renamed APIs
- `api-no-private-access` — Don't reach into `_prefixed` names from outside the module
- `api-instance-vs-module-fn` — Pick the namespace that matches ownership

### Code Simplification (`simplify-`)

- `simplify-early-return` — Return early; don't nest the happy path
- `simplify-extract-after-duplication` — Second copy is the decision point; third is the safe default
- `simplify-cached-property` — `@cached_property` on immutable instances; not thread-safe
- `simplify-comprehensions` — Comprehensions over `for` + `.append()`
- `simplify-any-all-builtins` — `any()` / `all()` over manual flag + `break`
- `simplify-fallback-or` — `x or default` when falsy values aren't semantic
- `simplify-flatten-nested-if` — `if cond1 and cond2:` when no intervening code
- `simplify-inline-single-use-vars` — Drop intermediates used once
- `simplify-remove-dead-code` — Delete commented-out code; git preserves history

### Performance (`perf-`)

- `perf-set-for-membership` — `set` for repeated `in` checks
- `perf-dict-index-over-nested-loops` — Build a `dict` for lookups
- `perf-lru-cache-pure-fns` — `functools.lru_cache` / `functools.cache` on pure functions
- `perf-generator-over-list` — Stream with generators when memory or latency matters
- `perf-combine-iterations` — Fuse `filter` + `map` into one pass
- `perf-compile-regex-module-level` — Compile static regex at module scope; matters in tight loops
- `perf-type-adapter-constant` — Module-scope `TypeAdapter` *(applicability: pydantic)*
- `perf-isinstance-tuple-syntax` — Tuple form is marginally faster; profiled hot paths only

### Naming (`naming-`)

- `naming-rename-on-behavior-change` — Rename when behavior changes; stale names mislead
- `naming-consistent-terminology` — Same concept, same word across code/docs/errors
- `naming-specific-over-generic` — `toolset_id`; not bare `id`
- `naming-drop-redundant-prefixes` — `ToolConfig.description`; not `ToolConfig.tool_description`
- `naming-upper-case-constants` — `MAX_RETRIES`; `_` prefix for internal
- `naming-no-type-suffixes` — No `_dict` / `_list` suffixes; types annotate types

### Imports & Structure (`imports-`)

- `imports-no-side-effects` — Modules must be cheap to import — no network/model/env reads at import
- `imports-top-of-file` — Imports at the top; documented exceptions for circular / optional / deferred
- `imports-optional-dependencies` — `try` / `except ImportError` with install hints
- `imports-scope-helpers-to-usage` — Define helpers near where they're used
- `imports-remove-unused` — Delete unused imports
- `imports-no-duplicates` — One import per name

## How to Use

Read individual rule files for detail:

```
rules/data-mutable-defaults.md
rules/error-specific-exceptions.md
```

Each rule has:

- Impact level in frontmatter
- Brief explanation
- Incorrect example
- Correct example
- Optional note on edge cases

For the full compiled guide with all rules expanded: `AGENTS.md`.
