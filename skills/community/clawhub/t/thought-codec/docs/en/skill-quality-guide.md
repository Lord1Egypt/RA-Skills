# Skill Quality Guide

A good ThoughtCodec skill is specific, executable, bilingual, and reviewable.

## Required Sections

Each published skill should include:

- Frontmatter with `name`, `description`, `version`, `status`, `language`, `type`, and `models`.
- A top-level title.
- When to use the skill.
- Inputs the skill expects.
- Step-by-step workflow.
- Output contract.
- Codex notes.
- Claude notes.
- Boundaries and safety notes.
- Example prompt.

## Writing Principles

- Prefer direct instructions over abstract advice.
- Make assumptions explicit.
- Keep the skill narrow enough to run reliably.
- Include examples where the skill could be misunderstood.
- Keep private information out of examples.
- Put large supporting material in `references/`.
- Maintain both English and Simplified Chinese versions.

## Status Levels

- `draft`: unfinished or template material that should not be presented as a published skill.
- `preview`: reviewed enough for public use, but still expected to evolve through real usage.
- `stable`: repeatedly validated in real workflows with low expected churn.

The first public ThoughtCodec skills use `preview`. This keeps the repository honest while making it clear that the skills are usable and reviewable.

## Compatibility Note

ThoughtCodec keeps extra frontmatter fields for its bilingual catalog and release process. If a skill is copied into a Codex-native skill directory, keep at least `name` and a trigger-ready `description`; project-specific metadata may be removed if the target runtime requires stricter frontmatter.

## Review Checklist

- Can a new reader understand when to use this skill?
- Are required inputs clear?
- Are steps ordered and actionable?
- Is the output format explicit?
- Are Codex and Claude differences named where useful?
- Are edge cases or safety concerns named?
- Does the catalog entry match the files?
