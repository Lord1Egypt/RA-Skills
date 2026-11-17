## Description:

Generates a concise daily morning brief from recent notifications by extracting key updates, missed items, follow-ups, decisions, and must-do-today actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and individual users use this skill to turn mixed work, personal, calendar, system, and platform notifications into a high-density morning brief. It helps identify important updates, actionable tasks, missed responses, follow-ups, decision points, and schedule risks for the current day.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query recent notifications across connected work and personal apps, which may expose sensitive content.

Mitigation: Review the skill before installation, configure the narrowest notification sources possible, and use explicit time windows.

Risk: Broad notification searches may collect more information than needed for a morning brief.

Mitigation: Require confirmation before broad searches and prefer scoped app, group, person, or project filters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/yoooclaw-daily-morning-brief)
- [ClawHub publisher profile](https://clawhub.ai/user/vivalavida-say-hi)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured conversation text with Markdown-style sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not generate files; returns a fallback morning greeting when there is not enough actionable notification evidence.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
