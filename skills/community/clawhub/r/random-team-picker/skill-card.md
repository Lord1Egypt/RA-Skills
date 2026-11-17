## Description:

Randomly selects team members or splits a group into teams, with options for weighted selection, exclusions, and repeated fair distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darbling](https://clawhub.ai/user/darbling)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, facilitators, and team leads use this skill to pick participants for meetings, reviews, or activities, or to split a participant list into teams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extremely large or untrusted weight values can cause weighted selection to build an oversized in-memory list.

Mitigation: Use modest, trusted integer weights until weight size validation or a non-expanding weighted sampling approach is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darbling/skills/random-team-picker)
- [Publisher profile](https://clawhub.ai/user/darbling)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text selections or team lists, with Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local random selection; weighted selection accepts name:weight pairs.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
