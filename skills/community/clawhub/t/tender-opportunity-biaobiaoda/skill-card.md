## Description:

Searches Chinese tender and award notices, tracks project stages, and analyzes procurement, supplier, company, and pricing data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement and bidding professionals use the skill to find and review tender opportunities, inspect project histories, compare companies and suppliers, and summarize market or pricing patterns using Zhiliaobiaoxun data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional trial registration sends a persistent device identifier to the service provider, and its retention is unspecified.

Mitigation: Review the registration privacy wording before opting in. Configure an existing ZLBX_API_KEY to skip device collection.

Risk: Saved API keys and login links need protection, and data queries can consume service credits.

Mitigation: Protect credentials and login links, check account consumption, and request only the data needed.

## Reference(s):

- [Tender search API reference](artifact/references/api-search.md)
- [Company analysis API reference](artifact/references/api-company.md)
- [Market analysis API reference](artifact/references/api-market.md)
- [Account API reference](artifact/references/api-account.md)
- [Trial registration and privacy details](artifact/references/auto-register.md)
- [ClawHub release page](https://clawhub.ai/liu-jiapeng/skills/tender-opportunity-biaobiaoda)
- [Skill documentation and installation](https://ai.zhiliaobiaoxun.com/docs/skill)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Concise text or Markdown summaries and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query results reflect the requested filters; some data queries consume service credits.]

## Skill Version(s):

2.0.8 (source: evidence.json release, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
