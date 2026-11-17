## Description:

Yunlv Customs Scout helps users analyze customs trade signals to identify import and export buyers, competitor customers, market intelligence, scoring insights, and outreach drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External B2B trade-development teams use this skill to prospect importers, compare competitor customer relationships, score buyer opportunities, and prepare outreach from customs-data signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customs and contact data may be heuristic, stale, or overstated.

Mitigation: Verify underlying customs records, contact sources, and scoring inputs before acting on any lead or opportunity recommendation.

Risk: Sensitive business prospecting queries or lead lists may use unclear local or remote data paths.

Mitigation: Confirm whether query data is sent to Yunlv's remote API and obtain explicit user approval before exporting lead lists.

Risk: Generated outreach can trigger email, WhatsApp, or LinkedIn contact obligations.

Mitigation: Require user approval before outreach and review messages for GDPR, CAN-SPAM, and applicable local-market requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangm-a3/skills/yunlv-customs-scout)
- [Yunlv homepage](https://yunlvai.com)
- [Yunlv customs data API](https://api.yunlvai.com)
- [Data filter rules](references/data_filter_rules.md)
- [Customer scoring model](references/customer_scoring_model.md)
- [Outreach templates](references/outreach_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown reports, JSON analysis objects, and concise outreach drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include buyer scores, market-heat assessments, competitor-customer recommendations, and contact or outreach templates.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
