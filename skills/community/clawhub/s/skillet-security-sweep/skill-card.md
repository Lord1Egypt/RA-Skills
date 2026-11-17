## Description:

Use when asked to security-audit a repository, find vulnerabilities and prescribe fixes, check for leaked secrets, review dependencies for known CVEs, or harden a project before exposure. Read-only audit. Applying the fixes belongs to expedite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to audit authorized repositories for exposed secrets, vulnerable dependencies, unsafe input handling, authorization gaps, and risky exposure, then prioritize verified findings with remediation guidance before exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auditing a repository or its Git history without authorization could expose sensitive information or exceed the intended scope.

Mitigation: Use the skill only on repositories and histories you are authorized to inspect.

Risk: A discovered credential could be exposed again through a report, tool log, or shared output.

Mitigation: Redact secrets and refer to them only by file, line, and type; never copy or echo their values.

Risk: Findings based on configuration that cannot be inspected may be incomplete or overstated.

Mitigation: Mark such findings unverified, lower severity by one level, and identify skipped areas in the report.

## Reference(s):

- [Security Sweep on ClawHub](https://clawhub.ai/escoffier-labs/skills/skillet-security-sweep)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown security-audit report with a verdict, scorecard, prioritized findings, remediation guidance, backlog, and not-checked areas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only audit; secret values are never included in reports or logs. Findings dependent on unavailable configuration are marked unverified and assigned one lower severity.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
