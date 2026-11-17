## Description:

System health validator that checks skill files, paths, permissions, binaries, backup freshness, and encryption, then produces pass/fail reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto)

### License/Terms of Use:


## Use Case:

External OpenClaw Greek Accounting operators, administrators, and agent users use this skill to run read-only system health checks before scheduled or critical accounting operations. It reports file, directory, permission, dependency, backup, encryption, and lock status with remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects sensitive accounting, authentication, backup, and integrity paths, and saved reports can expose system status.

Mitigation: Install it only in the intended OpenClaw Greek Accounting environment and restrict access to generated reports and failure logs.

Risk: The setup example includes sudo-based dependency installation.

Mitigation: Review dependency installation before use and prefer the organization's normal package-management process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/satoshistackalotto/skills/system-health-check)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown-style health reports with inline shell commands and optional JSON report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only diagnostic output; saved reports may contain sensitive system status and should be access-controlled.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
