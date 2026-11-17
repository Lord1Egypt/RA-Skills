## Description:

Scan ClawHub skills for security vulnerabilities before installing them, including prompt injections, malware payloads, hardcoded secrets, and other threats, using Snyk Agent Scan as a pre-flight check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[firefrog-pepe](https://clawhub.ai/user/firefrog-pepe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to stage a ClawHub skill, scan it before installation, and either install clean results or quarantine suspicious results for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports unsafe path handling that could affect local files during staging or installation.

Mitigation: Use a disposable or backed-up workspace and review slug and path handling before trusting the installer on important local data.

Risk: The security evidence reports mutable runtime dependencies, including scanner installation at runtime.

Mitigation: Pin and review scanner versions before operational use, and avoid running unreviewed dependency updates in sensitive environments.

Risk: Scanner availability or configuration failures can prevent the pre-install scan from completing.

Mitigation: Configure SNYK_TOKEN and verify the scan completed before installing a staged skill.

Risk: The script includes a scan bypass option for explicit override cases.

Mitigation: Use the bypass only after manual review and an explicit risk acceptance decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/firefrog-pepe/skills/skill-guard-snyk-agent-scan)
- [uv installer](https://astral.sh/uv/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, exit-code guidance, and scanner review instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local staging, quarantine, and scan-report paths through the shell wrapper.]

## Skill Version(s):

1.0.3 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
