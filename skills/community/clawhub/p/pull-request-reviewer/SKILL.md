# pr-reviewer

## Description
Review pull requests and code diffs across any language. Finds logic bugs, missing tests, security holes, breaking API changes, and naming problems before they merge. Returns a structured report: block-merge issues first, then warnings, then style suggestions.

## Use when
- "review my PR"
- "check this diff"
- "is this PR mergeable"
- "what's wrong with this change"
- "code review"
- Any git diff, patch file, or PR description paste

## Supported languages
Any language with a git diff. Specialised checklist for: Python, JavaScript/TypeScript, C#, Go, Rust, Java/Kotlin, SQL migrations.

## Input
Paste one of:
- A git diff (`git diff main...feature-branch`)
- A GitHub/GitLab PR URL (if accessible)
- Raw code with a description of what it changes

Optionally specify: target branch, framework, whether this is a library (breaking changes matter more) or an app.

## Output format

```
## PR Review

### Block Merge
- [Finding] — [why this must be fixed before merging]
  ✗ Problem: [problematic code]
  ✓ Fix:     [corrected code]

### Warnings (fix before next release)
- [Finding] — [explanation]

### Suggestions (style / future-proofing)
- [Finding] — [explanation]

### Approved
- [Specific patterns done right — always include at least one]

### Summary
[2–3 sentences: biggest risk, top fix, overall verdict (merge / fix first / needs major work)]
```

## Review checklist

### Logic & correctness
- Off-by-one errors in loops or slices
- Null/nil dereference without guard
- Incorrect error handling (swallowed, wrong type checked)
- Wrong variable captured in closure/lambda
- Race condition introduced (shared mutable state, no lock)
- Missing edge case (empty input, zero value, max value)

### Security
- User input used without sanitisation (SQL, shell, HTML)
- Secret or credential added to source (API key, password, token)
- Insecure deserialization
- Overly permissive CORS / auth bypass
- Path traversal risk

### Tests
- New behaviour with zero test coverage
- Test that only tests the happy path (no error case)
- Mock that makes the test vacuously pass
- Missing assertion (test calls but never asserts)

### API / interface
- Public method signature changed without deprecation
- Required parameter added to existing public function
- Return type narrowed or widened unexpectedly
- Serialised field renamed (breaks existing clients)

### Performance
- N+1 query introduced
- Unbounded loop over user-supplied collection
- Synchronous I/O in async context
- Large allocation in hot path

### Style
- Inconsistent naming with surrounding code
- Dead code left in (commented-out blocks, unused variables)
- TODO left without ticket reference
- Misleading variable/function name

## Severity definitions
- **Block Merge:** Correctness bug, security hole, data loss risk, or breaking API change — must be fixed
- **Warning:** Performance issue, missing test coverage, or hard-to-debug behavior — fix before release
- **Suggestion:** Style, clarity, or maintainability improvement — up to the author

## Self-improvement instructions
After each review, note the most common finding category (logic, security, tests, API, performance, style). After 20 reviews, surface the top 3 patterns as "Most common PR issues in [language]" to help users learn, not just fix.
