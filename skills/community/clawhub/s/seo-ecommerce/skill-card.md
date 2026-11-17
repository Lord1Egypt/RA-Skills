## Description:

Analyzes e-commerce product pages and stores for product SEO, schema readiness, Google Shopping visibility, Amazon marketplace intelligence, competitor pricing, and marketplace keyword gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

SEO practitioners, e-commerce operators, and developers use this skill to audit product pages, validate Product schema, compare marketplace visibility, and identify keyword or pricing opportunities. It can run standalone for on-page and schema checks, with optional paid DataForSEO Merchant API calls for live Google Shopping and Amazon intelligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketplace intelligence may send keywords, domains, or URLs to DataForSEO and can incur API costs.

Mitigation: Use the built-in cost checks, request approval for warned endpoints such as Amazon search, and choose free-only or locale-scoped analysis when appropriate.

Risk: Live marketplace and UCP guidance can depend on current external platform requirements.

Mitigation: Revalidate marketplace endpoint behavior, schema requirements, and UCP version guidance before treating findings as final recommendations.

## Reference(s):

- [DataForSEO Merchant API Reference](references/marketplace-endpoints.md)
- [UCP - Universal Commerce Protocol](references/ucp-universal-commerce-protocol.md)
- [Google Merchant UCP Developer Guide](https://developers.google.com/merchant/ucp)
- [Universal Commerce Protocol Specification](https://ucp.dev)
- [ClawHub Skill Page](https://clawhub.ai/asale-ai/skills/seo-ecommerce)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, JSON snippets, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional DataForSEO marketplace calls may require credentials, budget checks, and user approval before spend.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
