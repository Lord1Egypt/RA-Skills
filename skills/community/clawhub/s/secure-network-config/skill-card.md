## Description:

网络配置排障 helps users configure and troubleshoot private network connections for privacy and remote access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IT operators, and security-minded users use this skill to prepare private network settings, diagnose connection failures, and produce setup or remediation guidance for privacy and remote access workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command and file-write authority while guiding private-network configuration, which can affect VPN, DNS, credentials, or system network settings.

Mitigation: Review the skill carefully before installing and approve each command, file change, network configuration change, and outbound API call before it runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/secure-network-config)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional JSON-style result summaries and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose network configuration changes, file edits, commands, and environment-variable setup; user approval is required before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
