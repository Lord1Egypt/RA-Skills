## Description:

Generates Canton Fair lead discovery strategies, customer-development plans, booth and category references, and personalized outreach content for trade show prospecting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business-development teams use this skill to plan Canton Fair prospecting, evaluate buyer or exhibitor fit, structure lead information, and draft follow-up messages. Developers may also use the bundled planner script for product-to-booth matching, buyer scoring, and outreach schedule generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles business lead and contact data for outreach planning.

Mitigation: Keep lead data in the user's controlled environment and verify contact accuracy, consent or lawful basis, unsubscribe handling, and applicable privacy or anti-spam requirements before using outreach.

Risk: The skill requires TRADEGPT_API_KEY access to Yunlv's API.

Mitigation: Install only when the user is comfortable sharing the disclosed request data with Yunlv's API and protect the API key from logs, prompts, and generated output.

Risk: Coverage, match scores, contact match rates, and outreach performance are presented as claims that may be incomplete or inaccurate.

Mitigation: Treat scores and generated recommendations as planning aids, validate important leads manually, and review all generated messages before sending.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/skills/yunlv-cantonfair)
- [Yunlv Homepage](https://yunlvai.com)
- [Yunlv MatchGPT API](https://api.yunlvai.com)
- [Canton Fair Categories](references/canton_fair_categories.md)
- [Outreach Templates](references/outreach_templates.md)
- [Follow-Up Strategy](references/followup_strategy.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured JSON-style lead strategy reports with optional shell command usage for the bundled planner script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TRADEGPT_API_KEY for Yunlv MatchGPT API-backed strategy generation; generated outreach is intended for user review before sending.]

## Skill Version(s):

1.1.0 (source: evidence.release and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
