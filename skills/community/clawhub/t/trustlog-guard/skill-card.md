## Description:

Financial governance for OpenClaw agents that tracks API spend, enforces budget limits, detects runaway loops, delivers cost briefings, and reads session .jsonl logs locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anouartrust](https://clawhub.ai/user/anouartrust)

### License/Terms of Use:


## Use Case:

Developers and teams using OpenClaw use this skill to review local agent spend, compare costs by period and model, enforce daily or monthly budgets, and identify expensive or anomalous sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads OpenClaw session logs to calculate spend, which may expose local conversation metadata, model usage, timestamps, and cost records to the agent running the skill.

Mitigation: Use the skill only when local session-log access is acceptable, and prefer limiting analysis to a specific agent or time range when the environment supports it.

Risk: The skill persists budget settings in a local budgets.json file.

Mitigation: Review or clear the local budget file when saved daily or monthly budget settings should no longer apply.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown-style cost reports, budget status summaries, anomaly alerts, and local JSON budget configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are based on local OpenClaw session logs and include USD totals, message counts, model breakdowns, projections, warnings, and optimization tips.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
