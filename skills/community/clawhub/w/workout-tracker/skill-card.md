## Description:

A personal fitness tracking skill that records text-based workout entries, parses exercises, sets, reps, and weights, writes them to a local MySQL database, and supports training plans, history queries, progress tracking, and cardio or ball-sport records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[query1988](https://clawhub.ai/user/query1988)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a local personal workout assistant to record gym sets, cardio sessions, available equipment, training status, and workout history. It is intended for single-user local deployment with fitness data stored in MySQL rather than a cloud service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs credentials for a local MySQL database that may contain personal fitness history.

Mitigation: Use a dedicated MySQL user limited to the workout_tracker database with only INSERT, SELECT, UPDATE, and DELETE permissions.

Risk: Database credentials can leak if stored in shell startup files, committed configuration, or loosely permissioned .env files.

Mitigation: Prefer interactive secret entry or a local secret manager; if using an .env file, keep it out of version control and set permissions to chmod 600.

Risk: Unpinned Python dependencies can change behavior across installs.

Mitigation: Pin dependencies where possible before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/query1988/skills/workout-tracker)
- [Publisher Profile](https://clawhub.ai/user/query1988)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, SQL guidance]

**Output Format:** [Markdown with SQL and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-facing workout logs, summaries, training plans, setup guidance, and parameterized MySQL query patterns.]

## Skill Version(s):

1.3.7 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
