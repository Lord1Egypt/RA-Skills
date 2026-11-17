## Description:

Track AI agent spending in real time with cost summaries, budget alerts, daily and weekly reports, and cost-per-task breakdowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vanthienha199](https://clawhub.ai/user/vanthienha199)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to estimate AI-agent usage costs, review spending over time, configure budget thresholds, and receive alerts when estimated spend approaches or exceeds limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores estimated spending history locally, which may include task labels and usage patterns.

Mitigation: Use the explicit start and stop tracking commands, and delete ~/.openclaw/cost-log.json to clear stored history.

Risk: Broad budget-related wording may cause the skill to activate when the user is discussing costs or billing.

Mitigation: Keep tracking disabled unless active cost logging is wanted, and use explicit enable or disable commands to control logging.

Risk: Cost values are estimates when exact token counts are unavailable.

Mitigation: Label approximated values as estimated and review pricing assumptions before relying on the totals for billing decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and plain text summaries with local JSON cost-log updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces estimated cost reports, budget alerts, trend summaries, and local cost-log updates when tracking is enabled.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
