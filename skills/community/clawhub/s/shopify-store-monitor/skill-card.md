## Description:

Track Shopify store sales and monitor store performance using PPSPY sales monitoring tools. Create monitoring tasks, inspect hourly and daily sales, and manage monitored stores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyanggod](https://clawhub.ai/user/fanyanggod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor Shopify store sales through PPSPY, including creating monitoring tasks, reviewing real-time sales records, and inspecting hourly or daily sales statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an external npm MCP server with access to the user's PPSPY API key.

Mitigation: Install only after trusting PPSPY and the ppspy-mcp-server package, avoid administrator installation when possible, and use a limited PPSPY API key if available.

Risk: Delete operations can remove monitoring groups, tasks, or monitoring setup.

Mitigation: Confirm group and task IDs before running delete operations.

Risk: Some PPSPY API calls consume account credits or monitoring quota.

Mitigation: Review PPSPY billing, recharge, and quota status before creating monitoring tasks or making repeated API calls.

## Reference(s):

- [PPSPY official website](https://www.ppspy.com)
- [PPSPY API site](https://api.ppspy.com/)
- [ClawHub skill page](https://clawhub.ai/fanyanggod/skills/shopify-store-monitor)
- [Publisher profile](https://clawhub.ai/user/fanyanggod)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Text]

**Output Format:** [Markdown with setup steps, tool names, and natural-language usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npm and a PPSPY_API_KEY; PPSPY account credits or monitoring quota may be consumed by some API calls.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
