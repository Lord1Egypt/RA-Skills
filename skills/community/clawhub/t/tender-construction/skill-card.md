## Description:

Queries and analyzes construction and municipal tenders, awards, companies, and market trends using the user's requested scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bailianai](https://clawhub.ai/user/bailianai)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement, sales, and bidding teams use this agent to find construction and municipal tender and award notices, track project timelines, research companies and competitors, and analyze procurement and pricing patterns.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Conflicting account-recovery instructions could prompt account re-registration when an existing API key stops working.

Mitigation: Preserve existing credentials and require an explicit account-change decision before registering again.

Risk: Trial registration uses a stable MAC hash as a device identifier and can create saved credentials or login links.

Mitigation: Prefer an existing API key when available, review device data collection before consenting, and protect saved keys and login links.

## Reference(s):

- [Tender search reference](references/api-search.md)
- [Company research reference](references/api-company.md)
- [Company registry reference](references/api-registry.md)
- [Market analysis reference](references/api-market.md)
- [Account reference](references/api-account.md)
- [Account registration and recovery reference](references/auto-register.md)
- [Product homepage](https://ai.zhiliaobiaoxun.com/?ch=s155)
- [Skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown summaries and tables with concise analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected filters and may be limited to the requested page or scope.]

## Skill Version(s):

1.0.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
