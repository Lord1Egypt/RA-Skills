## Description:

Extract sentiment patterns, repeated pain points, and feature requests from customer reviews to prioritize product fixes and copy improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, product teams, and ecommerce operators use this skill to turn customer review corpora into a Review Analysis report with aspect sentiment, ranked pain points, feature requests, and prioritized product and listing-copy actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer review text and IDs can contain personal or sensitive information in saved or shared reports.

Mitigation: Avoid unnecessary personal data, de-identify review IDs and quotes in shared reports, and apply normal retention and access controls to saved baseline reports.

Risk: Small, biased, fake, or incentivized review samples can produce misleading product and copy recommendations.

Mitigation: Record pulled and analyzed counts, remove duplicates and templated spam, quantify fake or incentivized reviews, enforce sample thresholds, and hand-verify a 10-15% coding sample.

## Reference(s):

- [Review Analysis Report Template](references/output-template.md)
- [Sentiment Coding Guide](references/sentiment-coding-guide.md)
- [Pain-Point Taxonomy](references/pain-point-taxonomy.md)
- [Review Analysis Quality Checklist](assets/quality-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown Review Analysis report with tables, de-identified quotes, and prioritized action lists.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires review text and supporting review metadata such as star rating, date, variant or SKU, verified-purchase flag, and review ID.]

## Skill Version(s):

1.1.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
