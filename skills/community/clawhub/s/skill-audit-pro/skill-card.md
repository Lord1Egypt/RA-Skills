## Description:

Scans installed OpenClaw skills for security issues such as hardcoded credentials, shell-injection patterns, environment exposure, and network-exfiltration indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohmanymoneygomyhome-creator](https://clawhub.ai/user/ohmanymoneygomyhome-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to scan installed or local skills and receive security-oriented findings before or after installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read installed and workspace skill files, as well as OpenClaw session routing metadata.

Mitigation: Install only where that local file and routing metadata access is acceptable, and prefer a version with explicit opt-in reporting and narrower scan scope.

Risk: Reports may expose recipient metadata through CHANNELS output.

Mitigation: Use a version that removes CHANNELS output or review report destinations before enabling automated channel delivery.

Risk: Broad scanning can traverse more files than intended or follow unsafe paths.

Mitigation: Prefer a version that rejects symlinks and applies scan size and time limits.

## Reference(s):

- [Skill Security Audit Reference](references/security-checks.md)
- [ClawHub Skill Page](https://clawhub.ai/ohmanymoneygomyhome-creator/skills/skill-audit-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style security scan reports with severity summaries, issue locations, recommendations, and command-line guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit report text for configured OpenClaw channels and command-line exit codes for allow, warning, or block recommendations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
