## Description:

Reminds the user of commitments they already know, such as meetings, deadlines, bills, promises, and follow-ups, at an appropriate lead time and in the user's preferred style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to identify reminder-worthy commitments, choose lead times, phrase reminders, and maintain local reminder preferences without turning reminders into alerts or scheduled task execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder preferences, learned timing, and active reminder history may store personal commitments locally under ~/Clawic/data/remind/.

Mitigation: Use the skill only on a profile where local storage of personal commitments is acceptable, and review or delete ~/Clawic/data/remind/ to clear reminder history.

Risk: Proactive reminder detection may create unwanted reminders if implicit commitments are interpreted too aggressively.

Mitigation: Follow the offer-first rule for early implicit detections, respect quiet hours and skip preferences, and confirm before storing learned preferences.

## Reference(s):

- [ClawHub Remind Skill Page](https://clawhub.ai/ivangdavila/skills/remind)
- [Remind Skill Homepage](https://clawic.com/skills/remind)
- [Reminder Triggers](triggers.md)
- [Timing Defaults](timing.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with reminder wording and local preference updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference or update local reminder preferences under ~/Clawic/data/remind/ when the user confirms storage.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
