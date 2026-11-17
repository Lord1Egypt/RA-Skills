## Description:

AI Investment Research - Double Color Ball (SSQ) Prediction fetches historical draw data, applies a Contextual Quantum-like Bayesian Network simulation, and sends Top 10 recommendations to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rix-zhang](https://clawhub.ai/user/rix-zhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch recent SSQ draw history, generate a speculative Top 10 lottery-number report, and optionally deliver the report to a configured Feishu group.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Speculative lottery-number output may be mistaken for reliable financial or investment advice.

Mitigation: Present results as entertainment or research, preserve the report's risk warning, and avoid representing recommendations as predictive certainty.

Risk: When FEISHU_SSQ_GROUP_ID is configured, the generated report is sent to that Feishu group.

Mitigation: Verify the target group ID before use and leave FEISHU_SSQ_GROUP_ID unset when chat-only output is preferred.

Risk: The report depends on public draw data fetched from an external source.

Mitigation: Confirm the retrieved issue range and data recency before relying on the generated report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rix-zhang/skills/ssq-prediction)
- [500.com SSQ historical draw data](https://datachart.500.com/ssq/history/newinc/history.php?start=24001&end=24200)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with ranked lottery-number combinations and optional Feishu delivery command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Top 10 recommendations; sends to Feishu only when FEISHU_SSQ_GROUP_ID is configured.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
