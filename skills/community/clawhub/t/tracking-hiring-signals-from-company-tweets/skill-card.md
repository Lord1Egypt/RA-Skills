## Description:

Tracks hiring signals and growth indicators from company Twitter/X posts using apidojo's Tweet scraper on Apify, returning company handles, roles, teams, dates, and growth indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers, talent intelligence teams, venture investors, and competitor analysts use this skill to monitor company Twitter/X activity for early hiring and growth signals. It helps identify actively hiring companies, roles, teams, recency, and signal strength.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify tokens or Twitter/X search terms may be exposed when using the REST fallback URL with a token query parameter.

Mitigation: Prefer the MCP/helper flow or an Authorization header, keep APIFY_TOKEN in environment or secret storage, and use a least-privilege token.

Risk: Hiring signals extracted from tweets can be stale, ambiguous, or posted by aggregators rather than official company accounts.

Mitigation: Filter job boards and staffing accounts, deduplicate by company handle, keep uncertain roles marked as unspecified, and verify links close to report use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/tracking-hiring-signals-from-company-tweets)
- [Publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify actor: apidojo/tweet-scraper](https://apify.com/apidojo/tweet-scraper)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Markdown, Files]

**Output Format:** [Markdown report with tables; optional CSV or JSON exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Apify/Twitter search inputs and may save CSV or JSON result files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
