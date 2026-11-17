## Description:

Unified search API across Google, Amazon, Yelp, OpenTable, Walmart, and more. Use when searching for products, local businesses, restaurants, shopping, images, news, or any web search. One API key, many engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianpcook](https://clawhub.ai/user/ianpcook)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run structured searches across web, local, shopping, image, and news engines through SerpAPI. It is useful for product research, local business discovery, restaurant lookup, shopping comparison, image search, news search, and general web search tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, selected engine parameters, and any explicit or configured default location are sent to SerpAPI.

Mitigation: Avoid sensitive internal queries and private addresses unless that disclosure is acceptable.

Risk: The skill requires a SerpAPI API key.

Mitigation: Keep SERPAPI_API_KEY scoped to SerpAPI and manage it as a service credential.

## Reference(s):

- [SerpAPI homepage](https://serpapi.com)
- [ClawHub SerpAPI skill page](https://clawhub.ai/ianpcook/skills/serpapi)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration, JSON, Text]

**Output Format:** [JSON by default, with optional human-readable text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SERPAPI_API_KEY and may use an explicit or configured default location for local searches.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
