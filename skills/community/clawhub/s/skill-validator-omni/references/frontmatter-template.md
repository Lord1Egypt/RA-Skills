# SKILL.md Frontmatter Template

Copy this into a new `SKILL.md`, replace the placeholders, then delete this comment block.

> Codex note: this template is the Hermes flavour. OpenAI Codex rejects `version`, `author`, `platforms`, and `compatibility` at the top level — Codex skills take only `name`, `description`, `license`, `allowed-tools`, `metadata`. Use this template for Hermes/Claude/skills.sh targets; strip the extra fields (and drop `metadata.hermes`) for a strict Codex skill. Run `skill-validator-omni <dir> -s codex` to confirm.

```yaml
---
name: <skill-name>                  # must equal the directory name; lowercase-hyphens
description: <What it does + when to use it. One sentence, third person, <=60 chars, ends with period.>
version: 0.1.0                      # semver; new skills start at 0.1.0
author: Adel Ben Yahia (adelpro)    # credit the human first
license: MIT
platforms: [linux, macos, windows]  # audit: only what the skill actually invokes
compatibility: <env requirements, e.g. "Requires python3 and an API key.">
allowed-tools: <optional, experimental: space-separated pre-approved tools, e.g. "Bash(git:*) Read">
metadata:
  author: Adel Ben Yahia (adelpro)
  version: 0.1.0
  hermes:
    tags: [Short, Descriptive, Tags]
    related_skills: [other-skill-that-exists]
---
```

## Field Rules

| Field | Rule |
|---|---|
| `name` | lowercase letters, numbers, hyphens only. 1-64 chars. No leading/trailing hyphen, no `--`. MUST match directory name. |
| `description` | Third person ("Writes...", "Extracts..."). What + when. Under 60 chars total — the system prompt index truncates at 57. Ends with a period. No marketing words (powerful, comprehensive, seamless). |
| `version` | Semver. 0.1.0 for new skills. |
| `author` | Human first, then collaborator if any. |
| `platforms` | `[linux, macos, windows]` unless the skill genuinely invokes OS-specific things. |
| `compatibility` | Only if there are real requirements: env vars, system packages, network access. Max 500 chars. |
| `allowed-tools` | Optional/experimental. Space-separated tools pre-approved to run (e.g. `Bash(git:*) Read`). Support varies by client. |
| `metadata.hermes.tags` | 3-6 short routing tags. |
| `metadata.hermes.related_skills` | Only skills that actually exist. |

## Body Skeleton

```markdown
# <Skill Name>

2-3 sentence intro: what it does, what it doesn't do, dependency stance.

## When to Use
- bulleted triggers

## Don't Use For
- bulleted counter-triggers

## Prerequisites
- exact env vars, installs, API key sourcing

## Procedure
1. numbered steps, each with a checkable completion criterion

## Common Edge Cases
- what to do at the boundaries

## Pitfalls
- known limits, things that look broken but aren't

## Verification
- how to prove the skill worked
```

Keep the whole body under 500 lines. Long examples go in `references/`, logic in `scripts/`, copy-paste material in `templates/`.
