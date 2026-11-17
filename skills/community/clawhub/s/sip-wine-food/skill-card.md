## Description:

Uses Sippai's MCP endpoint to search partner restaurants, retrieve bottle and glass wine menus and menu-sorted dishes, and help agents answer wine and featured-dish questions without fabricating unavailable items or prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sippai](https://clawhub.ai/user/sippai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent hosts use this skill to answer questions about Sippai partner restaurants, including available bottle or glass wines and featured dishes. The skill is intended for workflows where the host can connect to the Sippai MCP endpoint and rely on returned restaurant, wine, and dish data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a remote Sippai MCP service and may require an API key in some host environments.

Mitigation: Install it only when MCP access is intended, and provide any required key through the host's secure environment or configuration rather than embedding secrets in skill files.

Risk: Restaurant searches may return multiple matches, and menu data may be incomplete or unavailable.

Mitigation: Ask the user to choose a restaurant when multiple records match, and answer only from returned fields, explicitly saying when the service did not return a requested item or price.

## Reference(s):

- [Sippai wine and food skill documentation](https://sipsiip.com/ai/getwinefood)
- [ClawHub skill listing](https://clawhub.ai/sippai/skills/sip-wine-food)
- [Sippai MCP endpoint](https://mcp.sipsiip.com/api/sippai)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown or plain text responses based on MCP tool-returned JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include restaurant disambiguation prompts; answers should use only tool-returned fields and state when data is unavailable.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact files list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
