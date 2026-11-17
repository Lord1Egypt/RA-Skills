## Description:

A running coach that logs training, offers evidence-driven guidance, and sends visual training plans through Telegram, with optional local Garmin data sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enawareness](https://clawhub.ai/user/enawareness)

### License/Terms of Use:

MIT-0

## Use Case:

Runners use this skill to track workouts, review training and optional Garmin health metrics, and receive personalized coaching and visual weekly plans in Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Garmin credentials, session tokens, and sensitive health metrics remain on the local machine until deleted.

Mitigation: Enable Garmin sync only if local storage is acceptable; protect the skill data directory and delete saved Garmin data and tokens when no longer needed.

Risk: Sending a plan uploads its images to the configured Telegram chat.

Mitigation: Check the configured chat ID and review plan images before running send commands.

## Reference(s):

- [Run Coach on ClawHub](https://clawhub.ai/enawareness/skills/run-coach)

## Skill Output:

**Output Type(s):** [Text, Guidance, Images]

**Output Format:** [Telegram coaching messages and training-plan image albums]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional Garmin sync stores activity and health summaries locally.]

## Skill Version(s):

1.1.8 (source: frontmatter, CHANGELOG, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
