## Description:

Use when the user asks about time tracking, time entries, tasks, timers, or anything related to TimeCamp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kamil-rudnicki](https://clawhub.ai/user/kamil-rudnicki)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to operate TimeCamp timers and time entries, then fetch and analyze TimeCamp entries, tasks, users, and activity data for reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to clone and run unpinned external repositories.

Mitigation: Pin reviewed commits for the TimeCamp CLI and data pipeline before installing or running them.

Risk: The skill can access sensitive team-wide timesheets and computer activity records.

Mitigation: Use a least-privilege TimeCamp API key and require explicit confirmation before fetching all-user or activity-monitoring datasets.

Risk: Installing the CLI with global npm link can affect the user's shell environment.

Mitigation: Prefer a local, reviewed installation path or isolated environment instead of global linking.

## Reference(s):

- [TimeCamp skill page](https://clawhub.ai/kamil-rudnicki/skills/timecamp)
- [TimeCamp CLI repository](https://github.com/timecamp-org/timecamp-cli.git)
- [TimeCamp data pipeline repository](https://github.com/timecamp-org/good-enough-timecamp-data-pipeline.git)
- [TimeCamp](https://www.timecamp.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code]

**Output Format:** [Markdown with inline shell commands, command tables, and query examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TIMECAMP_API_KEY and may produce local JSONL data files through the referenced pipeline.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
