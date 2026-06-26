# Project Skill Context

## Purpose

`project.skill.md` is a project-local adapter file for a reusable global skill.

Use it when a skill needs environment-specific facts such as:
- exact commands
- repo paths
- output locations
- local conventions
- guardrails
- validation rules

## Why it exists

Do not edit a reusable global skill every time a new repository needs local setup. That contaminates the shared skill with assumptions that only apply in one project.

Instead:
- the skill ships `project.skill.template.md`
- a setup agent or user creates `project.skill.md` in the project root
- later agents read `project.skill.md` first when local context matters

## Precedence

When instructions conflict, use this order:

1. direct user instructions
2. `project.skill.md`
3. `SKILL.md`
4. referenced docs and scripts defaults

## What belongs in `project.skill.md`

Include:
- exact commands (`pnpm test`, `uv run pytest`, etc.)
- important paths
- safe output destinations
- files that must not be modified
- tool/runtime expectations
- local constraints
- validation expectations
- concrete examples

## What does not belong there

Avoid:
- general theory about the skill
- duplicated content from `SKILL.md`
- secrets or raw credentials
- speculative notes like "probably" or "maybe"
- broad project docs unrelated to the skill

## Agent behavior

If the skill depends on local context:
1. look for `project.skill.md` in the project root
2. read it before substantial work
3. if missing, create it from `project.skill.template.md`
4. do not guess when exact local details should be documented

## Good signs

A strong `project.skill.md` is:
- short enough to scan
- concrete
- command-heavy
- path-specific
- easy to update

## Failure modes

Common mistakes:
- editing the global skill instead of creating project-local context
- storing secrets in the file
- copying the template but leaving placeholders unresolved
- making it a giant project README instead of a skill-specific local operating guide
