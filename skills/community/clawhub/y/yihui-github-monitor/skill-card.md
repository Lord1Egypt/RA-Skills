## Description:

Monitor multiple GitHub repos with configurable alert policies for releases, PRs, and security, sending low-noise notifications via scheduled cron jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1yihui](https://clawhub.ai/user/1yihui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure recurring monitoring for selected GitHub repositories, with alerts for releases, merged pull requests, security-related changes, and daily digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitoring the wrong repositories, schedule, or notification target can create unwanted alerts or route update information to the wrong place.

Mitigation: Confirm the repository list, alert policy, schedule, and notification target before installing or updating the skill.

Risk: Recurring monitoring stores cursor and digest state, so an unexpected state file path can create or update state in the wrong workspace location.

Mitigation: Review the configured state file path and keep it isolated for this monitor so deduplication and digest state remain predictable.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with concise impact summaries and optional event-level details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Brief impact summaries are the default; event-level details are expanded only on request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
