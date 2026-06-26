---
name: skill-activation-booster
version: 1.0.0
description: Skill Activation Booster - Fix the 40% activation problem. Optimize triggers, descriptions, and context so agents actually use your skills.
emoji: 🚀
tags: [activation, optimization, skill, triggers, ai-agent]
---

# Skill Activation Booster 🚀

Fix the 40% activation problem. Optimize triggers, descriptions, and context so agents actually use your skills.

## The Problem

Tessl Research (April 2026) discovered a critical issue:
> **Agents only activate relevant skills ~40% of the time in unforced settings.**

This means 60% of the time, agents ignore valuable skills they have access to. Your skill might be amazing, but if the agent never activates it, it's worthless.

## Root Causes of Low Activation

### 1. Vague Triggers
```
❌ Bad: "Use this skill when working with databases"
✅ Good: "Trigger when user mentions: SQL, PostgreSQL, MySQL, 'query', 'database schema', 'migrate data'"
```

### 2. Missing Context Signals
```
❌ Bad: Description only mentions one use case
✅ Good: Description lists 5+ specific scenarios with example phrases
```

### 3. Generic Descriptions
```
❌ Bad: "A helpful tool for developers"
✅ Good: "PostgreSQL query optimizer - fix slow queries, analyze execution plans, suggest indexes"
```

### 4. Buried Instructions
```
❌ Bad: Key trigger words buried in paragraph 3
✅ Good: Trigger words in first 2 sentences of description
```

### 5. Competing Skills
```
❌ Bad: 3 skills all trigger on "git"
✅ Good: One skill for "git commit", another for "git branch", another for "git conflict"
```

## Optimization Checklist

### Phase 1: Trigger Audit

- [ ] List all trigger words/phrases
- [ ] Check if trigger words appear in user's natural language
- [ ] Verify triggers don't overlap with other skills
- [ ] Test: "Would this phrase activate the skill?"

### Phase 2: Description Optimization

- [ ] First 50 chars contain primary trigger
- [ ] Description matches how users actually ask for help
- [ ] Include 3-5 example user phrases that should trigger
- [ ] Mention alternatives: "When user asks X OR Y OR Z"

### Phase 3: Context Enhancement

- [ ] Add "When NOT to use" section (reduces false activations)
- [ ] Include common synonyms for key concepts
- [ ] Add domain-specific terminology
- [ ] List related but different scenarios

### Phase 4: Activation Testing

- [ ] Test with 10 natural user phrases
- [ ] Verify skill activates when it should
- [ ] Verify skill doesn't activate when it shouldn't
- [ ] Adjust based on results

## Optimization Template

```markdown
## Skill Activation Profile

### Primary Triggers (must activate)
- "phrase 1"
- "phrase 2"
- "phrase 3"

### Secondary Triggers (should activate)
- "related phrase 1"
- "related phrase 2"

### Anti-Triggers (should NOT activate)
- "similar but different 1"
- "similar but different 2"

### Example User Messages That Should Trigger

1. "Can you help me optimize this SQL query?"
2. "The database is running slow"
3. "I need to add an index to my table"

### Example User Messages That Should NOT Trigger

1. "Can you optimize this Python code?" (not database)
2. "Help me design a database schema" (different skill)

### Optimized Description (first 80 chars)

[Primary trigger word] - [what it does] - [when to use]
```

## Quick Wins

### Add Trigger Phrases Section
```
## Trigger Phrases

This skill activates when user mentions:
- "query optimization"
- "slow query"
- "execution plan"
- "add index"
- "database performance"
```

**Impact:** +15-25% activation rate

### Front-Load Key Terms
```
Before: "This is a comprehensive tool that helps with database operations including optimization..."

After: "SQL Query Optimizer - Fix slow queries and improve database performance. Use when user mentions 'slow query', 'execution plan', or 'add index'."

**Impact:** +10-20% activation rate
```

### Add Synonyms
```
## Also Known As

Users might say:
- "tune my query" (same as optimize)
- "speed up my database" (same as improve performance)
- "why is my query slow" (same as query optimization)
```

**Impact:** +5-10% activation rate

## Activation Rate Testing

### Test Script
```
For each test phrase:
1. Present phrase to agent in isolation
2. Check if skill is activated
3. Record: activated (yes/no)
4. Calculate activation rate

Expected: 80%+ for direct triggers
Expected: 50%+ for secondary triggers
Expected: <10% for anti-triggers (false positives)
```

### Test Phrases Template
```markdown
## Test Phrases for [Skill Name]

### Direct Triggers (should activate 80%+)
| Phrase | Activated? | Notes |
|--------|------------|-------|
| [phrase 1] | ? | |
| [phrase 2] | ? | |
| [phrase 3] | ? | |

### Secondary Triggers (should activate 50%+)
| Phrase | Activated? | Notes |
|--------|------------|-------|
| [phrase 1] | ? | |
| [phrase 2] | ? | |

### Anti-Triggers (should activate <10%)
| Phrase | Activated? | Notes |
|--------|------------|-------|
| [phrase 1] | ? | |
| [phrase 2] | ? | |
```

## Integration with Skill Quality Evaluator

After evaluating a skill's quality, use this skill to:
1. Check activation reliability score
2. If <80, run optimization checklist
3. Re-test activation rate
4. Iterate until ≥80%

## License

MIT
