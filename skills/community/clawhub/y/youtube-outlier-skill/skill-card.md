## Description:

Finds trending YouTube outlier videos by niche, analyzes key concepts, saves data to Google Sheets, and posts summaries to Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalime](https://clawhub.ai/user/dalime)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to monitor YouTube niches for recent high-performing videos, summarize why they may be outliers, and distribute the results through Google Sheets and Discord.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically write reports to a configured Google Sheet and post summaries to a configured Discord channel.

Mitigation: Use tightly scoped service-account and bot permissions, verify destination IDs before use, and add a confirmation or dry-run path before enabling automatic posting.

Risk: The skill includes an Anthropic analysis path that is under-disclosed in the artifact documentation.

Mitigation: Disclose the Anthropic call to users or disable it when external model processing is not approved.

Risk: Discord output may expose generated summaries or allow disruptive formatting in a shared channel.

Mitigation: Sanitize and limit Discord output, disable mentions, and route reports only to approved channels.

Risk: Dependency and credential handling require review before installation.

Mitigation: Audit and update dependencies, store credentials securely, and grant only the minimum API scopes required for YouTube, Google Sheets, Discord, and model-provider access.

## Reference(s):

- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)
- [ClawHub Skill Page](https://clawhub.ai/dalime/skills/youtube-outlier-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, External records]

**Output Format:** [Text status messages, Discord Markdown summaries, and Google Sheets rows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured YouTube, Google Sheets, Discord, and optional Anthropic credentials.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
