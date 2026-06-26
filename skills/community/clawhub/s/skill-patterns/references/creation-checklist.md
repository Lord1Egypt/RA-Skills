# Skill Creation Checklist

Use this checklist to verify that a newly created skill is complete.

## Basic Structure

- [ ] `SKILL.md` exists and contains required fields
- [ ] `name` field: skill identifier (lowercase, hyphen-separated)
- [ ] `description` field: clearly explains purpose and trigger conditions
- [ ] `metadata.trigger-keywords` or `metadata.trigger-phrases`: activation word list
- [ ] Directory structure follows standards (references/, assets/ as needed)

## SKILL.md Content Quality

- [ ] Clearly explains when to activate (trigger conditions)
- [ ] Clearly explains core capabilities/responsibilities
- [ ] Has execution flow or step instructions
- [ ] Has output format requirements (if applicable)
- [ ] Has correct/incorrect example comparisons (if applicable)
- [ ] Explains which references/assets files need to be loaded

## Pattern Matching

Based on skill type, confirm the correct pattern is selected:

- [ ] **Tool Wrapper**: Has references/conventions.md or similar convention files
- [ ] **Generator**: Has assets/template.md and references/style-guide.md
- [ ] **Reviewer**: Has references/checklist.md with clear severity levels (error/warning/info)
- [ ] **Inversion**: Has clear question list and interview flow, prohibits premature execution
- [ ] **Pipeline**: Has clear step sequence and checkpoints (⏸️)

## Maintainability

- [ ] Conventions/checklists separated from main logic (for independent updates)
- [ ] Templates use variable placeholders (e.g., `{{title}}`)
- [ ] Has version number (in SKILL.md metadata or filename)
- [ ] Has clear directory organization and naming

## Testing & Validation

- [ ] Trigger word test: activate with trigger words, confirm skill responds correctly
- [ ] Flow test: execute complete flow per skill instructions
- [ ] Boundary test: test handling of ambiguous input, error input
- [ ] Output validation: confirm output format meets expectations

## Documentation Completeness

- [ ] README.md (if needed, explains skill purpose and usage)
- [ ] Example files (if needed, shows typical input/output)
- [ ] Changelog (if needed, records version evolution)

## Pre-release Checks

- [ ] No sensitive information (API Keys, passwords, internal URLs)
- [ ] No hardcoded paths (use relative paths)
- [ ] .gitignore configured correctly (exclude secrets, temp files)
- [ ] Code/scripts executable (if scripts/ directory exists)

---

## Quick Scoring

**Structure Completeness**: _/5 (5 basic structure items)
**Content Quality**: _/5 (SKILL.md quality)
**Pattern Matching**: _/5 (pattern selection & implementation)
**Maintainability**: _/5 (separation & organization)
**Test Coverage**: _/5 (testing validation)

**Total Score**: __/25

- 20-25 points: Ready to publish
- 15-19 points: Needs improvement
- <15 points: Recommend refactor
