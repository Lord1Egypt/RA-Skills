# ClawHub Readiness Checklist

Use this checklist before publishing the skill to ClawHub.

## Table of contents
- 1. Metadata quality
- 2. Structure quality
- 3. Operational completeness
- 4. Portability review
- 5. Release bar

## 1. Metadata quality

Check the SKILL frontmatter:
- `name` is lowercase hyphen-case
- `description` clearly states:
  - what the skill does
  - when it should trigger
  - that V1 defaults to CLI temporary workers, while persistent sessions are only advanced / later options

The description should be understandable even to someone who has never seen 小马 / 小牛 before.

## 2. Structure quality

The skill folder should contain only what helps the agent do the job:
- `SKILL.md`
- `references/` files that are actually used
- optional `scripts/` only if they provide real deterministic value

Do not add:
- README.md
- CHANGELOG.md
- installation guide files
- random design notes

## 3. Operational completeness

Before release, confirm the skill answers these questions clearly:
- What are 小马 and 小牛?
- Why is V1 based on CLI temporary workers instead of persistent-by-default setup?
- How do you dispatch work?
- How do you perform QA?
- How do you recover if a worker/session breaks?
- When should you avoid this workflow?

If any of these answers are vague, the skill is not ready.

## 4. Portability review

The skill should not assume Jerry-specific private context unless explicitly marked as an example.

Review for:
- user-specific names or secrets
- hardcoded private environment details
- assumptions that only fit one workspace layout
- instructions that depend on undocumented local habits

Allowed:
- 小马 / 小牛 as default role names, because they are part of the workflow design
- making clear that operators may rename these roles while preserving the same execution-worker / QA-worker structure

Not allowed:
- private credentials
- hidden infrastructure assumptions
- references to unpublished internal state as if universal

## 5. Release bar

The skill is ready for ClawHub only if:
- the trigger description is clear
- SKILL.md is compact and navigable
- references are linked directly from SKILL.md
- there is a clear creation + operation + recovery path
- a fresh OpenClaw operator could understand how to use the skill without your chat history

If possible, do one dry-run audit before publishing:
- pretend you have never seen the workflow before
- read only `SKILL.md`
- follow the references it points to
- verify that the path from concept → setup → use → recovery is complete
