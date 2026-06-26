---
name: skill-publishing
description: Guide to publishing and sharing Hermes skills through ClawHub, including safe login practices, release hygiene, and security scan preparation.
tags: [publish, clawhub, github, skills, community, devops]
version: 1.1.1
---

# Hermes Skill Publishing Guide

## When to use

- You are preparing a skill for ClawHub publication.
- You need to update a published skill version.
- You want a short checklist for passing the security scan.

## Safe login

Prefer reading the token privately instead of pasting it directly into a shared command line history.

```bash
read -s CLAWHUB_TOKEN
clawhub login --token "$CLAWHUB_TOKEN" --no-browser
unset CLAWHUB_TOKEN
```

## Publish a skill

```bash
clawhub publish /path/to/skill-folder \
  --slug "skill-slug" \
  --name "Display Name" \
  --version "1.0.0" \
  --changelog "What changed in this release" \
  --tags "latest,tag1,tag2"
```

## Useful commands

- `clawhub whoami`
- `clawhub inspect <slug>`
- `clawhub search <query>`
- `clawhub delete <slug>`
- `clawhub skill merge <source-slug> <target-slug>`

## Security scan checklist

Before publishing:

- Remove secrets, tokens, and internal URLs.
- Remove fake commands or instructions for tools that are not actually included.
- Use official download sources only.
- Avoid hardcoded system paths and unsafe command examples.
- Keep examples focused on the skill's real behavior.
- Rewrite or remove anything that could look like exfiltration, persistence, or privilege escalation.

## Release hygiene

- Bump the version every time you republish.
- Keep the changelog factual and short.
- Use English titles and descriptions if the target audience is broad.
- Merge or delete duplicate skills so only the canonical version remains active.
