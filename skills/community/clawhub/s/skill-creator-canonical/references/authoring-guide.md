# Authoring Guide

Use this reference when you need principles for writing or restructuring a skill.

## What a skill is
A skill is a small package that gives an agent reusable procedural knowledge.
A skill may include:
- `SKILL.md` for core workflow and navigation
- `scripts/` for deterministic repeated actions
- `references/` for detailed material loaded on demand
- `assets/` for templates or files used in outputs

## Core principles
1. Keep `SKILL.md` lean.
2. Prefer concise examples over long explanation.
3. Match freedom to fragility.
4. Use low or medium freedom when weaker models need reliability.
5. Put each recurring fact, script, or template in one home.

## Degrees of freedom
- High freedom: multiple approaches are valid and the skill includes explicit decision rules.
- Medium freedom: a preferred pattern exists but some variation is safe.
- Low freedom: the sequence is fragile or consistency is critical.

## Writing rules
- Write one action per sentence in execution sections.
- Spell out branches with `if -> then -> else` logic.
- Name outputs or stop conditions when order matters.
- Avoid ambiguous pronouns when reference chains are long.
- Use concrete paths.
- Use checklists when order matters.
- Use `Read [filename] when [condition]. Purpose: [verb + noun].` for reference navigation.

## Folder rules
- Keep only files that directly support the skill.
- Do not add stray process docs by default.
- Prefer `references/` over bloating `SKILL.md` with long explanations.
- Prefer `scripts/` when the same code would otherwise be rewritten.
- Prefer `assets/` for starter files or templates used in outputs.

## Frontmatter rules
- Required fields: `name`, `description`.
- `description` must say what the skill does and when to use it.
- Keep names lowercase, short, and hyphenated.
