# Description Patterns

The frontmatter description is the main trigger surface. Write it for another agent, not for a human landing page.

## Good Pattern

```yaml
description: Audit, score, and improve agent skills before publishing, sharing, or installing them. Use when reviewing a SKILL.md file or skill folder for trigger quality, progressive disclosure, resource references, cross-agent compatibility, safety risks, install friction, marketplace positioning, or launch readiness.
```

Why it works:

- Names the action: audit, score, improve.
- Names the artifact: agent skills, `SKILL.md`, skill folder.
- Names trigger contexts: publishing, sharing, installing, marketplace readiness.
- Names evaluation dimensions: trigger quality, safety, compatibility, install friction.

## Templates

Capability plus trigger contexts:

```yaml
description: <Verb> <artifact/domain> for <outcome>. Use when <user intent 1>, <user intent 2>, or <user intent 3>.
```

Tool integration:

```yaml
description: Work with <tool/system/file type> to <specific jobs>. Use when the user asks to <common action>, <common action>, or <common action>; includes <important boundary or setup note>.
```

Workflow skill:

```yaml
description: Run a structured <workflow name> workflow for <audience/problem>. Use when <starting condition>, <handoff condition>, or <review condition>.
```

## Anti-Patterns

- "This skill helps with productivity." Too vague.
- "The ultimate agent skill for everything." Too broad and hype-heavy.
- "Use this when the user needs help." No trigger signal.
- Long installation docs in frontmatter. Move them to the body or references.
- Claims that the skill sends, publishes, pays, deploys, deletes, or edits systems when it only drafts instructions.
