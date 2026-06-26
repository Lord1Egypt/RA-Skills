# Audit Rules: The Full Rulebook

> Detailed scoring rules and evaluation criteria for Skill Quality Check. Use this as the definitive reference when auditing Skills.

---

## Overview

Skill Quality Check evaluates Skills across 5 dimensions:

| Dimension | Points | Weight |
|-----------|--------|--------|
| YAML Frontmatter | 10 | 10% |
| Description Quality | 40 | 40% |
| Body Quality | 40 | 40% |
| Resource Layering | 10 | 10% |
| Performance Impact | ±5 | bonus/penalty |

**Maximum score: 100 + 5 bonus points**

---

## Dimension 1: YAML Frontmatter (10 pts)

### Required Fields

Every SKILL.md must have:

```yaml
---
name: <skill-name>           # Required
description: >                # Required
---
```

### Scoring Rules

| Condition | Points | Rationale |
|-----------|--------|-----------|
| Only `name` and `description` present | +2 | Minimal, correct |
| `description` is multi-line (`>` or `\|`) | +1 | Properly formatted |
| Additional fields present (version, author, etc.) | -1 per field | Token waste |
| Missing `name` | 0 | Critical failure |
| Missing `description` | 0 | Critical failure |

### Deduction Table

| Issue | Deduction | Severity |
|-------|-----------|----------|
| Extra fields in frontmatter | -1 each | Minor |
| `name` contains spaces | -1 | Convention issue |
| `description` is blank | 0 pts | Critical |
| `name` is missing | 0 pts | Critical |

### Best Practice: Frontmatter Examples

#### ✅ Perfect Frontmatter

```yaml
---
name: pdf-processing
description: >
  PDF document creation and editing. Use when working with .pdf files.
  Keywords: pdf, document, adobe, rotate, merge.
---
```

#### ❌ Bloated Frontmatter

```yaml
# ❌ This wastes context tokens
---
name: pdf-processing
version: 1.0.0
author: John Doe
license: MIT
created: 2024-01-01
updated: 2024-03-15
tags: [pdf, documents, automation]
description: >
  Comprehensive PDF processing...
---
```

---

## Dimension 2: Description Quality (40 pts)

This is the most heavily weighted dimension because Description is Level 1 content — always loaded, always consuming tokens.

### Sub-dimensions (10 pts each)

#### 2.1 Trigger Accuracy (10 pts)

**What it measures:** Does the description clearly explain when to use the Skill?

| Score | Criteria |
|-------|----------|
| 10 | Clear, specific trigger conditions stated |
| 7-9 | Clear but could be more specific |
| 4-6 | Vague or generic trigger |
| 0-3 | No trigger information |

**Red flags:**
- "Useful for many tasks"
- "General assistant"
- "Can help with various things"

**Good signals:**
- "Use when: writing tests, debugging, adding features"
- "Triggers on: pdf, document, rotate, merge"

#### 2.2 Conciseness (10 pts)

**What it measures:** Is the description appropriately sized?

| Score | Token Estimate | Action |
|-------|---------------|--------|
| 10 | <50 tokens | Perfect |
| 8-9 | 50-100 tokens | Good |
| 5-7 | 100-150 tokens | Acceptable |
| 3-4 | 150-200 tokens | Too long |
| 0-2 | >200 tokens | Severely bloated |

**Token estimation:** ~4 characters = 1 token

#### 2.3 Keyword Coverage (10 pts)

**What it measures:** Are relevant trigger keywords included?

| Score | Criteria |
|-------|----------|
| 10 | 3-5 relevant keywords, well-chosen |
| 7-9 | Keywords present but could be better |
| 4-6 | Only 1-2 keywords |
| 0-3 | No keywords |

**Good keywords:**
- Domain-specific: "tdd", "pytest", "red-green"
- Action-based: "debug", "analyze", "generate"
- File-based: "pdf", "docx", "csv"

#### 2.4 Non-Redundancy (10 pts)

**What it measures:** Does it avoid explaining what AI already knows?

| Score | Criteria |
|-------|----------|
| 10 | No WAI content, all project-specific |
| 7-9 | Minimal WAI, mostly useful |
| 4-6 | Noticeable WAI, but useful content present |
| 0-3 | Mostly WAI ("Claude is smart...") |

**WAI (Writing About AI) examples to avoid:**
- "Claude is a powerful LLM..."
- "You are an AI assistant that..."
- "The model can understand and generate..."

### Description Scoring Examples

#### ✅ Excellent (40/40)

```yaml
description: >
  TDD test-driven development workflow. Use when writing new features,
  adding tests, or fixing bugs. Keywords: test-driven, TDD, pytest,
  red-green, unit test.
```

Score: 10 + 9 + 10 + 10 = **39/40**

#### ⚠️ Acceptable (25/40)

```yaml
description: >
  This skill helps with coding tasks. It provides guidance on best
  practices for software development and can assist with various
  programming challenges.
```

Score: 5 + 5 + 4 + 4 = **18/40**

#### ❌ Poor (10/40)

```yaml
description: >
  Claude is an advanced AI assistant capable of understanding complex
  software engineering concepts. This skill helps Claude help users
  by providing context about the codebase and coding best practices...

  [continues for 300+ words]
```

Score: 2 + 1 + 1 + 2 = **6/40**

---

## Dimension 3: Body Quality (40 pts)

### Sub-dimensions

#### 3.1 Progressive Disclosure (10 pts)

**What it measures:** Is content appropriately layered?

| Score | Criteria |
|-------|----------|
| 10 | Perfect layering: L1 in description, L2 in body, L3 in resources |
| 8-9 | Good layering, minor issues |
| 5-7 | Some content misplaced (docs in body, etc.) |
| 0-4 | Severe layering violations |

**Common violations:**
- Execution instructions in Description (should be in body)
- Detailed documentation in body (should be in references/)
- Code blocks in body (should be in scripts/)

#### 3.2 Role Setting (10 pts)

**What it measures:** Does SKILL.md start with clear role/context?

| Score | Criteria |
|-------|----------|
| 10 | Clear role statement in first paragraph |
| 7-9 | Role present but not at start |
| 4-6 | Implicit role, could be clearer |
| 0-3 | No role information |

**✅ Good role setting:**
```markdown
# PDF Processing Skill

You are a professional document preparation assistant specializing in creating and editing PDF documents.
```

#### 3.3 Example Usage (10 pts)

**What it measures:** Are there sufficient, relevant, diverse examples?

| Score | Criteria |
|-------|----------|
| 10 | 3-5 diverse, structured examples |
| 7-9 | Examples present, minor improvements needed |
| 4-6 | 1-2 examples, could use more |
| 0-3 | No examples or very poor examples |

**Example quality factors:**
- **Relevance:** Do they match real use cases?
- **Diversity:** Do they cover edge cases?
- **Format:** Are they structured (XML tags, input/output)?

#### 3.4 Instruction Clarity (10 pts)

**What it measures:** Are instructions clear, step-by-step, unambiguous?

| Score | Criteria |
|-------|----------|
| 10 | All steps clear, error cases handled, format specs present |
| 7-9 | Mostly clear, minor ambiguities |
| 4-6 | Some unclear steps or missing info |
| 0-3 | Vague instructions, major gaps |

**Checklist:**
- [ ] Numbered steps for sequences
- [ ] Conditional branches covered
- [ ] Error handling explained
- [ ] Output format specified

---

## Dimension 4: Resource Layering (10 pts)

### Sub-dimensions

#### 4.1 scripts/ Usage (5 pts)

**What it measures:** Is code properly in scripts/?

| Score | Criteria |
|-------|----------|
| 5 | No scripts needed, OR scripts used appropriately |
| 4 | Could use scripts but fine without |
| 2-3 | Some repeated code in body (should be in scripts/) |
| 0-1 | Significant repeated code, poorly organized |

#### 4.2 references/ Usage (5 pts)

**What it measures:** Are long docs properly in references/?

| Score | Criteria |
|-------|----------|
| 5 | No long docs needed, OR docs in references/ |
| 4 | Could use references but fine without |
| 2-3 | Some long docs in body (should be in references/) |
| 0-1 | Body severely bloated with documentation |

---

## Dimension 5: Performance Impact (bonus/penalty)

This dimension can add or subtract points based on real-world impact.

### 5.1 Level 1 Token Cost

| Condition | Adjustment |
|-----------|-------------|
| Description <50 tokens | +1 |
| Description 50-100 tokens | 0 |
| Description 100-150 tokens | -1 |
| Description 150-200 tokens | -2 |
| Description >200 tokens | -3 |

### 5.2 Level 2 Volume

| Condition | Adjustment |
|-----------|-------------|
| SKILL.md <200 lines | +1 |
| SKILL.md 200-500 lines | 0 |
| SKILL.md 500-1000 lines | -1 |
| SKILL.md >1000 lines | -2 |

### 5.3 Misfire Risk

| Condition | Adjustment |
|-----------|-------------|
| Description has specific keywords | 0 |
| Description is moderately vague | -1 |
| Description is very generic | -2 |

---

## Final Score Calculation

```
Total = Frontmatter + Description + Body + Resources + Performance
```

### Score Bands

| Score | Grade | Action |
|-------|-------|--------|
| 85-100 | 🟢 Excellent | Install immediately |
| 70-84 | 🟡 Good | Installable, improvements suggested |
| 50-69 | 🔴 Acceptable | Consider optimizing first |
| <50 | ⚫ Poor | Not recommended |

---

## Priority Classification

After scoring, classify improvement suggestions:

### 🔴 P0 (Must Fix)

Issues that critically impact functionality or cause significant token waste:
- Missing `name` or `description`
- Description >200 tokens
- SKILL.md >1000 lines
- No usable instructions

### 🟡 P1 (Should Fix)

Issues that reduce quality or efficiency:
- Description >150 tokens
- Missing examples
- No role setting
- Content misplaced between layers

### 🟢 P2 (Nice to Have)

Minor optimizations:
- Add more keywords
- Improve example diversity
- Slightly more concise wording

---

## Complete Scoring Worksheet

```
SKILL AUDIT WORKSHEET
═══════════════════════════════════════════════════════
Skill: _______________________
Source: _______________________
Date: _______________________
─────────────────────────────────────────────────────
DIMENSION 1: YAML FRONTMATTER               [__/10]
  • Required fields present?               +__ (max 2)
  • Multi-line description?               +__ (max 1)
  • Extra fields (deduct -1 each)?        -__
─────────────────────────────────────────────────────
DIMENSION 2: DESCRIPTION QUALITY            [__/40]
  2.1 Trigger Accuracy                    [__/10]
  2.2 Conciseness                        [__/10]
  2.3 Keyword Coverage                     [__/10]
  2.4 Non-Redundancy                      [__/10]
─────────────────────────────────────────────────────
DIMENSION 3: BODY QUALITY                  [__/40]
  3.1 Progressive Disclosure               [__/10]
  3.2 Role Setting                        [__/10]
  3.3 Example Usage                       [__/10]
  3.4 Instruction Clarity                 [__/10]
─────────────────────────────────────────────────────
DIMENSION 4: RESOURCE LAYERING             [__/10]
  4.1 scripts/ Usage                      [__/5]
  4.2 references/ Usage                   [__/5]
─────────────────────────────────────────────────────
DIMENSION 5: PERFORMANCE IMPACT            [__/5]
  5.1 Level 1 Cost                        __
  5.2 Level 2 Volume                      __
  5.3 Misfire Risk                        __
─────────────────────────────────────────────────────
TOTAL SCORE                                 __/100
═══════════════════════════════════════════════════════
GRADE: 🟢 Excellent / 🟡 Good / 🔴 Acceptable / ⚫ Poor
═══════════════════════════════════════════════════════
```

---

## Example Audit

### Example: TDD Skill (Hypothetical)

```
DIMENSION 1: YAML FRONTMATTER               [9/10]
  • name + description present             +2
  • Multi-line description                 +1
  • No extra fields                       0

DIMENSION 2: DESCRIPTION QUALITY           [36/40]
  2.1 Trigger: "TDD workflow"            9/10
  2.2 Conciseness: ~80 tokens             8/10
  2.3 Keywords: TDD, pytest, red-green    10/10
  2.4 Non-Redundancy: no WAI              9/10

DIMENSION 3: BODY QUALITY                  [35/40]
  3.1 Progressive Disclosure: good          9/10
  3.2 Role Setting: "You are a TDD..."    9/10
  3.3 Examples: 4 good examples            9/10
  3.4 Clarity: clear steps                 8/10

DIMENSION 4: RESOURCE LAYERING             [9/10]
  4.1 scripts/: pytest wrapper             4/5
  4.2 references/: no long docs           5/5

DIMENSION 5: PERFORMANCE IMPACT             [-1]
  5.1 Level 1 Cost: 80 tokens             -1
  5.2 Level 2 Volume: 250 lines           0
  5.3 Misfire Risk: specific keywords     0

─────────────────────────────────────────
TOTAL: 88/100   🟢 EXCELLENT
─────────────────────────────────────────
```

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-03-29 | Initial release |
