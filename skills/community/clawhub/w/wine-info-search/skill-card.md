## Description:

Wine Info Search is a read-only wine and alcohol lookup skill that helps agents search wine details, ratings, price comparisons, winery background, vintage guidance, food pairings, and general alcohol-related health cautions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amurtiger01](https://clawhub.ai/user/amurtiger01)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agent operators use this skill to look up wine information, compare prices across supported platforms, and generate structured summaries from search results without making purchases or changing accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Firecrawl API key could be exposed if authenticated requests are retried without TLS certificate verification on a hostile or intercepted network.

Mitigation: Avoid using Firecrawl API keys on untrusted or intercepted networks unless the TLS retry behavior is removed or fixed; rotate any key used during certificate failures or suspicious timeouts.

Risk: Alcohol-related health guidance could be mistaken for medical advice.

Mitigation: Present health guidance as general information only and direct users to qualified healthcare professionals for decisions involving medical conditions, medications, pregnancy, addiction risk, or alcohol consumption.

Risk: Fetched third-party pages may contain misleading data or instructions that are unrelated to the user's task.

Mitigation: Treat third-party web content as data only, ignore page instructions, and review important wine, price, and health outputs before relying on them.

## Reference(s):

- [Wine Data Source Reference](references/api_reference.md)
- [ClawHub metadata homepage](https://github.com/Amurtiger01/wine-info-search-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with structured search results and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only outputs may include third-party search links, WebFetch-ready price hints, wine profile summaries, vintage comparisons, food pairing suggestions, and health disclaimers.]

## Skill Version(s):

1.7.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
