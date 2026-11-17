## Description:

B2B foreign-trade customer discovery skill for global company data collection and BOI scoring triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External business development and sales users use this skill to find potential B2B customers by industry, geography, and revenue range, then review BOI-scored lead lists with company contact fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lead outputs can include contact emails that may be regulated personal or business data.

Mitigation: Confirm legal basis, consent posture, and regional marketing rules before using results for outreach.

Risk: The skill can collect contact information during customer discovery.

Mitigation: Require explicit user intent before including contact fields or automating contact collection.

Risk: The declared coze-api dependency is open-ended.

Mitigation: Pin and review the dependency version before deployment.

## Reference(s):

- [Trade Hunter ClawHub release](https://clawhub.ai/wangm-a3/skills/trade-hunter)
- [wangm-a3 publisher profile](https://clawhub.ai/user/wangm-a3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples and CSV-style lead lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include company names, locations, industries, revenue estimates, contact emails, summaries, BOI scores, and customer-distribution map guidance.]

## Skill Version(s):

1.0.0 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
