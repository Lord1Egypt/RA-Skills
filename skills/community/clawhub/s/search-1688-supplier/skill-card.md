## Description:

Searches 1688 suppliers through the AlphaShop API using product links, image URLs, or keywords, with optional filters for price, minimum order quantity, and 48-hour shipping rate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External buyers, sourcing teams, and agents use this skill to find and compare 1688 suppliers from a product link, image URL, product ID, or keyword. It returns one best matching product and supplier result, or explains when explicit filters remove all matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplier-search keywords, 1688 product IDs or links, and image URLs are sent to AlphaShop.

Mitigation: Avoid confidential queries and internal-only URLs or images; use the skill only when sharing that search data with AlphaShop is acceptable.

Risk: AlphaShop API access depends on configured credentials.

Mitigation: Use dedicated AlphaShop API keys and manage them through the deployment environment instead of embedding secrets in prompts or files.

Risk: Loose dependency ranges may change behavior over time.

Mitigation: Pin or review dependency versions during deployment.

## Reference(s):

- [AlphaShop AI Select Provider Search API](references/api.md)
- [ClawHub skill release page](https://clawhub.ai/1688aiinfra/skills/search-1688-supplier)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON from the search script, followed by Markdown supplier and product presentation when shown to the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns one best match after filtering; no-match cases include counts and an explanatory message.]

## Skill Version(s):

1.0.4 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
