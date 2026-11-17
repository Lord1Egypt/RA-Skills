## Description:

Helps users discover Canton Fair exhibitor and buyer leads, score potential matches, export contact lists, and draft personalized outreach using Yunlv AI MatchGPT API and bundled Canton Fair reference material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External business development and export sales teams use this skill to find, prioritize, and follow up with Canton Fair leads by product keyword, industry category, company name, or booth number. It supports lead-list generation, match scoring, outreach drafting, and follow-up planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send search terms, target-company lists, and contact-related workflow data to a third-party API.

Mitigation: Review the skill before installation, obtain explicit user approval before API queries, and confirm what Yunlv AI receives and retains.

Risk: The skill can export contact data and prepare email or WhatsApp outreach.

Mitigation: Require user approval before exports or outreach, verify consent and applicable privacy rules, and review generated contact lists and messages before use.

Risk: Automated lead scoring and generated outreach may be inaccurate or misleading.

Mitigation: Treat match scores and outreach drafts as recommendations, then manually verify high-value leads, contact validity, and message content before acting.

## Reference(s):

- [Canton Fair Categories](references/canton_fair_categories.md)
- [Outreach Templates](references/outreach_templates.md)
- [Follow-up Strategy](references/followup_strategy.md)
- [Yunlv AI Homepage](https://yunlvai.com)
- [Yunlv AI MatchGPT API](https://api.yunlvai.com)
- [Canton Fair Official Site](https://www.cantonfair.org.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with structured JSON lead-list examples and outreach templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include lead records, match scores, contact fields, outreach drafts, and follow-up recommendations that require user review before use.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact SKILL.md lists 1.0.0 and clawhub.yaml lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
