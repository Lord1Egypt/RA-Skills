## Description:

Segment your customer base using Recency, Frequency, and Monetary value scoring to identify Champions, Loyal Customers, At-Risk buyers, and Churned segments — then generate targeted retention and reactivation campaigns for each group.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce and retention marketing teams use this skill to score customers by recency, frequency, and monetary value, assign named segments, and plan segment-specific retention, win-back, and suppression campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RFM analysis can expose sensitive customer order history and contact data.

Mitigation: Use the smallest necessary export, prefer customer IDs over emails, store outputs securely, and delete temporary datasets when analysis is complete.

Risk: Segment-driven outreach can violate consent, opt-out, suppression, SMS, phone, advertising, or privacy requirements if activated without review.

Mitigation: Verify consent status, opt-outs, suppression lists, and applicable marketing and privacy laws before launching email, SMS, phone, or ad-audience campaigns.

Risk: Poor data quality can produce misleading segments and inappropriate campaign actions.

Mitigation: Apply the provided checklist before campaign deployment, including net revenue validation, removal of test or wholesale orders, duplicate customer handling, and segment sanity checks.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/leooooooow/skills/rfm-segmenter)
- [Output Template](artifact/output-template.md)
- [Segment Action Playbook](artifact/segment-action-playbook.md)
- [Scoring Methodology Guide](artifact/scoring-methodology.md)
- [Quality Checklist](artifact/checklist.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, guidance]

**Output Format:** [Markdown reports, scoring guidance, campaign matrices, checklists, and optional Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces customer segment classifications, campaign recommendations, validation checks, and review cadence guidance; it does not execute hidden tools or call external services.]

## Skill Version(s):

1.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
