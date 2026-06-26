---
name: skill-quality-check
description: >
  Quality audit for AI Agent Skills. Use before installing or after writing any SKILL.md.
  Scores 5 dimensions with actionable improvements. Works for skills written for Claude, Cursor, Codex, and any AI agent. Keywords: audit, skill, quality, review, score, assess, best practices, vet.
---

# Skill Quality Check 🔍

Universal quality assessment framework for AI Agent Skills. Evaluates any SKILL.md file across **5 dimensions**, outputting a quantified score and actionable improvement suggestions. Designed to work with skills built for Claude, Cursor, Codex, OpenClaw, or any AI agent.

## When to Use

- Before installing a new Skill from any source
- After writing your own Skill (self-check)
- Comparing quality of similar Skills
- Evaluating Skills for ClawHub/SkillHub submission
- As companion to Skill Creator — learn to write, then learn to audit

## Audit Protocol

### Step 1: Locate and Read the Target Skill

Find the SKILL.md file:

```
# Path priority (in order):
1. User-specified path
2. <skills-dir>/<skill-name>/SKILL.md

   # Common locations by platform:
   #   OpenClaw:     ~/.openclaw/skills/<skill-name>/SKILL.md
   #   QClaw:        ~/.qclaw/skills/<skill-name>/SKILL.md
   #   Claude Code:  ~/.claude/skills/<skill-name>/SKILL.md
   #   Cursor:       ~/.cursor/skills/<skill-name>/SKILL.md
   #   Codex:        ~/.codex/skills/<skill-name>/SKILL.md
3. <repo>/skills/<skill-name>/SKILL.md
4. <repo>/<skill-name>/SKILL.md

# If installing from GitHub without a local copy, fetch via curl:
curl -s "https://raw.githubusercontent.com/<owner>/<repo>/main/skills/<skill>/SKILL.md"
```

Then scan the directory for supporting files:
```
skill-name/
├── SKILL.md       ✅ required
├── scripts/       ✅ optional (lazy-loaded)
├── references/   ✅ optional (lazy-loaded)
└── assets/        ✅ optional (lazy-loaded)
```

### Step 2: YAML Frontmatter Review

SKILL.md must have YAML frontmatter with **only** these fields:

```yaml
---
name: <skill-name>      ✅ required
description: >          ✅ required
# Fields below are NOT recommended in frontmatter:
# ❌ version           → package metadata
# ❌ author            → non-standard
# ❌ license           → non-essential
# ❌ compatibility     → most Skills don't need it
# ❌ tags              → non-standard
---
```

**Review checklist:**
- [ ] Does `name` and `description` exist?
- [ ] Is `description` under 150 characters (trigger-level content must be concise)?
- [ ] Does `description` include trigger keywords ("when to use")?
- [ ] Are there extra fields wasting Level 1 tokens?

### Step 3: Description Quality Assessment

Description is Level 1 content — the AI uses it to decide whether to trigger the Skill. **It is a trigger, not a manual.**

**✅ Good Description:**
```
TDD test-driven development workflow. Use when writing new features,
adding tests, or debugging. Keywords: test-driven, TDD, red-green-refactor.
```

**❌ Bad Description:**
```
This is a comprehensive guide to Test-Driven Development using the
red-green-refactor cycle. First, write a failing test that describes
the behavior you want. Then write the minimum code to make it pass...
```
*(Too long — contains Level 2 content that belongs in SKILL.md body)*

**Scoring rubric (each dimension 0-10):**

| # | Dimension | Question |
|---|-----------|----------|
| 1 | Trigger Accuracy | Does it clearly state when to use this Skill? |
| 2 | Conciseness | Under 150 chars? No explanatory filler? |
| 3 | Keyword Coverage | Does it include trigger keywords (e.g. TDD, debug, pdf)? |
| 4 | Non-Redundancy | Does it avoid restating what AI already knows? |

### Step 4: SKILL.md Body Quality Assessment

**Five assessment dimensions (0-10 each):**

#### 4.1 Progressive Disclosure

Does it follow the three-layer loading principle?

| Layer | Content | When Loaded |
|-------|---------|-------------|
| Level 1 | name + description | Always in context |
| Level 2 | SKILL.md body | On skill trigger |
| Level 3 | scripts/ + references/ + assets/ | On execution, never in context |

**Review checklist:**
- [ ] Trigger conditions → should be in Description (Level 1)
- [ ] Execution steps, tool instructions → SKILL.md body (Level 2)
- [ ] Detailed docs, scripts, templates → references/scripts (Level 3)
- [ ] SKILL.md body under 500 lines?

#### 4.2 Role Setting

Does the Skill open with a clear role or context definition?

**✅ Good example:**
```
# PDF Processing Skill

You are a professional document preparation assistant specializing in
PDF creation and editing workflows...
```

#### 4.3 Examples

Are there sufficient, relevant, and diverse examples?

Claude recommends 3-5 examples that are:
- **Relevant**: tied to real use cases
- **Diverse**: cover edge cases
- **Structured**: wrapped in XML tags

**Review checklist:**
- [ ] Input/output example pairs present?
- [ ] Core use cases covered?
- [ ] Edge cases shown?

#### 4.4 Instruction Clarity

Are instructions clear, actionable, and unambiguous?

**Review checklist:**
- [ ] Steps listed with numbered lists?
- [ ] Conditional branches explained?
- [ ] Error/exception handling covered?
- [ ] Output format specified (e.g. JSON structure)?

### Step 5: Resource Layer Assessment

Are bundled resources used appropriately?

| Resource | When to Use | Review Question |
|----------|-------------|-----------------|
| scripts/ | Deterministic/repeated code execution | Is there repetitive code that should be a script? |
| references/ | Detailed docs, API specs, domain knowledge | Is there >10k chars of docs not in references/? |
| assets/ | Templates, images, fonts for output | Are there files that should be assets, not inline content? |

**Review checklist:**
- [ ] Long docs in SKILL.md body that should be in references/?
- [ ] Repeated code snippets that should be scripts?
- [ ] Scripts have correct paths and dependency notes?

### Step 6: Performance Impact Assessment

#### 6.1 Level 1 Token Cost

**Formula:**
```
Level 1 cost ≈ len(description) / 4 tokens
(English: ~4 chars ≈ 1 token)
```

**Benchmarks:**
- Excellent: < 50 tokens
- Good: 50-100 tokens
- Too long: > 150 tokens → needs trimming

#### 6.2 Level 2 Volume

**Review checklist:**
- [ ] SKILL.md body over 500 lines (~5000 tokens)?
- [ ] Repetitive content that can be trimmed?
- [ ] AI-common-knowledge content that should be deleted?

#### 6.3 Mis-trigger Risk

**High-risk signals:**
- Multiple Skills with overlapping Description keywords
- Vague Descriptions (e.g. "general-purpose assistant")
- Too many installed Skills (>10) increases mis-trigger risk

### Step 7: Comprehensive Scoring

Aggregate all dimension scores into the final report.

```
SKILL AUDIT REPORT
═══════════════════════════════════════════════════════════════
Skill: [skill-name]
Source: [local path / GitHub URL / ClawHub]
Audited: [date]
───────────────────────────────────────────────────────────────
I.   YAML FRONTMATTER COMPLIANCE       [X/10]
     ✅ [passed items]
     ❌ [issues]

II.  DESCRIPTION QUALITY               [X/40]
     Trigger Accuracy        [X/10]
     Conciseness             [X/10]
     Keyword Coverage        [X/10]
     Non-Redundancy          [X/10]

III. BODY QUALITY                      [X/40]
     Progressive Disclosure  [X/10]
     Role Setting            [X/10]
     Examples                [X/10]
     Instruction Clarity     [X/10]

IV.  RESOURCE LAYERING                 [X/10]
     scripts/ Usage           [X/5]
     references/ Usage       [X/5]

V.   PERFORMANCE IMPACT                [-5 to +2]
     Level 1 Cost            [penalty/bonus]
     Level 2 Volume          [penalty/bonus]
     Mis-trigger Risk        [penalty/bonus]
───────────────────────────────────────────────────────────────
OVERALL SCORE: X / 100
───────────────────────────────────────────────────────────────
Grade:
  🟢 Excellent (85-100)  — Worth installing, top quality
  🟡 Good (70-84)        — Usable, has room for improvement
  🔴 Acceptable (50-69) — Usable but needs optimization
  ⚫ Poor (<50)          — Not recommended
───────────────────────────────────────────────────────────────
VI.  IMPROVEMENT RECOMMENDATIONS (priority order)

  🔴 P0 (must fix):
     - [specific issue and fix]

  🟡 P1 (strongly recommended):
     - [specific issue and fix]

  🟢 P2 (optional):
     - [nice-to-have improvements]
═══════════════════════════════════════════════════════════════
```

## Scoring Reference

| Score | Grade | Meaning | Action |
|-------|-------|---------|--------|
| 85-100 | 🟢 Excellent | Meets all best practices | Install directly |
| 70-84 | 🟡 Good | Meets most standards, minor issues | Install, address P1 items |
| 50-69 | 🔴 Acceptable | Functional but有明显缺陷 | Fork and fix, or wait for update |
| <50 | ⚫ Poor | Fails best practices | Do not install, find alternatives |

## Common Issue Diagnosis

| Symptom | Cause | Fix |
|---------|-------|-----|
| Description too long | Frontmatter >150 tokens | Move details to body, keep only trigger keywords |
| Body too long | SKILL.md >500 lines | Split into references/ |
| No examples | Text-only instructions | Add 3-5 XML-wrapped example pairs |
| Vague role | No clear Skill boundary | Add role-setting paragraph |
| AI-common-knowledge filler | Explaining what AI already knows | Delete, keep only project-specific context |
| Not layered | Docs in body | Move to references/ |
| Mis-triggers | Overlapping or vague keywords | Differentiate Descriptions |

## Skill Quality Check vs. Skill Vetter

| Dimension | Skill Vetter | Skill Quality Check |
| **Goal** | Security review | Quality review |
| **Core question** | Will this Skill harm me? | Is this Skill well-written? |
| **Focus** | Malicious code, permission abuse | Writing standards, performance |
| **When** | Before any install | When assessing quality |
| **Output** | Security report | Quality score + recommendations |

**Use both in sequence:** Vet for safety first, then audit for quality.

## Quick Audit Commands

```bash
# Fetch SKILL.md from GitHub
curl -s "https://raw.githubusercontent.com/<owner>/<repo>/main/skills/<skill>/SKILL.md"

# Check frontmatter
grep -A 5 "^---" SKILL.md | head -10

# Estimate Level 2 volume (lines → ~10 tokens/line)
wc -l SKILL.md
```

## Output Requirements

Every audit report must include:
1. **Overall score** (X/100) with grade label
2. **Five dimension subscores** (radar chart optional)
3. **Improvement recommendations** (P0/P1/P2 priority)
4. **Clear "install or not" conclusion**

Do not say "this Skill is pretty good" — deliver a specific score, specific issues, and specific fixes.

---

*Good Skills deserve thorough auditing. Bad Skills deserve honest feedback.* 🔍🦀

---

## Examples

### Example 1: Perfect Description (Score 10/10)

**Input:**
```
name: tdd-skill
description: >
  TDD test-driven development workflow. Use when writing new features,
  adding tests, or fixing bugs. Keywords: test-driven, TDD, red-green-refactor,
  pytest, unit test.
```

**Audit Result:**
- Trigger Accuracy 10/10 — explicitly states when to use
- Conciseness 10/10 — well under 150 chars
- Keyword Coverage 10/10 — all key triggers present
- Non-Redundancy 10/10 — no AI-common-knowledge filler
- **Description Score: 40/40**

---

### Example 2: Manual-Style Description (Score 3/10)

**Input:**
```
name: tdd-skill
description: >
  This is a comprehensive guide to Test-Driven Development using
  the red-green-refactor cycle. First, you write a failing test that
  describes the behavior you want. Then write the minimum code to make
  it pass. Then refactor while keeping tests green. This approach
  ensures high test coverage and better code quality...
```

**Audit Result:**
- Trigger Accuracy 5/10 — mentions TDD but buried in explanation
- Conciseness 1/10 — 280+ chars, reads like a manual
- Keyword Coverage 5/10 — "TDD" present but no concise trigger list
- Non-Redundancy 1/10 — explains the TDD cycle (Level 2 content in Level 1)
- **Description Score: 12/40**

**P0 Recommendation:**
> Rewrite Description to be under 150 chars. Move the cycle explanation to SKILL.md body.

---

### Example 3: Good Role Setting (Score 9/10)

**Input:**
```markdown
# PDF Processing Skill

You are a professional document preparation assistant specializing in
PDF creation, editing, and conversion workflows. You have deep knowledge
of PDF structure, reportlab, pypdf, and weasyprint.
```

**Audit Result:**
- Role clarity 9/10 — clear persona and domain
- Skill boundary 9/10 —明确的职责范围
- Context specificity 9/10 — project-specific tools named

**Minor improvement (P2):** Could add one sentence about what this Skill does NOT cover (e.g. OCR, scanned PDFs).

---

### Example 4: Poor Role Setting (Score 2/10)

**Input:**
```markdown
# My Skill

This skill helps you get things done. Use it when you need help.
It provides instructions and guidelines for various tasks.
```

**Audit Result:**
- Role clarity 2/10 — "assistant" is too generic
- Skill boundary 1/10 — "various tasks" defines nothing
- Context specificity 1/10 — no project-specific information

**P0 Recommendation:**
> Replace generic language with specific domain context. Define what the Skill does and does not cover.

---

### Example 5: Well-Layered Skill (Score 8/10)

**Directory structure:**
```
awesome-skill/
├── SKILL.md              80 lines  (Level 2: execution flow only)
├── references/
│   ├── api-spec.md       450 lines (Level 3: detailed API docs)
│   └── troubleshooting.md 120 lines (Level 3: edge cases)
└── scripts/
    └── validate.sh        (Level 3: deterministic execution)
```

**Audit Result:**
- Progressive Disclosure 9/10 — clear layer separation
- Body size 9/10 — 80 lines is ideal (not bloated)
- Resource usage 8/10 — all heavy content in references/
- **Resource Layering Score: 8.5/10**

**Minor improvement (P2):** Could add a brief Layer 1 summary in Description listing which references/ files are most relevant.

---

### Example 6: Bloated SKILL.md (Score 2/10)

**Symptom:** SKILL.md has 620 lines including a 300-line API reference pasted directly in the body.

**Audit Result:**
- Progressive Disclosure 1/10 — Level 3 content in Level 2
- Body size 1/10 — 620 lines far exceeds 500-line guideline
- Conciseness 1/10 — 300-line API doc belongs in references/

**P0 Recommendation:**
> Move the API reference to `references/api-spec.md`. SKILL.md body should be execution flow only (under 500 lines).

---

### Example 7: Mis-Trigger Risk (Score -3 Performance Impact)

**Scenario:** User has 12 Skills installed. Two of them have "debug" in their Description:

| Skill | Description trigger keyword |
|-------|----------------------------|
| systematic-debugging | "debugging, error, bug" |
| general-helper | "debug, logs, errors, general assistance" |

**Audit Result:**
- Mis-trigger Risk: -3 penalty
- The overlap means "debug" alone can't reliably select the right Skill

**P1 Recommendation:**
> Differentiate: systematic-debugging should use "systematic-debugging, root-cause" (more specific); general-helper should remove "debug" entirely or move it lower in priority.
