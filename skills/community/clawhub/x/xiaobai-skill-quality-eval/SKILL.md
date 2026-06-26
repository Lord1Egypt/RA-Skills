---
name: skill-quality-eval
version: 1.0.0
description: Skill Quality Evaluator - Score any skill on 6 dimensions. Catch 30% of skills that look good but fail silently. Based on Tessl Research 2026 findings.
emoji: 📊
tags: [evaluation, quality, skill, testing, reliability, ai-agent]
---

# Skill Quality Evaluator 📊

Score any skill on 6 dimensions. Catch the 30% of skills that look good but fail silently.

## Why This Matters

Tessl Research (April 2026) found:
- **20% accuracy gain** when using a good skill vs no skill
- **3X cost savings** when small model + right skill matches large model
- **40% activation rate** — agents often fail to use available skills
- **30% of evaluation tasks have leakage** — skills that seem great but aren't

This skill helps you evaluate and improve your skills systematically.

## 6-Dimension Evaluation

### 1. Activation Reliability (0-100)
> Can the agent find and activate this skill when needed?

Checklist:
- [ ] Trigger words are specific and unambiguous
- [ ] Description matches actual functionality
- [ ] No conflicting skills with similar triggers
- [ ] Skill is discovered when user asks relevant questions

**Common Issues:**
- Vague description → agent doesn't know when to use it
- Missing trigger words → skill never activates
- Too broad → activates when it shouldn't

**Score Guide:**
- 90+: Agent activates correctly 95%+ of the time
- 70-89: Activates in most relevant contexts
- 50-69: Sometimes activates, sometimes misses
- <50: Agent rarely finds/uses this skill

### 2. Task Coverage (0-100)
> Does the skill handle the tasks it claims to cover?

Checklist:
- [ ] Each claimed capability has a usage example
- [ ] Edge cases are documented
- [ ] Known limitations are stated
- [ ] Failure modes are explained

**Common Issues:**
- Claims broad coverage but only handles happy path
- No examples for secondary features
- Undocumented prerequisites

**Score Guide:**
- 90+: All claimed tasks have working examples
- 70-89: Main tasks covered, some gaps in secondary features
- 50-69: Core functionality works but incomplete
- <50: Major claims unsupported

### 3. Instruction Clarity (0-100)
> Can the agent follow the instructions without confusion?

Checklist:
- [ ] Instructions are step-by-step, not vague guidelines
- [ ] Decision points have clear criteria
- [ ] Output format is specified
- [ ] Anti-patterns are listed

**Common Issues:**
- "Do X when appropriate" → when is appropriate?
- Missing priority/precedence rules
- Contradictory instructions

**Score Guide:**
- 90+: Agent follows instructions correctly 95%+ of the time
- 70-89: Mostly clear, occasional confusion
- 50-69: Agent frequently asks for clarification
- <50: Instructions are ambiguous or contradictory

### 4. Leakage Resistance (0-100)
> Does the evaluation actually test the skill, or does it leak answers?

Checklist:
- [ ] Examples don't contain verbatim solutions
- [ ] Test tasks require genuine skill application
- [ ] No shortcut paths that bypass skill content
- [ ] Evaluation criteria measure real capability

**Common Issues (from Tessl Research):**
- Example tasks are too similar to skill content
- Skill contains answers verbatim
- Test can be solved by pattern matching without understanding

**Score Guide:**
- 90+: No leakage, genuine skill testing
- 70-89: Minor leakage that doesn't significantly inflate scores
- 50-69: Moderate leakage, scores may be 10-20% inflated
- <50: Major leakage, evaluation results unreliable

### 5. Model Compatibility (0-100)
> Does the skill work across different model sizes?

Checklist:
- [ ] Tested with at least 2 model sizes
- [ ] Works with smaller/cheaper models
- [ ] Performance difference between models documented
- [ ] Minimum model requirements stated

**Tessl Finding:** Small model + right skill ≈ Large model at 3X lower cost.

**Score Guide:**
- 90+: Works well with small models (haiku-level)
- 70-89: Works with medium models (sonnet-level)
- 50-69: Requires large models (opus-level)
- <50: Even large models struggle

### 6. Real-World Value (0-100)
> Does using this skill actually improve outcomes vs no skill?

Checklist:
- [ ] Measurable improvement over baseline
- [ ] Users would notice the difference
- [ ] Saves time or reduces errors
- [ ] No negative side effects

**Score Guide:**
- 90+: Clear, significant improvement (20%+ accuracy gain)
- 70-89: Noticeable improvement
- 50-69: Marginal improvement
- <50: No improvement or negative impact

## Evaluation Report Template

```markdown
# Skill Evaluation Report

**Skill**: [name]
**Version**: [version]
**Date**: YYYY-MM-DD
**Evaluator**: [agent/session]

## Overall Score: XX/100

| Dimension | Score | Status |
|-----------|-------|--------|
| Activation Reliability | XX | 🟢/🟡/🔴 |
| Task Coverage | XX | 🟢/🟡/🔴 |
| Instruction Clarity | XX | 🟢/🟡/🔴 |
| Leakage Resistance | XX | 🟢/🟡/🔴 |
| Model Compatibility | XX | 🟢/🟡/🔴 |
| Real-World Value | XX | 🟢/🟡/🔴 |

🟢 80+ | 🟡 50-79 | 🔴 <50

## Critical Issues
1. [Issue] → [Fix]

## Improvement Recommendations
1. [Recommendation] → [Expected impact]

## Quick Wins (easy fixes, big impact)
1. [Fix] → +X points on [dimension]
```

## Usage

### Evaluate a skill
```
Read the skill's SKILL.md and evaluate on all 6 dimensions.
Generate the evaluation report.
Save to memory/evaluations/<skill-name>-eval.md
```

### Improve a skill based on evaluation
```
1. Read evaluation report
2. Focus on lowest-scoring dimension
3. Apply quick wins first
4. Re-evaluate
5. Repeat until all dimensions ≥ 70
```

### Batch evaluate all skills
```
For each skill in skills/ directory:
  1. Read SKILL.md
  2. Evaluate on 6 dimensions
  3. Generate report
  4. Identify top 3 improvements
Save summary to memory/evaluations/batch-report.md
```

## Anti-Patterns to Detect

| Pattern | Issue | Fix |
|---------|-------|-----|
| "Do X when appropriate" | Vague trigger | Define specific conditions |
| No examples | Agent can't learn | Add 3+ concrete examples |
| Only happy path | Fragile in production | Add error handling examples |
| Verbatim solutions | Leakage risk | Use different examples for eval |
| No model requirements | Unknown compatibility | Test with 2+ model sizes |

## License

MIT
