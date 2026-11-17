## Description:

Vorim AI gives OpenClaw agents cryptographic identity, permission checks, trust scores, and audit trails so actions can be verified, permissioned, and logged.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kzino](https://clawhub.ai/user/kzino)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to register OpenClaw agents with Vorim AI, check permissions before sensitive actions, verify identity and trust, and emit audit events after actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vorim receives permission decisions and audit metadata for agent activity.

Mitigation: Use the skill only when the Vorim service and publisher are trusted, and avoid sending sensitive action details that are not required for auditing.

Risk: The skill depends on a live API key and third-party MCP server for identity, permission, and audit workflows.

Mitigation: Scope VORIM_API_KEY tightly, rotate it if exposed, and review the MCP server package before installation.

Risk: The install guidance uses an unpinned npm MCP server package.

Mitigation: Pin and review the package version in deployment configurations before using the skill in controlled environments.

## Reference(s):

- [Vorim AI](https://vorim.ai)
- [Vorim AI Documentation](https://vorim.ai/docs)
- [@vorim/mcp-server on npm](https://www.npmjs.com/package/@vorim/mcp-server)
- [Source Repository](https://github.com/Kzino/vorim-openclaw-skill)
- [ClawHub Skill Page](https://clawhub.ai/kzino/skills/vorim-ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VORIM_API_KEY and the mcporter-installed Vorim MCP server for live permission, identity, and audit operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
