## Description: <br>
Use when user needs to find import/export trade data, competitor customers, or market intelligence from customs data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External B2B trade and sales teams use this skill to query customs and trade intelligence, identify active importers, analyze competitor customer relationships, score lead opportunities, and draft compliant outreach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send customs-data queries and business-intelligence inputs to Yunlv or TradeGPT APIs. <br>
Mitigation: Use only with trade and business data the user is comfortable sharing with the provider, and keep API credentials scoped and protected. <br>
Risk: The skill can enrich leads and produce outreach recommendations using contact details, competitor claims, and import-volume claims. <br>
Mitigation: Keep outreach in manual review mode and verify every recipient, message, channel, follow-up schedule, and factual claim before contacting prospects. <br>
Risk: Lead and outreach records may be stored locally by the skill workflow. <br>
Mitigation: Limit local retention to business need, protect exported lead files, and avoid logging API keys or bulk contact data. <br>
Risk: Outreach may be subject to GDPR, CAN-SPAM, platform, and regional marketing rules. <br>
Mitigation: Confirm applicable legal and platform requirements before using email, WhatsApp, LinkedIn, or follow-up sequences. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/skill-customs) <br>
- [Yunlv AI Homepage](https://yunlvai.com) <br>
- [Yunlv AI MatchGPT API](https://api.yunlvai.com) <br>
- [Global Customs Data](https://data.yunlvai.com) <br>
- [Customer Scoring Model](artifact/references/customer_scoring_model.md) <br>
- [Data Filter Rules](artifact/references/data_filter_rules.md) <br>
- [Outreach Templates](artifact/references/outreach_templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with structured JSON-style trade intelligence reports and outreach drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRADEGPT_API_KEY; may include importer profiles, supplier relationships, opportunity scores, contact details, outreach copy, and follow-up recommendations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
