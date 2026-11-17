## Description:

Use when a user needs to discover Canton Fair exhibitor leads, find trade-show business opportunities, retrieve exhibitor contacts, product categories, and booth numbers, and prepare outreach content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External business-development and export-sales users use this skill to query Canton Fair lead data, rank prospects, organize contact details, and generate personalized email or messaging content for user-directed outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lead exports and generated outreach may include personal or business contact data.

Mitigation: Confirm the data source and intended outreach are lawful for the target market, avoid bulk unsolicited messaging, and delete lead exports when no longer needed.

Risk: The skill depends on a TRADEGPT_API_KEY credential for the Yunlv AI MatchGPT API.

Mitigation: Store the API key in the environment only, protect it from logs and shared outputs, and rotate it if exposure is suspected.

Risk: Match scores and contact completeness are advisory and may be inaccurate or stale.

Mitigation: Manually verify high-priority contacts, booth details, and outreach claims before acting on them.

## Reference(s):

- [Skill Guangjiao ClawHub listing](https://clawhub.ai/wangm-a3/skills/yunlv-guangjiao)
- [Yunlv AI homepage](https://yunlvai.com)
- [Yunlv AI MatchGPT API](https://api.yunlvai.com)
- [Canton Fair product category reference](references/canton_fair_categories.md)
- [Outreach template reference](references/outreach_templates.md)
- [Follow-up strategy reference](references/followup_strategy.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, API Calls]

**Output Format:** [Markdown and structured text, with JSON examples for lead lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated outreach copy, ranked lead summaries, booth or category lookup guidance, and user-managed follow-up recommendations.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
