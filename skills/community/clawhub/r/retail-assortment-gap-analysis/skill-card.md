## Description:

Compare competing retail assortments through Crawlora catalogs. Use to find observed gaps in categories, brands, product attributes, variants, and price bands, with explicit catalog coverage and product-matching evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Retail analysts and merchandising teams use this skill to compare a retailer's assortment with competitors and produce an evidence-backed list of observed category, brand, attribute, variant, and price-band gaps. It helps distinguish sample gaps from confirmed catalog absence and records coverage limits for follow-up validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Crawlora API key could be exposed if handled insecurely.

Mitigation: Keep the key private in the CRAWLORA_API_KEY environment variable when running the helper.

Risk: Catalog queries and storefront URLs are sent to Crawlora, and collection may consume API credits.

Mitigation: Agree on collection scope and a credit budget before running the skill.

## Reference(s):

- [Crawlora API endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown report with a coverage ledger, comparable assortment matrix, and prioritized gap list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports counts, source URLs or IDs, collection scope, price basis, coverage, confidence, and suggested demand validation; conclusions depend on the collected sample and its completeness.]

## Skill Version(s):

1.0.11 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
