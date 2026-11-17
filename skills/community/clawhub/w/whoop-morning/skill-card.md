## Description:

Check WHOOP recovery/sleep/strain each morning and send suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[borahm](https://clawhub.ai/user/borahm)

### License/Terms of Use:


## Use Case:

External users use this skill to retrieve recent WHOOP recovery, sleep, and strain data and receive a short morning plan. It supports one-time OAuth setup and recurring morning automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive WHOOP health-account tokens and stores token material locally.

Mitigation: Use a dedicated WHOOP OAuth app, restrict permissions on ~/.clawdbot/.env and ~/.cache/whoop-morning/tokens.json, and avoid sharing backups or logs containing those files.

Risk: The referenced auth and report executables were not present in the reviewed artifact.

Mitigation: Review the installed executables before running the OAuth flow or scheduled morning report.

Risk: WHOOP refresh tokens rotate, and parallel refreshes can invalidate expected token state.

Mitigation: Avoid running multiple refresh operations at the same time and re-run authorization if token refresh returns 401 or 400.

## Reference(s):

- [WHOOP OAuth authorization endpoint](https://api.prod.whoop.com/oauth/oauth2/auth)
- [WHOOP OAuth token endpoint](https://api.prod.whoop.com/oauth/oauth2/token)
- [ClawHub skill page](https://clawhub.ai/borahm/skills/whoop-morning)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and generated morning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WHOOP OAuth credentials and a refresh token.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
