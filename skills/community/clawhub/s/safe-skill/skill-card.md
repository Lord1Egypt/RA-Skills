## Description:

Safe Skill is a static security scanner for AI agent skills that checks code and documentation for risky patterns, credential access, suspicious endpoints, obfuscation, and permission scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjzac](https://clawhub.ai/user/zjzac)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Safe Skill before installing or reviewing ClawHub, GitHub, or other third-party skills to produce a first-pass security assessment and installation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanner output can understate risk when target content suppresses or bypasses checks.

Mitigation: Treat scan results as first-pass triage and review high-impact behavior before installation.

Risk: The --env-check option can inspect local OpenClaw files, memory, installed skills, crontab, services, and PATH.

Mitigation: Use --env-check only with explicit intent and run scans for unknown repositories in a constrained workspace.

Risk: Static analysis can miss runtime-only behavior and does not perform network reputation checks.

Mitigation: Combine scanner findings with human review and stronger isolation when higher assurance is needed.

## Reference(s):

- [Safe Skill ClawHub page](https://clawhub.ai/zjzac/skills/safe-skill)
- [Artifact README](artifact/README.md)
- [Artifact skill manifest](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown summary with optional JSON scanner output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scanner exit codes indicate risk level; JSON output is available with --json.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
