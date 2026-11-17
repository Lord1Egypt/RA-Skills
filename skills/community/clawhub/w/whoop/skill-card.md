## Description:

WHOOP morning check-in (recovery/sleep/strain) with suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[borahm](https://clawhub.ai/user/borahm)

### License/Terms of Use:


## Use Case:

People who use WHOOP can have an agent run a morning check-in that fetches recent recovery, sleep, and strain data, then returns short suggestions for the day.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived WHOOP OAuth secrets and health-data access tokens are stored locally in plaintext files.

Mitigation: Use owner-only permissions for ~/.clawdbot/.env and ~/.cache/whoop-morning, limit the WHOOP app to needed scopes, and revoke or rotate authorization if either file may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/borahm/skills/whoop)
- [WHOOP OAuth authorization endpoint](https://api.prod.whoop.com/oauth/oauth2/auth)
- [WHOOP OAuth token endpoint](https://api.prod.whoop.com/oauth/oauth2/token)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WHOOP OAuth credentials and a refresh token; the daily run returns a short user-facing morning check-in.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
