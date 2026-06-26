---
name: skill-naming-standard
description: Use when naming, renaming, or reviewing agent skills. Produces cold-readable display names, kebab-case slugs, trigger descriptions, and approval-aware autonomy wording.
---

# Skill Naming Standard

Name the job, not the lore.

## Rules

- Use Title Case for display names.
- Use lowercase kebab-case for slugs.
- Keep slugs under 60 characters.
- Make names understandable without private memory.
- Prefer action, domain, and output over vibe.
- Keep nicknames as aliases inside the body, not in the slug.
- Use approval language when the skill can change external state.

## Naming Patterns

```text
<Domain> <Job>
<Domain> <Artifact> Builder
<Approval Gated> <External Action>
<Continuous> <Monitoring Loop>
<Read Only> <Review Task>
```

Examples:

```text
Expert Execution Upgrade      -> expert-execution-upgrade
Workspace Lifecycle Standard  -> workspace-lifecycle-standard
Cross Agent Skill Adapter     -> cross-agent-skill-adapter
Approval Gated Deployer       -> approval-gated-deployer
Continuous Stream Supervisor  -> continuous-stream-supervisor
```

## Decision Check

1. Could a new agent infer when to use it?
2. Does it describe the job instead of the author's mental shortcut?
3. Is it narrow enough to avoid grabbing unrelated tasks?
4. Does the name imply too much autonomy?
5. Does the description state approval boundaries?

## Output

```text
Display Name: <Title Case>
Slug: <kebab-case>
Description: <trigger + output + approval boundary>
Aliases: <private nicknames only if useful>
Why: <one sentence>
```
