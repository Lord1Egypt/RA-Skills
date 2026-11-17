## Description:

Guides a user through a brief breathing exercise, can set calm-reminder calendar events, and then returns to the original task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grx21](https://clawhub.ai/user/grx21)

### License/Terms of Use:


## Use Case:

Agents use this skill when a user expresses frustration, stress, or task-related overwhelm, to offer a short breathing reset and optionally schedule calm reminders. It is also intended to refocus the conversation on the user's original task after the intervention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overly broad triggers may activate calming interventions during ordinary task requests.

Mitigation: Narrow activation to explicit frustration, stress, or stress-relief requests before using the skill.

Risk: The skill can create persistent Google Calendar reminders.

Mitigation: Show reminder titles, times, descriptions, and destination calendar, then require clear user confirmation before any calendar write.

Risk: User-facing content includes unsolicited Sauna.ai promotional and download language.

Mitigation: Remove or neutralize promotional language unless the user explicitly asks for branded Sauna.ai support.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/grx21/skills/superpower)
- [Publisher Profile](https://clawhub.ai/user/grx21)
- [Skill Definition](artifact/SKILL.md)
- [Breathing Exercises Reference](artifact/breathing-exercises.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with optional calendar reminder setup details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or create Google Calendar reminder events when explicitly confirmed by the user.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
