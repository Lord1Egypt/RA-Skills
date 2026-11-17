## Description:

Scan codebases for technical debt, including TODO/FIXME comments, deprecated APIs, complexity hotspots, outdated patterns, missing tests, and large files, then prioritize findings with AI reasoning and generate remediation plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to audit codebases for technical debt, prioritize cleanup work before sprint planning, and generate actionable remediation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency health checks may contact package registries and disclose package names or local environment package information.

Mitigation: Run dependency checks only where that network access is acceptable, and skip them in offline or restricted-network environments.

Risk: Broad scans of large or sensitive repositories may surface more code context than intended.

Mitigation: Scope scans to the relevant subdirectory when working in large or sensitive repositories.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Human-readable text or Markdown reports, with optional JSON-style structures and shell commands for static analysis workflows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce prioritized findings with severity, risk, effort, impact, remediation steps, and CI-oriented exit-code guidance.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
