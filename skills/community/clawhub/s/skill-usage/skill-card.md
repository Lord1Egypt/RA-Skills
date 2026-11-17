## Description:

Install and set up the OpenClaw Skill Usage plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucifinil](https://clawhub.ai/user/lucifinil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install and verify the OpenClaw Skill Usage plugin, enable /skillusage commands, and choose between local-only analytics and shared cloud-backed usage spaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to install an external plugin and restart the OpenClaw Gateway.

Mitigation: Only invoke installation or restart steps after the user intentionally asks to install or enable the plugin and accepts the restart.

Risk: The installed plugin may use shared cloud-backed analytics where labels, routing identifiers, timestamps, status, and latency can be sensitive metadata.

Mitigation: Use local-only mode unless the user explicitly wants shared analytics, and explain what metadata is sent before shared setup.

Risk: The external plugin package may be unpinned or not independently verified.

Mitigation: Review the plugin package and publisher, and prefer a pinned or verified release before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lucifinil/skills/skill-usage)
- [Publisher Profile](https://clawhub.ai/user/lucifinil)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and slash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides plugin installation, gateway restart, verification commands, and optional shared analytics setup.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
