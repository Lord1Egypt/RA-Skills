## Description:

Surprise Buddy helps agents look up curated, country-scoped gift ideas with product titles, prices, images, fit rationale, and marketplace links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebastian1747](https://clawhub.ai/user/sebastian1747)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to help people find gift ideas by country, occasion, age, interests, profession, budget, and color preferences. The agent returns curated product options with marketplace links instead of performing a generic web search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gift preference filters are sent to an external MCP service.

Mitigation: Avoid entering sensitive personal details beyond the country, occasion, age range, budget, and preference filters needed for the gift search.

Risk: Returned marketplace URLs may contain query parameters needed for link function or attribution.

Mitigation: Preserve product URLs exactly as returned and review links before presenting them to users.

Risk: The curated database is not a generic web search or live price oracle.

Mitigation: Tell users that empty results are valid, prices may reflect last verification, and filters may need to be widened.

## Reference(s):

- [Surprise Buddy skill page](https://clawhub.ai/sebastian1747/skills/surprise-buddy)
- [Surprise Buddy developer landing page](https://www.surprise-buddy.com/en/agents)
- [Surprise Buddy MCP endpoint](https://www.surprise-buddy.com/api/mcp)
- [Surprise Buddy MCP discovery manifest](https://www.surprise-buddy.com/.well-known/mcp.json)
- [Surprise Buddy OpenAPI 3.1 spec](https://www.surprise-buddy.com/openapi.yaml)
- [Surprise Buddy LLMs.txt](https://www.surprise-buddy.com/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown gift cards with product details and links, backed by JSON MCP tool responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Country is required; returned product URLs should be preserved exactly as provided.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
