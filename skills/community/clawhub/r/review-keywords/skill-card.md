## Description:

Analyzes collected Amazon reviews to identify frequent and co-occurring buyer phrases, separated by positive and negative sentiment, for listing and advertising ideas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and analysts use the skill to summarize collected customer reviews, find frequently mentioned buyer language, and turn review evidence into listing or advertising test ideas. Review frequency describes the collected text and does not measure Amazon search demand or ad performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ARI credits may be spent without current approval, and combined spending limits are not reliably enforced.

Mitigation: Set confirmation to ask before every charge; use dedicated quote commands for estimates. A spending cap alone is insufficient until combined-cost enforcement is fixed.

Risk: Recurring review collection can continue to incur charges after an initial request.

Mitigation: Get explicit approval for recurring collection and review active schedules separately.

## Reference(s):

- [ARI API and CLI reference](references/reference.md)
- [ARI monitoring center](https://ari.funewa.com/zh/monitor)
- [ARI report center](https://ari.funewa.com/zh/reports)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Concise prose or structured Markdown summaries and reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keyword frequency and co-occurrence reflect collected review text; they are not search volume, ranking, CPC, or conversion metrics.]

## Skill Version(s):

1.5.3 (source: server-resolved release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
