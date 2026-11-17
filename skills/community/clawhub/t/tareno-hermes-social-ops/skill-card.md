## Description:

Operate Tareno social accounts, calendars, drafts, media, analytics and Get Viral projects through an authorized Tareno MCP connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarenoai](https://clawhub.ai/user/tarenoai)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers and teams use this skill with an authorized Tareno connection to inspect accounts and analytics, prepare drafts and media, research content ideas, and request approval for publishing or scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing, scheduling, editing or deleting content on the wrong account or before review.

Mitigation: Verify the workspace, account, content and timing; show the impact and Tareno approval request, then check the final action status.

Risk: Get Viral analysis may consume AI credits.

Mitigation: Show the quoted credit cost and obtain Tareno approval before starting analysis.

Risk: Connecting the service exposes selected social accounts to an agent integration.

Mitigation: Authorize only intended accounts, review available tools, preserve existing access policies and keep OAuth credentials out of prompts.

## Reference(s):

- [Tareno social operations source](https://github.com/TarenoAI/tareno-agent-skills/tree/main/skills/tareno-hermes-social-ops)
- [Tareno MCP documentation](https://tareno.co/docs/mcp)
- [Hermes MCP setup documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)
- [Example requests](references/example-prompts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown and plain text, with configuration or shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on authorized accounts and available Tareno tools; approval requests are not completed actions.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
