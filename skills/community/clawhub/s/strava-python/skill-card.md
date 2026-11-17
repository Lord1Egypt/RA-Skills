## Description:

Query Strava activities, stats, and workout data using Python/stravalib with interactive setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abclark](https://clawhub.ai/user/abclark)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to connect an agent to a personal Strava account, run OAuth setup, and request recent activities, last workout details, and running or cycling stats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores broad Strava OAuth credentials in a plaintext home-directory file.

Mitigation: Use a dedicated Strava API app, grant only scopes the user is comfortable with, protect or replace ~/.strava_credentials.json with secure secret storage or owner-only permissions, and revoke authorization when done.

Risk: The dependency is installed as an unpinned Python package.

Mitigation: Prefer an isolated Python environment and pin the stravalib version before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abclark/skills/strava-python)
- [Strava](https://www.strava.com)
- [Strava API App Settings](https://www.strava.com/settings/api)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads Strava activity and athlete data after user-configured OAuth credentials; outputs depend on account data and Strava API limits.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
