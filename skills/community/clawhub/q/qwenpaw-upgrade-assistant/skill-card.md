## Description:

Checks the installed and latest QwenPaw versions, reviews upgrade compatibility, and recommends upgrade and rollback steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trend0522](https://clawhub.ai/user/trend0522)

### License/Terms of Use:

MIT-0

## Use Case:

QwenPaw users and administrators use this skill to check whether an upgrade is available, assess compatibility with their skills, plugins, and MCP settings, and plan backup, upgrade, verification, or rollback steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Version and release-note checks contact external sites and may fail if they are unreachable.

Mitigation: Confirm the source and latest version independently when network checks fail or return unexpected results.

Risk: Compatibility checks may inspect local QwenPaw skills, plugins, and MCP settings before an upgrade.

Mitigation: Review what is inspected, back up important data, and approve any suggested changes before executing them; do not provide credentials.

## Reference(s):

- [QwenPaw Upgrade Assistant on ClawHub](https://clawhub.ai/trend0522/skills/qwenpaw-upgrade-assistant)
- [QwenPaw version information on PyPI](https://pypi.org/pypi/qwenpaw/json)
- [QwenPaw release notes](https://qwenpaw.agentscope.io/release-notes)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Structured Markdown report with version comparison, compatibility findings, and recommended steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides backup, upgrade, verification, and rollback guidance; does not automatically upgrade or request credentials.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
