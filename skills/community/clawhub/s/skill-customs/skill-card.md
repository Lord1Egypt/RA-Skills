## Description:

Helps users find import/export trade data, competitor customers, and customs-data market intelligence for B2B prospecting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External business development and trade teams use this skill to identify active buyers, analyze competitor customer relationships, score prospects, and draft compliant outreach based on customs and trade records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad business or trade prompts may invoke the skill even when the user did not intend to query customs-data services.

Mitigation: Confirm the user's intent before sending trade-data queries or initiating outreach workflows.

Risk: Generated prospect records and outreach drafts may contain inaccurate contact details or stale customs-data signals.

Mitigation: Verify high-value leads, contact fields, and score inputs before acting on recommendations.

Risk: Email, WhatsApp, or LinkedIn outreach can create compliance exposure if used without authorization or applicable consent.

Mitigation: Require user authorization for outreach and check messages against applicable GDPR, CAN-SPAM, and local marketing rules.

## Reference(s):

- [Yunlv AI homepage](https://yunlvai.com)
- [Yunlv AI MatchGPT API](https://api.yunlvai.com)
- [Global customs data API](https://data.yunlvai.com)
- [Data filter rules](artifact/references/data_filter_rules.md)
- [Customer scoring model](artifact/references/customer_scoring_model.md)
- [Outreach templates](artifact/references/outreach_templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown reports with JSON-style lead intelligence summaries and outreach drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prospect lists, opportunity scores, contact fields, supplier analysis, outreach timing, and email or messaging drafts.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
