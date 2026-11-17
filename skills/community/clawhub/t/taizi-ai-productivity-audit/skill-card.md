## Description:

Audits a user's current AI tool stack, scores each tool by ROI, identifies redundancies and gaps, and produces a structured report with savings analysis and top gap categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fresh3](https://clawhub.ai/user/fresh3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to inventory paid AI tools, score ROI, identify redundant subscriptions, and surface top gap categories before considering a paid stack-builder upgrade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free audit intentionally withholds specific replacement recommendations and steers users to a paid Stack Builder checkout.

Mitigation: Present the free-versus-paid boundary before use so users know the free output is an audit, not a complete replacement-stack recommendation.

Risk: The skill can offer to export a report to a local Markdown file.

Mitigation: Confirm the destination path with the user before allowing the agent to write the report.

Risk: ROI scores, savings estimates, and gap rankings can be misleading when the user's tool inventory is incomplete or approximate.

Mitigation: Collect tool name, monthly cost, primary use case, and usage frequency before scoring, and label cost and time-savings values as estimates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fresh3/skills/taizi-ai-productivity-audit)
- [Publisher Profile](https://clawhub.ai/user/fresh3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown report with ROI scores, redundancy analysis, top gap categories, potential savings, and optional local report export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The free audit names gap categories only and does not provide specific replacement-tool recommendations.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact _meta.json reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
