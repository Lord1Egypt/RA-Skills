## Description:

Searches US property listings for sale, rent, or sold comparables through the Zillapi API with filters for location, price, beds, baths, square footage, year built, home type, days on Zillow, and result count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zillapi](https://clawhub.ai/user/zillapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search US residential listings, rentals, and sold comparables when they provide an explicit location or bounding box and listing criteria.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Zillapi receives submitted search locations, bounding boxes, filters, and the API key for each query.

Mitigation: Use a dedicated Zillapi key and avoid submitting sensitive or unnecessary location criteria.

Risk: Broad searches may consume Zillapi credits because returned listings consume credits.

Mitigation: Keep max_items low and confirm broad searches before running them.

## Reference(s):

- [Zillapi Homepage](https://zillapi.com)
- [Zillapi OpenAPI Specification](https://zillapi.com/openapi.json)
- [Zillapi Property API Documentation](https://zillapi.com/api/properties/)
- [Zillapi Hosted MCP Server](https://api.zillapi.com/mcp)

## Skill Output:

**Output Type(s):** [API Calls, Structured data]

**Output Format:** [JSON object with listing data, metadata, or error details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZILLAPI_KEY; max_items is capped at 50 and each returned listing consumes one credit.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
