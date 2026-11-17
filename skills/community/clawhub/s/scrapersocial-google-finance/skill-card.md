## Description:

Provides public Google Finance quotes, historical prices, and instrument search through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can look up indicative prices, retrieve historical candles, and find instrument symbols for research or watchlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests require a ScraperSocial API key and can consume API credits.

Mitigation: Use a trusted API key and set limits on history or search requests to control credit use.

Risk: Public-page prices may be delayed or cached and are not licensed real-time market data.

Mitigation: Treat results as indicative; do not rely on them alone for trading or investment decisions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nikhonit/skills/scrapersocial-google-finance)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Structured market data]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quote, price-history, or search results; paginated results may include a cursor.]

## Skill Version(s):

1.0.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
