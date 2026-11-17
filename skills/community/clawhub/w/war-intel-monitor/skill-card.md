## Description:

Real-time war intelligence monitoring and emergency alert system for conflict zones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oliviapp8](https://clawhub.ai/user/oliviapp8)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure location-based conflict monitoring, emergency alerts, evacuation tracking, and safety briefings for wartime situations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for highly sensitive location, shelter, evacuation, and emergency contact data.

Mitigation: Use coarse location data where possible, keep configuration files out of synced folders and repositories, restrict file permissions, and avoid storing shelter details or contact numbers unless needed.

Risk: The skill directs persistent monitoring jobs and external alerts.

Mitigation: Review the exact schedule, command, recipients, payload contents, and removal steps before enabling cron jobs or alert integrations.

Risk: Emergency recommendations may be based on incomplete or fast-changing conflict information.

Mitigation: Prioritize official emergency, embassy, defense, and civil aviation sources, and review generated guidance before acting on it.

## Reference(s):

- [Quick Setup Guide](references/setup-guide.md)
- [Configuration Template](references/config-template.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefings and alerts with JSON configuration and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include location-specific threat assessments, evacuation options, alert schedules, and external alert setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
