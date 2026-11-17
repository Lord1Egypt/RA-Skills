## Description:

Design automated win-back campaigns targeting lapsed customers with personalized re-engagement sequences across email, SMS, and paid ads, using recency-based segmentation to maximize reactivation rates and recovered revenue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and ecommerce operators use this skill to design and quality-check lapsed-customer win-back campaigns, including segmentation, channel sequencing, suppression logic, measurement, and post-campaign analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Win-back campaign planning may involve customer identifiers or ad audience uploads.

Mitigation: Confirm the team is allowed to process and upload the relevant customer data, and route campaigns through privacy or legal review where required.

Risk: SMS outreach without valid consent can create compliance exposure.

Mitigation: Verify SMS opt-in consent before enrollment, maintain consent records, observe quiet hours, and include opt-out language.

Risk: Contacting suppressed, opted-out, invalid, or converted customers can create legal, deliverability, and customer experience problems.

Mitigation: Honor opt-outs and suppression lists, remove invalid contacts, and configure cross-channel suppression after purchase or unsubscribe events.

## Reference(s):

- [Win-Back Campaign Skill](artifact/SKILL.md)
- [Win-Back Campaign Output Template](artifact/output-template.md)
- [Recency-Frequency-Monetary Segmentation Guide for Win-Back Campaigns](artifact/segmentation-guide.md)
- [Multi-Channel Strategy Guide for Win-Back Campaigns](artifact/channel-strategy-guide.md)
- [Win-Back Campaign Quality Checklist](artifact/quality-checklist.md)
- [Klaviyo Win-Back Flow Best Practices](https://www.klaviyo.com/blog/winback-email-examples)
- [FCC TCPA Compliance Guide](https://www.fcc.gov/consumers/guides/stop-unwanted-robocalls-and-texts)
- [Google Ads Customer Match](https://support.google.com/google-ads/answer/6379332)
- [Meta Custom Audiences Documentation](https://www.facebook.com/business/help/744354708981227)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown campaign plans, tables, checklists, and channel configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference customer segments, consent status, suppression rules, holdout groups, and ad audience configuration; does not execute code.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
