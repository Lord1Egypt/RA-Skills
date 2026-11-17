## Description:

Logs workouts, retrieves training history, estimates personal records, and summarizes exercise volume using a local CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dsdevq](https://clawhub.ai/user/dsdevq)

### License/Terms of Use:

MIT

## Use Case:

People and their agents use this skill to record gym sessions, review workout history and volume, estimate lifting records, and correct or remove sessions stored locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a separately installed global npm CLI.

Mitigation: Review and trust the CLI package before installing or running it.

Risk: Deleting a session has no confirmation prompt and may be irreversible; editing changes saved records.

Mitigation: Confirm the user's intent and session ID before destructive changes, and back up important workout records.

Risk: Broad workout-related triggers may match ambiguous requests.

Mitigation: Clarify whether the user wants to view or change records before acting.

## Reference(s):

- [workout-claw on ClawHub](https://clawhub.ai/dsdevq/skills/workout-claw)
- [fitdown input notation](https://github.com/datavis-tech/fitdown)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain-language workout summaries and CLI command guidance; CLI responses are YAML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workout records are stored locally as JSON; personal records are estimated from logged sets.]

## Skill Version(s):

0.4.0 (source: server-resolved ClawHub release; bundled SKILL.md still says 0.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
