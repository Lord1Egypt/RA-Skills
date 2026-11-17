## Description:

SN Data by Shikshan Nivesh: 8-K events by item number, House members' trades and FINRA short interest for US-listed companies, each linked to its source. Use when a question asks what a company disclosed, who in Congress traded it, or how much of it is sold short.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shikshannivesh](https://clawhub.ai/user/shikshannivesh)

### License/Terms of Use:

MIT-0

## Use Case:

People researching US-listed companies use this skill to retrieve and summarize 8-K events, House member trade disclosures, and FINRA short interest with links to the source filings. It supports factual reporting, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A data key could be exposed if printed or stored in a shared file.

Mitigation: Keep SN_KEY in an environment variable; do not print it or put it in a file you share.

Risk: Financial disclosures and short-interest figures could be mistaken for investment recommendations.

Mitigation: Cite the source filing, state the reporting period, and keep answers informational without buy or sell calls.

## Reference(s):

- [SN Data developer documentation](https://shikshannivesh.com/data/developers)
- [SN Data AI setup guide](https://shikshannivesh.com/data/ai)
- [SN Data API OpenAPI specification](https://shikshannivesh.com/api/v1/openapi.json)
- [ClawHub release](https://clawhub.ai/shikshannivesh/skills/sec-filings-and-8k-events)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown with linked source filings and reporting periods]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports figures as returned, includes source links, and keeps the content informational rather than investment advice.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
