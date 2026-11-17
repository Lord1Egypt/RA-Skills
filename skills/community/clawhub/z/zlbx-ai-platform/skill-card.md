## Description:

A Chinese-language procurement assistant for searching tenders, assessing bid decisions, finding early opportunities, and researching companies through Zhiliaobiaoxun data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bailianai](https://clawhub.ai/user/bailianai)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking procurement, sales, and bid teams use this skill to find and analyze public procurement opportunities, assess bid feasibility, and review companies through their tender histories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches consume platform credits and send research terms—and, for local-document analysis, extracted project identifiers—to Zhiliaobiaoxun.

Mitigation: Confirm the requested scope and expected credit use before paid searches; avoid sending identifiers that are not needed.

Risk: Reports may contain signed sk links that grant login-free access, with expiration and access scope not established.

Mitigation: Treat these URLs as access-bearing; remove signatures or replace them with safe sharing links before forwarding reports.

Risk: HTML link handling should be corrected before the report renderer processes untrusted inputs.

Mitigation: Use trusted inputs until HTML link handling has been corrected.

Risk: Company contact details and risk claims in reports may be sensitive or require verification.

Mitigation: Review contact details and verify risk claims before sharing reports.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/bailianai/skills/zlbx-ai-platform)
- [Zhiliaobiaoxun Skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML]

**Output Format:** [Text and Markdown responses; structured HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search summaries, bid feasibility and strategy analyses, opportunity findings, company intelligence, and account summaries based on retrieved data.]

## Skill Version(s):

1.1.6 (source: server-resolved release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
