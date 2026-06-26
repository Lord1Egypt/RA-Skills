# D1: Design Quality

## Rubric

| Score | Meaning |
|-------|---------|
| 9-10 | Exemplary. Follows AgentSkills best practices (see skill-creator/SKILL.md) near-perfectly. |
| 7-8 | Solid. One or two minor issues. |
| 5-6 | Functional but sloppy. Multiple structural issues. |
| 3-4 | Poor. Major design problems. |
| 1-2 | Broken. Not a valid skill structure. |

## Scoring Rules

Start at 10. Apply deductions. **Floor = 1** (never score 0 unless skill is not a skill at all).

Deductions are tiered by severity:

- **Major (-2):** Problems that affect skill triggering, context waste, or structural correctness.
- **Minor (-1):** Polish issues, minor inconsistencies.

**No double-counting:** If one issue appears in multiple checklist categories (e.g., a TODO in SKILL.md counts under both completeness and file organization), deduct once only under the most relevant category.

## Checklist

### Frontmatter
- [ ] Major: Non-standard fields in YAML (version, author, emoji, metadata, tags)
- [ ] Minor: `name` not kebab-case or ≥64 chars

### Description
- [ ] Major: Marketing filler ("best-in-class", "comprehensive", "definitive", "cutting-edge")
- [ ] Major: Dumps sub-details (dimension names, sub-features) into description instead of body
- [ ] Minor: Trigger phrases don't match how users actually speak

### Progressive Disclosure
- [ ] Major: SKILL.md body >500 lines
- [ ] Major: Heavy reference material in body instead of references/
- [ ] Minor: No read-when conditions on reference links
- [ ] Minor: File >100 lines without TOC

### File Organization
- [ ] Major: Extraneous files (README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md)
- [ ] Major: Non-asset file types in assets/ (.sh, .py, .exe)
- [ ] Minor: Symlinks present

### Token Efficiency
- [ ] Minor: Same information repeated across SKILL.md and references/
- [ ] Minor: Verbose explanations where concise examples suffice

### Freedom Degree
- [ ] Minor: Freedom level doesn't match task fragility (over-constrained creative tasks or under-guarded dangerous ops)

### Internal Consistency
- [ ] Major: Description promises capabilities not delivered in body
- [ ] Major: Quick Start or examples reference files/scripts that don't exist
- [ ] Minor: Section descriptions contradict each other
