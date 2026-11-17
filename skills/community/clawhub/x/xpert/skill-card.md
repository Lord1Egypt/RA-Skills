## Description:

Grow on X (Twitter) with Xpert — connect over MCP or REST, then draft, rewrite, schedule, analyze, and reply in the user's own voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xpert](https://clawhub.ai/user/xpert)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use Xpert to connect to an X account, draft and rewrite posts, schedule approved content, analyze engagement, and reply to audiences in the user's own voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad write, direct-message, admin, and generic API capabilities can affect a connected X account.

Mitigation: Grant only the minimum OAuth scopes needed for the task, avoid `dm` and `admin` unless required, and review post, campaign, account-connection, and API-key actions before allowing them.

Risk: Generated social content could be inaccurate, off-brand, or published before the user is ready.

Mitigation: Show generated posts, replies, and schedules to the user for approval before publishing or scheduling.

## Reference(s):

- [Xpert homepage](https://xpert.so)
- [Xpert MCP server card](https://xpert.so/.well-known/mcp/server-card.json)
- [Xpert OAuth authorization server metadata](https://api.xpert.so/.well-known/oauth-authorization-server)
- [Xpert MCP protected resource metadata](https://mcp.xpert.so/.well-known/oauth-protected-resource)
- [ClawHub skill page](https://clawhub.ai/xpert/skills/xpert)

## Skill Output:

**Output Type(s):** [guidance, configuration, API calls, text, markdown]

**Output Format:** [Markdown guidance with endpoint URLs, OAuth flow details, and task-oriented API or MCP actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OAuth 2.1 authorization; generated posts, direct messages, account changes, and API-key actions should be reviewed before execution.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
