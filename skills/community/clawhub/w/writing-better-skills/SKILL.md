---
name: writing-better-skills
description: Use when creating or improving a skill for an AI agent, especially when the skill needs strong trigger wording, project-local context, references, scripts, tests, self-healing rules, or a completion gate another agent could follow without guessing.
license: Complete terms in LICENSE.txt
---

# Writing Better Skills

Create better skills for agents.

A skill helps an agent do work. It is reusable operational guidance plus optional references, scripts, tests, and narrow remediation. It is **not** something that "turns an agent into a skill."

This skill is the control plane for authoring other skills:
- it tells the agent **when** to use the skill-creation framework
- **what laws** must not be violated
- **which references** to read for each decision
- **when** scripts, tests, and self-healing are justified
- **what completion means**

## When to Use

Use this when authoring or revising a skill and you need to decide:
- what belongs in `SKILL.md`
- what should move into `references/`
- when project-local context is needed
- when to add scripts and tests
- whether self-healing is justified
- whether a fresh agent could use the skill without guessing

## The Iron Laws

```text
NO PROJECT-SPECIFIC CONTEXT IN THE GLOBAL SKILL
```

If a path, command, constraint, or convention belongs to one repository, it goes in `project.skill.md`, not in the reusable skill.

```text
NO SKILL IS COMPLETE UNTIL A FRESH AGENT COULD USE IT WITHOUT GUESSING CRITICAL FACTS
```

If another agent would have to invent project-local commands, output paths, trigger conditions, or completion criteria, the skill is incomplete.

**Violating the letter of these laws is violating the spirit of the skill.**

## Project-Local Context Comes First

The global skill must stay reusable.

Before doing substantial work with a skill in a repository:

1. Look for `project.skill.md` in the **project root**.
2. If it exists, read it before taking action.
3. If it does not exist and local context is needed, create it from `project.skill.template.md`.
4. Put environment-specific paths, commands, constraints, and conventions in `project.skill.md`, not in the global skill.
5. Treat `project.skill.md` as overriding generic guidance in `SKILL.md` when local details differ.

Read `references/project-skill-context.md` before defining or revising that contract.

## Skill Organization Model

### `SKILL.md` = the router
`SKILL.md` is the main behavioral document. It should tell the agent:
- when to use the skill
- what laws and stop conditions apply
- what order to follow
- which references to read
- which scripts to run
- what completion requires

### `references/` = deep guidance
References hold heavier, conditional, or decision-specific material.

Use references for:
- description-writing rules
- project-local context rules
- architecture-level decisions
- script/test conventions
- self-healing rules
- behavioral validation
- completion gates

### `scripts/` = deterministic helpers
Use scripts for repeated deterministic work the agent should not keep re-deriving.

### `tests/` = proof
Use tests to prove shipped scripts or promised behaviors work.

### `self-healing/` = narrow remediation
Use self-healing only for safe, local, repeatable fixes.

## Architecture Levels

Choose the smallest structure that reliably supports the work.

### Minimal skill
```text
my-skill/
└── SKILL.md
```

### Reference-backed skill
```text
my-skill/
├── SKILL.md
├── project.skill.template.md
└── references/
```

### Operational skill
```text
my-skill/
├── SKILL.md
├── project.skill.template.md
├── references/
├── scripts/
└── tests/
```

### Resilient operational skill
```text
my-skill/
├── SKILL.md
├── project.skill.template.md
├── references/
├── scripts/
├── tests/
└── self-healing/
```

Read `references/skill-architecture-levels.md` before deciding how much structure to add.

## Authoring Phases

You must complete each phase before moving on.

### Phase 1: Define the boundary
Decide:
- what problem the skill solves
- what belongs in the reusable global skill
- what must remain project-local
- whether local context actually matters

If local commands, paths, outputs, or constraints vary by project, plan for `project.skill.template.md`.

### Phase 2: Define trigger and routing
Write the frontmatter and top of `SKILL.md`.

Requirements:
- description says **when to use** the skill
- `SKILL.md` routes the agent to `project.skill.md` early when local context matters
- `SKILL.md` tells the agent which references/scripts matter at which step

Read `references/description-writing.md` before finalizing the description.

### Phase 3: Add only justified structure
Add references, scripts, tests, and self-healing only when earned.

Use these references:
- `references/script-test-conventions.md` before shipping scripts
- `references/self-healing-rules.md` before adding self-healing
- `references/skill-testing.md` before deciding what to validate

### Phase 4: Validate fresh-agent usability
Before calling the skill complete, test whether a fresh agent could:
- identify when to use the skill
- find the right local context file
- choose the right reference or script
- know what completion means

Read `references/behavioral-validation-checklist.md`.

### Phase 5: Apply the completion gate
Do not claim the skill is complete until it passes the completion gate.

Read `references/completion-gate.md`.

## Routing Map

Use this map while authoring:

- Need to define project-local context? → `references/project-skill-context.md`
- Need to choose architecture level? → `references/skill-architecture-levels.md`
- Need to write a better trigger description? → `references/description-writing.md`
- Need to add or test scripts? → `references/script-test-conventions.md`
- Need to decide whether healing is allowed? → `references/self-healing-rules.md`
- Need to validate fresh-agent usability? → `references/behavioral-validation-checklist.md`
- Need to decide if the skill is complete? → `references/completion-gate.md`
- Need general workflow or output guidance? → `references/workflows.md`, `references/output-patterns.md`

## Scripts in This Repo

Use the shipped scripts when they reduce repeated, deterministic work:

- `scripts/quick_validate.py` — fast validation of frontmatter and core structural promises

If you find yourself manually re-checking the same structural conditions repeatedly, prefer strengthening this validator rather than rewriting the checks ad hoc.

## Reference Skill

See `reference-skills/release-notes-generator/` for a canonical reference skill authored using this framework.

Use it as a model implementation of:
- a reusable global skill
- a shipped `project.skill.template.md`
- references routed from `SKILL.md`
- a deterministic script with a paired test
- narrow self-healing

It is a specimen of the framework, not a substitute for the framework.

## Red Flags — STOP

Stop and correct course if you are thinking:
- "I’ll just put this command/path in SKILL.md"
- "The agent can infer the local commands"
- "This script is too small to test"
- "I’ll add the test later"
- "This self-healing is probably safe"
- "The example will clarify the missing instructions"
- "A fresh agent will figure it out"
- "Close enough"

All of these usually mean you are about to violate one of the iron laws.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "It’s faster to put the path in SKILL.md" | That contaminates the global skill with local assumptions. Use `project.skill.md`. |
| "Agents can infer the local commands" | Guessing local commands is exactly what project-local context is for. |
| "This script is simple, it doesn’t need a test" | If it is worth shipping, it is usually worth validating. |
| "Self-healing can just fix a bunch of stuff" | Broad auto-fixes are risk, not resilience. |
| "The worked example will show the pattern" | The skill itself must be usable without depending on an example. |
| "The structure looks right, so the skill is done" | Organization alone does not prove fresh-agent usability. |

## Completion Gate

Before claiming a skill is complete, verify all of these:
- the description says when to use the skill
- the global skill contains no project-specific commands, paths, or constraints
- `SKILL.md` routes the agent to `project.skill.md` early when local context matters
- references are clearly named and linked from `SKILL.md`
- shipped scripts are justified and paired with tests, or explicitly exempted with a reason
- self-healing is narrow and safe
- a fresh agent could use the skill without guessing critical facts

## Bottom Line

A better skill is not just more elaborate.

A better skill:
- stays reusable at the global level
- pushes local facts into `project.skill.md`
- routes the agent clearly through references and scripts
- validates what it ships
- resists rationalization
- is complete only when a fresh agent could use it without guessing
