## Description:

Time Analyzer tracks activities, analyzes time usage patterns, and generates productivity suggestions and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to record activities, review time allocation, identify active periods and frequent activities, and generate productivity reports or suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented cron setup can replace existing scheduled jobs and create persistent daily execution.

Mitigation: Review and merge crontab entries manually instead of piping a single entry to crontab; enable scheduled reports only when persistence is intended.

Risk: Tracked activities are stored locally in ~/.time-analyzer and may reveal personal routines.

Mitigation: Use the skill only on trusted machines, restrict access to the local data directory, and clear records when they are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/time-analyzer)
- [Publisher Profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local activity records and configuration under ~/.time-analyzer when the CLI is used.]

## Skill Version(s):

1.0.3 (source: server evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
