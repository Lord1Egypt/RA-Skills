## Description:

Search Viator tours, activities and experiences via MCP. Use when the user asks to find tours, activities, excursions, day trips, tickets, or "things to do" in a city or destination, get details/pricing/availability for a Viator product, list attractions in a destination, or convert supplier-currency prices. Triggers on phrases like "things to do in Rome", "find a food tour in Paris", "is this tour available in September", "Viator", "book an excursion" (search only — no booking), or "skip-the-line Colosseum tickets". Requires the @chrischall/viator-mcp package installed and the viator server registered (see Setup), plus a Viator Partner API key (free Basic Access affiliate tier).

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel assistants use this skill to find and compare Viator tours, attractions, availability, and prices for named destinations. It supports searches and product details only; booking takes place through Viator links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Viator API key could be exposed through credential-bearing configuration.

Mitigation: Protect VIATOR_API_KEY and keep credential-bearing configuration out of version control.

Risk: The external runtime package was not fully verified.

Mitigation: Review and pin the package version before setup.

## Reference(s):

- [Viator MCP package on npm](https://www.npmjs.com/package/@chrischall/viator-mcp)
- [Viator Partner Resources](https://partnerresources.viator.com/)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON tour, attraction, destination, availability, and pricing results, optionally summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and product details only; booking is not supported.]

## Skill Version(s):

2.2.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
