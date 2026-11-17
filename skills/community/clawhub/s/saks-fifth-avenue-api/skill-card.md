## Description:

Search Saks Fifth Avenue listings and retrieve product, pricing, variant inventory, store availability, store, suggestion, and designer data as structured JSON through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and shopping agents can search Saks Fifth Avenue products, compare sale and regular prices, check online variants and nearby store availability, and retrieve designer or store information.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Store availability lookups send the supplied ZIP code or coordinates to Scavio, creating a location privacy concern.

Mitigation: Ask before sharing location data and use a ZIP code instead of precise coordinates when it meets the user's needs.

Risk: The security review was partial because four local references could not be resolved.

Mitigation: Review the unresolved references and complete a full security scan before deployment.

## Reference(s):

- [Scavio Saks product API documentation](https://scavio.dev/docs/saks-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=saks-fifth-avenue-api)
- [Scavio Saks API overview](https://scavio.dev/saks-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=saks-fifth-avenue-api)

## Skill Output:

**Output Type(s):** [Structured data, API results, Shopping guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product and store data returned by the API; availability and prices may change.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
