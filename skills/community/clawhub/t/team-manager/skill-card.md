## Description:

Coordinates a Russian-language team workflow with morning briefings, evening reports, hourly reminders for missing reports, and day-off status handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirra87654321](https://clawhub.ai/user/mirra87654321)

### License/Terms of Use:


## Use Case:

Team leads and operations coordinators use this skill to run a daily reporting workflow on Moscow time, including morning briefings, evening report collection, hourly reminders for missing reports, and day-off status handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local status tracking may retain team response or day-off status in state.json.

Mitigation: Confirm where state.json is stored, what status data it contains, and how to delete or rotate that local state before relying on it for real team tracking.

Risk: The workflow assumes Russian-language communications and Moscow time.

Mitigation: Install it only when that language and schedule fit the team, or adapt the reminders before deployment.

## Reference(s):

- [Team Manager on ClawHub](https://clawhub.ai/mirra87654321/skills/team-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Text or Markdown messages with team status updates and reminder prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Moscow time scheduling and may track response status in state.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
