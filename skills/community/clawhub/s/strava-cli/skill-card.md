## Description:

Interact with Strava via the strava-client-cli Python tool to view activities, athlete profiles, stats, and export data, including setup for Strava account creation, API app configuration, and OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geodeterra](https://clawhub.ai/user/geodeterra)

### License/Terms of Use:


## Use Case:

Developers and Strava users can use this skill to set up Strava OAuth credentials and run CLI commands for profile, statistics, activity lookup, and data export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned third-party Python CLI.

Mitigation: Pin or verify the strava-client-cli package version before installation or execution.

Risk: Strava OAuth client secrets and tokens may be stored locally or exposed through shell history.

Mitigation: Use restrictive permissions on ~/.config/strava-cli, avoid placing secrets in shell history, and rotate credentials if exposed.

Risk: Exported Strava activity data can contain private and location-sensitive information.

Mitigation: Treat exported files as private data and limit sharing, retention, and access.

## Reference(s):

- [Strava API application settings](https://www.strava.com/settings/api)
- [Strava OAuth authorization endpoint](https://www.strava.com/oauth/authorize)
- [Strava OAuth token endpoint](https://www.strava.com/oauth/token)
- [ClawHub skill page](https://clawhub.ai/geodeterra/skills/strava-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides OAuth setup and CLI usage; resulting exports can include private Strava activity data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
