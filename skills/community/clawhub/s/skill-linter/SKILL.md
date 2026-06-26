---
name: skill-linter
description: Analyze and validate SKILL.md files for best practices, common issues, and improvement suggestions. Use when reviewing a Skill, creating a new Skill, or when asked to check/audit/improve a SKILL.md file.
allowed-tools: Read, Edit, Write
---

# Skill Linter & Advisor

Analyze SKILL.md files against Claude Code Skills best practices and provide actionable feedback.

## Analysis Process

1. **Read the SKILL.md file** - Load the complete content
2. **Parse frontmatter** - Validate YAML structure and required fields
3. **Check content structure** - Verify best practices for the markdown body
4. **Compare against patterns** - Match against known good Skill patterns
5. **Generate report** - Provide structured feedback with severity levels

## Validation Checklist

### Frontmatter (YAML Header)

| Check | Severity | Description |
|-------|----------|-------------|
| Has `---` delimiters | 🔴 Critical | Must have opening and closing `---` |
| Valid YAML syntax | 🔴 Critical | YAML must parse without errors |
| Has `name` field | 🟡 Warning | Defaults to directory name, but explicit is better |
| Has `description` | 🔴 Critical | Required for auto-trigger to work |
| Description quality | 🟡 Warning | Should be specific, mention when to use |
| `disable-model-invocation` | 🟢 Info | Only set if you want manual-only |
| `user-invocable` | 🟢 Info | Set to false to hide from / menu |
| `allowed-tools` | 🟡 Warning | Specify if Skill needs specific tools |
| `model` override | 🟢 Info | Only if you need specific model |
| `context: fork` | 🟢 Info | Use for long-running or isolated tasks |
| `agent` with context | 🟢 Info | Required when context: fork |

### Content Structure

| Check | Severity | Description |
|-------|----------|-------------|
| Has clear title/heading | 🟡 Warning | First line should indicate purpose |
| Has process/steps | 🟡 Warning | Skills should have actionable steps |
| Has output format | 🟡 Warning | Define expected output structure |
| Uses specific language | 🟡 Warning | Avoid vague terms like "etc", "etc." |
| Has examples | 🟢 Info | Concrete examples improve reliability |
| Has constraints/guardrails | 🟢 Info | Define what NOT to do |
| Appropriate length | 🟡 Warning | Too short (<100 words) or too long (>2000) |

### Common Issues

| Issue | Severity | Fix |
|-------|----------|-----|
| Missing description | 🔴 Critical | Add description explaining when to trigger |
| Description too vague | 🟡 Warning | Be specific about use cases |
| No clear output format | 🟡 Warning | Add expected output structure |
| Missing tool declarations | 🟡 Warning | Add `allowed-tools` if using tools |
| Too many responsibilities | 🟡 Warning | Split into multiple focused Skills |
| Hardcoded paths | 🟡 Warning | Use variables or relative paths |
| No error handling guidance | 🟢 Info | Add what to do when things go wrong |

## Output Format

```
# Skill Analysis Report

## File: {filepath}

### Frontmatter Analysis

| Field | Status | Value | Notes |
|-------|--------|-------|-------|
| name | ✅/⚠️/❌ | {value} | {feedback} |
| description | ✅/⚠️/❌ | {value} | {feedback} |
| ... | | | |

**Frontmatter Score:** X/10

### Content Analysis

| Check | Status | Notes |
|-------|--------|-------|
| Has clear purpose | ✅/⚠️/❌ | {feedback} |
| Actionable steps | ✅/⚠️/❌ | {feedback} |
| Output format defined | ✅/⚠️/❌ | {feedback} |
| Has examples | ✅/⚠️/❌ | {feedback} |
| Appropriate length | ✅/⚠️/❌ | {word_count} words |

**Content Score:** X/10

### Issues Found

#### 🔴 Critical (Must Fix)
1. {issue description} → {fix suggestion}

#### 🟡 Warnings (Should Fix)
1. {issue description} → {fix suggestion}

#### 🟢 Suggestions (Nice to Have)
1. {issue description} → {fix suggestion}

### Overall Assessment

**Total Score:** X/10

**Verdict:**
- ✅ Excellent - Ready to use
- 🟡 Good - Minor improvements suggested
- ⚠️ Needs Work - Address warnings before using
- ❌ Critical Issues - Must fix before using

### Recommended Actions

1. {action item}
2. {action item}
3. {action item}

### Improved Version (Optional)

If significant improvements are needed, provide a rewritten SKILL.md:

```yaml
---
# improved frontmatter
---

# Improved content...
```
```

## Skill Patterns Reference

### Pattern 1: Checklist/Task Skill
For: Code review, testing, validation tasks

Structure:
- Clear trigger description
- Step-by-step process
- Checklist categories
- Severity ratings
- Structured output format

### Pattern 2: Generator Skill
For: Documentation, commit messages, reports

Structure:
- Input requirements
- Analysis steps
- Template/format specification
- Examples
- Constraints

### Pattern 3: Explorer/Research Skill
For: Code exploration, debugging, analysis

Structure:
- Context gathering (!commands)
- Investigation steps
- What to look for
- How to present findings

### Pattern 4: Workflow Skill
For: Multi-step processes, releases, deployments

Structure:
- Prerequisites check
- Sequential steps
- Validation points
- Rollback guidance

## Examples of Good Descriptions

✅ **Good:**
- "Perform a thorough code review following the team checklist. Use when reviewing code changes, pull requests, or when the user asks for a code review."
- "Generate API documentation from source code. Use when the user asks to document an API endpoint, route handler, or controller."
- "Create a standardized git commit message following Conventional Commits format. Use when the user asks to commit or create a commit message."

❌ **Bad:**
- "Does code review" (too vague)
- "Helps with documentation" (when?)
- "A skill for git" (too broad)

## Examples of Good Output Formats

✅ **Good:**
```markdown
## Output Format

Structure your review as:

**Summary**
[One-paragraph overall assessment]

**Critical Issues**
[Must fix before merging]

**Approved?**
[YES / NO / YES WITH CONDITIONS]
```

❌ **Bad:**
```markdown
Just give me a review of the code.
```
