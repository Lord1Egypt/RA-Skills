## Description:

Orchestrates startup work: routes tasks to specialized agents and applies stage-appropriate priorities for advising founders on product-market fit, growth, hiring, fundraising, runway, and burn decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External founders and startup operators use this skill to get stage-aware advice, coordinate specialist agent work, and prioritize decisions around PMF, growth, runway, fundraising, hiring, sales, and product strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain startup context such as stage, business model, runway, and preferences under ~/Clawic/data/startup/.

Mitigation: Only provide business-sensitive details that are appropriate to store locally for future advice, and review the local startup data directory when privacy requirements change.

Risk: Startup advice can be stage-sensitive and may be misleading if the founder's current stage, runway, or business model is wrong or missing.

Mitigation: State the assumed stage and key constraints before acting on recommendations, and update the stored configuration when those assumptions change.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/startup)
- [Clawic Skill Page](https://clawic.com/skills/startup)
- [Publisher Profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stage assumptions, prioritized recommendations, agent-routing briefs, decision gates, and local configuration guidance.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
