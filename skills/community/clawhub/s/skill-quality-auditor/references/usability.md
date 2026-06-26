# D4: Usability

## Rubric

| Score | Meaning |
|-------|---------|
| 9-10 | Solves a real problem elegantly. Easy to maintain and extend. |
| 7-8 | Practical and well-maintained. Minor issues. |
| 5-6 | Useful but has maintainability or dependency concerns. |
| 3-4 | Marginal value or hard to maintain. |
| 1-2 | No practical value or unmaintainable. |

## Scoring Rules

Start at 10. Apply deductions. **Floor = 1**.

- **Major (-2):** Problems that prevent practical use or make maintenance impossible.
- **Minor (-1):** Maintainability friction, minor dependency issues.

**Subjective items (marked ⚠️):** Assess conservatively. When uncertain, don't deduct. Document your reasoning.

## Checklist

### Practical Value
- [ ] Major ⚠️: Skill doesn't solve a problem the base model already handles (e.g., a skill that just teaches "how to write markdown")
- [ ] Minor: Target users not identifiable from description

### Maintainability
- [ ] Major: Patterns/lists/configs hardcoded in shell scripts (should use JSON/YAML)
- [ ] Minor: No documented update path (how to add patterns, fix errors, evolve the skill)
- [ ] Minor: Magic numbers or unexplained constants

### Dependency Sanity
- [ ] Major: Unnecessary binaries required
- [ ] Minor: Requires CLI tool but doesn't specify how to install
- [ ] Minor: Dependencies not justified (no explanation of why each is needed)

### Cross-Platform
- [ ] Minor: Hardcoded platform-specific paths (/usr/local/ without fallback, etc.)
- [ ] Minor: Shell scripts use `#!/bin/bash` instead of `#!/usr/bin/env bash`
- [ ] Minor: Claims Windows support but no actual Windows handling

### Graceful Degradation
- [ ] Minor: No fallback or error message when optional dependency is missing
