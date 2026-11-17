## Description:

The trust layer for AI agents -- encrypted channels, identity, audit, attestations, trust circles, key rotation, and federation using MLS protocol (RFC 9420).

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicholasraimbault](https://clawhub.ai/user/nicholasraimbault)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure and operate Skytale MCP tools for encrypted multi-agent messaging, shared context, identity, key rotation, audit logging, attestations, trust circles, and federation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script installs the external skytale-sdk[mcp] package without a pinned version.

Mitigation: Install in an isolated Python environment and pin a reviewed skytale-sdk version before enabling the MCP server for sensitive workflows.

Risk: The skill depends on API keys and cryptographic exchange tokens for encrypted messaging.

Mitigation: Keep SKYTALE_API_KEY, encryption keys, key packages, and Welcome messages out of prompts, logs, and channel messages; review the MCP configuration before use.

## Reference(s):

- [Skytale OpenClaw integration documentation](https://skytale.sh/docs/integrations/openclaw)
- [Openclaw skill page on ClawHub](https://clawhub.ai/nicholasraimbault/skills/skytale)
- [nicholasraimbault publisher profile on ClawHub](https://clawhub.ai/user/nicholasraimbault)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require SKYTALE_API_KEY, Python, and OpenClaw MCP configuration; channel names use org/namespace/service format.]

## Skill Version(s):

0.5.2 (source: server release metadata; artifact frontmatter reports 0.5.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
