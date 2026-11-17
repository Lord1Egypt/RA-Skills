## Description:

MoltGuard helps protect OpenClaw agents and users from prompt injection, data exfiltration, and malicious commands hidden in files or web content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaslwang](https://clawhub.ai/user/thomaslwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and manage MoltGuard protection for OpenClaw agents, including status checks, account linking, API key configuration, dashboard access, and enterprise enrollment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users or agents to install an unpinned third-party plugin that performs remote security checks.

Mitigation: Use only if OpenGuardrails/Core is trusted with the security context it may inspect, and prefer a pinned, audited plugin version before deployment.

Risk: The artifact says status and claim commands show API keys or agent credentials.

Mitigation: Do not share `/og_status` or `/og_claim` output, and treat screenshots, logs, and terminal transcripts from those commands as sensitive.

Risk: The artifact says credentials are stored locally under the OpenClaw credentials directory.

Mitigation: Confirm credential file permissions on shared machines and verify uninstall behavior removes local MoltGuard configuration and credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thomaslwang/skills/skill-antivirus)
- [OpenGuardrails MoltGuard Homepage](https://github.com/openguardrails/openguardrails/tree/main/moltguard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that install or configure a third-party OpenClaw plugin and display local credential or status information.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports MoltGuard 6.8.21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
