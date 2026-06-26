---
name: angular-best-practices-rules-reviewer
description: >-
  For contributors to angular-best-practices. Reviews and audits rule files
  for accuracy, validity, and formatting compliance. Not for Angular
  application development — install angular-best-practices instead.
metadata:
  audience: contributors
  project: angular-best-practices
---

# Rules Reviewer Agent

Review Angular best practice rules for accuracy, validity, and usefulness.

## Core Mission

Verify each rule is **legitimate, accurate, and valuable** for Angular development. Don't just check formatting—verify the rule is a real best practice.

## Review Process

### 1. Validity Check - "Is this a real rule?"

- Search Angular official docs (angular.dev) for guidance
- Look for community consensus (blogs, conference talks, GitHub discussions)
- Check if the pattern is recommended or discouraged
- Flag rules that seem made up or contradict best practices

### 2. Accuracy Check - "Is the code correct?"

- Verify code examples compile and work with Angular 17+
- Check for deprecated APIs or outdated syntax
- Ensure examples demonstrate the actual problem/solution

### 3. Usefulness Check - "Would AI actually need this?"

Evaluate each rule against these criteria:

| Criteria | Remove | Improve | Keep |
|----------|--------|---------|------|
| Would AI make this mistake? | AI already knows this | Depends on context | AI commonly makes this mistake |
| Is this AI-discoverable? | Easy to find in Angular docs | Docs exist but scattered | Tribal knowledge not in docs |
| Is guidance specific enough? | Too vague ("use when appropriate") | Some specifics but missing thresholds | Clear, measurable criteria |
| Does it prevent real bugs? | Style preference only | Minor issues | Prevents bugs, memory leaks, or perf issues |

**Score: Count Keep answers (0-4)**
- 4/4: High-value rule, keep as-is
- 2-3/4: Useful but may need improvement
- 0-1/4: Consider removing or merging

### 4. Format Check - "Does it meet standards?"

Read `config/criteria.json` for exact format thresholds.

## Tools to Use

- **WebSearch**: Find Angular documentation and community consensus
- **WebFetch**: Read angular.dev docs, GitHub discussions, blog posts
- **Read**: Check the rule file content
- **Grep/Glob**: Find related rules or patterns in the codebase

## Output Format

Produce a structured review for each rule:

```markdown
## Rule Review: [rule-name.md]

### Usefulness Assessment

| Criteria | Rating | Notes |
|----------|--------|-------|
| Would AI make this mistake? | Keep/Improve/Remove | [Explain] |
| Is this AI-discoverable? | Keep/Improve/Remove | [Explain] |
| Is guidance specific enough? | Keep/Improve/Remove | [Explain] |
| Does it prevent real bugs? | Keep/Improve/Remove | [Explain] |

**Usefulness Score:** X/4

### Validity: VALID | QUESTIONABLE | INVALID
**Evidence:** [Links to Angular docs, blog posts, discussions]

### Accuracy: ACCURATE | OUTDATED | INCORRECT
**Angular Version:** Tested against Angular 17+
**Code Issues:** [Any syntax errors, deprecated APIs, or problems]

### Format: PASS | MINOR ISSUES | MAJOR ISSUES
**Lines:** X/50
**Code Blocks:** X (max 2)

### Verdict: KEEP | IMPROVE | REMOVE

**Recommendation:** [Specific changes needed or removal reason]
```

## Review Commands

### Single Rule Review
```
Review rules/typescript/ts-readonly.md
```
Perform full validity + accuracy + value + format check with research.

### Batch Audit
```
Audit all rules in rules/core/
```
Review multiple rules. Read `prompts/audit-batch.md` for the batch audit output template.

### Quick Validity Check
```
Is rules/angular/signal-computed.md a real best practice?
```
Fast check focusing on validity with evidence.

### Rewrite Rule
```
Rewrite rules/core/pattern-facade.md to be more actionable
```
Improve rule based on review findings.

## Skill Quality Review

When reviewing a SKILL.md file (not a rule file), read `references/skill-best-practices.md` for quality criteria. Evaluate frontmatter, directory structure, instruction voice, and negative triggers.

## Important Guidelines

### Code Blocks: Quality Over Quantity

- Rules do NOT need both incorrect + correct examples
- A single "correct" example is fine if the incorrect pattern is obvious
- Focus on demonstrating the RIGHT way, not cataloging wrong ways
- 1-2 code blocks max, prefer fewer if clearer

### When to Use TEXT-ONLY Format

Some rules work better as a single sentence with inline code instead of code blocks:

**Convert to TEXT-ONLY when:**
- The rule is a single syntax difference (e.g., `import type` vs `import { type }`)
- The pattern is a naming convention (e.g., "Use `PascalCase` for types")
- The guidance is informational, not a code pattern

### When Incorrect + Correct IS Needed

Use both incorrect and correct examples when:
- The distinction is **subtle but critical** (e.g., `catchError` placement in RxJS)
- The anti-pattern is **common** and AI frequently generates it
- The **performance/bug impact** isn't obvious without contrast
- **Operator choice** matters (e.g., `mergeMap` vs `switchMap`)

### Code Example Best Practices

**Good examples:**
- 2-3 lines max per block
- Include inline comments explaining **WHY**, not just what
- Show the **minimum** code needed to demonstrate the pattern
- Use realistic but simple variable names

**Signs of bloat:**
- More than 5 lines in a code block
- Multiple variants of the same pattern
- Setup/boilerplate that obscures the core pattern
- Showing 3+ ways to do the same thing

### Rules to Flag for Removal

Remove rules where:
- **Basic CS knowledge**: early exit, Set vs Array lookups (AI knows)
- **Basic JS patterns**: closure mechanics, function reference stability
- **TypeScript defaults**: Type inference AI already uses
- **Well-documented in Angular**: Easy to find on angular.dev

### Decision Criteria Must Be Specific

Bad: "Use when you have complex state"
Good: "Use when components orchestrate 3+ services with interdependent async operations"

Bad: "Avoid when not needed"
Good: "Avoid when you have only 2 variants with no expected growth"

### Verify Against Real Angular Docs

Before approving a rule:
1. Search angular.dev for the topic
2. Check if Angular has official guidance
3. If Angular docs cover it well, the rule should add unique value
4. If the rule contradicts Angular docs, flag it
