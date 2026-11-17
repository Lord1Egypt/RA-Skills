## Description:

YRI AdX helps agents manage Facebook advertising through the baiz.ai MCP API, including campaign creation, budget changes, audience targeting, creative management, and performance monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuriskills](https://clawhub.ai/user/yuriskills)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, ad operators, and developers use this skill to prepare, launch, monitor, and adjust Facebook ad campaigns through baiz.ai using JSON-RPC curl commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, publish, stop, copy, or adjust Facebook ad campaigns in ways that may affect spend and delivery.

Mitigation: Verify each campaign or budget-changing action before sending it, test with sandbox or low-limit accounts first, and avoid autonomous use.

Risk: BAIZ_API_TOKEN grants access through baiz.ai to connected advertising accounts.

Mitigation: Use a revocable minimal-permission or read-only test token where possible, keep the token sensitive, and revoke it if metadata or endpoint behavior does not match the artifact.

Risk: Users must trust baiz.ai with ad account access and billing impact.

Mitigation: Review baiz.ai terms, privacy practices, token scopes, and dashboard behavior before connecting production advertising accounts.

Risk: Marketplace or registry metadata that omits BAIZ_API_TOKEN could lead to unsafe credential handling.

Mitigation: Halt installation and contact the publisher if the registry listing does not declare BAIZ_API_TOKEN as a required sensitive credential.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuriskills/skills/yuri-ad-skill)
- [Publisher profile](https://clawhub.ai/user/yuriskills)
- [baiz.ai](https://baiz.ai)
- [baiz.ai MCP endpoint](https://baiz.ai/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON-RPC curl examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIZ_API_TOKEN supplied as a sensitive environment variable; API calls are stateless HTTPS requests to baiz.ai.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
