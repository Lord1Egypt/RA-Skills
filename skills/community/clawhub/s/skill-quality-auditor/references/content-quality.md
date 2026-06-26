# D2: Content Quality

## Rubric

| Score | Meaning |
|-------|---------|
| 9-10 | Every claim accurate, every instruction clear and complete. |
| 7-8 | Solid. Minor inaccuracies or missing edge cases. |
| 5-6 | Mostly correct but has vague instructions or gaps. |
| 3-4 | Multiple problems: outdated info, unclear steps, missing coverage. |
| 1-2 | Broken or actively misleading. |

## Scoring Rules

Start at 10. Apply deductions. **Floor = 1**.

- **Major (-2):** Factually wrong, instructions ambiguous enough to cause agent failure.
- **Minor (-1):** Minor gaps, missing examples, polish issues.

**No double-counting** with D1: if an issue is structural (belongs in D1), don't also deduct here.

## Checklist

### Accuracy
- [ ] Major: Claims about tools/CLI/APIs are wrong or outdated
- [ ] Major: Made-up capabilities or features that don't exist
- [ ] Minor: Incorrect version numbers, URLs, or paths in examples

### Clarity
- [ ] Major: Instructions ambiguous — agent would have to guess
- [ ] Minor: Steps lack clear ordering (not numbered where order matters)
- [ ] Minor: Conditional logic implicit instead of explicit

### Completeness
- [ ] Major: Doesn't cover functionality promised in description
- [ ] Major: TODO/placeholder content in published skill
- [ ] Minor: Empty sections or stub headings

### Examples
- [ ] Minor: Missing examples where they'd clearly help
- [ ] Minor: Examples are outdated or syntactically incorrect
- [ ] Minor: Abstract descriptions where concrete commands/output would be better
- [ ] Major: Examples contain unsafe commands (curl|bash, pip install from untrusted URLs, etc.)

### Error Handling
- [ ] Minor: No guidance for missing dependencies
- [ ] Minor: No guidance for tool/service unavailability

### Verifiability
- [ ] Minor: Steps lack verification (no "expect X output" or "verify by Y")
