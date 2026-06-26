---
name: ai-code-reviewer
description: Automated code review — security vulnerabilities, performance issues, best practices, refactoring suggestions, and documentation gaps. Supports Python, JavaScript/TypeScript, Go, Rust, and more. PR-ready review comments.
metadata:
  version: 1.0.0
  author: TKDigital
  category: Developer Tools
  tags: [code review, security, performance, refactoring, best practices, pull request, developer tools]
---

# AI Code Reviewer

Comprehensive automated code reviews — security, performance, best practices, and refactoring suggestions.

## What It Does

1. **Security Scan** — SQL injection, XSS, SSRF, secrets in code, insecure dependencies
2. **Performance Analysis** — N+1 queries, memory leaks, inefficient loops, caching opportunities
3. **Best Practices** — Code style, naming conventions, SOLID principles, DRY violations
4. **Refactoring Suggestions** — Concrete before/after code improvements
5. **Documentation Gaps** — Missing docstrings, unclear function names, no type hints
6. **Complexity Analysis** — Cyclomatic complexity, function length, nesting depth
7. **PR-Ready Comments** — Output formatted as pull request review comments

## Usage

### Full Code Review
```
Review this code for security, performance, and best practices:

Language: [Python/JavaScript/TypeScript/Go/Rust]
Context: [What does this code do?]
Priority: [Security first / Performance first / General review]

[Paste code or file path]

For each issue found:
1. Severity (critical/high/medium/low)
2. Category (security/performance/style/bug)
3. Line reference
4. What's wrong
5. How to fix (with corrected code)
```

### Security-Focused Review
```
Security audit this code. I'm looking for:
- SQL injection vulnerabilities
- XSS attack vectors
- Authentication/authorization bypasses
- Secrets or credentials in code
- Insecure dependencies
- SSRF/CSRF vulnerabilities
- Input validation gaps

Language: [Language]
[Paste code]
```

### Performance Review
```
Analyze this code for performance issues:
- Database query efficiency (N+1, missing indexes)
- Memory usage and potential leaks
- Algorithm complexity (can it be optimized?)
- Caching opportunities
- Async/concurrency improvements

Context: This handles [X requests/second] and processes [Y data]
[Paste code]
```

### Refactoring Guide
```
Suggest refactoring improvements for this code:
- Reduce complexity
- Improve readability
- Apply design patterns where beneficial
- Remove duplication
- Improve testability

Show before/after for each suggestion.
[Paste code]
```

### PR Review Format
```
Review this pull request diff:

[Paste diff or describe changes]

Output as PR comments:
- File: [filename]
- Line: [number]
- Comment: [review comment]
- Suggestion: [code suggestion if applicable]
```

## Output Format

```
# Code Review Report

**Files Reviewed**: [count]
**Language**: [language]
**Overall Score**: [X/100]

## 🔴 Critical Issues ([count])

### Issue 1: [Title]
- **Severity**: Critical
- **Category**: Security
- **Location**: [file:line]
- **Problem**: [Description]
- **Impact**: [What could happen]
- **Fix**:
  ```[language]
  // Before (vulnerable)
  [old code]
  
  // After (fixed)
  [new code]
  ```

## 🟡 Warnings ([count])
[Medium-severity issues]

## 🔵 Suggestions ([count])
[Low-severity improvements]

## 🟢 Positive Observations
[What's already good about the code]

## Summary
- Critical: [X] (must fix before merge)
- Warnings: [X] (should fix soon)
- Suggestions: [X] (nice to have)
- Score: [X/100]
```

## Supported Languages
- Python (3.8+)
- JavaScript / TypeScript
- Go
- Rust
- Ruby
- PHP
- Java / Kotlin
- C / C++
- Shell / Bash

## Best Practices

- Provide context about what the code does — better context = better review
- Specify your priority (security vs performance vs general)
- For large codebases, review one module/file at a time
- Pair with `security-auditor` for infrastructure-level security checks
- Use the PR format output to paste directly into GitHub/GitLab reviews

## References

- `references/security-patterns.md` — Common vulnerability patterns by language
- `references/performance-patterns.md` — Common performance anti-patterns
