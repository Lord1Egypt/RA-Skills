## Description: <br>
Complete Zillow property data toolkit via Zillapi.com for address, URL, and zpid lookup, Zestimate data, listing search, photos, schools, price history, and agent contact retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikhonit](https://clawhub.ai/user/nikhonit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and real-estate workflows use this skill to retrieve user-requested U.S. property, valuation, listing, school, photo, price-history, and listing-agent data through Zillapi. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Zillapi API key and uses it to send property lookup requests to Zillapi. <br>
Mitigation: Use a dedicated API key, monitor credit usage, and avoid submitting addresses or listing searches that should not be sent to Zillapi. <br>
Risk: Each intended lookup can consume Zillapi credits and may return large property records. <br>
Mitigation: Call the tools only for explicit user requests about property data and confirm ambiguous intent before making a request. <br>


## Reference(s): <br>
- [Zillapi homepage](https://zillapi.com) <br>
- [Zillapi OpenAPI spec](https://zillapi.com/openapi.json) <br>
- [Zillapi property API documentation](https://zillapi.com/api/properties/) <br>
- [Hosted Zillapi MCP server](https://api.zillapi.com/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/nikhonit/zillow-full) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON data, Guidance] <br>
**Output Format:** [Python dictionaries containing Zillapi JSON responses or structured error objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZILLAPI_KEY and sends user-requested property queries to Zillapi.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
