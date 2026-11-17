## Description:

Security auditing for OpenClaw agent skills that scans for dangerous patterns, vulnerable dependencies, and suspicious behaviors before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathanliu811026](https://clawhub.ai/user/jonathanliu811026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to audit OpenClaw agent skills before installation, including checks for dangerous code patterns, filesystem risks, network vulnerabilities, suspicious shell commands, and vulnerable dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to run the external npm package `skillguard-audit`, so the reviewed artifact does not fully define the code that will execute.

Mitigation: Use a pinned and reviewed package version with a lockfile-backed install, and run audits in an isolated environment without unnecessary credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jonathanliu811026/skills/skill-guard-security)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON report examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces audit verdicts such as SAFE, CAUTION, or DANGEROUS with risk details for reviewed skills.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
