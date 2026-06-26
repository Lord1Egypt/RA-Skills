# Optimization Patterns

Use these rewrite patterns when improving a skill for discovery.

## Naming

Good names are short, literal, and task-led.

- Prefer `postgres-backup` over `db-guardian`
- Prefer `pdf-redline` over `document-workbench`
- Prefer `linear-address-comments` over `issue-orchestrator`

Checklist:

- Include the target object or system
- Include the main action
- Avoid brand-only names unless the brand itself is a search term
- Keep the slug stable once distribution starts unless the current name materially harms recall

## Description

Structure the description like this:

1. State what the skill does
2. State when to use it
3. State the common task variations

Template:

`<Action> <object/system> for <main outcome>. Use when you need to <job 1>, <job 2>, <job 3>, or when the user asks about <common query phrasing>.`

## Query Coverage

Cover four keyword classes:

- Exact task phrase
- Synonyms and adjacent phrasings
- Tool or platform names
- User-intent language

Example for a backup skill:

- Exact: `postgres backup`
- Synonyms: `database dump`, `restore`, `retention policy`
- Platform: `PostgreSQL`, `pg_dump`, `pg_restore`
- Intent: `disaster recovery`, `verify backups`, `scheduled backups`

## First-Screen Content

Place these near the top of `SKILL.md`:

- One-sentence summary
- Preconditions
- 3 to 5 realistic example prompts
- Core commands or workflow entry points
- Important constraints that affect success

## Trust and Conversion

Add the strongest truthful trust signals available:

- Required environment variables and tools
- Cost or rate-limit notes
- Examples that clearly work
- Links to references for non-obvious constraints
- Maintenance cues such as recent updates or clear ownership

## Rewrite Rule

Do not broaden a skill only to chase search traffic. Keep terms that are:

- Relevant to the actual workflow
- Supported by examples or references
- Likely to be used by a real user
