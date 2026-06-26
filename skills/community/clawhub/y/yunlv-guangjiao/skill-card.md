## Description: <br>
Use when the user needs to discover Canton Fair exhibitor or buyer leads, find exhibitor contacts, identify product categories and booth numbers, and prepare outreach drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business development and export sales users use this skill to research Canton Fair leads, rank potential prospects, organize contact information, and draft personalized follow-up messages for manual outreach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote API use may send queries and lead data to YunlvAI, while the release security summary notes conflicting privacy and storage disclosures. <br>
Mitigation: Use a dedicated revocable API key, avoid submitting unnecessary sensitive data, and review YunlvAI privacy and retention terms before deployment. <br>
Risk: The skill supports lead discovery and outreach drafting, which can enable bulk or non-compliant contact practices. <br>
Mitigation: Use generated outreach only after human review, avoid bulk outreach, and verify GDPR, CAN-SPAM, and local contact-data obligations. <br>
Risk: Exported leads, query history, outreach drafts, and logs may contain contact or business-sensitive data. <br>
Mitigation: Store outputs in controlled locations, restrict access, and delete exported leads, query history, outreach drafts, and logs when no longer needed. <br>


## Reference(s): <br>
- [Skill release page](https://clawhub.ai/wangm-a3/yunlv-guangjiao) <br>
- [Publisher profile](https://clawhub.ai/user/wangm-a3) <br>
- [YunlvAI homepage](https://yunlvai.com) <br>
- [YunlvAI MatchGPT API](https://api.yunlvai.com) <br>
- [Canton Fair Categories Reference](references/canton_fair_categories.md) <br>
- [Outreach Templates](references/outreach_templates.md) <br>
- [Follow-up Strategy](references/followup_strategy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured lead-list examples, JSON examples, outreach templates, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRADEGPT_API_KEY for YunlvAI MatchGPT API use; generated email and messaging content is intended for user review and manual sending.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
