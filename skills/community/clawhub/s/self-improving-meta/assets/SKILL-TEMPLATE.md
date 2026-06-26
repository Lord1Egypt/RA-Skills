# Meta Skill Template

Template for creating skills extracted from meta-learnings. Meta-skills are special: they modify the infrastructure that all other skills depend on. Extra care in testing is required.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Concise description of the agent infrastructure pattern, prompt fix, or hook improvement this skill addresses. Include trigger conditions."
---

# Skill Name

Brief introduction: what infrastructure problem this skill solves, which prompt files or hooks it affects, and its origin.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Infrastructure trigger] | [Fix or improvement to apply] |
| [Related trigger] | [Alternative approach] |

## Background

Why this meta-knowledge matters. What agent misbehavior it prevents. What context efficiency or reliability improvement it provides.

## The Problem

### Current State

Description of the problematic prompt file content, hook behavior, rule conflict, or skill gap.

```
// Example of the broken instruction, verbose prompt, or conflicting rule
```

### Impact

How this infrastructure problem manifests in agent behavior: misinterpretation, ignored rules, context waste, silent failures.

## Solution

### Fix

```
// Corrected instruction, compressed prompt, resolved conflict, or fixed hook
```

### Step-by-Step

1. Identify the infrastructure problem
2. Locate all affected files (prompt files, hooks, rules, skills)
3. Apply the fix with minimal disruption
4. Test in a fresh session to verify agent behavior
5. Document the change in the affected file's version history

## Testing

### Fresh Session Test

Meta-skills MUST be tested in a fresh session because:
- Prompt file changes affect all subsequent agent behavior
- Hook changes alter the bootstrap sequence
- Rule changes can cascade through multiple skills

### Verification Checklist

- [ ] Agent correctly interprets the modified instruction
- [ ] No other rules or skills are broken by the change
- [ ] Context token usage is reduced (if compression was applied)
- [ ] Hook fires correctly and produces expected output
- [ ] No regressions in related skills

## Propagation

Meta-skills propagate differently from domain skills:

| Change Type | Propagation Scope |
|-------------|-------------------|
| AGENTS.md edit | All future sessions, all agents |
| SOUL.md edit | All future sessions, behavioral changes |
| TOOLS.md edit | All future tool usage patterns |
| MEMORY.md edit | Memory management for all sessions |
| Hook code fix | All future bootstraps |
| Skill template update | All future skill extractions |
| Rule file update | All agents reading that rule file |

## Rollback

If the meta-skill causes regressions:

1. Revert the prompt file / hook / rule to previous version
2. Log the regression as a new META issue
3. Re-evaluate the original learning with additional context

## Source

Extracted from meta learning entry.
- **Learning ID**: LRN-YYYYMMDD-XXX or META-YYYYMMDD-XXX
- **Original Category**: prompt_drift | rule_conflict | skill_gap | hook_failure | context_bloat | instruction_ambiguity
- **Area**: agent_config | skill_authoring | hook_scripts | prompt_files | rule_files | memory_management | extension_api
- **Extraction Date**: YYYY-MM-DD
```

---

## Minimal Template

For simple meta-skills that don't need all sections:

```markdown
---
name: skill-name-here
description: "What infrastructure pattern this addresses and when to apply it."
---

# Skill Name

[Problem statement in one sentence]

## Problem

Description of the infrastructure issue and its impact on agent behavior.

## Solution

Corrected instruction, compressed prompt, or fixed hook code.

## Testing

Verify in a fresh session that agent behavior is correct.

## Source

- Learning ID: LRN-YYYYMMDD-XXX
```

---

## Naming Conventions

- **Skill name**: lowercase, hyphens for spaces
  - Good: `prompt-file-compression`, `hook-error-handling`, `rule-deduplication`
  - Bad: `PromptCompression`, `fix_hooks`, `meta1`

- **Description**: Start with action verb, mention the infrastructure component
  - Good: "Compresses verbose SOUL.md personality directives to save context tokens. Use when SOUL.md exceeds 200 lines."
  - Bad: "Prompt stuff"

- **Files**:
  - `SKILL.md` — Required, main documentation
  - `scripts/` — Optional, automation (compression, validation, auditing)
  - `references/` — Optional, detailed docs
  - `assets/` — Optional, templates

---

## Extraction Checklist

Before creating a skill from a meta-learning:

- [ ] Infrastructure fix is verified (tested in fresh session)
- [ ] Fix is broadly applicable (not a one-off typo correction)
- [ ] Affected files are identified and listed
- [ ] Propagation scope is understood (which agents/sessions are affected)
- [ ] Rollback plan exists
- [ ] Name follows conventions
- [ ] Description includes trigger conditions

After creating:

- [ ] Update original learning with `promoted_to_skill` status
- [ ] Add `Skill-Path: skills/skill-name` to learning metadata
- [ ] Test skill by reading it in a fresh session
- [ ] Verify no regressions in affected prompt files, hooks, or rules
- [ ] Notify team if the change affects shared infrastructure
