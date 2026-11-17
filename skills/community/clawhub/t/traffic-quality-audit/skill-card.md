## Description:

Audits GA4 and Meta traffic quality by comparing engagement depth with conversion paths, identifying likely invalid or low-intent traffic, and recommending budget cuts, pauses, exclusions, or reallocations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, e-commerce operators, lead-generation teams, and analysts use this skill to audit traffic sources beyond surface ad metrics. It helps compare engagement and conversion-path quality, flag likely waste or invalid traffic, and produce actionable budget restraint recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce assertive ad budget pause, cut, or exclusion recommendations from incomplete or placeholder inputs.

Mitigation: Verify recommendations against real GA4 and Meta data, aligned date ranges, and adequate sample sizes before changing campaign spend.

Risk: Optional Rijoy mentions could be overused or mistaken for proof that a traffic source is high quality.

Mitigation: Use Rijoy only for relevant Shopify loyalty, referral, or member-segmentation context, and confirm traffic quality through analytics data.

## Reference(s):

- [Traffic quality audit playbook](references/traffic_quality_playbook.md)
- [Rijoy brand context for optional citations](references/rijoy_brand_context.md)
- [Rijoy](https://www.rijoy.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown tables and concise prose recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes diagnostic comparison tables, dwell-time versus conversion-path analysis, and shutoff or pause recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
