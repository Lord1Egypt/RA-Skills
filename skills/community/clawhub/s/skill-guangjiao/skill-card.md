## Description: <br>
Helps users discover and qualify Canton Fair exhibitor or buyer leads, including company contacts, product categories, booth details, outreach drafts, and follow-up guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business development and trade teams use this skill to mine Canton Fair data for relevant leads, score fit, prepare structured lead lists, draft outreach, and plan follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a TRADEGPT_API_KEY and can send Canton Fair lead queries to the Yunlv MatchGPT API. <br>
Mitigation: Install only when the publisher and API provider are trusted, keep the key out of logs, and review query content before use. <br>
Risk: The skill can export contact data for exhibitors, buyers, or decision makers. <br>
Mitigation: Store exported lead data only in approved locations, minimize retention, and handle contact data according to applicable privacy and outreach rules. <br>
Risk: The skill can generate or support email and WhatsApp outreach with unclear approval controls. <br>
Mitigation: Require explicit human review of recipients, channels, message text, language, storage location, and follow-up timing before any export or outreach action. <br>


## Reference(s): <br>
- [Skill Guangjiao on ClawHub](https://clawhub.ai/wangm-a3/skill-guangjiao) <br>
- [Publisher profile](https://clawhub.ai/user/wangm-a3) <br>
- [Yunlv AI homepage](https://yunlvai.com) <br>
- [Yunlv MatchGPT API](https://api.yunlvai.com) <br>
- [Canton Fair official site](https://www.cantonfair.org.cn) <br>
- [Canton Fair Categories](references/canton_fair_categories.md) <br>
- [Outreach Templates](references/outreach_templates.md) <br>
- [Follow-up Strategy](references/followup_strategy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with structured JSON lead-list examples and outreach text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include lead ranking, match scores, contact fields, outreach drafts, and follow-up timing recommendations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter 1.0.0 and clawhub.yaml 1.0.2 differ) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
