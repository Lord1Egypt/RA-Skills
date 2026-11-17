## Description:

Looks up Zillow Zestimate, rent Zestimate, tax assessed value, and last sold price for a U.S. property through the ZillAPI service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zillapi](https://clawhub.ai/user/zillapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill when they need a property valuation anchor from an address, zpid, or Zillow URL. It is intended for explicit valuation requests, not listing search, photos, school data, or cases where an address appears only incidentally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided property addresses or zpids to the ZillAPI service for valuation data.

Mitigation: Use it only when the user has explicitly requested a valuation lookup and is comfortable sharing that property information with ZillAPI.

Risk: Calls require a ZillAPI API key and may consume API credits.

Mitigation: Configure ZILLAPI_KEY only in trusted environments and confirm that a lookup is needed before calling the API.

## Reference(s):

- [ZillAPI homepage](https://zillapi.com)
- [ZillAPI OpenAPI specification](https://zillapi.com/openapi.json)
- [ZillAPI property API documentation](https://zillapi.com/api/properties/)
- [ZillAPI hosted MCP server](https://api.zillapi.com/mcp)
- [ClawHub skill page](https://clawhub.ai/zillapi/skills/zillow-zestimate)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON object containing valuation data or a structured error object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ZILLAPI_KEY environment variable and either a zpid or address; address lookups first resolve a zpid before requesting valuation data.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
