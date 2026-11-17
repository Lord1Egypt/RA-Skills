## Description:

Generates real-time A-share sector research reports with market data, news summaries, U.S. stock correlations, catalysts, risks, and anomaly alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harveyzzzz](https://clawhub.ai/user/harveyzzzz)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to create market research briefings for supported A-share sectors, AI-related news, and stock movement alerts. It is informational only and does not provide investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports include Content Science branding by default.

Mitigation: Review generated Markdown before sharing and remove or approve the branding for white-label or neutral deployments.

Risk: Sector names, search terms, and market queries may be sent to external public financial or news services.

Mitigation: Avoid submitting confidential watchlists or sensitive research terms, and review third-party data-source policies before use.

Risk: The skill writes generated market and news snapshots under .local.

Mitigation: Treat .local outputs as potentially sensitive research records and delete them when no longer needed.

Risk: Financial analysis and stock mappings may be incomplete, stale, or misleading.

Mitigation: Use outputs as informational research aids only, verify against authoritative market data, and keep the included investment disclaimer visible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harveyzzzz/skills/stockselectionmodel)
- [Publisher profile](https://clawhub.ai/user/harveyzzzz)
- [Data source notes](artifact/references/source_list.md)
- [Sector analysis prompt](artifact/references/sector_prompt.md)
- [AI news analysis prompt](artifact/references/analysis_prompt.md)
- [A-share stock mapping](artifact/references/stock_mapping.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown reports with JSON data snapshots and command-oriented workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated JSON snapshots under .local; optional TAVILY_API_KEY enables enhanced news search.]

## Skill Version(s):

1.0.0 (source: release metadata; artifact frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
