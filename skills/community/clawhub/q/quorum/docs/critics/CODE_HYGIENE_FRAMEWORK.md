# Quorum Code Hygiene Framework
## Unified Reference for the Code Hygiene Critic

**Version:** 1.0  
**Date:** 2026-03-05  
**Scope:** Python and PowerShell code-level quality evaluation  
**Grounded in:** ISO/IEC 25010:2023, ISO/IEC 5055:2021 (CISQ), Ruff v0.9.x, Pylint v4.0.x, PSScriptAnalyzer  
**Companion document:** `SECURITY_CRITIC_FRAMEWORK.md`

### Two-Critic Architecture

Quorum separates code evaluation into two complementary critics with distinct responsibilities:

- **Code Hygiene Critic** (this document) evaluates structural quality: correctness, error handling, complexity, naming, duplication, async patterns, resource management, and maintainability. It uses ISO 25010 Maintainability and Reliability as its primary quality model, with CISQ CWE mappings for deterministic grounding.

- **Security Critic** (`SECURITY_CRITIC_FRAMEWORK.md`) evaluates attack resistance: injection, authentication, authorization, cryptography, secrets handling, and SSRF. It uses OWASP ASVS 5.0 and CWE Top 25 as its primary frameworks, with NIST SA-11 for compliance vocabulary.

The boundary is clean: when code hygiene detects a pattern that has security implications (e.g., `eval()` usage, missing input validation), it flags the finding and **delegates** to the Security Critic for security-specific assessment. The Security Critic receives pre-screen evidence from the deterministic layer and adds LLM judgment. Neither critic duplicates the other's evaluation — findings cite which critic owns the assessment.

---

## Status

**v0.7.3 State:** Framework design complete. All features shipped.

- [x] Framework design and documentation
- [x] 12 evaluation categories specified
- [x] ISO/IEC 25010:2023 (Maintainability + Reliability) grounding
- [x] Two-layer architecture (deterministic + LLM) with delegation boundaries
- [x] Full SAST tool integration (Ruff/Pylint) — shipped in pre-screen
- [x] Business logic validation workflow (SEC-02) — shipped
- [x] Learning memory wiring — shipped v0.5.3

**Known Limitations:**
- Ruff and Bandit run in pre-screen; full deterministic coverage continues to expand
- Business logic checks require specification/requirements context

---

## Table of Contents

1. [Scope Decisions: What ISO 25010 Maps to Code Review](#1-scope-decisions)
2. [Evaluation Categories with Two-Layer Architecture](#2-evaluation-categories)
3. [Coverage Matrix](#3-coverage-matrix)
4. [Priority Tiers](#4-priority-tiers)
5. [Agentic Code Patterns](#5-agentic-code-patterns)
6. [Framework Citation Index](#6-framework-citation-index)

---

## 1. Scope Decisions

### ISO 25010 Characteristics Included vs. Excluded

Not all 40 sub-characteristics are evaluable from source code. The following table records which are in-scope for the Code Hygiene Critic and why.

| ISO 25010 Characteristic | Included? | Rationale |
|--------------------------|-----------|-----------|
| Maintainability → Modularity | ✅ | Coupling metrics, circular dependency detection — rich static signal |
| Maintainability → Reusability | ✅ | DRY violations, code duplication — tool-detectable |
| Maintainability → Analysability | ✅ | Complexity metrics, naming, comments — primary hygiene target |
| Maintainability → Modifiability | ✅ | Coupling, complexity, test presence — strong static signal |
| Maintainability → Testability | ✅ | Test coverage patterns, dependency injection, isolation |
| Reliability → Faultlessness | ✅ | Error-prone patterns, undefined behavior — strong static signal |
| Reliability → Fault Tolerance | ✅ | Exception handling, swallowed errors — critical hygiene category |
| Reliability → Availability | ⚠️ Partial | Static can flag missing retry/timeout; full evaluation requires runtime |
| Reliability → Recoverability | ⚠️ Partial | Transaction patterns detectable; completeness requires LLM |
| Performance Efficiency → Resource Utilization | ✅ | Memory leaks, unclosed handles, blocking calls — static-detectable |
| Performance Efficiency → Time Behaviour | ⚠️ Partial | Algorithmic complexity (O(n²) patterns) — static heuristic only |
| Performance Efficiency → Capacity | ⚠️ Partial | Unbounded loops, missing limits — partial static signal |
| Compatibility → Coexistence | ⚠️ Partial | Global state pollution, port conflicts — limited static signal |
| Compatibility → Interoperability | ⚠️ Partial | API contract adherence, serialization safety — static can check types at boundaries |
| Interaction Capability → User Error Protection | ✅ | Input validation, null checks — direct static coverage |
| Interaction Capability → Self-Descriptiveness | ✅ | Docstrings, naming — static measurable |
| Flexibility → Adaptability | ✅ | Hardcoded environment assumptions, platform-specific code |
| Security (all sub-chars) | ⚠️ Delegated | Handled in SECURITY_CRITIC_FRAMEWORK.md — cited only where hygiene overlaps |
| Functional Suitability → Completeness | ❌ | Requires spec knowledge not available from code alone |
| Functional Suitability → Correctness | ❌ | Requires spec knowledge; partially addressed by testing |
| Functional Suitability → Appropriateness | ❌ | Design-level judgment; not code-reviewable |
| Interaction Capability → Appropriateness Recognizability | ❌ | UX-level; API naming partially covered under Self-Descriptiveness |
| Interaction Capability → Learnability | ❌ | UX-level; no meaningful code signal |
| Interaction Capability → Operability | ❌ | UX-level; error message quality partially covered under Fault Tolerance |
| Interaction Capability → User Engagement | ❌ | UI/UX design; not code-reviewable |
| Interaction Capability → Inclusivity | ❌ | Accessibility expertise required; not code-level |
| Interaction Capability → User Assistance | ❌ | Help system design; not code-level |
| Flexibility → Scalability | ⚠️ Partial | Stateful anti-patterns, synchronization bottlenecks — static heuristic only (NEW in 2023) |
| Flexibility → Installability | ❌ | Deployment reasoning; not code-level |
| Flexibility → Replaceability | ❌ | Migration/interface compatibility reasoning; not code-level |
| Safety → Operational Constraint | ⚠️ Context | Boundary checks, constrained numerical operations — include when code is safety-critical |
| Safety → Fail Safe | ⚠️ Context | Missing fallback states, unhandled exception paths — include when code is safety-critical |
| Safety → Risk Identification | ❌ | Domain-specific safety reasoning; no general code-level signal |
| Safety → Hazard Warning | ❌ | Requires semantic understanding of warning/alert patterns; UX-adjacent |
| Safety → Safe Integration | ❌ | Integration boundary safety — requires system-level context beyond code review |

### CISQ Dimensions Alignment

| CISQ Dimension | Code Hygiene Relevance | Coverage Strategy |
|----------------|----------------------|-------------------|
| Reliability (ASCRM) | HIGH | Error handling, concurrency, resource management categories |
| Maintainability (ASCMM) | VERY HIGH | Complexity, duplication, naming, import hygiene categories |
| Performance Efficiency (ASCPEM) | MODERATE | Resource management, async patterns categories |
| Security (ASCSM) | DELEGATED | See SECURITY_CRITIC_FRAMEWORK.md |

---

## 2. Evaluation Categories

Each category has:
- **ISO 25010 grounding** (sub-characteristic)
- **CISQ grounding** (CWE IDs)
- **Deterministic checks**: specific tool rules — run in pre-screen layer before LLM
- **LLM judgment checks**: what the critic evaluates that tools cannot

---

### CAT-01: Code Correctness

**ISO 25010:** Reliability → Faultlessness  
**CISQ:** CWE-252, CWE-390, CWE-394, CWE-480, CWE-595, CWE-597, CWE-682, CWE-703  
**Supplementary (non-CISQ, high hygiene value):** CWE-561 (Dead Code — CISQ Maintainability), CWE-570/CWE-571 (Always False/True — CISQ Security+Maintainability)  
**Default Tier:** Tier 1

#### Deterministic Checks

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| Ruff | `F821` | Undefined name — guaranteed `NameError` at runtime |
| Ruff | `F401` | Unused imports — dead code, potential import side effects |
| Ruff | `F841` | Local variable assigned but never used |
| Ruff | `F811` | Redefinition of unused name |
| Ruff | `E999`, `E901` | Syntax errors — file cannot be executed |
| Ruff | `B007` | Unused loop control variable |
| Ruff | `B023` | Function definition in loop captures loop variable by reference |
| Ruff | `PLE0117`, `PLE0100` | Non-local used without binding; `return` outside function |
| Pylint | `E0601` `undefined-variable` | Variable used before assignment |
| Pylint | `E0102` `function-redefined` | Class/function/method redefined |
| Pylint | `W0612` `unused-variable` | Assigned but never used |
| Pylint | `E1101` `no-member` | Attribute access on wrong type |
| Pylint | `W0640` `cell-var-from-loop` | Closure captures loop variable — behavior differs from intent |
| Pylint | `W4701` `modified-iterating-dict` | Mutating dict during iteration — `RuntimeError` |
| Pylint | `W4702` `modified-iterating-set` | Same for sets |
| PSScriptAnalyzer | `PSAvoidAssignmentToAutomaticVariable` | Assigning to `$_`, `$true`, `$false`, `$null`, `$PSItem` |
| PSScriptAnalyzer | `PSPossibleIncorrectComparisonWithNull` | `$var -eq $null` instead of `$null -eq $var` |
| PSScriptAnalyzer | `PSPossibleIncorrectUsageOfAssignmentOperator` | `=` used where `-eq` was intended in conditional |
| PSScriptAnalyzer | `PSPossibleIncorrectUsageOfRedirectionOperator` | `>` used where `-gt` was intended |
| PSScriptAnalyzer | `PSUseDeclaredVarsMoreThanAssignments` | Variables assigned but never read |
| PSScriptAnalyzer | `PSAvoidInvokingEmptyMembers` | Calling empty string member — always a bug |

#### LLM Judgment Checks

| Check | Why LLM Is Needed |
|-------|-------------------|
| Off-by-one errors in range/index logic | Tools see syntax; LLM reasons about boundary conditions in context |
| Wrong algorithm / incorrect logic | No tool can verify implementation matches intent — requires semantic understanding |
| Incorrect operator usage (beyond syntactic) | Tools catch `=` vs `-eq`; LLM catches mathematically wrong operations |
| Unreachable branches beyond dead code detection | Complex conditional logic where branches are logically impossible but syntactically valid |
| Incorrect comparison semantics (string vs numeric types) | Beyond CWE-595/597 rule checks; LLM can spot type coercion bugs in context |

---

### CAT-02: Error Handling

**ISO 25010:** Reliability → Fault Tolerance, Reliability → Faultlessness  
**CISQ:** CWE-703 (parent); CWE-248, CWE-252, CWE-390, CWE-391, CWE-392, CWE-394 (child weaknesses of CWE-703 per CISQ conformance model)  
**Default Tier:** Tier 1

#### Deterministic Checks

**Python:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| Ruff | `BLE001` | Blind `except:` — catches `SystemExit`, `KeyboardInterrupt`, `GeneratorExit` |
| Ruff | `S110` | `try-except-pass` — exceptions swallowed silently |
| Ruff | `B012` | `return`/`break`/`continue` in `finally` block — silences exceptions |
| Ruff | `B904` | `raise X` inside `except` without `from` — destroys exception chain |
| Ruff | `TRY201` | Useless `raise` in except block |
| Ruff | `TRY301` | `raise` inside a `try` block — ambiguous catch scope |
| Ruff | `TRY400` | `logging.error()` used instead of `logging.exception()` — loses traceback |
| Ruff | `TRY401` | Redundant exception in logging call |
| Pylint | `W0702` `bare-except` | Bare `except:` clause |
| Pylint | `W0718` `broad-exception-caught` | `except Exception:` too broad |
| Pylint | `W0706` `try-except-raise` | `raise` in `except` without exception handling |
| Pylint | `W0716` `raise-missing-from` | Exception chaining — `raise X from original` |

**PowerShell:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| PSScriptAnalyzer | `PSAvoidUsingEmptyCatchBlock` | `catch {}` — silently swallows all exceptions |

**TBD (no rule exists):**
- `-ErrorAction Stop` not used with cmdlets inside `try/catch` (PowerShell)
- `$ErrorActionPreference` not set to `Stop` in non-interactive scripts (PowerShell)

#### LLM Judgment Checks

| Check | Why LLM Is Needed |
|-------|-------------------|
| Exception handling completeness | Does the code handle all meaningful failure modes, not just syntactic presence of try/catch? |
| Appropriate exception granularity | Are `except TypeError`, `except ValueError` used where `except Exception` is used? Wrong granularity hides bugs. |
| Error propagation correctness | Does the exception include enough context to diagnose at the call site? |
| Recovery logic adequacy | After catching an exception, is the recovery action correct or does it leave state corrupt? |
| Exception hierarchy misuse | Catching parent when only child was intended; catching exceptions from wrong subsystem |
| PowerShell `$?` vs `try/catch` | Using `$?` fragile flag vs structured exception handling — tools don't flag this |

---

### CAT-03: Resource Management

**ISO 25010:** Performance Efficiency → Resource Utilization, Reliability → Recoverability  
**CISQ:** CWE-401, CWE-404, CWE-459, CWE-672, CWE-772, CWE-775, CWE-1088, CWE-1091  
**Default Tier:** Tier 1

#### Deterministic Checks

**Python:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| Ruff | `S113` | HTTP request without timeout parameter — hung connections |
| Ruff | `ASYNC210` | Blocking HTTP call inside async function — freezes event loop |
| Ruff | `ASYNC212` | `httpx` synchronous call in async context |
| Ruff | `ASYNC230` | `open()` in async function without `aiofiles` |
| Ruff | `ASYNC251` | `time.sleep()` inside async function |
| Ruff | `B019` | `lru_cache` on instance method — cache holds `self` reference; memory leak |
| Pylint | `W3101` `missing-timeout` | `requests` library calls without timeout |

**PowerShell:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| PSScriptAnalyzer | — | No PSSA rule for `-TimeoutSec` absence on `Invoke-WebRequest`/`Invoke-RestMethod` **(GAP)** |

**TBD / Gaps:**
- Context manager misuse (`open()` not in `with` block) — no dedicated Ruff rule (partially caught by Pylint `W1514`)
- Connection pool exhaustion patterns — no static rule

#### LLM Judgment Checks

| Check | Why LLM Is Needed |
|-------|-------------------|
| Context manager usage completeness | Does all file/socket/database code use `with` statements or `try/finally`? No single rule covers all resource types. |
| Connection lifecycle management | Are connections explicitly closed/pooled in all code paths including exception paths? |
| Timeout adequacy | Even when timeouts exist, are they sized appropriately for the operation? LLM assesses context. |
| Memory accumulation in loops | Collecting unbounded results into lists inside loops — no direct static check |
| Generator vs. list for large datasets | LLM identifies where `list()` materializes all data when streaming was possible |

---

### CAT-04: Complexity & Modularity

**ISO 25010:** Maintainability → Analysability, Maintainability → Modifiability, Maintainability → Modularity  
**CISQ:** CWE-407, CWE-1047, CWE-1048, CWE-1064, CWE-1080, CWE-1083, CWE-1084, CWE-1121  
**Default Tier:** Tier 1 (complexity metrics), Tier 2 (modularity analysis)

#### Deterministic Checks

**Python:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| Pylint | `R0912` `too-many-branches` | > 12 branches (configurable) — CWE-1121 proxy |
| Pylint | `R0914` `too-many-locals` | > 15 local variables |
| Pylint | `R0911` `too-many-return-statements` | > 6 return statements |
| Pylint | `R0913` `too-many-arguments` | > 5 arguments — CWE-1064 |
| Pylint | `R0915` `too-many-statements` | > 50 statements per function — CWE-1080 proxy |
| Pylint | `R1702` `too-many-nested-blocks` | > 5 nested blocks |
| Pylint | `R0401` `cyclic-import` | Circular module dependencies — CWE-1047 |
| Pylint | `R0801` `duplicate-code` | Copy-paste code — CWE-1041 |
| Ruff | `PLR0912` | Too many branches (Ruff port of Pylint) |
| Ruff | `PLR0913` | Too many arguments (Ruff port) |
| Ruff | `C901` | McCabe complexity (requires explicit enable) |

**PowerShell:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| PSScriptAnalyzer | — | No built-in complexity threshold rule **(GAP)** — use `Measure-ScriptComplexity` custom rule or external tooling |
| PSScriptAnalyzer | `PSAvoidGlobalVars` | Global variable coupling — CWE-1083 analog |
| PSScriptAnalyzer | `PSAvoidGlobalFunctions` | Global function scope pollution |
| PSScriptAnalyzer | `PSAvoidGlobalAliases` | Global alias pollution |

#### LLM Judgment Checks

| Check | Why LLM Is Needed |
|-------|-------------------|
| Cohesion assessment | Does a class/module do one thing or multiple unrelated things? Metrics measure size but not purpose alignment. |
| Inappropriate abstraction | Function too abstract (does nothing concrete) or too specific (can't be reused) — requires design judgment |
| God class / God function | Beyond line-count metrics; LLM identifies when a class is doing architectural work it shouldn't |
| Layer violation | Tools detect call graph cycles; LLM identifies when the wrong layer is calling the wrong layer for semantic reasons |
| PowerShell module structure | Proper use of `Export-ModuleMember`, appropriate function/module decomposition |

---

### CAT-05: Code Duplication & Reusability

**ISO 25010:** Maintainability → Reusability  
**CISQ:** CWE-1041  
**Default Tier:** Tier 2

#### Deterministic Checks

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| Pylint | `R0801` `duplicate-code` | Copy-paste code blocks (clone detection) — CWE-1041 |
| Ruff | `SIM` (selected) | Simplifiable code patterns (e.g., `SIM118`: dict.keys() iteration) |
| PSScriptAnalyzer | — | No built-in duplicate detection **(GAP)** |

#### LLM Judgment Checks

| Check | Why LLM Is Needed |
|-------|-------------------|
| Near-duplicate logic with parameter variation | Clone detection catches exact copies; LLM identifies functionally identical code that differs cosmetically |
| Missed abstraction opportunity | Two functions doing the same thing with different names that escaped clone detection |
| Inlining vs. DRY tradeoff | Sometimes duplication is intentional (performance, clarity); LLM assesses whether the duplication is justified |

---

### CAT-06: Naming & Documentation

**ISO 25010:** Maintainability → Analysability, Interaction Capability → Self-Descriptiveness  
**CISQ:** CWE-1052, CWE-1085  
**Default Tier:** Tier 2

#### Deterministic Checks

**Python:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| Ruff | `D100–D107` | Missing docstrings (module, class, function, method variants) |
| Ruff | `D200–D215` | Docstring format (one-liner, multi-line, blank lines) |
| Ruff | `N801–N818` | Naming conventions (class, function, variable, constant naming) |
| Ruff | `ERA001` | Commented-out code — CWE-1085 |
| Ruff | `T20` (`T201`, `T203`) | `print`/`pprint` left in code (use logging) |
| Ruff | `T10` (`T100`) | Debugger import left in code |
| Pylint | `C0103` `invalid-name` | Names not conforming to configured naming conventions |
| Pylint | `C0114` `missing-module-docstring` | Module-level docstring missing |
| Pylint | `C0115` `missing-class-docstring` | Class docstring missing |
| Pylint | `C0116` `missing-function-docstring` | Function docstring missing |
| Pylint | `W0511` `fixme` | TODO/FIXME comments — unresolved debt |

**PowerShell:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| PSScriptAnalyzer | `PSProvideCommentHelp` | Functions missing comment-based help block (`.SYNOPSIS`, `.DESCRIPTION`, etc.) |
| PSScriptAnalyzer | `PSAvoidUsingWriteHost` | `Write-Host` instead of `Write-Verbose`/`Write-Output` |
| PSScriptAnalyzer | `PSUseApprovedVerbs` | Function verb not in PowerShell approved verb list |
| PSScriptAnalyzer | `PSUseSingularNouns` | Function noun is plural |
| PSScriptAnalyzer | `PSAvoidUsingPositionalParameters` | Positional parameters — self-documentation failure |
| PSScriptAnalyzer | `PSAvoidUsingCmdletAliases` | Aliases (`ls`, `%`, `?`) in scripts — unreadable in isolation |

#### LLM Judgment Checks

| Check | Why LLM Is Needed |
|-------|-------------------|
| Docstring accuracy | Is the docstring actually correct about what the function does? Tools detect presence; LLM detects lies. |
| Naming clarity | `process_data()` tells us nothing; `normalize_user_email()` does. Tools check convention; LLM checks semantics. |
| Magic numbers / magic strings | Beyond CWE-1052 pattern matching — are hardcoded literals semantically meaningful? Do they need named constants? |
| Comment quality | Inline comments that explain *why*, not just *what* — tools can't evaluate this |
| PowerShell help block completeness | `ProvideCommentHelp` fires on absence; LLM evaluates whether the description is actually useful |

---

### CAT-07: Type Safety & Data Integrity

**ISO 25010:** Reliability → Faultlessness  
**CISQ:** CWE-681, CWE-704, CWE-758  
**Default Tier:** Tier 2

#### Deterministic Checks

**Python:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| Ruff | `ANN001–ANN204` | Missing type annotations on function arguments and return types |
| Ruff | `PGH003` | Blanket `type: ignore` suppressing all type errors |
| Ruff | `ISC001`, `ISC002` | Implicit string concatenation — unintended joins |
| Ruff | `DTZ001–DTZ011` | Timezone-naive datetime objects (DTZ001, DTZ005 most important) |
| Ruff | `B015` | Pointless comparison — logic never changes based on this condition |
| Pylint | `E1101` `no-member` | Attribute access on wrong type (requires type inference) |
| Pylint | `W0611` | Unused import — can signal type annotation imports not used at runtime |

**PowerShell:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| PSScriptAnalyzer | `PSAvoidMultipleTypeAttributes` | Multiple `[type]` attributes causing unexpected coercion |
| PSScriptAnalyzer | `PSUseOutputTypeCorrectly` | `[OutputType()]` doesn't match actual returned types |
| PSScriptAnalyzer | `PSAvoidDefaultValueForMandatoryParameter` | Mandatory+default is contradictory — type contract violation |

**Note:** Full type-checking requires `mypy` or `pyright` (Python) — not part of Ruff/Pylint by default. Ruff `ANN` rules check annotation presence, not correctness.

#### LLM Judgment Checks

| Check | Why LLM Is Needed |
|-------|-------------------|
| Type annotation correctness | `ANN` rules check presence; LLM checks whether `List[str]` should actually be `Optional[List[str]]` |
| Implicit type coercion bugs | Python's `==` between string and int returns `False`; PowerShell coerces types aggressively — LLM spots contextual confusion |
| `None` propagation | Does the code handle `None` return values at all call sites? Requires semantic dataflow reasoning. |
| Optional chaining adequacy | Are `.get()` calls used appropriately on dicts that might be missing keys? |
| PowerShell type coercion surprises | Numeric strings, array vs scalar pipeline behavior — LLM identifies where PowerShell implicit coercion causes bugs |

---

### CAT-08: Async & Concurrency Correctness

**ISO 25010:** Reliability → Fault Tolerance, Reliability → Faultlessness  
**CISQ:** CWE-366, CWE-662, CWE-833, CWE-835, CWE-1088  
**Default Tier:** Tier 1 (for async-heavy code)

#### Deterministic Checks

**Python:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| Ruff | `ASYNC100` | `with timeout()` scope containing no `await` — timeout never fires |
| Ruff | `ASYNC110` | Busy-wait loop using `sleep()` — use `asyncio.Event` instead |
| Ruff | `ASYNC115` | `asyncio.sleep(0)` as checkpoint — use proper checkpoint |
| Ruff | `ASYNC210` | Blocking HTTP call inside async function |
| Ruff | `ASYNC212` | `httpx` sync call in async context |
| Ruff | `ASYNC220–222` | Blocking subprocess creation in async context |
| Ruff | `ASYNC230` | `open()` without `aiofiles` in async context |
| Ruff | `ASYNC251` | `time.sleep()` in async function |
| Ruff | `RUF006` | `asyncio.create_task()` result not stored — task silently garbage collected |
| Pylint | `E1700` `yield-inside-async-function` | `yield` in async function (wrong type) |
| Pylint | `W0611` | Unused import of `asyncio` (signals dead async code) |

**PowerShell:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| PSScriptAnalyzer | `PSUseUsingScopeModifierInNewRunspaces` | Variables in `Start-Job`/`Invoke-Command`/`ForEach-Object -Parallel` without `$using:` scope |

**Note:** PowerShell `ForEach-Object -Parallel` concurrency errors (shared state, race conditions) have no PSSA rules — this is a **GAP**.

#### LLM Judgment Checks

| Check | Why LLM Is Needed |
|-------|-------------------|
| Async/sync boundary errors | Is `await` used consistently throughout a call chain, or does it break down at some layer? |
| Incorrect cancellation handling | Does the code propagate `asyncio.CancelledError` or swallow it? |
| Race condition identification | Shared mutable state accessed from multiple tasks/threads — tools catch basic patterns, LLM reasons about access sequences |
| `asyncio.create_task` lifecycle | Even with `RUF006` flagging lost references, LLM evaluates whether task cancellation and exception handling are complete |
| PowerShell parallel state sharing | `ForEach-Object -Parallel` with shared collections — LLM identifies thread-unsafe patterns tools miss |
| Deadlock potential | Tools detect some patterns (CWE-833); LLM reasons about lock acquisition order in complex scenarios |

---

### CAT-09: Import & Dependency Hygiene

**ISO 25010:** Maintainability → Modularity  
**CISQ:** CWE-1047, CWE-1048  
**Default Tier:** Tier 1

#### Deterministic Checks

**Python:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| Ruff | `F401` | Unused imports |
| Ruff | `I001` | Import sort order (isort) |
| Ruff | `TID251–253` | Banned imports (configurable), import style |
| Ruff | `TCH001–003` | Imports that should be in `TYPE_CHECKING` block |
| Pylint | `R0401` `cyclic-import` | Circular module dependencies — CWE-1047 |
| Pylint | `W0401` `wildcard-import` | `from x import *` — name collision risk, pollutes namespace |
| Pylint | `C0414` `useless-import-alias` | `import x as x` — pointless alias |

**PowerShell:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| PSScriptAnalyzer | `PSMissingModuleManifestField` | Missing `Version`, `Author`, `Description` in module manifest |
| PSScriptAnalyzer | `PSUseToExportFieldsInManifest` | Wildcard exports instead of explicit lists |
| PSScriptAnalyzer | `PSAvoidUsingDeprecatedManifestFields` | Deprecated manifest fields |
| PSScriptAnalyzer | `PSAvoidUsingWMICmdlet` | Deprecated WMI cmdlets; use CIM equivalents |
| PSScriptAnalyzer | `PSAvoidOverwritingBuiltInCmdlets` | Redefining built-in cmdlets |
| PSScriptAnalyzer | `PSAvoidReservedWordsAsFunctionNames` | Function names matching reserved keywords |

#### LLM Judgment Checks

| Check | Why LLM Is Needed |
|-------|-------------------|
| Import placement correctness | Are imports at module top, or scattered? Are conditional imports justified? |
| Dependency necessity | Are all imported packages actually used in meaningful ways, or is the dependency gratuitous? |
| Version pinning adequacy | `requirements.txt` with unpinned versions (`requests`) vs pinned (`requests==2.31.0`) — LLM assesses risk |
| PowerShell `RequiredModules` correctness | Are module dependencies declared in manifest? Are versions constrained appropriately? |

---

### CAT-10: Style & Formatting

**ISO 25010:** Maintainability → Analysability  
**CISQ:** CWE-1080, CWE-1085  
**Default Tier:** Tier 2 (auto-fixable items handled before critic invocation)

#### Deterministic Checks

**Python:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| Ruff | `E1xx`, `E2xx`, `E3xx` | Indentation, whitespace, blank lines |
| Ruff | `E5xx` | Line length (default 88 for Black compatibility) |
| Ruff | `W291`, `W293` | Trailing whitespace |
| Ruff | `I001` | Import sort order |
| Ruff | `COM812`, `COM819` | Missing/trailing commas |
| Ruff | `Q000–Q003` | Quote style consistency |

**PowerShell:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| PSScriptAnalyzer | `PSUseConsistentIndentation` | Tabs vs spaces, indent size |
| PSScriptAnalyzer | `PSUseConsistentWhitespace` | Operators, braces, pipes whitespace |
| PSScriptAnalyzer | `PSPlaceOpenBrace`, `PSPlaceCloseBrace` | Brace placement style |
| PSScriptAnalyzer | `PSAvoidTrailingWhitespace` | Trailing whitespace in diffs |
| PSScriptAnalyzer | `PSAvoidLongLines` | Configurable max line length |
| PSScriptAnalyzer | `PSUseCorrectCasing` | Cmdlet canonical casing |

**Note:** Style checks should be auto-fixed (Ruff `--fix`, `Format-PSSScriptAnalyzerInput`) before the LLM critic runs. LLM should not waste tokens on formatting.

#### LLM Judgment Checks

| Check | Why LLM Is Needed |
|-------|-------------------|
| Logical organization within files | Are related functions grouped together? Does the file have a coherent reading order? Tools check format; LLM checks structure. |
| Comment clarity and necessity | Is there a comment for every non-obvious decision? Are comments redundant (restate the code)? |
| Consistent abstraction level | Does a function mix high-level and low-level operations in confusing ways? |

---

### CAT-11: Portability & Compatibility

**ISO 25010:** Flexibility → Adaptability, Compatibility → Coexistence  
**CISQ:** CWE-758, CWE-1051  
**Default Tier:** Tier 2

#### Deterministic Checks

**Python:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| Ruff | `UP` (pyupgrade) | Python version compatibility; upgrade to modern syntax patterns |
| Ruff | `YTT101–117` | `sys.version` checks using wrong comparison methods |
| Ruff | `EXE001–005` | Shebang line issues, executable bit inconsistencies |
| Ruff | `INP001` | Files missing `__init__.py` in namespace packages |

**PowerShell:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| PSScriptAnalyzer | `PSUseCompatibleCmdlets` | Cmdlets not available on target PS version/platform |
| PSScriptAnalyzer | `PSUseCompatibleSyntax` | Syntax requiring PS 7.0+ (ternary, `??=`, etc.) used without version guard |
| PSScriptAnalyzer | `PSUseCompatibleTypes` | .NET types unavailable in target environments |
| PSScriptAnalyzer | `PSUseCompatibleCommands` | External commands not available cross-platform |
| PSScriptAnalyzer | `PSUseBOMForUnicodeEncodedFile` | BOM for Windows PowerShell 5.1 compatibility |

#### LLM Judgment Checks

| Check | Why LLM Is Needed |
|-------|-------------------|
| Hardcoded OS assumptions | `os.sep == '\\'`, Windows-only path formats, hardcoded `/etc/` paths — tools catch some; LLM catches subtle assumptions |
| Platform-specific API usage without guards | Code that works on Linux but silently fails on Windows (e.g., `signal.SIGKILL`) |
| PowerShell Windows vs. Linux parity | Cmdlets that differ in behavior between PS 5.1 and PS 7 on Linux (e.g., `Get-Acl`, `Get-AuthenticodeSignature`) |
| Hardcoded configuration (CWE-1051 analog) | IP addresses, ports, connection strings embedded as literals — LLM identifies what should be configurable |

---

### CAT-12: Testability

**ISO 25010:** Maintainability → Testability  
**CISQ:** (no direct CWEs; inferred from CWE-1047 — high coupling reduces testability)  
**Default Tier:** Tier 2

#### Deterministic Checks

**Python:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| Ruff | `PT` (flake8-pytest-style) | Test style issues (fixtures, assertion patterns, raises) |
| Ruff | `S101` | `assert` in production code (only appropriate in tests) |
| Pylint | `R0913` | Too many arguments — functions with many arguments are hard to test |
| Pylint | `R0401` | Circular imports — prevents isolated unit test loading |

**PowerShell:**

| Tool | Rule(s) | What It Catches |
|------|---------|----------------|
| PSScriptAnalyzer | `PSDSCDscTestsPresent` | DSC resources should include Pester tests |

**Note:** Coverage metrics require `coverage.py` (Python) or Pester (PowerShell) — these run separately from linting.

#### LLM Judgment Checks

| Check | Why LLM Is Needed |
|-------|-------------------|
| Testability assessment | Are functions pure? Do they have side effects that make mocking required? Is the design injectable? |
| Missing test coverage indicators | LLM identifies complex logic branches that appear untested based on code structure |
| Pester test quality | Are PowerShell Pester tests actually testing behavior, or just calling the function without assertions? |
| Test isolation | Are there hidden dependencies (global state, filesystem, network) that make tests fragile? |
| Mock adequacy | Are tests using mocks for external dependencies, or making real network calls? |

---

## 3. Coverage Matrix

| Category | Deterministic (Ruff/Pylint) | Deterministic (PSScriptAnalyzer) | LLM Needed | Coverage Assessment |
|----------|-----------------------------|----------------------------------|------------|---------------------|
| CAT-01: Code Correctness | ✅ Strong (F, B, PL, E rules) | ✅ Strong (assignment, comparison rules) | ✅ Logic errors, off-by-one | **PARTIAL** |
| CAT-02: Error Handling | ✅ Strong (BLE, TRY, B012, Pylint exceptions) | ⚠️ Weak (only EmptyCatchBlock) | ✅ Completeness, propagation | **PARTIAL (PS: LLM-HEAVY)** |
| CAT-03: Resource Management | ✅ Strong Python (S113, ASYNC*) | ❌ Gap — no timeout rules | ✅ Completeness, lifecycle | **PARTIAL (PS: GAP)** |
| CAT-04: Complexity & Modularity | ✅ Strong Python (Pylint R-codes) | ❌ Gap — no complexity metrics | ✅ Cohesion, God classes | **PARTIAL (PS: LLM-ONLY)** |
| CAT-05: Code Duplication | ✅ Moderate (Pylint R0801) | ❌ Gap | ✅ Near-duplicate logic | **PARTIAL (PS: LLM-ONLY)** |
| CAT-06: Naming & Documentation | ✅ Strong (D, N, ANN rules; Pylint C-codes) | ✅ Strong (ProvideCommentHelp, ApprovedVerbs, Aliases) | ✅ Accuracy, clarity | **PARTIAL** |
| CAT-07: Type Safety | ✅ Moderate (ANN, DTZ, ISC; Pylint E1101) | ⚠️ Partial (MultipleType, OutputType) | ✅ Correctness, None propagation | **PARTIAL** |
| CAT-08: Async & Concurrency | ✅ Strong Python (ASYNC*, RUF006) | ⚠️ Partial (using scope only) | ✅ Race conditions, cancel handling | **PARTIAL (PS: LLM-HEAVY)** |
| CAT-09: Import Hygiene | ✅ Strong Python (F401, I, TCH, Pylint R0401) | ✅ Strong (manifest rules, deprecated cmdlets) | ✅ Necessity, version pinning | **PARTIAL** |
| CAT-10: Style & Formatting | ✅ Full (E, W, Q, COM; Pylint C-codes) | ✅ Full (CodeFormatting preset) | ⚠️ Organization, comment quality | **FULL (format) / PARTIAL (structure)** |
| CAT-11: Portability | ✅ Moderate (UP, YTT) | ✅ Strong (UseCompatible* rules) | ✅ OS assumptions, hardcoded config | **PARTIAL** |
| CAT-12: Testability | ✅ Partial (PT, S101, Pylint R-codes) | ⚠️ Minimal (DSC only) | ✅ Design, isolation, mock adequacy | **LLM-HEAVY** |

---

## 4. Priority Tiers

### Tier 1: Always Run (Every Validation)

Every validation regardless of depth setting.

**Rationale:** These catch bugs that will cause runtime failures or are security-adjacent. High signal, low noise.

| Check | Tool(s) | Category | CWE |
|-------|---------|----------|-----|
| Undefined names / compile errors | Ruff `F821`, `E999`, `E901` | CAT-01 | CWE-561, CWE-665 |
| Unused imports | Ruff `F401` | CAT-09 | CWE-561 |
| Mutable default arguments | Ruff `B006`, `RUF009`, `RUF012` | CAT-01, CAT-08 | CWE-665 |
| Blind exception swallowing | Ruff `BLE001`, `S110`; Pylint `W0702` | CAT-02 | CWE-390, CWE-703 |
| Empty catch block | PSScriptAnalyzer `PSAvoidUsingEmptyCatchBlock` | CAT-02 | CWE-390 |
| HTTP requests without timeout | Ruff `S113`; Pylint `W3101` | CAT-03 | CWE-1088 |
| Blocking call in async function | Ruff `ASYNC210`, `ASYNC251` | CAT-08 | CWE-1088 |
| Lost async task reference | Ruff `RUF006` | CAT-08 | CWE-404 |
| Assignment to automatic variables | PSScriptAnalyzer `PSAvoidAssignmentToAutomaticVariable` | CAT-01 | — |
| Invoke-Expression usage | PSScriptAnalyzer `PSAvoidUsingInvokeExpression` | CAT-01, Security | CWE-78, CWE-94 |
| Variable used before assignment | Pylint `E0601` | CAT-01 | CWE-665 |
| Dict mutation during iteration | Pylint `W4701`, `W4702` | CAT-01 | CWE-662 |
| Loop variable captured by closure | Ruff `B023`; Pylint `W0640` | CAT-01 | CWE-665 |
| **LLM: Error handling completeness** | LLM | CAT-02 | CWE-703 |
| **LLM: Logical correctness (obvious)** | LLM | CAT-01 | CWE-480, CWE-682 |

### Tier 2: Standard Depth

In addition to Tier 1. For standard and thorough validation.

| Check | Tool(s) | Category | CWE |
|-------|---------|----------|-----|
| Exception chaining | Ruff `B904`; Pylint `W0716` | CAT-02 | CWE-703 |
| Timezone-naive datetimes | Ruff `DTZ005`, `DTZ001` | CAT-07 | — |
| f-string in logging | Ruff `G004` | CAT-06 | CWE-1050 (perf) |
| Complexity metrics | Pylint `R0912`, `R0913`, `R0914`, `R0915` | CAT-04 | CWE-1064, CWE-1121 |
| Circular imports | Pylint `R0401` | CAT-09 | CWE-1047 |
| Naming conventions | Ruff `N801–N818`; Pylint `C0103` | CAT-06 | — |
| Missing docstrings | Ruff `D100–D107`; Pylint `C0114–C0116` | CAT-06 | — |
| Missing function help | PSScriptAnalyzer `PSProvideCommentHelp` | CAT-06 | — |
| Cmdlet aliases in scripts | PSScriptAnalyzer `PSAvoidUsingCmdletAliases` | CAT-06 | — |
| Positional parameters | PSScriptAnalyzer `PSAvoidUsingPositionalParameters` | CAT-06 | — |
| Async cancel scope errors | Ruff `ASYNC100` | CAT-08 | CWE-662 |
| Return value tracking | Ruff `RET501–508` | CAT-01 | CWE-252 |
| Type annotations presence | Ruff `ANN001–204` | CAT-07 | — |
| Print statements in non-scripts | Ruff `T20` | CAT-06 | — |
| **LLM: Resource lifecycle** | LLM | CAT-03 | CWE-404, CWE-772 |
| **LLM: Cohesion assessment** | LLM | CAT-04 | CWE-1083 |
| **LLM: Naming clarity** | LLM | CAT-06 | — |
| **LLM: Type annotation correctness** | LLM | CAT-07 | CWE-704 |
| **LLM: Testability assessment** | LLM | CAT-12 | — |

### Tier 3: Thorough Depth Only

Deep analysis. Only at `--depth thorough`. Higher cost, lower frequency.

| Check | Tool(s) | Category | CWE |
|-------|---------|----------|-----|
| Code duplication | Pylint `R0801` | CAT-05 | CWE-1041 |
| Excessive fan-out | Pylint `R0902` | CAT-04 | CWE-1048 |
| Portability analysis | Ruff `UP`, `YTT`; PSScriptAnalyzer `UseCompatible*` | CAT-11 | CWE-758 |
| Commented-out code | Ruff `ERA001` | CAT-06 | CWE-1085 |
| Unused arguments | Ruff `ARG001–005` | CAT-06 | CWE-1064 |
| **LLM: Near-duplicate logic** | LLM | CAT-05 | CWE-1041 |
| **LLM: Architecture/layer violations** | LLM | CAT-04 | CWE-1054 |
| **LLM: Hardcoded configuration review** | LLM | CAT-11 | CWE-1051, CWE-1052 |
| **LLM: PowerShell concurrency patterns** | LLM | CAT-08 | CWE-662 |
| **LLM: Test quality assessment** | LLM | CAT-12 | — |
| **LLM: Overall design coherence** | LLM | CAT-04 | — |

---

## 5. Agentic Code Patterns

Dedicated section for code patterns specific to AI/agentic systems. These patterns appear frequently in LLM-generated code, agent orchestration frameworks (LangChain, AutoGen, CrewAI), and AI infrastructure code.

---

### AP-01: Prompt Construction

**Risk:** Prompt injection, unintended behavior, costly API calls from malformed prompts.

#### Deterministic Checks

| Tool | Rule | What It Catches |
|------|------|----------------|
| Ruff | `S608` | SQL-injection pattern — same string interpolation anti-pattern applies to prompt construction |
| Ruff | `ISC001`, `ISC002` | Implicit string concatenation in prompt templates — accidental joins |
| Ruff | `B021` | f-string used as docstring — f-strings in unexpected string positions |

#### LLM Judgment Checks

| Check | What to Look For |
|-------|-----------------|
| Unsanitized user input in prompts | User-provided text directly interpolated into `system` or `user` messages without sanitization. Look for `f"...{user_input}..."` patterns flowing to LLM API calls. |
| Role boundary enforcement | Does the prompt enforce clear separation between system instructions and user content? Concatenated system + user messages are prompt injection vectors. |
| Prompt template exfiltration risk | Does the system prompt include instructions the user should not see? Is it protected from "repeat your instructions" attacks? |
| Jinja2 / template engine use | Any `Environment(autoescape=False)` with user-influenced template variables — XSS and injection risk (Ruff `S701`). |
| Token budget management | Prompts constructed without length checks — can exceed model context limits causing silent truncation. |
| Structured output schemas | Does the code validate that LLM responses conform to expected JSON schema before processing? |

---

### AP-02: LLM API Call Patterns

**Risk:** Hung agents, cost overruns, silent failures, data leakage.

#### Deterministic Checks

| Tool | Rule | What It Catches |
|------|------|----------------|
| Ruff | `S113` | HTTP request without timeout — all LLM API calls are HTTP |
| Ruff | `ASYNC210` | Synchronous HTTP call in async agent — blocks entire event loop |
| Ruff | `S501`, `S323` | SSL verification disabled — MITM risk on API traffic |
| Ruff | `S105–S107` | Hardcoded API keys (OpenAI, Anthropic, etc.) |
| Pylint | `W3101` | `requests` calls without timeout parameter |

#### LLM Judgment Checks

| Check | What to Look For |
|-------|-----------------|
| Retry logic completeness | Are transient API errors (429 rate limit, 503 service unavailable) retried with exponential backoff? Or do they propagate immediately as unhandled exceptions? |
| Model version pinning | Is `model="gpt-4"` or `model="gpt-4-turbo-2024-04-09"` used? Unpinned model names are subject to silent capability changes. |
| Response validation | Is the LLM response checked for expected structure before accessing fields? `response.choices[0].message.content` fails if API returns an error structure. |
| Cost controls | Are `max_tokens` set to prevent runaway generation? Are token counts tracked? |
| Streaming response handling | If streaming, are incomplete responses handled? Is the stream closed properly on error? |
| API key scope | Is the API key scoped to minimum permissions? Is it read from environment variable or secrets manager, not source? |

---

### AP-03: Error Handling in Agent Pipelines

**Risk:** Silent failures that appear as success; cascading failures that bring down entire pipelines.

#### Deterministic Checks

| Tool | Rule | What It Catches |
|------|------|----------------|
| Ruff | `BLE001` | Blind `except:` in agent tool handlers |
| Ruff | `S110` | `try-except-pass` in agent pipeline stages |
| Ruff | `B904` | Exception chaining loss in agent orchestration |
| Ruff | `TRY400` | `logging.error()` instead of `logging.exception()` — loses traceback |
| Pylint | `W0718` `broad-exception-caught` | `except Exception:` hiding tool call failures |

#### LLM Judgment Checks

| Check | What to Look For |
|-------|-----------------|
| Partial success handling | Does the pipeline handle the case where some tools succeed and others fail? Is partial state rolled back or tracked? |
| Structured error returns vs. exceptions | Agent frameworks often expect tools to return error dicts rather than raise exceptions. Is the contract consistent? |
| Timeout vs. exception consistency | When a tool times out, is it treated the same as a failed tool call, or does it propagate differently? |
| Fallback behavior | Does the agent have a meaningful fallback when a tool fails? Or does it silently proceed with missing data? |
| Error context preservation | When errors are logged, do they include the input that caused the failure, the tool that failed, and the pipeline stage? |
| `asyncio.CancelledError` propagation | This must NOT be swallowed. Look for `except Exception:` blocks that would catch it in async agent code. |

---

### AP-04: Credential & Secret Management

**Risk:** Credential exposure in code, logs, process lists, version control.  
**Delegation:** This section identifies credential management patterns for pre-screening. Security assessment of findings is owned by SEC-07 in `SECURITY_CRITIC_FRAMEWORK.md`. Code Hygiene flags the pattern; the Security Critic assesses severity, exploitability, and remediation.

#### Deterministic Checks

| Tool | Rule | What It Catches |
|------|------|----------------|
| Ruff | `S105–S107` | Hardcoded password/secret patterns |
| Ruff | `S108` | Hardcoded temp file paths (secrets written to predictable locations) |
| PSScriptAnalyzer | `PSAvoidUsingConvertToSecureStringWithPlainText` | Plaintext secrets in PowerShell automation |
| PSScriptAnalyzer | `PSAvoidUsingUsernameAndPasswordParams` | String-typed credential parameters |
| PSScriptAnalyzer | `PSAvoidUsingPlainTextForPassword` | Parameter names signaling plaintext credentials |
| PSScriptAnalyzer | `PSUsePSCredentialType` | Credential parameters should be `[PSCredential]` type |

#### LLM Judgment Checks

| Check | What to Look For |
|-------|-----------------|
| Environment variable usage | Are secrets loaded from `os.environ.get()` with no fallback defaults that expose the secret? (e.g., `os.environ.get("API_KEY", "sk-hardcoded-fallback")`) |
| Secrets in log output | Are credentials, tokens, or API keys logged at any log level, including DEBUG? |
| Secrets in exception messages | Exception messages that include credential values (`f"Failed to authenticate with key {api_key}"`) |
| Secrets in function signatures | API keys passed as function parameters vs. injected via configuration objects |
| Version control risk | Are `.env` files or config files with secrets excluded from version control (`.gitignore`)? |
| PowerShell SecureString adequacy | Is `SecureString` used only as a type wrapper while the value is immediately `ConvertFrom-SecureString` back to plaintext? |

---

### AP-05: Timeout & Retry Logic

**Risk:** Hung agents, no forward progress, resource exhaustion from infinite retries.

#### Deterministic Checks

| Tool | Rule | What It Catches |
|------|------|----------------|
| Ruff | `S113` | HTTP requests without timeout |
| Ruff | `ASYNC100` | Timeout scope with no awaitable inside — timeout never fires |
| Ruff | `ASYNC110` | Busy-wait polling loop — use `asyncio.Event` |
| Pylint | `W3101` | `requests` without timeout |

#### LLM Judgment Checks

| Check | What to Look For |
|-------|-----------------|
| Retry with exponential backoff | Is backoff calculated correctly? Is there a maximum retry count? Is there jitter to avoid thundering herd? |
| Retry on correct exception types | Retrying on `ValueError` (logic error) instead of `ConnectionError`/`TimeoutError` wastes calls and can loop forever. |
| Circuit breaker pattern | For high-volume agent systems, is there a circuit breaker that stops retrying a consistently failing service? |
| Timeout scope completeness | Does the timeout cover the entire operation (including connection + read), or just one phase? |
| Retry state isolation | Does retry logic correctly reset or reuse state between attempts? |
| PowerShell retry patterns | `Invoke-WebRequest` / `Invoke-RestMethod` — `-TimeoutSec` present? Retry loop uses `$ErrorActionPreference = 'Stop'`? |

---

### AP-06: Logging & Observability

**Risk:** Undebuggable agents; production failures that leave no trace.

#### Deterministic Checks

| Tool | Rule | What It Catches |
|------|------|----------------|
| Ruff | `LOG001` | Direct `Logger()` instantiation instead of `getLogger()` |
| Ruff | `LOG002` | `getLogger()` not using `__name__` — breaks logger hierarchy |
| Ruff | `LOG007` | `.exception()` with `exc_info=False` — loses traceback |
| Ruff | `LOG015` | Logging on root logger — hard to filter |
| Ruff | `G004` | f-string in log call — eagerly evaluated even when level is disabled |
| Pylint | `W1201` `logging-not-lazy` | `%` format evaluated eagerly in log calls |
| PSScriptAnalyzer | `PSAvoidUsingWriteHost` | `Write-Host` bypasses pipeline; use `Write-Verbose` / `Write-Information` |

#### LLM Judgment Checks

| Check | What to Look For |
|-------|-----------------|
| Structured logging for agent decisions | Does the agent log which tool it chose and why? Which prompt template was used? What the LLM returned before parsing? |
| Log level appropriateness | Is DEBUG used for verbose agent state, INFO for significant events, ERROR for failures — or is everything at one level? |
| Correlation IDs | For multi-step agent pipelines, is there a request/run ID that threads through all log entries? |
| Sensitive data in logs | PII, credentials, or full prompt content in log output — even at DEBUG level. |
| Log coverage at failure points | Are all exception handlers logging before re-raising or returning error? |
| PowerShell transcript risk | Does the script log sensitive data that would appear in PowerShell transcripts if enabled? |

---

## 6. Framework Citation Index

Quick reference: evaluation category → source frameworks.

| Category | ISO 25010 Sub-characteristics | CISQ CWEs | 
|----------|-------------------------------|-----------|
| CAT-01: Code Correctness | Reliability → Faultlessness | CWE-252, CWE-390, CWE-480, CWE-561, CWE-570, CWE-571, CWE-703 |
| CAT-02: Error Handling | Reliability → Fault Tolerance | CWE-248, CWE-252, CWE-390, CWE-391, CWE-703 |
| CAT-03: Resource Management | Performance Efficiency → Resource Utilization | CWE-401, CWE-404, CWE-459, CWE-672, CWE-772, CWE-1088 |
| CAT-04: Complexity & Modularity | Maintainability → Analysability, Modularity, Modifiability | CWE-407, CWE-1047, CWE-1048, CWE-1054, CWE-1064, CWE-1080, CWE-1121 |
| CAT-05: Code Duplication | Maintainability → Reusability | CWE-1041 |
| CAT-06: Naming & Documentation | Maintainability → Analysability; Interaction Capability → Self-Descriptiveness | CWE-1052, CWE-1085 |
| CAT-07: Type Safety | Reliability → Faultlessness | CWE-681, CWE-704, CWE-758 |
| CAT-08: Async & Concurrency | Reliability → Fault Tolerance, Faultlessness | CWE-366, CWE-662, CWE-833, CWE-835, CWE-1088 |
| CAT-09: Import Hygiene | Maintainability → Modularity | CWE-1047, CWE-1048 |
| CAT-10: Style & Formatting | Maintainability → Analysability | CWE-1080, CWE-1085 |
| CAT-11: Portability | Flexibility → Adaptability; Compatibility → Coexistence | CWE-758, CWE-1051 |
| CAT-12: Testability | Maintainability → Testability | (Inferred from CWE-1047 coupling) |
| AP-01: Prompt Construction | Reliability → Fault Tolerance; Security → Integrity | CWE-20, CWE-94 |
| AP-02: LLM API Calls | Reliability → Availability, Fault Tolerance | CWE-252, CWE-1088 |
| AP-03: Agent Pipeline Errors | Reliability → Fault Tolerance, Recoverability | CWE-248, CWE-390, CWE-703 |
| AP-04: Credential Management | Security → Confidentiality | CWE-259, CWE-321, CWE-798 |
| AP-05: Timeout & Retry | Reliability → Availability | CWE-1088, CWE-835 |
| AP-06: Logging & Observability | Security → Non-repudiation; Maintainability → Analysability | CWE-778 |

---

### SEI CERT Applicability Note

SEI CERT Coding Standards cover C, C++, Java, Perl, and Android — **there is no official CERT standard for Python or PowerShell**. Where CERT principles transfer by analogy (e.g., FIO02-C for path canonicalization, ENV33-C for command injection, MSC30-C for random number generation), this framework cites them as `CERT XXX-C analog` to indicate the principle applies but no official rule exists for the target language. CERT is not cited as a grounding standard for Python/PowerShell quality assessment. See `SECURITY_CRITIC_FRAMEWORK.md` §6 for the full CERT applicability analysis.

---

## 7. Delegation Severity Cap

**Design intent:** Code Hygiene assigns **LOW or MEDIUM severity only** for security-adjacent
patterns (eval/exec, Invoke-Expression, hardcoded credentials, unsanitized prompt inputs).
This is intentional — security severity, exploitability, and remediation assessment for these
patterns is delegated to the Security Critic.

**Rationale:** Assigning HIGH/CRITICAL from the Code Hygiene Critic for patterns that the
Security Critic also evaluates would create artificial severity inflation through aggregation.
The Code Hygiene finding exists for traceability (code is hard to audit/test); the Security
Critic provides the risk verdict.

**Finding format for delegated patterns:**
```
"Code hygiene concern: [pattern] is difficult to audit and test.
Security severity and exploitability assessment delegated to SecurityCritic."
Severity: LOW or MEDIUM (hygiene concern only)
```

---

*Framework version: 1.1 · Updated: 2026-03-06*  
*Sources: ISO/IEC 25010:2023, ISO/IEC 5055:2021 (CISQ/OMG ASCQM), Ruff v0.9.x rule set, Pylint v4.0.x checker docs, PSScriptAnalyzer latest*
