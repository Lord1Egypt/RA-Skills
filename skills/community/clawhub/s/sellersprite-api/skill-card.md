## Description:

SellerSprite Product Research fetches Amazon market data through the SellerSprite API for product research, keyword analysis, competitor lookup, ASIN details, and Blue Ocean Index scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boyd4y](https://clawhub.ai/user/boyd4y)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, analysts, and developers use this skill to query SellerSprite-powered Amazon product, category, keyword, competitor, ASIN, and quota data from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned external CLI package that can receive SellerSprite API keys and product research queries.

Mitigation: Use a pinned and reviewed @teamclaw/sellersprite-cli version before deployment, and only expose the SellerSprite key required for the current workflow.

Risk: SellerSprite API credentials could be exposed through local configuration or project files.

Mitigation: Prefer environment-scoped secrets, avoid committing or storing keys in project files, and rotate the key if the dependency or local config may have been exposed.

## Reference(s):

- [API Endpoints](references/api-endpoints.md)
- [Error Handling](references/error-handling.md)
- [Marketplace Codes](references/marketplace-codes.md)
- [SellerSprite Open API Portal](https://open.sellersprite.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bun, the @teamclaw/sellersprite-cli package, and a SellerSprite API key supplied through environment variable or CLI configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
