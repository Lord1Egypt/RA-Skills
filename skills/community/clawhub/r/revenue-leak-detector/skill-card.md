## Description:

Identify high-value audience segments missing premium monetization opportunities. Analyzes subscriber databases and engagement patterns to generate upsell sequences. Use when the user needs LTV optimization, churn prevention, or strategic revenue growth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

External business, marketing, and revenue operations teams use this skill to analyze customer and subscriber segments, find under-monetized cohorts, and draft upsell, retention, win-back, alerting, and reporting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests live business credentials for payment, email, and spreadsheet systems.

Mitigation: Use restricted read-only API keys where possible, prefer sandbox data for review, and avoid placing long-lived production secrets in shared agent environments.

Risk: Slack notifications and Google Sheets exports can expose customer identifiers or sensitive revenue data.

Mitigation: Keep exports disabled until identifiers are redacted or explicitly approved under the organization's privacy obligations.

Risk: Revenue projections, churn scores, and campaign recommendations may be wrong or misleading if source data is incomplete or stale.

Mitigation: Review analyses with revenue or marketing owners before changing pricing, launching campaigns, or contacting customers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/revenue-leak-detector)
- [Skill homepage](https://github.com/ncreighton/empire-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with analysis summaries, campaign sequences, configuration examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference external business systems including Stripe, Mailchimp, Google Sheets, Slack, CRM, analytics, and email platforms when configured by the user.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
