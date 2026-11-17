## Description:

Searches tender and award notices and analyzes procurement opportunities, bidders, companies, and market trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement and sales teams use the skill to find tender and award notices, track upcoming opportunities, and analyze companies, suppliers, competitors, and procurement trends.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Registration instructions conflict, and automatic registration uses a persistent device identifier.

Mitigation: Prefer a manually configured API key; request consent before automatic registration and explain the device features collected.

Risk: API credentials and login links could expose account access, while search terms may contain confidential business information.

Mitigation: Keep API keys and login links private, and avoid submitting confidential search terms.

Risk: The service's server-side data retention and deletion practices are unverified.

Mitigation: Avoid sending information that should not be processed by the service.

## Reference(s):

- [Tender search API guide](references/api-search.md)
- [Company analysis API guide](references/api-company.md)
- [Market analysis API guide](references/api-market.md)
- [Company registry API guide](references/api-registry.md)
- [Account API guide](references/api-account.md)
- [Published ClawHub skill page](https://clawhub.ai/liu-jiapeng/skills/tender-search)
- [Zhiliaobiaoxun skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Concise procurement search results, summaries, comparisons, and analysis; tables when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content depends on the user's search criteria and the available service records.]

## Skill Version(s):

2.1.10 (source: SKILL.md frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
