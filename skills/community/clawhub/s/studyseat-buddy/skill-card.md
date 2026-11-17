## Description:

This skill helps university students find available classrooms for self-study, group discussion, exam prep, or meetings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjmorant12](https://clawhub.ai/user/jjmorant12)

### License/Terms of Use:

MIT-0

## Use Case:

External university students use this skill to find suitable campus classrooms for individual study, exam preparation, group discussion, or meetings. The skill filters by time, location, capacity, preferences, schedule conflicts, and recent on-site feedback, then explains the recommended rooms and cautions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled classroom, schedule, and feedback files use sample campus data and may not reflect real room availability.

Mitigation: Replace the sample data with school-managed classroom and schedule data, and tell users to confirm availability with official systems or posted notices.

Risk: The included demo admin page uses hardcoded accounts and client-side administrative behavior.

Mitigation: Keep the demo page as a prototype only unless authorization is moved server-side and hardcoded accounts are removed.

Risk: User or admin-entered text in the demo interface could be unsafe if connected to production data flows.

Mitigation: Safely render or sanitize all entered text before using the interface with real users, APIs, or production data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jjmorant12/skills/studyseat-buddy)
- [Skill instructions](artifact/SKILL.md)
- [Classroom data reference](artifact/references/classroom_data.md)
- [Schedule data reference](artifact/references/schedule_data.md)
- [Feedback data reference](artifact/references/feedback_data.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown recommendation response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a concise recommendation set with learning mode, 1-3 room options, avoided-room rationale, best choice, and usage cautions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
