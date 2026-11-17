## Description:

Build a personal workout tracking system with exercises, routines, progression, and PRs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to maintain local workout logs, routines, exercise lists, progression notes, and personal records. The agent can summarize prior sessions and suggest next workout targets based on the user's recorded history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workout, recovery, injury, and optional health-related notes may be stored as local Markdown files under ~/workouts/.

Mitigation: Avoid recording sensitive medical details unless the user is comfortable keeping them in local files, and review the local ~/workouts/ contents before sharing or syncing them.

## Reference(s):

- [ClawHub Workouts skill page](https://clawhub.ai/ivangdavila/skills/workouts)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown workout logs, routines, exercise lists, personal-record notes, and concise text guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs the agent to create and maintain local files under ~/workouts/.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
