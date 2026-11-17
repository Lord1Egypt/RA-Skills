## Description:

Analyzes observed supplier and origin concentration using Crawlora ImportYeti company reports and public company evidence to produce a sourced supply-chain exposure brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement analysts and researchers use this skill to compare observed importer supplier and origin exposure, preserving the underlying shipment measures, reporting periods, coverage gaps, and source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, scrape URLs, ImportYeti lookups and the API key are sent to Crawlora; confidential procurement details could be disclosed.

Mitigation: Use a Crawlora-scoped API key, monitor credit usage, and submit confidential procurement details only when authorized to share them with Crawlora.

Risk: Incomplete public shipment coverage or incompatible periods and measures can make supplier concentration appear misleading.

Mitigation: Show the observation period, measure and sample coverage; calculate shares only from comparable data with a complete denominator.

## Reference(s):

- [Skill endpoint reference](artifact/reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/supply-chain-concentration-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown exposure brief with source citations and observed breakdowns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes entity, period and measure ledgers; sample gaps and qualification questions.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
