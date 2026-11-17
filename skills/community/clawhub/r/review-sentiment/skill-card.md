## Description:

This skill analyzes Amazon product reviews and groups positive and negative sentiment by topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and product operators use the skill to find recurring praise and complaints, compare sentiment across review topics, and prepare evidence-based product insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some analysis requests can spend account credits without a fresh confirmation, and unanswered requests may resume later.

Mitigation: Set confirmation to ask before every charge, request a quote before paid analysis, use a manual schedule for one-time collection, and review recurring plans and pending requests.

## Reference(s):

- [CLI and API reference](references/reference.md)
- [ClawHub release page](https://clawhub.ai/funewa/skills/review-sentiment)
- [ARI reports](https://ari.funewa.com/zh/reports)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Files]

**Output Format:** [Chinese-language analysis and Markdown reports, with optional CSV review exports or HTML report exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings depend on the collected review sample and its time range; the skill reports data scope and avoids unsupported trend claims.]

## Skill Version(s):

1.5.3 (source: release metadata and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
