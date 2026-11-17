## Description:

A procurement research assistant focused on healthcare tenders, awards, project tracking, company information, and market analysis in China.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bailianai](https://clawhub.ai/user/bailianai)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement and bidding professionals use this skill to search Chinese healthcare tender and award notices, follow project timelines, review company records, and analyze suppliers, purchasers, and price trends. It also supports account-balance checks and procurement opportunity research.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Optional automatic trial registration sends device identifiers; the provider's fingerprint retention and deletion practices are not established by the supplied artifacts.

Mitigation: Review the device-identification privacy claim before using automatic registration. Configure a manually obtained API key to bypass device collection.

Risk: Company names and search filters are sent to Zhiliaobiaoxun, and paid queries consume account credits.

Mitigation: Limit queries to the information needed and review the filters and potential credit use before running paid searches.

Risk: Saved API keys and automatic-login links can grant access to the account.

Mitigation: Protect the saved key and login links; do not expose them in shared output.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/bailianai/skills/tender-medical)
- [Product homepage and API key access](https://ai.zhiliaobiaoxun.com/?ch=s154)
- [Search API reference](artifact/references/api-search.md)
- [Company data API reference](artifact/references/api-company.md)
- [Market analysis API reference](artifact/references/api-market.md)
- [Account API reference](artifact/references/api-account.md)
- [Company registry interpretation guidance](artifact/references/api-registry.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise summaries, Markdown tables, and query guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results reflect the requested search scope and available provider data.]

## Skill Version(s):

1.0.6 (source: frontmatter; server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
