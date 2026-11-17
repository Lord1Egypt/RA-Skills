---
name: work-productivity-skillscan-security-workflow-helper
description: Run a security review workflow for Codex or ClawHub skills before activation or publication. Use when the user needs to inspect skill files, scripts, permissions, network behavior, secret handling, dependency risks, or release-readiness gates.
---

# Work Productivity SkillScan Security Workflow Helper

Use this skill as a pre-activation or pre-publish security gate for skill folders. It focuses on practical review steps an agent can perform locally before a user trusts a skill.

Read `references/requirement-plan.md` when you need demand evidence or acceptance criteria.

## Scan Scope

Establish:

- Skill folder path and intended runtime.
- Files that execute code: scripts, package manifests, agent configs, hooks, or generated binaries.
- Declared tools, network calls, file writes, and credential touchpoints.
- Whether the review is advisory, blocking, or release-gating.

## Workflow

1. Inventory the skill folder and separate instructions, references, scripts, assets, and generated files.
2. Inspect executable content for destructive commands, shell injection, credential exposure, unsafe downloads, and broad filesystem writes.
3. Review `SKILL.md` triggers for overbroad activation or misleading capability claims.
4. Check dependencies and scripts for pinned versions, install-time behavior, and external network use.
5. Produce findings with severity, evidence, affected file, and recommended fix.
6. Decide pass, pass with warnings, or block, based on the user's gate policy.

## Guardrails

- Do not execute untrusted scripts unless the user asks and the environment is appropriate.
- Prefer static inspection before dynamic tests.
- Treat secrets, tokens, private URLs, and copied user content as sensitive.
- Keep findings actionable and tied to exact files.

## Outputs

- Skill security scan report.
- Blocking findings and remediation checklist.
- Safe publish or activation recommendation.
- Follow-up validation commands when dynamic testing is appropriate.

## Validation Checklist

- Executable files and dependencies were inspected.
- Any risky operation has a file reference and severity.
- The final pass/block decision matches the evidence.
- The user can remediate each finding without guessing.

## Triggers

Keywords: SkillScan, skill security, scan skill, pre-publish review, unsafe script, dependency risk, activation gate, secret handling.

Example requests:

- `Scan this skill before I publish it.`
- `Use $work-productivity-skillscan-security-workflow-helper to review scripts and permissions.`
- `Tell me whether this ClawHub skill should be blocked for security reasons.`
