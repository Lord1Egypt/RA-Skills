## Description:

rili provides local calendar and Chinese lunar date lookups through a bundled Node script, including weekdays, month views, traditional lunar festivals, and Gregorian-lunar conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Chinese-language calendar questions, including Gregorian dates, weekdays, lunar dates, zodiac signs, supported traditional lunar festivals, month views, and lunar-to-Gregorian conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lunar calendar results depend on local Node Intl Chinese calendar support and may not be suitable for high-precision astronomical or regional folk-calendar use.

Mitigation: Use the skill for common calendar questions and verify results against authoritative calendars before relying on them for precision-sensitive, regional, or formal use.

Risk: The skill is scoped to date lookup and conversion, not calendar event management, reminders, shared schedules, or integrations.

Mitigation: Route event creation, reminder, meeting, and shared-calendar requests to an appropriate calendar integration instead of this local lookup skill.

## Reference(s):

- [rili ClawHub skill page](https://clawhub.ai/jvy/skills/rili)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON returned by local Node commands, with concise natural-language guidance for the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Node runtime with Intl Chinese calendar support; no external API calls are used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
