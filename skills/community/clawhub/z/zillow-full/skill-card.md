## Description:

zillow-full helps agents retrieve US property records, valuations, listing searches, photos, schools, price history, and listing-agent details through the Zillapi API for user-directed Zillow or real estate requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zillapi](https://clawhub.ai/user/zillapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer intentional US property, valuation, rental, listing, comps, and Zillow URL questions when a Zillapi API key is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Property addresses, Zillow URLs, zpids, and listing filters are sent to Zillapi with the user's API key.

Mitigation: Use the skill only for intentional property or listing requests, and avoid sending incidental addresses or unrelated real estate text.

Risk: Successful Zillapi calls may consume account credits, especially listing searches that return multiple records.

Mitigation: Prefer narrow tools for specific answers and keep listing search result limits tight.

## Reference(s):

- [zillow-full tool reference](artifact/reference.md)
- [Zillapi homepage](https://zillapi.com)
- [Zillapi OpenAPI spec](https://zillapi.com/openapi.json)
- [Zillapi REST property docs](https://zillapi.com/api/properties/)
- [Zillapi hosted MCP server](https://api.zillapi.com/mcp)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON-like Python dictionaries and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZILLAPI_KEY; successful Zillapi calls may consume credits.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
