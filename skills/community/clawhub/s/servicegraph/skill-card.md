## Description:

Servicegraph helps agents handle explicit ServiceGraph requests by discovering available datasets and schemas, searching free brief rows, and unlocking selected contact or metric details with credits after confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user explicitly asks for ServiceGraph data discovery, schema exploration, dataset search, or selected row unlocks. It is intended for dataset-agnostic ServiceGraph workflows and directs the agent to confirm pricing before spending credits.

### Deployment Geography for Use:

Global, with the skill directing searches toward U.S. firms where applicable.

## Known Risks and Mitigations:

Risk: ServiceGraph queries may send search criteria or dataset requests over the network.

Mitigation: Use the configured ServiceGraph API or MCP endpoint only and avoid sending secrets or unnecessary sensitive inputs.

Risk: Unlocking rows can spend ServiceGraph credits and reveal contact or metric details.

Mitigation: Check the dataset price and credit balance when needed, then get explicit user confirmation before unlocking rows.

Risk: REST authentication depends on a ServiceGraph API key.

Mitigation: Keep SERVICEGRAPH_API_KEY in environment variables or harness-managed auth and do not paste keys into chat.

## Reference(s):

- [ServiceGraph API](https://api.servicegraph.co)
- [ServiceGraph MCP Server](https://mcp.servicegraph.co)
- [ServiceGraph API Keys](https://servicegraph.co/profile/api-keys)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell Commands, Markdown]

**Output Format:** [Markdown guidance with inline API or shell examples and optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query ServiceGraph over the network; unlocking selected rows requires explicit user confirmation and can spend ServiceGraph credits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
