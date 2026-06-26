# Behavioral Validation Checklist

Use this checklist before claiming a skill is complete.

## Fresh-agent usability

A fresh agent using only the skill should be able to answer:
- When should this skill be used?
- What file should be read first?
- What parts are global vs project-local?
- Which references matter for the current step?
- Which scripts should be used instead of re-implementing logic?
- What proves the skill is working?

## Required checks

### 1. Trigger clarity
- The frontmatter description says when to use the skill.
- The trigger conditions are concrete enough that another agent can identify applicability.

### 2. Local context routing
- `SKILL.md` tells the agent early to look for `project.skill.md` when local context matters.
- The skill does not require editing the global skill for project-specific setup.

### 3. Reference routing
- `SKILL.md` tells the agent which reference to read for which decision.
- References are modular, not a junk drawer.

### 4. Script routing
- `SKILL.md` tells the agent when to use shipped scripts.
- Deterministic repeated logic is not left as implicit reimplementation work.

### 5. Completion clarity
- The skill says what completion means.
- The agent can tell what must be verified before claiming success.

## Failure signs

The skill is not ready if a fresh agent would have to guess:
- project-specific commands
- output paths
- whether a script should exist
- whether a failure should trigger self-healing
- what "done" means
