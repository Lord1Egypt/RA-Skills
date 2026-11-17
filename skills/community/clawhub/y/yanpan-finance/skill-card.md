## Description:

A-Share Multi-Dimensional Quantitative Analysis MCP Server - broker research reports, AI news analysis, and stock comprehensive analysis

This skill is ready for commercial/non-commercial use.

## Publisher:

[li-evan](https://clawhub.ai/user/li-evan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers connect AI agents to a hosted MCP server for China A-share broker research reports, AI-analyzed news, and stock analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext bearer-token setup guidance can expose API keys or sensitive financial queries in transit.

Mitigation: Use the hosted endpoint only if you trust the operator and accept plaintext transport risk; prefer HTTPS before sending valuable credentials or sensitive queries.

Risk: The submitted server code includes hardcoded default authentication and database administrator credentials.

Mitigation: For self-hosting, remove hardcoded secrets, rotate exposed credentials, and use least-privilege database accounts.

Risk: Broad query access and uncapped result sizes can increase data exposure or service abuse risk.

Mitigation: Add scopes or rate limits, escape search input, and cap result limits before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/li-evan/skills/yanpan-finance)
- [Publisher profile](https://clawhub.ai/user/li-evan)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and text responses from MCP tools, plus JSON configuration guidance for setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool responses can include full-text research reports, AI news summaries, sentiment analysis, investment recommendations, and stock analysis reports.]

## Skill Version(s):

1.5.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
