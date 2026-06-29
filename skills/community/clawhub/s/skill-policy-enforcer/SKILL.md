---
name: skill-policy-enforcer
description: Use when checking an agent Skill against a local or enterprise policy before installation, publication, CI approval, marketplace review, or repository merge.
---

# Skill Policy Enforcer

## Overview

Enforce a caller-supplied policy over an agent Skill folder. Use it when a team needs repeatable pass/fail checks instead of a one-off security review.

## Quick Start

Run with a policy file:

```bash
python <this-skill>/scripts/enforce_skill_policy.py <skill-folder> --policy policy.yaml --markdown
```

Run without `--policy` to apply the default conservative policy. Use `--json` for CI.

## Policy Workflow

1. Locate the candidate skill folder and policy file.
2. Read `references/policy-schema.md` if the policy shape is unclear.
3. Run `scripts/enforce_skill_policy.py`.
4. Treat `deny` findings as blocking and `warn` findings as review items.
5. Report which policy rule caused each finding.

## Policy Scope

The default policy checks:

- required files and allowed frontmatter fields
- maximum file size and `SKILL.md` word count
- forbidden secret paths such as `.env`, `.ssh`, and private keys
- dangerous shell patterns such as recursive delete, shell pipe install, and encoded execution
- network use, if disabled by policy
- unfinished markers and generated template leftovers

## Required Behavior

- Do not override policy because a finding seems inconvenient.
- Do not invent policy exceptions. Ask for an updated policy file if needed.
- Quote the exact rule id for every deny or warning.
- If `--json` output is available, base final status on the machine result.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating policy as advice | Deny findings block install or release. |
| Auditing only `SKILL.md` | Policy applies to every file under the skill folder. |
| Hardcoding one company's rules | Put local rules in `policy.yaml`. |
| Missing hidden files | Scan dotfiles and nested resource folders too. |

## Output Contract

End with one of:

- `PASS`: no deny findings.
- `PASS_WITH_WARNINGS`: warnings remain.
- `FAIL`: at least one deny finding.
