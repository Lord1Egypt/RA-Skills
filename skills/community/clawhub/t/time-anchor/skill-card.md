## Description:

Time Anchor helps agents run deterministic local date math for current dates, days or weeks until target dates, weekday ambiguity, and month-end information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elroyic](https://clawhub.ai/user/elroyic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when an assistant needs reliable date calculations for deadlines, milestones, weekdays, and month-end planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on ordinary planning or scheduling language because its trigger scope is broad.

Mitigation: Install it only when local date-math assistance is desired, and verify that the response context actually requires date calculations.

Risk: The full-anchor output depends on configured target dates that may be user-specific or stale.

Mitigation: Review and customize the configured target dates before relying on full-anchor output for planning decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; script output is plain text with JSON for weekday ambiguity.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a local Python helper for deterministic date calculations.]

## Skill Version(s):

1.1.0 (source: evidence release and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
