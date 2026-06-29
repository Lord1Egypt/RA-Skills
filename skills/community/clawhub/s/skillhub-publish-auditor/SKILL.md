---
name: skillhub-publish-auditor
description: Use when preparing a Skill folder for public release to SkillHub, ClawHub, or another agent-skill marketplace, especially before publishing third-party installable skills, scripts, references, metadata, or examples.
---

# SkillHub Publish Auditor

## Overview

Audit an agent Skill as a public package, not a private note. The goal is to catch release blockers, weak discovery metadata, unsafe scripts, credential leaks, unfinished template markers, and packaging issues before upload.

## Quick Start

Run the bundled auditor from the skill folder you want to publish:

```bash
python <this-skill>/scripts/audit_skill_release.py <skill-folder> --markdown
```

Use `--json` for CI or automated marketplace checks.

## Release Standard

Apply four gates in order:

1. Structure: `SKILL.md` exists, frontmatter parses, name is publishable, and no unfinished template markers remain.
2. Discovery: description starts with `Use when`, names concrete triggers, and does not summarize the whole workflow.
3. Safety: scripts and references do not read secrets, hide instruction-override payloads, run destructive shell commands, or send local data out.
4. Packaging: resource links resolve, examples are intentional, auxiliary files are not clutter, and UI metadata is useful.

Read `references/release-checklist.md` when judging borderline findings or preparing a manual review.

## Required Behavior

- Treat every file in the candidate skill as publishable supply-chain content.
- Inspect scripts before recommending release, even when `SKILL.md` looks clean.
- Mark issues as `blocker`, `warn`, or `info`; keep each finding specific.
- Recommend exact file-level fixes, but do not auto-edit unless the user asks.
- If the skill executes code, require at least one local smoke test or explain why no test can run.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Publishing template text | Remove unfinished markers and generated instructions. |
| Description explains workflow | Rewrite it as trigger conditions only. |
| Security review stops at `SKILL.md` | Scan every script, reference, config, and example. |
| Marketplace metadata ignored | Check `agents/openai.yaml` when present. |
| "Harmless" helper scripts read env files | Flag environment, SSH, credential, token, and key access. |

## Output Contract

End with a release decision:

- `READY`: no blockers.
- `READY_WITH_WARNINGS`: warnings remain, but no release blocker.
- `BLOCKED`: one or more blockers must be fixed before publishing.
