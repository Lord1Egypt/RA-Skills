# AI Code Review

Systematic code review framework covering security vulnerabilities, performance bottlenecks, maintainability issues, and best practices across major programming languages.

## Description

This skill provides a structured approach to reviewing code like a senior engineer. It produces actionable, prioritized feedback organized by severity (Critical / Warning / Suggestion) and category (Security / Performance / Maintainability / Correctness / Style). Works across Python, JavaScript/TypeScript, Go, Rust, Java, and other common languages.

## When to Use

- Reviewing a pull request or code submission
- Auditing code for security vulnerabilities before deployment
- Identifying performance issues in hot paths
- Onboarding new developers with consistent review standards
- Reviewing AI-generated code for production readiness

## Instructions

### Review Process

#### Phase 1: Quick Scan (30 seconds)

Before deep analysis:
1. **Understand intent**: What does this code do? Read commit message or PR description.
2. **Check scope**: Is the change focused, or does it touch unrelated files?
3. **Assess risk**: Does this modify auth, payment, data persistence, or external APIs? Flag as high-risk.

#### Phase 2: Category-by-Category Review

##### Security (🔴 Critical if found)

Check for these common vulnerabilities:

| Vulnerability | Pattern to Look For |
|--------------|-------------------|
| **SQL Injection** | String concatenation in queries, raw SQL without parameterization |
| **XSS** | Unescaped user input rendered in HTML, `innerHTML` with user data |
| **Path Traversal** | User-controlled file paths, `../` not sanitized |
| **Hardcoded Secrets** | API keys, passwords, tokens in source code |
| **Insecure Deserialization** | `eval()`, `pickle.loads()`, `JSON.parse` on untrusted data |
| **IDOR** | Missing authorization checks on resource access endpoints |
| **Command Injection** | `os.system()`, `exec()`, `subprocess` with user input |
| **Broken Auth** | Weak password hashing, missing rate limiting, JWT without validation |

For each finding, specify:
- The vulnerable code location
- Attack scenario
- Recommended fix with code example

##### Performance (🟡 Warning if found)

Check for:
- **N+1 queries**: Database calls inside loops
- **Unbounded operations**: Loops without limits on user-controlled data size
- **Memory leaks**: Unclosed connections, unbounded caches, event listeners not removed
- **Inefficient algorithms**: O(n²) where O(n) suffices, unnecessary copies
- **Synchronous blocking**: File I/O or HTTP calls on the main thread/event loop
- **Missing pagination**: Loading full datasets instead of paginated results
- **Redundant computations**: Repeated calculations that could be cached

##### Correctness (🔴 Critical if found)

Check for:
- **Off-by-one errors**: Loop bounds, index calculations, substring operations
- **Null/undefined handling**: Missing null checks before dereferencing
- **Race conditions**: Shared mutable state without synchronization
- **Error handling**: Swallowed exceptions, missing error cases, overly broad catch
- **Edge cases**: Empty inputs, negative numbers, zero, max values, Unicode
- **Type mismatches**: Comparing different types, implicit coercions

##### Maintainability (🟢 Suggestion if found)

Check for:
- **Function length**: Functions over 30 lines should be considered for splitting
- **Complexity**: Deep nesting (>3 levels), long parameter lists (>5 params)
- **Naming**: Single-letter variables (except loop indices), ambiguous names, inconsistency
- **Duplication**: Repeated logic that should be extracted
- **Dead code**: Unused imports, unreachable branches, commented-out code
- **Magic numbers**: Unexplained numeric literals

#### Phase 3: Output Format

Organize findings as:

```
## Code Review Summary

**Overall Assessment**: [Ready to merge / Needs changes / Request changes]

### 🔴 Critical (must fix)
1. [Category] **Title**: Description + Location + Fix suggestion

### 🟡 Warning (should fix)
1. [Category] **Title**: Description + Location + Fix suggestion

### 🟢 Suggestion (nice to have)
1. [Category] **Title**: Description + Location + Fix suggestion

### ✅ Highlights
- Things done well (positive reinforcement)
```

### Language-Specific Rules

**Python:**
- Use type hints for public functions
- Prefer `pathlib.Path` over `os.path`
- Use context managers for resources
- Follow PEP 8 line length (88 chars for Black, 79 for flake8)

**JavaScript/TypeScript:**
- Use `const` by default, `let` only when reassignment needed
- Prefer `interface` over `type` for object shapes in TypeScript
- Avoid `any` — use `unknown` and narrow with type guards
- Use optional chaining (`?.`) and nullish coalescing (`??`) over manual checks

**Go:**
- Handle errors explicitly — never use `_ = err`
- Keep functions under 50 lines
- Use table-driven tests
- Accept interfaces, return structs

## Examples

**Finding Example:**
```
🔴 Critical [Security] SQL Injection in user lookup
Location: src/auth/login.py:42
The `username` parameter is directly interpolated into the SQL query:
  cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
Fix: Use parameterized queries:
  cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
```

**Suggestion Example:**
```
🟢 Suggestion [Maintainability] Extract magic number
Location: src/utils/cache.py:18
The value 86400 appears without explanation. It represents seconds in a day.
Fix: Define as a named constant:
  CACHE_TTL_SECONDS = 86_400  # 24 hours
```

## Tips

- Review the diff, not the full file — focus on what changed
- Always check the test coverage for changed code
- Use automated tools (linter, type checker, security scanner) first — human review should catch what tools miss
- When suggesting changes, provide the fixed code, not just the description
- Be specific about severity — calling everything "critical" dilutes real critical issues
