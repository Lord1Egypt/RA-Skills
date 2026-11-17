## Description:

Track and log AI API usage across providers, calculate costs, and generate daily, weekly, monthly, or real-time usage reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[punkaze](https://clawhub.ai/user/punkaze)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to record AI API token usage across common providers, estimate costs, and generate filtered usage reports by period, model, or task type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local usage logs may expose model names, task types, usage volume, or cost patterns on shared machines.

Mitigation: Install only where local usage metadata is acceptable, and periodically review or delete usage-logs/api-cells.jsonl when the data is no longer needed.

Risk: Cost estimates can become inaccurate if provider pricing changes after the skill release.

Mitigation: Confirm current provider pricing before relying on generated cost reports for budgeting or billing decisions.

## Reference(s):

- [Usage Tracker on ClawHub](https://clawhub.ai/punkaze/skills/usage-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Plain text or Markdown reports with local JSONL usage-log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports support period, model, and task-type filters; usage logs persist locally at usage-logs/api-cells.jsonl.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
