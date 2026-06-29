---
name: skill-launch-doctor
description: Audit, score, and improve agent skills before publishing, sharing, or installing them. Use when reviewing a SKILL.md file or skill folder for trigger quality, progressive disclosure, resource references, cross-agent compatibility, safety risks, install friction, marketplace positioning, launch readiness, or when rewriting a skill description to increase installs without locking it to one agent runtime.
---

# Skill Launch Doctor

## Overview

Use this skill to diagnose whether an agent skill is easy to discover, safe to install, compatible across runtimes, and ready for a marketplace or team rollout. Prefer deterministic checks first, then use judgment to rewrite only the parts that block adoption.

## Quick Start

From a repository root:

```bash
python3 skills/skill-launch-doctor/scripts/audit_skill.py path/to/skill
```

When running from this skill directory:

```bash
python3 scripts/audit_skill.py path/to/skill
```

JSON output for automation:

```bash
python3 scripts/audit_skill.py path/to/skill --format json
```

Fail a CI or release gate below a threshold:

```bash
python3 scripts/audit_skill.py path/to/skill --fail-under 85
```

## Workflow

1. Identify the target skill folder. If the user gives a single `SKILL.md`, audit its parent directory.
2. Run `scripts/audit_skill.py` and read the score, subscores, and findings.
3. Fix P0/P1 findings first: missing frontmatter, weak trigger description, unsafe install commands, missing resources, or runtime lock-in.
4. Rewrite `description` as a clear trigger surface: what it does, when to use it, and concrete user intents.
5. Trim the body so it teaches workflow, not generic agent behavior. Move detailed rubrics, examples, schemas, or provider-specific notes into `references/`.
6. Keep platform-specific metadata optional. Do not make the skill depend on one agent unless the skill truly cannot work elsewhere.
7. Re-run the audit and report the before/after score with remaining risks.

## Review Heuristics

Strong skills usually have:

- A `SKILL.md` with only `name` and `description` in frontmatter.
- A description that names the job, the triggering contexts, and the artifacts or workflows it handles.
- A short body with a decision tree or concrete workflow.
- Scripts for repeated or fragile operations.
- References for longer guidance that should not always enter context.
- Explicit output contracts so agents know what to produce.
- Clear safety boundaries around destructive actions, credentials, payments, publishing, and external messages.
- Runtime-neutral instructions unless a runtime dependency is essential.

Weak skills usually have:

- Vague descriptions such as "helps with productivity".
- Long README-style body text that repeats common agent advice.
- Required tools or APIs without setup guidance.
- Hard-coded local paths, private names, secrets, or one-machine assumptions.
- Unreviewed shell commands for install or publish flows.
- Unreferenced bundled resources or references to files that do not exist.

## Rewrite Rules

When improving a skill:

- Preserve the author's actual capability. Do not claim automation, integrations, or safety guarantees that are not implemented.
- Prefer concrete trigger language over marketing language.
- Remove platform lock-in unless requested by the user.
- Keep compatibility claims modest and testable.
- Keep the body concise. Put deeper scoring details in `references/launch-rubric.md`.
- Ask before changing author identity, license, pricing, or public publishing metadata.

## Resources

- `scripts/audit_skill.py`: stdlib-only auditor for a skill directory.
- `references/launch-rubric.md`: detailed scoring rubric and severity definitions.
- `references/description-patterns.md`: trigger description templates and anti-patterns.

## Output Contract

When reporting an audit, include:

- Overall score and verdict.
- P0/P1 findings with file paths and concrete fixes.
- Description rewrite, if the existing trigger surface is weak.
- Compatibility notes for generic AgentSkills and Hermes-style taps.
- Remaining launch risks and the smallest next action.
