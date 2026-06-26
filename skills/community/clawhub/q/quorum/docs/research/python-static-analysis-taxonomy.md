# Python Static Analysis Rule Taxonomy: Ruff + Pylint

> **Purpose:** Map the complete deterministic rule space of Ruff and Pylint against code quality dimensions. Understand what linters DO cover, what they DON'T cover, and which rules are most relevant to agentic/AI-generated code quality.
>
> **Sources:** `docs.astral.sh/ruff/rules/` · `pylint.readthedocs.io/en/stable/user_guide/checkers/features.html` · Ruff GitHub
>
> **Date:** March 2026 · **Ruff Version:** 0.9.x (900+ rules) · **Pylint Version:** 4.0.x

---

## Table of Contents

1. [Quality Dimensions Reference](#1-quality-dimensions-reference)
2. [Ruff Rule Taxonomy](#2-ruff-rule-taxonomy)
   - [Rule Categories Summary Table](#21-ruff-rule-categories-summary-table)
   - [Category Deep-Dives](#22-ruff-category-deep-dives)
3. [Pylint Rule Taxonomy](#3-pylint-rule-taxonomy)
   - [Message Category System](#31-pylint-message-category-system)
   - [Checker Modules](#32-pylint-checker-modules-summary)
4. [Quality Dimension Coverage Matrix](#4-quality-dimension-coverage-matrix)
5. [Code Hygiene Priority Rules](#5-code-hygiene-priority-rules)
6. [Agentic/AI Code Relevance](#6-agenticai-code-relevance)
7. [Coverage Gaps: What Deterministic Tools Can't Catch](#7-coverage-gaps)

---

## 1. Quality Dimensions Reference

These five dimensions are used throughout to classify rules:

| Dimension | Definition | Example Violations |
|-----------|-----------|-------------------|
| **Reliability** | Code behaves correctly and predictably | Mutable defaults, bare exceptions, undefined names |
| **Maintainability** | Code is readable, understandable, modifiable | Missing docstrings, too-complex functions, dead code |
| **Security** | Code resists attack, avoids unsafe patterns | Hardcoded credentials, SQL injection, insecure crypto |
| **Performance** | Code uses resources efficiently | Unnecessary comprehensions, blocking async calls |
| **Style** | Code follows consistent conventions | Naming, formatting, import order |

---

## 2. Ruff Rule Taxonomy

Ruff currently supports **over 900 lint rules** reimplemented in Rust. Rules are identified by prefix codes. Default enabled rules: `E`, `F` (plus subset).

### 2.1 Ruff Rule Categories Summary Table

| Prefix | Plugin Origin | ~Rules | Primary Dimension | Hygiene Priority |
|--------|--------------|--------|-------------------|-----------------|
| **E** | pycodestyle (errors) | ~170 | Style | Low–Medium |
| **W** | pycodestyle (warnings) | ~50 | Style | Low |
| **F** | Pyflakes | ~100 | Reliability | **🔴 HIGH** |
| **I** | isort | 3 | Style | Low |
| **N** | pep8-naming | 13 | Style | Low–Medium |
| **D** | pydocstyle | ~50 | Maintainability | Medium |
| **UP** | pyupgrade | ~50 | Maintainability | Low–Medium |
| **B** | flake8-bugbear | ~35 | Reliability | **🔴 HIGH** |
| **C4** | flake8-comprehensions | 20 | Performance / Style | Low–Medium |
| **S** | flake8-bandit | ~65 | **Security** | **🔴 HIGH** |
| **A** | flake8-builtins | 6 | Reliability | Medium |
| **ANN** | flake8-annotations | 9 | Maintainability | Medium |
| **ARG** | flake8-unused-arguments | 5 | Maintainability | Medium |
| **ASYNC** | flake8-async | 15 | Reliability / Performance | **🔴 HIGH** |
| **BLE** | flake8-blind-except | 1 | Reliability | **🔴 HIGH** |
| **COM** | flake8-commas | 3 | Style | Low |
| **CPY** | flake8-copyright | 1 | Maintainability | Low |
| **DTZ** | flake8-datetimez | 10 | Reliability | Medium |
| **DJ** | flake8-django | 7 | Reliability / Security | Medium |
| **EM** | flake8-errmsg | 3 | Maintainability | Low |
| **ERA** | eradicate | 1 | Maintainability | Low |
| **EXE** | flake8-executable | 5 | Reliability | Low |
| **FA** | flake8-future-annotations | 2 | Style | Low |
| **FAST** | FastAPI | 3 | Reliability | Medium |
| **FBT** | flake8-boolean-trap | 3 | Maintainability | Medium |
| **FIX** | flake8-fixme | 4 | Maintainability | Low |
| **FLY** | flynt | 1 | Style | Low |
| **G** | flake8-logging-format | 8 | Performance / Maintainability | Medium |
| **ICN** | flake8-import-conventions | 3 | Style | Low |
| **INP** | flake8-no-pep420 | 1 | Reliability | Low |
| **INT** | flake8-gettext | 3 | Reliability | Low |
| **ISC** | flake8-implicit-str-concat | 4 | Reliability | Medium |
| **LOG** | flake8-logging | 7 | Reliability / Maintainability | **🔴 HIGH** |
| **N** | pep8-naming | 13 | Style | Low |
| **NPY** | NumPy-specific | ~5 | Reliability | Medium |
| **PD** | pandas-vet | ~20 | Performance / Reliability | Medium |
| **PERF** | Perflint | ~10 | Performance | Medium |
| **PGH** | pygrep-hooks | ~5 | Reliability / Maintainability | Medium |
| **PIE** | flake8-pie | 8 | Maintainability | Medium |
| **PL** | Pylint (Ruff port) | ~50 | Mixed | Medium–High |
| **PT** | flake8-pytest-style | ~30 | Maintainability | Medium |
| **PTH** | flake8-use-pathlib | ~20 | Maintainability | Low |
| **PYI** | flake8-pyi (type stubs) | ~65 | Maintainability | Low (stubs only) |
| **Q** | flake8-quotes | ~5 | Style | Low |
| **RET** | flake8-return | ~8 | Maintainability | Medium |
| **RSE** | flake8-raise | 2 | Reliability | Medium |
| **RUF** | Ruff-specific | ~20 | Mixed | Medium |
| **SIM** | flake8-simplify | ~30 | Maintainability | Medium |
| **SLOT** | flake8-slots | 3 | Performance / Reliability | Low |
| **T10** | flake8-debugger | 1 | Reliability | Medium |
| **T20** | flake8-print | 2 | Maintainability | Medium |
| **TCH** / **TC** | flake8-type-checking | ~10 | Performance | Low |
| **TD** | flake8-todos | ~6 | Maintainability | Low |
| **TID** | flake8-tidy-imports | ~4 | Maintainability | Low |
| **TRY** | tryceratops | ~20 | Reliability / Maintainability | Medium |
| **UP** | pyupgrade | ~50 | Maintainability | Low |
| **YTT** | flake8-2020 | 10 | Reliability | Low |
| **AIR** | Apache Airflow | 7 | Reliability | Low (Airflow only) |
| **INT** | flake8-gettext | 3 | Reliability | Low |

**Total Ruff rule categories: ~58** · **Total rules: ~900+**

---

### 2.2 Ruff Category Deep-Dives

#### F — Pyflakes (Reliability: Undefined names, unused imports)

> **Default enabled. Most critical category.** Catches actual bugs.

| Code Range | Coverage |
|-----------|----------|
| F401 | Unused imports |
| F811 | Redefinition of unused name |
| F821 | Undefined name |
| F841 | Local variable assigned but never used |
| F401–F811 | Module import issues |
| F841–F901 | Variable scoping, return issues |

- **~100 rules** covering: undefined names, unused imports/variables, redefined names, augmented assignment to undefined, format string issues, star imports
- **Quality dimension:** Reliability (primary), Maintainability
- **Agentic relevance:** Very high — AI code frequently imports unused libraries, defines variables it never uses

#### E / W — pycodestyle (Style)

> Formatting and style rules. Many overlap with formatters (Black/ruff format).

| Range | Focus |
|-------|-------|
| E1xx | Indentation |
| E2xx | Whitespace |
| E3xx | Blank lines |
| E4xx | Imports (formatting) |
| E5xx | Line length |
| E7xx | Statement style |
| E9xx | Runtime errors (syntax) |
| W1xx–W6xx | Warnings: trailing whitespace, deprecated features |

- **~220 rules** total (E + W)
- E9xx rules (`E901` syntax errors, `E999` compile errors) are **high priority** — actual syntax failures
- Most E/W rules are low-priority style nitpicks safely handled by auto-formatter
- **Quality dimension:** Style (primary)

#### B — flake8-bugbear (Reliability: Bug-prone patterns)

> **High signal-to-noise ratio. Strongly recommended.** Finds real bugs.

| Code | Rule | Why It Matters |
|------|------|---------------|
| B006 | Mutable argument default | Classic Python gotcha — shared state across calls |
| B007 | Unused loop control variable | Dead code / logic error |
| B008 | Function call in default argument | Executed once at definition, not per-call |
| B012 | Jump statement in finally | Silences exceptions |
| B019 | `lru_cache` on instance method | Memory leak |
| B023 | Function uses loop variable | Closure captures by reference |
| B904 | Raise without `from` in except | Loses exception chain |
| B905 | `zip()` without `strict=` | Silent data truncation |

- **~35 rules** covering: mutable defaults, exception handling, loop hazards, ABC issues, generator confusion
- **Quality dimension:** Reliability (primary)
- **Agentic relevance:** High — `B006` (mutable defaults), `B904` (exception chaining) common in AI-generated code

#### S — flake8-bandit (Security)

> Static security analysis. Maps to OWASP/CWE vulnerability categories.

| Code Range | Security Domain |
|-----------|----------------|
| S101–S108 | Code injection: `assert`, `exec`, hardcoded secrets, temp files |
| S110–S113 | Exception swallowing, requests without timeouts |
| S201–S202 | Framework issues (Flask debug, tarfile) |
| S301–S324 | Dangerous imports: pickle, marshal, insecure hash (MD5/SHA1), XML attacks |
| S401–S415 | Suspicious import detection (telnet, FTP, pycrypto) |
| S501–S509 | Network security: SSL cert bypass, insecure protocol versions, weak keys |
| S601–S612 | Injection: shell injection, subprocess, SQL injection |
| S701–S704 | Template injection: Jinja2 XSS, Mako, unsafe markup |

- **~65 rules** covering virtually all OWASP Top 10 categories
- Notable high-severity rules:
  - `S105–S107`: Hardcoded passwords
  - `S113`: HTTP request without timeout ← critical for agentic code
  - `S301`: Pickle deserialization
  - `S323`: SSL certificate verification bypass
  - `S506`: `yaml.load()` without safe_load
  - `S608`: SQL injection via string concatenation
- **Quality dimension:** Security (primary)
- **Agentic relevance:** **Very high** — AI code making API calls often skips timeouts (`S113`), uses `eval`/`exec` (`S307`, `S102`), hardcodes credentials

#### ASYNC — flake8-async (Reliability: Async/await correctness)

> Critical for async-heavy code patterns common in agentic systems.

| Code | Rule |
|------|------|
| ASYNC100 | `with timeout()` with no await inside |
| ASYNC110 | Busy-wait loop using `sleep()` — use `Event` instead |
| ASYNC210 | Blocking HTTP call in async function |
| ASYNC212 | httpx blocking method in async context |
| ASYNC220–222 | Subprocess creation with blocking methods |
| ASYNC230 | `open()` in async function (use `aiofiles`) |
| ASYNC251 | `time.sleep()` in async function |

- **15 rules** covering async correctness, blocking calls, cancellation scopes
- **Quality dimension:** Reliability, Performance
- **Agentic relevance:** **Extremely high** — agentic frameworks (LangChain, AutoGen, CrewAI) are async-heavy; blocking HTTP calls inside async agents are a common mistake

#### LOG — flake8-logging + G — flake8-logging-format

> Logging hygiene — critical for observability in production systems.

| Code | Rule | Why It Matters |
|------|------|---------------|
| LOG001 | Direct `Logger()` instantiation | Use `getLogger()` |
| LOG002 | `getLogger()` not using `__name__` | Breaks logger hierarchy |
| LOG004 | `.exception()` outside except handler | Incorrect stack trace |
| LOG007 | `.exception()` with `exc_info=False` | Defeats exception logging |
| LOG015 | Call on root logger | Hard to filter/suppress |
| G004 | f-string in logging statement | Eagerly evaluated; hurts perf |
| G201 | `.error(..., exc_info=True)` | Use `.exception()` instead |

- **15 rules** total (LOG + G)
- **Quality dimension:** Maintainability, Performance
- **Agentic relevance:** High — agents need structured logging for tracing decisions; bad logging patterns make debugging agentic pipelines very hard

#### TRY — tryceratops (Reliability: Exception handling patterns)

> Opinionated exception handling best practices.

| Code | Rule |
|------|------|
| TRY002 | Create custom exception classes |
| TRY003 | Avoid string messages in exceptions |
| TRY004 | Prefer `TypeError` over bare check |
| TRY201 | Useless `raise` in except |
| TRY300 | Consider moving code to `else` block |
| TRY301 | `raise` inside `try` block |
| TRY401 | Redundant exception in logging |

- **~20 rules**
- **Quality dimension:** Reliability, Maintainability

#### PERF — Perflint (Performance)

| Code | Rule |
|------|------|
| PERF101 | `list()` over generator in comprehension |
| PERF102 | `dict.keys()` iteration instead of `dict` |
| PERF203 | `try/except` in loop body |
| PERF401 | Manual list-append loop → use comprehension |

- **~10 rules**
- **Quality dimension:** Performance

#### RUF — Ruff-specific rules

> Ruff's own additions — no external plugin equivalent.

| Code | Rule |
|------|------|
| RUF005 | Collection literal concatenation (use spread) |
| RUF006 | `asyncio.create_task()` result not stored (lost reference!) |
| RUF009 | Mutable default in `dataclass` |
| RUF010 | Explicit `str()` in f-string conversion |
| RUF012 | Mutable class variable in dataclass |
| RUF100 | Unused `# noqa` directive |

- **~20 rules**, including several high-value reliability rules
- **RUF006 is critical for async code** — storing `asyncio.create_task()` results prevents garbage collection of running tasks
- **Quality dimension:** Mixed

#### PL — Pylint (Ruff port)

Ruff ports a subset of Pylint checks for speed:

| Prefix | Pylint Category | Example Rules |
|--------|----------------|--------------|
| PLC | Convention | `invalid-characters-in-docstring`, `non-ascii-module-import` |
| PLE | Error | `bad-str-strip-call`, `nonexistent-operator`, `not-callable` |
| PLR | Refactor | `too-many-return-statements`, `too-many-branches`, `magic-value-comparison` |
| PLW | Warning | `useless-else-on-loop`, `redefined-loop-name`, `assert-on-tuple` |

- **~50 rules** ported from Pylint
- **Quality dimension:** Mixed (Reliability, Maintainability)

#### DTZ — flake8-datetimez (Reliability: Timezone correctness)

| Code | Rule |
|------|------|
| DTZ001 | `datetime()` without `tzinfo` |
| DTZ003 | `datetime.utcnow()` (deprecated pattern) |
| DTZ005 | `datetime.now()` without `tz` |
| DTZ007 | `strptime()` without `%z` |

- **10 rules** — timezone-naive datetimes cause subtle bugs in distributed systems
- **Agentic relevance:** Medium — agents generating timestamps for logging/events need timezone awareness

---

## 3. Pylint Rule Taxonomy

Pylint uses a **message ID system** with letter + 4 digits:

### 3.1 Pylint Message Category System

| Prefix | Category | Severity | Description |
|--------|----------|----------|-------------|
| **F** | Fatal | 🔴 Critical | Errors that prevent further processing |
| **E** | Error | 🔴 High | Definite bugs — code is wrong |
| **W** | Warning | 🟡 Medium | Suspicious patterns, probable bugs |
| **R** | Refactor | 🔵 Medium | Refactoring suggestions |
| **C** | Convention | ⚪ Low | Style/convention violations |
| **I** | Informational | ⚪ Low | Informational only |

### 3.2 Pylint Checker Modules Summary

| Checker | Rules (approx) | Primary Dimension | Key Rules |
|---------|---------------|-------------------|-----------|
| **Basic** | ~35 | Reliability, Style | `dangerous-default-value`, `pointless-statement`, `eval-used`, `exec-used`, `assert-on-tuple` |
| **Classes** | ~40 | Reliability, Maintainability | `abstract-method`, `attribute-defined-outside-init`, `invalid-str-returned`, `super-init-not-called` |
| **Design** | 8 | Maintainability | `too-many-branches`, `too-many-arguments`, `too-many-locals`, `too-many-return-statements` |
| **Exceptions** | ~15 | Reliability | `bare-except`, `broad-exception-caught`, `raise-missing-from`, `bad-except-order` |
| **Format** | ~10 | Style | `line-too-long`, `bad-indentation`, `trailing-whitespace` |
| **Imports** | ~15 | Maintainability, Reliability | `cyclic-import`, `wildcard-import`, `wrong-import-order`, `import-error` |
| **Logging** | ~6 | Performance, Maintainability | `logging-not-lazy`, `logging-format-interpolation`, `logging-too-many-args` |
| **Refactoring** | ~40 | Maintainability | `too-many-nested-blocks`, `no-else-return`, `consider-using-ternary`, `inconsistent-return-statements`, `stop-iteration-return` |
| **Variables** | ~30 | Reliability | `undefined-variable`, `unused-variable`, `redefined-outer-name`, `cell-var-from-loop` |
| **Typecheck** | ~20 | Reliability | `not-callable`, `no-member`, `unsubscriptable-object` |
| **Async** | 2 | Reliability | `yield-inside-async-function`, `not-async-context-manager` |
| **String** | ~10 | Reliability | `bad-format-string`, `truncated-format-string` |
| **Dataclass** | 1 | Reliability | `invalid-field-call` |
| **Lambda-Expressions** | 2 | Style | `unnecessary-lambda-assignment`, `unnecessary-direct-lambda-call` |
| **Miscellaneous** | ~3 | Maintainability | `fixme` (TODO/FIXME detection) |
| **Modified-Iteration** | 3 | Reliability | `modified-iterating-dict`, `modified-iterating-set`, `modified-iterating-list` |
| **Nonascii** | 3 | Style | Non-ASCII identifiers/filenames |
| **Method-Args** | 2 | Reliability | `missing-timeout` ← critical for HTTP clients |
| **Match-Statements** | 6 | Reliability | Structural pattern matching validation |
| **Similarity** | 2 | Maintainability | `duplicate-code` |

**Pylint total: ~500+ messages** (including many checks Ruff doesn't port)

#### Notable Pylint-Unique Checks

These exist in Pylint but are NOT in Ruff:

| Rule | Code | Category | Why Matters |
|------|------|----------|-------------|
| `no-member` | E1101 | Error | Attribute access on wrong type — catches many runtime errors |
| `cyclic-import` | R0401 | Refactor | Module dependency cycle detection |
| `duplicate-code` | R0801 | Refactor | Copy-paste detection |
| `too-many-branches` | R0912 | Refactor | Complexity metric |
| `cell-var-from-loop` | W0640 | Warning | Closure captures loop variable |
| `broad-exception-caught` | W0718 | Warning | `except Exception:` anti-pattern |
| `missing-timeout` | W3101 | Warning | HTTP calls without timeout |
| `logging-not-lazy` | W1201 | Warning | Lazy log formatting |

---

## 4. Quality Dimension Coverage Matrix

### Ruff Coverage by Dimension

| Dimension | Ruff Categories | Coverage Level | Notes |
|-----------|----------------|----------------|-------|
| **Reliability** | F, B, S, ASYNC, BLE, RUF, A, DTZ, ISC, LOG, TRY, PLE | 🟢 **Strong** | Best coverage area |
| **Security** | S, PGH | 🟢 **Strong** | ~65 security rules; maps to OWASP |
| **Maintainability** | D, ANN, ARG, ERA, FIX, LOG, PIE, PT, RET, SIM, TD, TRY | 🟡 **Moderate** | Good structural rules; misses semantic |
| **Performance** | C4, ASYNC, G, PERF, TCH | 🟡 **Moderate** | Micro-optimizations + async blocking |
| **Style** | E, W, I, N, Q, COM, FA, ISC | 🟢 **Strong** | Comprehensive; most auto-fixable |

### Pylint Coverage by Dimension

| Dimension | Pylint Checkers | Coverage Level | Notes |
|-----------|----------------|----------------|-------|
| **Reliability** | Basic, Classes, Exceptions, Variables, Typecheck, Modified-Iteration | 🟢 **Strong** | Semantic analysis catches more than Ruff |
| **Security** | Basic (eval/exec), Method-Args | 🟡 **Moderate** | Less thorough than Ruff/Bandit |
| **Maintainability** | Design, Imports, Refactoring, Similarity | 🟢 **Strong** | Unique: complexity metrics, duplicate detection |
| **Performance** | Logging | 🟡 **Moderate** | Primarily logging optimization |
| **Style** | Format, Convention, Nonascii | 🟡 **Moderate** | Covers basics; Ruff is more comprehensive |

---

## 5. Code Hygiene Priority Rules

**"Hygiene" = Rules that catch real bugs or serious maintainability problems, not style nitpicks.**

### Tier 1: Always Enable (High Signal, Low Noise)

| Rule | Tool | Category | What It Catches |
|------|------|----------|----------------|
| `F401` | Ruff | Reliability | Unused imports (dead code, potential import side effects) |
| `F821` | Ruff | Reliability | Undefined name — actual NameError at runtime |
| `F841` | Ruff | Reliability | Local variable assigned but never used |
| `B006` | Ruff | Reliability | Mutable default argument — shared state across calls |
| `B007` | Ruff | Reliability | Unused loop control variable |
| `B019` | Ruff | Reliability | `lru_cache` on instance method — memory leak |
| `B023` | Ruff | Reliability | Function capturing loop variable by reference |
| `BLE001` | Ruff | Reliability | Blind `except:` catching everything |
| `S113` | Ruff | Security | HTTP request without timeout |
| `S105–S107` | Ruff | Security | Hardcoded passwords/secrets |
| `ASYNC210` | Ruff | Reliability | Blocking HTTP call in async function |
| `ASYNC251` | Ruff | Reliability | `time.sleep()` in async function |
| `RUF006` | Ruff | Reliability | `asyncio.create_task()` result not stored |
| `LOG007` | Ruff | Reliability | `.exception()` with `exc_info=False` |
| `DTZ005` | Ruff | Reliability | `datetime.now()` without timezone |
| `bare-except` | Pylint | Reliability | Bare `except:` swallows SystemExit/KeyboardInterrupt |
| `broad-exception-caught` | Pylint | Reliability | `except Exception:` too permissive |
| `undefined-variable` | Pylint | Reliability | Variable used before assignment |
| `modified-iterating-dict` | Pylint | Reliability | Mutating dict during iteration — RuntimeError |
| `missing-timeout` | Pylint | Reliability | HTTP client call without timeout |

### Tier 2: Enable for Production Code

| Rule | Tool | Category | What It Catches |
|------|------|----------|----------------|
| `B904` | Ruff | Reliability | `raise X` inside `except` without `from` — loses exception chain |
| `B905` | Ruff | Reliability | `zip()` without `strict=` — silent data truncation |
| `S301` | Ruff | Security | `pickle` deserialization |
| `S323` | Ruff | Security | SSL cert verification disabled |
| `S506` | Ruff | Security | `yaml.load()` without safe_load |
| `S608` | Ruff | Security | SQL injection via string concatenation |
| `TRY300` | Ruff | Reliability | Code that should be in `else` block instead of `try` |
| `PERF203` | Ruff | Performance | `try/except` inside loop body |
| `PIE796` | Ruff | Reliability | Enum contains duplicate value |
| `G004` | Ruff | Performance | f-string in logging (eagerly evaluated) |
| `too-many-branches` | Pylint | Maintainability | Cyclomatic complexity |
| `too-many-arguments` | Pylint | Maintainability | Functions with too many params |
| `cyclic-import` | Pylint | Maintainability | Circular dependencies |
| `raise-missing-from` | Pylint | Reliability | Exception chaining |
| `cell-var-from-loop` | Pylint | Reliability | Closure captures loop variable |

### Tier 3: Enable with Judgment (Context-Dependent)

| Rule | Tool | Notes |
|------|------|-------|
| `D` (pydocstyle) | Ruff | Valuable for libraries; noisy for scripts |
| `ANN` (annotations) | Ruff | Enforce type annotations; aggressive for quick scripts |
| `FBT` (boolean trap) | Ruff | Opinionated; good for APIs |
| `ARG` (unused arguments) | Ruff | Noisy with callbacks/interfaces |
| `ERA001` (commented code) | Ruff | Useful but flag legitimate comment blocks |
| `S101` (assert) | Ruff | Legitimate in tests; not in production code |

---

## 6. Agentic/AI Code Relevance

Patterns specific to **LLM-generated code, agentic frameworks, and AI system infrastructure**.

### 6.1 API Call Patterns

| Rule | Tool | Code | Agentic Relevance |
|------|------|------|------------------|
| `S113` | Ruff | Security | **Critical**: LLM API calls (OpenAI, Anthropic, etc.) without timeout → hung agents |
| `missing-timeout` | Pylint | W3101 | Same — catches `requests` library calls missing timeout |
| `ASYNC210` | Ruff | Reliability | Blocking HTTP in async agent — freezes event loop |
| `ASYNC212` | Ruff | Reliability | `httpx` sync call in async context |
| `S501` | Ruff | Security | `verify=False` on HTTPS calls — risks MITM |
| `B008` | Ruff | Reliability | Function call in default arg — API client instantiated once, not per-call |

### 6.2 Prompt Construction

| Rule | Tool | Code | Agentic Relevance |
|------|------|------|------------------|
| `S608` | Ruff | Security | SQL injection via string concat — same logic applies to prompt injection if user content is directly interpolated |
| `ISC001/ISC002` | Ruff | Reliability | Implicit string concatenation — hard-to-read prompts with accidental joins |
| `B021` | Ruff | Reliability | f-string used as docstring — f-strings in unexpected positions |
| `EM102` | Ruff | Maintainability | f-string in exception message — same pattern appears in prompt templates |
| `G004` | Ruff | Performance | f-string in logging — prompt templates shouldn't be lazily evaluated in logging |

### 6.3 Error Handling in Agents

| Rule | Tool | Code | Agentic Relevance |
|------|------|------|------------------|
| `BLE001` | Ruff | Reliability | Blind `except:` — agent swallows all errors including KeyboardInterrupt |
| `B012` | Ruff | Reliability | `return/break/continue` in `finally` — silences errors in cleanup |
| `TRY201` | Ruff | Reliability | Useless `raise` in except — errors not propagated correctly |
| `TRY301` | Ruff | Reliability | `raise` inside `try` — raise in wrong place |
| `S110` | Ruff | Security | `try-except-pass` — swallows exceptions silently |
| `broad-exception-caught` | Pylint | Reliability | `except Exception:` in agent tool calls hides real errors |
| `raise-missing-from` | Pylint | Reliability | Losing exception chain in agent pipeline makes debugging impossible |
| `B904` | Ruff | Reliability | Same issue — exception chaining in agent orchestration |

### 6.4 State Management

| Rule | Tool | Code | Agentic Relevance |
|------|------|------|------------------|
| `B006` | Ruff | Reliability | **Critical**: Mutable default arguments in tool definitions — shared state between agent invocations |
| `B039` | Ruff | Reliability | Mutable `ContextVar` default — shared state in async agent context |
| `RUF009` | Ruff | Reliability | Mutable default in `dataclass` — shared state in agent memory structures |
| `RUF012` | Ruff | Reliability | Mutable class variable in dataclass — agent state contamination |
| `B019` | Ruff | Reliability | `lru_cache` on instance method — cache holds reference to `self`, memory leak |

### 6.5 Async/Concurrent Agent Patterns

| Rule | Tool | Code | Agentic Relevance |
|------|------|------|------------------|
| `RUF006` | Ruff | Reliability | **Critical**: `asyncio.create_task()` result not stored — async agent tasks silently die |
| `ASYNC100` | Ruff | Reliability | Cancel scope with no await — timeout never fires |
| `ASYNC110` | Ruff | Reliability | Busy-wait loop in agent polling — use `Event` |
| `ASYNC115` | Ruff | Reliability | `sleep(0)` as checkpoint — use `lowlevel.checkpoint()` |
| `ASYNC230` | Ruff | Reliability | Blocking file I/O in async agent — blocks event loop |
| `PERF203` | Ruff | Performance | `try/except` in agent loop body — avoid if exception is rare |

### 6.6 Logging & Observability (Agent Tracing)

| Rule | Tool | Code | Agentic Relevance |
|------|------|------|------------------|
| `LOG001` | Ruff | Maintainability | Direct `Logger()` instead of `getLogger()` — breaks logger hierarchy |
| `LOG002` | Ruff | Maintainability | Not using `__name__` — makes log tracing across agent modules difficult |
| `LOG007` | Ruff | Reliability | `.exception()` with `exc_info=False` — loses stack trace in agent error logging |
| `G004` | Ruff | Performance | f-string in log — eagerly evaluated even if DEBUG is disabled |
| `logging-not-lazy` | Pylint | Performance | Same issue with `%` formatting |

### 6.7 Security in AI Systems

| Rule | Tool | Code | Agentic Relevance |
|------|------|------|------------------|
| `S307` | Ruff | Security | `eval()` usage — agents must not eval user input or LLM output |
| `S102` | Ruff | Security | `exec()` usage — same risk, code execution |
| `S506` | Ruff | Security | `yaml.load()` without safe_load — agents parsing tool configs |
| `S301` | Ruff | Security | `pickle` deserialization — agents deserializing tool state or memory |
| `S105–S107` | Ruff | Security | Hardcoded API keys — LLM API credentials in source |
| `S701` | Ruff | Security | Jinja2 autoescape=False — prompt templates with XSS risk |

---

## 7. Coverage Gaps

**What deterministic linters fundamentally CANNOT catch:**

### 7.1 Semantic / Logical Issues

| Gap | Why Linters Miss It | Detection Approach |
|-----|--------------------|--------------------|
| Wrong algorithm / logic errors | Can't reason about intent vs. implementation | Testing, LLM review |
| Incorrect prompt construction | No understanding of LLM semantics | LLM-based review, testing |
| Off-by-one errors | Requires value reasoning | Testing, fuzzing |
| Race conditions (beyond basic patterns) | Requires execution flow analysis | Concurrency testing, ThreadSanitizer |
| Incorrect model parameter choices | Domain knowledge required | Config validation, testing |

### 7.2 Architecture & Design

| Gap | Why Linters Miss It | Detection Approach |
|-----|--------------------|--------------------|
| Inappropriate coupling / cohesion | No module-level design reasoning | Architecture review |
| Missing abstraction layers | No design pattern knowledge | Code review |
| Scalability issues | No runtime behavior modeling | Load testing |
| Stateful agent memory leaks | Complex lifecycle reasoning | Memory profiling |
| Prompt injection vulnerabilities | Requires NLP understanding | Specialized AI security tools |

### 7.3 Data & Type Safety

| Gap | Why Linters Miss It | Detection Approach |
|-----|--------------------|--------------------|
| Type errors at runtime (beyond annotation checks) | Requires full type inference | mypy, pyright |
| None propagation errors | Requires dataflow analysis | mypy strict mode |
| Dict key errors | Runtime values unknown statically | Testing |
| Serialization mismatches (JSON schema) | No schema knowledge | Pydantic, runtime validation |
| LLM response schema violations | Dynamic content | Output parsers, retry logic |

### 7.4 External Dependencies

| Gap | Why Linters Miss It | Detection Approach |
|-----|--------------------|--------------------|
| Third-party API breaking changes | Can't analyze external services | Integration tests |
| Dependency vulnerabilities (transitive) | Not a linting problem | `safety`, `pip-audit` |
| Rate limiting / quota exhaustion | Runtime state | Testing, monitoring |
| LLM model deprecation | External service | Version pinning, alerts |

### 7.5 Testing Adequacy

| Gap | Why Linters Miss It | Detection Approach |
|-----|--------------------|--------------------|
| Missing test coverage | Requires coverage instrumentation | `coverage.py` |
| Flaky tests | Requires execution | Test runners |
| Missing edge case tests | Requires domain knowledge | AI-assisted test gen |
| Mock vs real behavior divergence | Runtime semantics | Integration tests |

---

## Summary: Recommended Ruff Configuration for Agentic Python Code

```toml
[tool.ruff.lint]
select = [
    # Core correctness — always enable
    "F",       # Pyflakes: undefined names, unused imports
    "E9",      # pycodestyle: syntax errors
    "B",       # flake8-bugbear: bug-prone patterns
    "BLE",     # Blind except
    "RUF",     # Ruff-specific (includes RUF006: lost task reference)
    
    # Security — critical for AI systems
    "S",       # flake8-bandit: security issues
    
    # Async correctness — critical for agentic code
    "ASYNC",   # Blocking calls in async, cancel scope issues
    
    # Logging observability
    "LOG",     # Logging instantiation and usage
    "G",       # Logging format
    
    # Exception handling quality
    "TRY",     # Exception handling patterns
    
    # Reliability patterns
    "DTZ",     # Timezone-aware datetimes
    "ISC",     # Implicit string concatenation
    "PIE",     # Misc reliability
    
    # Maintainability
    "SIM",     # Simplification
    "RET",     # Return statement patterns
    "T10",     # No debugger statements
    "T20",     # No print statements (use logging)
    
    # Performance
    "PERF",    # Performance anti-patterns
    
    # Import hygiene
    "I",       # isort
    "TCH",     # Type checking imports
]

ignore = [
    "S101",    # Allow assert in test files (configure per-file-ignores)
    "S603",    # subprocess without shell=True — noisy
    "B008",    # Function call in default — sometimes intentional (FastAPI Depends)
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S", "ARG"]
"scripts/**/*.py" = ["T20"]  # Allow print in scripts
```

---

## Appendix: Rule Count Reference

| Tool | Total Rules | Enabled by Default | Auto-fixable |
|------|------------|-------------------|-------------|
| **Ruff** | 900+ | ~50 (E+F subset) | ~400+ |
| **Pylint** | 500+ | ~300 | ~30 |
| **Combined (unique)** | ~1200+ | Configurable | ~400+ (Ruff) |

> **Note:** Counts are approximate and increase with each release. Ruff is actively growing (was ~800 rules in 2024, ~900+ in 2026). Pylint has been relatively stable.

---

*Document generated: 2026-03-06 · Research scope: Ruff v0.9.x + Pylint v4.0.x*
*Sources: docs.astral.sh/ruff/rules/ · pylint.readthedocs.io · Direct rule enumeration*
