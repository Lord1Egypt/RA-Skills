---
name: superpowers-open-writing-skills
description: >
  Use when creating new skills, editing existing skills, or verifying skills work before deployment. Adapts TDD methodology to process documentation for OpenClaw's SKILL.md format.
metadata:
  openclaw:
    emoji: "✍️"
---

# Writing Skills

## Overview

**Writing skills IS Test-Driven Development applied to process documentation.**

**Skills for SuperpowersOpen live in `~/.openclaw/skills/superpowers-open/`**

You write test cases (pressure scenarios), watch them fail (baseline behavior), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

**REQUIRED BACKGROUND:** You MUST understand superpowers-open:test-driven-development before using this skill. That skill defines the fundamental RED-GREEN-REFACTOR cycle. This skill adapts TDD to documentation.

## What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or tools. Skills help future AI instances find and apply effective approaches.

**Skills are:** Reusable techniques, patterns, tools, reference guides

**Skills are NOT:** Narratives about how you solved a problem once

## TDD Mapping for Skills

| TDD Concept | Skill Creation |
|-------------|----------------|
| **Test case** | Pressure scenario (test the skill with an AI) |
| **Production code** | Skill document (SKILL.md) |
| **Test fails (RED)** | AI violates rule without skill (baseline) |
| **Test passes (GREEN)** | AI complies with skill present |
| **Refactor** | Close loopholes while maintaining compliance |
| **Write test first** | Run baseline scenario BEFORE writing skill |
| **Watch it fail** | Document exact rationalizations AI uses |
| **Minimal code** | Write skill addressing those specific violations |
| **Watch it pass** | Verify AI now complies |
| **Refactor cycle** | Find new rationalizations → plug → re-verify |

## When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious to you
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)
- Others would benefit

**Don't create for:**
- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put in CLAUDE.md)
- Mechanical constraints (if it's enforceable with automation, automate it)

## Skill Types

### Technique
Concrete method with steps to follow (condition-based-waiting, root-cause-tracing)

### Pattern
Way of thinking about problems (flatten-with-flags, test-invariants)

### Reference
API docs, syntax guides, tool documentation

## Directory Structure

```
skills/superpowers-open/
  skill-name/
    SKILL.md              # Main reference (required)
    supporting-file.*     # Only if needed
```

**Separate files for:**
1. **Heavy reference** (100+ lines) - API docs, comprehensive syntax
2. **Reusable tools** - Scripts, utilities, templates

**Keep inline:**
- Principles and concepts
- Code patterns (< 50 lines)
- Everything else

## OpenClaw SKILL.md Structure

**Frontmatter (YAML):**
- Required: `name` (superpowers-open- prefix), `description`, `metadata.openclaw`
- `description`: Third-person, describes ONLY when to use (NOT what the skill does)
  - Start with "Use when..." to focus on triggering conditions
  - Include specific symptoms, situations, and contexts
  - **NEVER summarize the skill's process or workflow**

```yaml
---
name: superpowers-open-skill-name
description: >
  Use when [specific triggering conditions and symptoms].
  Include keywords and symptoms that signal this skill should load.
metadata:
  openclaw:
    emoji: "🔧"
---
```

## Claude Search Optimization (CSO)

**Critical for discovery:** Future AI needs to FIND your skill

### 1. Rich Description Field

**Purpose:** AI reads description to decide which skills to load. Make it answer: "Should I read this skill right now?"

**Format:** Start with "Use when..." to focus on triggering conditions

**CRITICAL: Description = When to Use, NOT What the Skill Does**

The description should ONLY describe triggering conditions. Do NOT summarize the skill's process or workflow in the description — AI may follow the description instead of reading the full skill content.

```yaml
# ❌ BAD: Summarizes workflow
description: Use when executing plans - dispatches subagent per task with code review

# ❌ BAD: Too much process detail
description: Use for TDD - write test first, watch it fail, write minimal code, refactor

# ✅ GOOD: Just triggering conditions
description: Use when implementing any feature or bugfix, before writing implementation code
```

### 2. Keyword Coverage

Use words AI would search for:
- Error messages: "Hook timed out", "ENOTEMPTY", "race condition"
- Symptoms: "flaky", "hanging", "zombie", "pollution"
- Synonyms: "timeout/hang/freeze", "cleanup/teardown"
- Tools: Actual commands, library names, file types

### 3. Token Efficiency

- Frequently-loaded skills: < 200 words total
- Other skills: < 500 words
- Move details to tool help or supporting files
- Use cross-references instead of repeating content

## Testing Skills

Different skill types need different test approaches:

### Discipline-Enforcing Skills (rules/requirements)
**Examples:** TDD, verification-before-completion, designing-before-coding
**Test with:** Pressure scenarios — do AI agents comply under stress?
**Success criteria:** Agent follows rule under maximum pressure

### Technique Skills (how-to guides)
**Examples:** condition-based-waiting, root-cause-tracing
**Test with:** Application scenarios — can they apply the technique correctly?
**Success criteria:** Agent successfully applies technique to new scenario

### Pattern Skills (mental models)
**Examples:** reducing-complexity, information-hiding concepts
**Test with:** Recognition + application + counter-examples
**Success criteria:** Agent correctly identifies when/how to apply pattern

### Reference Skills (documentation/APIs)
**Examples:** API documentation, command references
**Test with:** Retrieval + application scenarios
**Success criteria:** Agent finds and correctly applies reference information

## Bulletproofing Skills Against Rationalization

Skills that enforce discipline need to resist rationalization.

### Close Every Loophole Explicitly

```markdown
# ❌ BAD
Write code before test? Delete it.

# ✅ GOOD
Write code before test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete
```

### Address "Spirit vs Letter" Arguments

Add foundational principle early:
```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

### Build Rationalization Table

```markdown
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
```

### Create Red Flags List

```markdown
## Red Flags - STOP and Start Over

- Code before test
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**
```

## Skill Creation Checklist

**RED Phase - Write Failing Test:**
- [ ] Create pressure scenarios (3+ combined pressures for discipline skills)
- [ ] Run scenarios WITHOUT skill - document baseline behavior
- [ ] Identify patterns in rationalizations/failures

**GREEN Phase - Write Minimal Skill:**
- [ ] Name uses `superpowers-open-` prefix, letters, numbers, hyphens only
- [ ] YAML frontmatter with required fields
- [ ] Description starts with "Use when..." and includes specific triggers
- [ ] Description written in third person
- [ ] Keywords throughout for search
- [ ] Clear overview with core principle
- [ ] Address specific baseline failures identified in RED
- [ ] Run scenarios WITH skill - verify compliance

**REFACTOR Phase - Close Loopholes:**
- [ ] Identify NEW rationalizations from testing
- [ ] Add explicit counters (if discipline skill)
- [ ] Build rationalization table
- [ ] Create red flags list
- [ ] Re-test until bulletproof

**Quality Checks:**
- [ ] Small flowchart only if decision non-obvious
- [ ] Quick reference table
- [ ] Common mistakes section
- [ ] No narrative storytelling
- [ ] Supporting files only for tools or heavy reference

**Deployment:**
- [ ] Skill committed to `~/.openclaw/skills/superpowers-open/`

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to NEW skills AND EDITS to existing skills.

Write skill before testing? Delete it. Start over.
Edit skill without testing? Same.

## Anti-Patterns

### ❌ Narrative Example
"In session XYZ, we found empty projectDir caused..."
**Why bad:** Too specific, not reusable

### ❌ Multi-Language Dilution
example-js.js, example-py.py, example-go.go
**Why bad:** Mediocre quality, maintenance burden

### ❌ Code in Flowcharts
**Why bad:** Can't copy-paste, hard to read

## The Bottom Line

**Creating skills IS TDD for process documentation.**

Same Iron Law: No skill without failing test first.
Same cycle: RED (baseline) → GREEN (write skill) → REFACTOR (close loopholes).
Same benefits: Better quality, fewer surprises, bulletproof results.

If you follow TDD for code, follow it for skills. It's the same discipline applied to documentation.
