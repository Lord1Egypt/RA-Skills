## Description:

Add policy evaluation, human approval, and audit trails to any tool. Powered by SidClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vladuzh](https://clawhub.ai/user/vladuzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and organizations using OpenClaw agents use this skill to apply policy checks, human approval workflows, and audit trails to MCP tool calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MCP tool-call context and audit logs may be visible to a third-party governance service.

Mitigation: Use this skill only where SidClaw is trusted for the relevant data, and avoid proxying highly sensitive tools until data handling is documented.

Risk: The configured SDK or proxy package could change after installation if it is not pinned or reviewed.

Mitigation: Pin or vendor a reviewed SDK version where possible.

Risk: The governed agent process may still have broad local privileges.

Mitigation: Run OpenClaw with least-privilege credentials, filesystem access, and network access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vladuzh/skills/sidclaw-governance)
- [SidClaw Website](https://sidclaw.com)
- [SidClaw Documentation](https://docs.sidclaw.com)
- [SidClaw SDK on npm](https://www.npmjs.com/package/@sidclaw/sdk)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Markdown, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance depends on SidClaw policy decisions and configured environment variables.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
