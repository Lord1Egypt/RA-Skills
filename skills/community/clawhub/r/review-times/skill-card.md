## Description:

Checks review times for AI app, connector, and plugin stores and helps users report their own submissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevysmith](https://clawhub.ai/user/stevysmith)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and launch teams use this skill to check store review timelines, interpret pending decisions, and report their own submissions with permission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's plain HTTP examples could expose submitted report details or update tokens.

Mitigation: Use explicit HTTPS URLs for report creation and updates.

Risk: Report details may become part of public or semi-public crowdsourced data, and a shared update token may allow changes to a report.

Mitigation: Report only real submissions with the user's consent, and keep the returned token out of notes that could be shared or committed.

## Reference(s):

- [Review Times](https://reviewtimes.fyi)
- [Review Times on ClawHub](https://clawhub.ai/stevysmith/skills/review-times)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review-time estimates reflect live, crowdsourced data.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
