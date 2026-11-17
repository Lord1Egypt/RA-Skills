## Description:

Deploy static websites to W-Spaces for HTML/CSS/JS sites, landing pages, and single-page apps using project creation, code push, and API key authenticated deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trandactruong](https://clawhub.ai/user/trandactruong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create W-Spaces projects, push static HTML/CSS/JS content, deploy live wspaces.app URLs, and manage API keys and deployment history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passwords and API keys can be exposed through shell history, logs, committed environment files, or persistent shell startup files.

Mitigation: Use trusted shells or CI secret stores, avoid passing real passwords where history or logs are captured, do not commit .env files, avoid storing live keys in ~/.bashrc, and rotate any key that may have appeared in logs.

Risk: If WSPACES_API_URL is changed, credentials and project content can be sent to a non-default endpoint.

Mitigation: Verify WSPACES_API_URL is unset or exactly the intended W-Spaces API before running authentication, project, push, or deployment commands.

## Reference(s):

- [W-Spaces Public API v1](references/wspaces-api.md)
- [W-Spaces](https://wspaces.app)
- [ClawHub Skill Page](https://clawhub.ai/trandactruong/skills/wspaces-deploy)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a W-Spaces account, WSPACES_API_KEY, curl, and jq.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
