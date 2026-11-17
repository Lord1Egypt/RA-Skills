## Description:

MoltGuard is an OpenClaw security guard that helps detect prompt injection, data exfiltration, and malicious commands in files and web content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install and operate MoltGuard as a guardrail for prompt injection, data exfiltration, malicious commands, credential workflows, and security-status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned executable plugin, so behavior could change across installs or updates.

Mitigation: Prefer a pinned or verified plugin release and review update notes before installing or updating.

Risk: The skill handles API keys and Agent IDs that can appear in status or claim workflows.

Mitigation: Treat MoltGuard API keys and Agent IDs as secrets, avoid exposing them in logs or screenshots, and rotate them if disclosed.

Risk: Remote security scanning and credential storage are described with limited disclosure.

Mitigation: Review documentation for remote data handling and credential storage before use; prefer a private Core deployment for shared, regulated, or sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/superguard)
- [MoltGuard homepage](https://github.com/openguardrails/openguardrails/tree/main/moltguard)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, status, dashboard, account-claiming, enterprise enrollment, update, and uninstall guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
