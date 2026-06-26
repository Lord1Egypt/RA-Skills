# Code Correctness Analysis

Deep analysis of generated code for semantic correctness, logic errors,
and issues that tooling cannot catch. Runs as part of verify after every
task or range. Loaded by [verify.md](verify.md) — not triggered directly.

## When to Use

- When verify.md runs (after every task or range)
- Focuses on what LLM code reading catches that linters, type checkers,
  and test suites cannot: semantic correctness, logic errors, architectural
  issues

## When to Skip

- Quick mode (verify itself is skipped)
- Task only changed configuration, documentation, or static assets

## Workflow

### Step 1: Detect Project Tooling

Scan the project root for linter, type checker, and static analysis configs.
Read active rules and plugins to determine what is already covered.

| What to Find | Where to Check |
|--------------|----------------|
| Language/runtime | Manifest: package.json, pyproject.toml, go.mod, Cargo.toml, Gemfile, composer.json, *.csproj |
| Linter + active rules | Config files in project root -- read plugins/rules to determine coverage |
| Type checker + strictness | Language-specific config (strict mode, strict null checks, etc.) |
| Security scanner | Dedicated tools or linter plugins with security rules |
| Accessibility checker | Linter plugins with a11y rules |
| Test framework | Scripts or configs in manifest |
| Project conventions | `.artifacts/codebase/{area}.md` cache (if exists), else representative files |

Build a **tooling coverage map**: for each category below, note whether
active tooling already covers it (fully, partially, or not at all).

If the `.artifacts/codebase/{area}.md` cache exists for this area, read
project patterns (error handling conventions, data fetching approach,
auth strategy, etc.) to better calibrate which categories are most
relevant and what the project already handles by convention. Otherwise
scan a few representative files.

### Step 2: Select Relevant Categories

From the 24 categories below, select ONLY those that:

1. **Apply to the project's technology** -- no framework-specific checks for
   projects that don't use that framework
2. **Relate to code changed in the current task** -- skip database categories
   if no data layer code changed
3. **Are NOT covered by active tooling** -- skip TOOLING-ASSISTED categories
   when the relevant tooling is detected in Step 1

Target: 5-10 categories per analysis. Never run all 24 on a single pass.

### Step 3: Analyze Selected Categories

Read the changed files and analyze against each selected category.

Report only findings with >= 80% confidence. Flag uncertain findings
explicitly with "(uncertain)" in the description.

#### Tier 1 -- High Confidence

Categories where LLM code reading produces reliable results.

| # | Category | Detects | Tooling-Assisted |
|---|----------|---------|------------------|
| 1 | Missing error handling | Async without try/catch, unhandled promise rejections, empty catch blocks, unchecked error returns | No |
| 2 | Unhandled edge cases | Null/undefined not checked, empty collections not handled, division by zero, missing default branches | No |
| 3 | Race conditions | Shared state without synchronization, stale closures over mutable state, concurrent writes to same resource | No |
| 4 | Memory leaks | Event listeners not removed, subscriptions without cleanup, intervals/timers without clear, growing caches without eviction | No |
| 5 | Framework-specific violations | Hook rules (conditional calls, wrong deps), lifecycle misuse, directive errors, middleware ordering | Yes: skip if framework linter plugin active |
| 6 | Dead code paths | Unreachable code after return/throw, branches that never execute, logic shadowed by early returns | Partial: skip trivial cases if linter has unreachable-code rules |
| 7 | Type safety gaps | Any/unknown types, unsafe type assertions, missing type narrowing before access, implicit any | Yes: skip if type checker runs in strict mode |
| 8 | Inconsistent state | State updates that can leave UI/data in invalid state, partial updates without atomicity, derived state out of sync | No |
| 9 | API contract mismatch | Response handling that ignores optional fields, wrong HTTP status codes, request body missing required fields | No |
| 10 | Security vulnerabilities | XSS via unsanitized output, SQL/command injection, insecure randomness for security, hardcoded secrets, path traversal | Partial: skip if security linter/scanner active |

#### Tier 2 -- Medium Confidence

Categories requiring deeper reasoning about data and control flow.

| # | Category | Detects | Tooling-Assisted |
|---|----------|---------|------------------|
| 11 | Boundary conditions | Off-by-one errors, integer overflow, string truncation, timezone/DST edge cases, locale-dependent comparisons | No |
| 12 | Resource exhaustion | Unbounded loops, queries without pagination or limit, caches growing without eviction, file handles not closed | No |
| 13 | Concurrency issues | Double-submit without debounce, optimistic updates without rollback, stale reads after write, lost updates | No |
| 14 | Error propagation | Errors swallowed silently (catch without rethrow/log), missing error boundaries, fallback logic that hides failures | No |
| 15 | Data integrity | Partial writes without transaction, cascade operations not considered, orphan records after delete, constraint violations | No |
| 16 | Auth/authz gaps | Routes or operations without auth check, privilege escalation paths, insecure token storage or transmission | No |
| 17 | Input validation | User inputs without sanitization, missing length/range limits, format validation absent at system boundary | Partial: skip if schema validation lib covers all inputs |
| 18 | Dependency misuse | Deprecated API usage, incorrect lib arguments, missing required configuration, version-incompatible patterns | No |

#### Tier 3 -- Contextual Detection

Categories that depend on knowing the project and domain.

| # | Category | Detects | Tooling-Assisted |
|---|----------|---------|------------------|
| 19 | Performance anti-patterns | N+1 queries, unnecessary re-renders, missing memoization where expensive, large bundle imports for small usage | Partial: skip if perf-focused linter rules active |
| 20 | Accessibility gaps | Missing aria labels, keyboard navigation absent, focus management issues, semantic HTML misuse | Partial: skip if a11y linter plugin active |
| 21 | Internationalization | Hardcoded user-facing strings, locale-dependent date/number formatting, RTL layout not considered | No |
| 22 | Observability gaps | Critical operations without logging, error logs missing context (IDs, params), silent failures in background jobs | No |
| 23 | Configuration drift | Hardcoded values that should be env vars, magic numbers without explanation, environment-specific logic in shared code | No |
| 24 | Backward compatibility | Breaking changes in public APIs, schema migrations without fallback, removed fields still referenced by consumers | No |

### Step 4: Report Findings

Use the same format as verify.md findings with an added Category column:

| Finding | Severity | Category | Description |
|---------|----------|----------|-------------|
| Example | high | Race conditions | `fetchUser` and `updateUser` can run concurrently, causing stale data overwrite |

Severity levels:
- **critical**: Breaks core functionality, data loss, security breach
- **high**: Incorrect behavior under normal conditions, must fix before proceeding
- **medium**: Incorrect behavior under edge conditions, fix recommended
- **low**: Potential issue, note for awareness

Findings merge into verify.md's outcome determination (Step 7).

## Guidelines

**DO:**
- Detect tooling coverage BEFORE selecting categories
- Skip TOOLING-ASSISTED categories when relevant tooling is active
- Select only categories relevant to the code changed in this task
- Use >= 80% confidence threshold for reporting findings
- Merge findings into verify.md's outcome determination
- Include concrete code references (file, line, function) in findings

**DON'T:**
- Run all 24 categories on every analysis
- Report issues that linters or type checkers already catch
- Check framework-specific categories in projects that don't use that framework
- Flag style or formatting issues (that is tooling territory)
- Assume tooling is absent -- always check config files first
- Report findings below 80% confidence without flagging as uncertain
- Duplicate findings already reported by verify.md's other steps

## Error Handling

- No manifest found: assume minimal tooling, run more categories
- Cannot determine language/stack: ask user what stack is in use
- All categories covered by tooling: report "All code correctness categories
  covered by project tooling" and skip analysis
- Uncertain finding: flag as "(uncertain)" in description, never mark as
  critical or high severity
- No area cache: rely on config file scan only
- Changed files not identifiable: ask user which files to analyze
