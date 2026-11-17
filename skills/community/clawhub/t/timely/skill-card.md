## Description:

Manage Apple Reminders from the command line with geofencing, due dates, time-based alerts, and iCloud-synced reminder lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halbotley](https://clawhub.ai/user/halbotley)

### License/Terms of Use:


## Use Case:

Mac users and agents use this skill to create timely CLI commands for listing and creating Apple Reminders with due dates, natural-language times, or location-based arrive/depart triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party Homebrew tap and CLI that run locally.

Mitigation: Verify that the halbotley Homebrew tap and timely CLI are trusted before installation.

Risk: The timely CLI can access Apple Reminders data after macOS permission is granted.

Mitigation: Grant Reminders access only when needed and revoke it later in macOS privacy settings if the tool is no longer used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/halbotley/skills/timely)
- [Publisher profile](https://clawhub.ai/user/halbotley)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets macOS and the timely CLI installed from the halbotley Homebrew tap.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
