# Pattern 3: Reviewer

## Core Purpose

Separate **review criteria** from **review logic**, using external checklists for modular auditing.

## Use Cases

- Code Review
- Security audits (OWASP)
- Compliance checks
- Design reviews
- Documentation quality checks

## Directory Structure

```
skills/code-reviewer/
├── SKILL.md
└── references/
    └── review-checklist.md   # Review checklist
```

## SKILL.md Template

```markdown
---
name: code-reviewer
description: Python code quality review. Activates when users submit code for feedback, request review, or need code audit.
metadata:
  pattern: reviewer
  severity-levels: [error, warning, info]
  trigger-phrases: [code review, review this, check code, audit this]
---

You are a Python code reviewer. **Strictly follow this flow**:

## Step 1: Load Checklist
Load `references/review-checklist.md` to get complete review criteria.

## Step 2: Understand Code Intent
Read user's code first, understand its function and goals.
**Prohibit** finding faults without understanding intent.

## Step 3: Apply Checklist Item by Item
For each rule in checklist:
1. Check if code complies
2. If violation, record: line number + severity + reason + fix suggestion

## Step 4: Generate Structured Report

Output format as follows:

### 📊 Overview
- **Function**: What this code does
- **Overall quality**: One-sentence evaluation

### 🚨 Errors (must fix)
{{List all error-level issues}}

### ⚠️ Warnings (recommended to fix)
{{List all warning-level issues}}

### ℹ️ Tips (consider optimizing)
{{List all info-level issues}}

### 📈 Score
**X/10** - Scoring rationale

### 🎯 Top 3 Recommendations
{{Top 3 improvement suggestions ranked by impact}}
```

## references/review-checklist.md Template

```markdown
# Python Code Review Checklist v2.0

## P0 - Errors (must fix)

### Security
- [ ] Hardcoded passwords/keys/API tokens
- [ ] SQL injection risks (string-concatenated SQL)
- [ ] Command injection risks (os.system with user input)
- [ ] Sensitive information printed to logs

### Correctness
- [ ] Unhandled exceptions (bare except)
- [ ] Resources not released (files/connections not closed)
- [ ] Race condition risks
- [ ] Boundary conditions not handled (empty lists/None/negative numbers)

## P1 - Warnings (recommended to fix)

### Readability
- [ ] Functions over 50 lines
- [ ] Nesting over 4 levels
- [ ] Unclear variable naming (single letter/meaningless)
- [ ] Missing type annotations

### Performance
- [ ] Repeated calculations inside loops
- [ ] Unnecessary list copies
- [ ] Using list instead of generators
- [ ] N+1 query problems

### Maintainability
- [ ] Duplicate code (DRY principle)
- [ ] Magic numbers (undefined constants)
- [ ] Overly long parameter lists (>5)
- [ ] Missing docstrings

## P2 - Tips (can optimize)

### Best Practices
- [ ] Could use standard library instead of custom implementation
- [ ] Could use more Pythonic写法
- [ ] Could add unit tests
- [ ] Could add type hints
```

## Variants: Domain-Specific Reviewer

### Security Audit

```markdown
references/security-checklist.md
- OWASP Top 10
- Authentication/authorization checks
- Data encryption checks
- Log audit checks
```

### Frontend Design Review

```markdown
references/design-checklist.md
- Responsive layout
- Accessibility (a11y)
- Color contrast
- Interaction feedback
- Loading state handling
```

### EDA Code Review

```markdown
references/rtl-checklist.md
- Synthesizability checks
- Timing constraints
- Reset strategy
- Clock domain crossing
- Area optimization suggestions
```

## Output Example

```markdown
### 📊 Overview
- **Function**: User login validation, includes password hashing and JWT generation
- **Overall quality**: Core logic correct, but has 2 security risks

### 🚨 Errors (must fix)
1. **Line 15** - Hardcoded JWT_SECRET
   - Risk: Key leak allows Token forgery
   - Fix: Read from environment variable `os.environ.get("JWT_SECRET")`

2. **Line 28** - Bare except catches all exceptions
   - Risk: Masks real errors, hard to debug
   - Fix: Catch specific exception types `except AuthenticationError:`

### ⚠️ Warnings (recommended to fix)
1. **Line 10** - Function 65 lines, recommend splitting
2. **Line 33** - Missing type annotations

### 📈 Score
**6/10** - Functional but has serious security issues

### 🎯 Top 3 Recommendations
1. Remove hardcoded keys immediately (security risk)
2. Add input validation and parameter checks
3. Split function into validate_user() + generate_token()
```

## Pros & Cons

| Pros | Cons |
|-----|------|
| Checklists can be updated independently | Checklist design needs domain experts |
| Reusable (change checklist = change scenario) | May generate大量 low-value tips |
| Structured output, easy to automate | Severity classification may be subjective |

## Automation Extensions

### CI Integration

```bash
# Review output in JSON format for CI parsing
{
  "score": 6,
  "errors": [...],
  "warnings": [...],
  "info": [...]
}
```

### LLM-as-a-judge Integration

```markdown
## Step 5: Secondary Validation
Send review results to another LLM instance:
"Please evaluate if above review is reasonable, any omissions or misjudgments?"
```

---

## Checklist

- [ ] `references/checklist.md` exists with clear categorization
- [ ] Severity levels clear (error/warning/info)
- [ ] SKILL.md requires understanding code intent before review
- [ ] Output format is structured
- [ ] Has scoring mechanism and Top recommendations
