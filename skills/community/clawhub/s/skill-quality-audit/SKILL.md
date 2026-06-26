---
name: skill-quality-audit
description: >
  Audit and quality-review AI agent skills (SKILL.md files) against
  established best practices from the Nevo Systems skill-writing
  framework. Checks trigger quality, structure (rigid vs flexible),
  conciseness, progressive disclosure, and common mistakes.
  Use when reviewing, auditing, or evaluating an existing skill,
  when a skill isn't performing well, when the user says
  "review this skill", "audit my skill", "check this SKILL.md",
  "skill quality check", or "/skill-review".
---

# Skill Review

Audit a SKILL.md file against the following quality dimensions.
Report findings with severity (critical / warning / nit) and
actionable fix suggestions.

## Review Dimensions

Evaluate in order. Stop at critical findings — fix those first.

### 1. Trigger Quality

The `description` field in YAML frontmatter is the ONLY trigger mechanism.
It must answer three questions clearly:

- **What** does this skill do? (1-2 sentences)
- **When** should the agent use it? (contexts, task types)
- **What trigger phrases** activate it? (exact words users might say)

Red flags:

- [ ] Description is vague (<2 sentences or generic like "Helps with X")
- [ ] Trigger phrases are missing or too broad
- [ ] Trigger conditions are in the body, not the frontmatter
- [ ] Skill would trigger when irrelevant (overly broad scope)

### 2. Structure: Rigid vs Flexible

Determine if the skill matches the right structural approach:

| Approach    | Use When                          | Signs of Mismatch              |
|-------------|-----------------------------------|--------------------------------|
| **Rigid**   | Fragile task, consistency critical, skipping steps = failure | Loose guidelines for DB migration |
| **Flexible** | Multiple valid approaches, requires judgment | Overly prescriptive for code review |

Decision rule: **If the agent deviates from instructions, how much damage?**
- High damage → Must be rigid (numbered steps, checklists, exact commands)
- Low damage → Flexible OK (guidelines, heuristics, decision frameworks)

### 3. Conciseness

- [ ] Body is under 500 lines
- [ ] No explanations of things the model already knows (e.g., "write clear English", "use proper indentation")
- [ ] No conceptual documentation — instructions only (not "X is a system that...", but "Run X with these flags")
- [ ] Each paragraph justifies its token cost

### 4. Progressive Disclosure

Check the three-level loading strategy:

- **Level 1** (always in context): Frontmatter name + description — under ~100 words
- **Level 2** (on trigger): SKILL.md body — under 5,000 words, self-contained enough to start work
- **Level 3** (on demand): References/ — loaded only when needed

Red flags:

- [ ] SKILL.md body contains detailed API docs, schemas, or variant-specific content → move to `references/`
- [ ] Multiple variants/frameworks live in body instead of separate reference files
- [ ] No references/ directory exists but body exceeds 500 lines
- [ ] Reference files not explicitly mentioned in SKILL.md body

### 5. Common Mistakes Checklist

- [ ] **Over-explaining the obvious**: Instructions like "write grammatically correct English" or "use proper code formatting". The model already does this. **Remove.**
- [ ] **Trigger info in body**: "When to Use This Skill" section in the body is useless — only frontmatter matters for triggering. **Move to description or delete.**
- [ ] **Documentation instead of instructions**: Explaining what something is instead of telling the agent what to do. Replace "Database migrations are schema changes..." with "Back up the database before migration."
- [ ] **Too many tiny skills**: If two skills always trigger together, merge them. If a skill is under 20 lines after removing fluff, consider if it's too granular.
- [ ] **Context budget ignored**: Skill consumes excessive tokens → use progressive disclosure.
- [ ] **Bad naming**: `skill1`, `my-skill`, `helper`, `utils` → use descriptive, verb-led hyphen-case names.

### 6. Bundled Resources Check

- `scripts/`: Are they tested? Do they solve a repeatedly-rewritten problem?
- `references/`: Are they referenced from SKILL.md with clear "when to read" guidance?
- `assets/`: Are they output-oriented (templates, images), not documentation?
- No extraneous files (README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, etc.)

### 7. Trigger Testing (if applicable)

If a test plan exists or can be inferred:

- List 3 queries that SHOULD trigger this skill
- List 3 queries that SHOULD NOT trigger this skill
- Flag any overlap or ambiguity

## Output Format

```markdown
## Skill Review: [skill-name]

### Summary
[1-2 sentences: overall quality, primary issues]

### Findings

| # | Severity | Dimension | Issue | Fix |
|---|----------|-----------|-------|-----|
| 1 | critical | Trigger | ... | ... |

### Trigger Test
- ✅ Should trigger: ...
- ❌ Should NOT trigger: ...

### Score
- Trigger: X/10
- Structure: X/10
- Conciseness: X/10
- Progressive Disclosure: X/10
- Overall: X/10
```
