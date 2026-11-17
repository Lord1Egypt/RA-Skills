## Description:

Generates Amazon review and VOC reports with consumer insights, trends, variant analysis, competitor comparisons, and report archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and operators use this skill to collect and analyze product reviews, create VOC and related reports, and track customer feedback and product trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid actions may charge credits during preview flows or resume without a fresh user request.

Mitigation: Set autoconfirm off before use, use quote for previews, and require explicit approval for paid work; an unanswered quote does not authorize execution.

Risk: Recurring collection or competitor monitoring can create ongoing credit costs.

Mitigation: Use manual scheduling for one-time collection and review recurring costs before enabling monitoring.

Risk: Deepdive preview protection is reported as unresolved.

Mitigation: Avoid deepdive until its preview protection is fixed.

## Reference(s):

- [ARI CLI and API reference](artifact/references/reference.md)
- [ClawHub skill release](https://clawhub.ai/funewa/skills/review-report)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, CSV]

**Output Format:** [Markdown reports and summaries; CSV review exports; HTML report exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report scope and conclusions depend on available review data; paid analyses and recurring monitoring may consume account credits.]

## Skill Version(s):

1.5.3 (source: server release evidence, frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
