## Description:

Manage your B2B sales pipeline end-to-end. Track deals through stages, forecast revenue, log activities, and monitor pipeline health. Weighted forecasting by deal stage. All data stored locally in JSON database. No API keys required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cunningham050503-ops](https://clawhub.ai/user/cunningham050503-ops)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams and operators use this skill to maintain a local B2B deal pipeline, track activity, forecast weighted revenue, identify stale opportunities, qualify inbound leads, and draft outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sales pipeline records may include contact names, email addresses, deal values, and notes stored in a local JSON file.

Mitigation: Use the skill only on trusted machines and handle ~/.openclaw/workspace/sales-pipeline-agent/pipeline.json according to your organization's data handling rules.

Risk: Deleting a deal permanently removes the record without a confirmation step.

Mitigation: Back up the local pipeline JSON file before relying on the skill and review deal IDs carefully before delete actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cunningham050503-ops/skills/sales-pipeline-agent)
- [Sales Methodology Reference](artifact/references/sales_methodology.md)
- [Outreach Templates by Stage](artifact/references/outreach_templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples and JSON-formatted local pipeline records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local JSON database at ~/.openclaw/workspace/sales-pipeline-agent/pipeline.json; no API keys are required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
