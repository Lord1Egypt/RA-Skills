## Description:

Helps Finnish parents review Wilma school updates, identify actionable items, and optionally sync exams and events to a family calendar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aikarjal](https://clawhub.ai/user/aikarjal)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and caregivers use this skill to review their children's Wilma messages, schedules, homework, exams, bulletins, and lesson notes for timely actions, with optional family-calendar updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: School messages and attachments can contain sensitive student information.

Mitigation: Grant access only to trusted agents, review attachment save locations, and remove sensitive downloads when no longer needed.

Risk: Optional calendar changes or scheduled daily runs could affect the wrong family calendar.

Mitigation: Confirm the selected calendar before scheduling, and check existing events before adding or removing entries.

## Reference(s):

- [Wilma Triage on ClawHub](https://clawhub.ai/aikarjal/skills/wilma-triage)

## Skill Output:

**Output Type(s):** [Text, Calendar events]

**Output Format:** [Brief chat summary grouped by child, with optional calendar updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May remain silent when there are no actionable updates; requires Wilma access, and calendar sync is optional.]

## Skill Version(s):

2.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
