## Description:

Analyzes Samsung Health Connect data synced to Google Drive for sleep, steps, heart rate, SpO2, workouts, and daily health reports, requiring a Samsung Galaxy Watch or Ring with Health Connect backup enabled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mudgesbot](https://clawhub.ai/user/mudgesbot)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to install and operate a CLI for syncing Samsung Health Connect backups from Google Drive and generating health summaries from exported records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill works with sensitive health records synced from Google Drive.

Mitigation: Use only on a trusted machine and with a Google account or Drive folder the user is comfortable exposing to the downloaded CLI.

Risk: Installation clones mutable external code from a default branch.

Mitigation: Prefer a pinned commit or reviewed release before installation.

Risk: Downloaded health archives and parsed data may remain on disk after use.

Mitigation: Confirm where data is stored and how to delete local copies before using the skill.

## Reference(s):

- [ClawHub Samsung Health skill page](https://clawhub.ai/mudgesbot/skills/samsung-health)
- [Source repository listed by skill metadata](https://github.com/mudgesbot/samsung-health-skill)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with shell-command examples and optional JSON CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires gog and python3; health summaries depend on the user's Samsung Health Connect backup contents.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
