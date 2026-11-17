## Description:

Reads OpenClaw session usage totals to show where tokens and estimated cost are going by session type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whooshinglander](https://clawhub.ai/user/whooshinglander)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to diagnose token and cost usage by session category, identify high-volume or high-cost drains, and decide where to reduce waste.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw session usage totals may reveal model choices, timestamps, costs, and session categories.

Mitigation: Use the skill only in environments where the agent is permitted to read OpenClaw session usage data.

Risk: The optional savings log creates or updates a local token-diet-log.md history file when the user explicitly asks to track improvements.

Mitigation: Request savings logging only when maintaining that local history is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/whooshinglander/skills/whereamiburningtokens)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown table with concise insight lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports session count, token totals, estimated cost, category percentages, and anomaly flags for the selected time window.]

## Skill Version(s):

1.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
