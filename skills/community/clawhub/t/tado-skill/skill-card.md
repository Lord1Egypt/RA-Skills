## Description:

Interact with Tado smart thermostat. Use for reading temperature, setting heating with auto-revert, viewing energy usage, and controlling zones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davek-dev](https://clawhub.ai/user/davek-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a Tado smart thermostat through Tado API examples for authentication, zone status, temperature overrides, override clearing, and energy usage checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tado access and refresh tokens can expose thermostat account access if stored in logs, shell history, shared terminals, or project files.

Mitigation: Keep TADO_TOKEN and TADO_REFRESH_TOKEN out of logs, shell history, shared terminals, and project files, and revoke or rotate tokens if exposed.

Risk: Temperature changes can affect the user's home until the selected termination condition is reached or cleared.

Mitigation: Before executing a heating change, verify the home, zone, target temperature, and termination type; prefer timer-based changes unless a lasting manual override is intended.

## Reference(s):

- [Tado OAuth2 device authorization endpoint](https://login.tado.com/oauth2/device_authorize)
- [Tado OAuth2 token endpoint](https://login.tado.com/oauth2/token)
- [Tado current user API endpoint](https://my.tado.com/api/v2/me)
- [Tado zones API endpoint](https://my.tado.com/api/v2/homes/$TADO_HOME_ID/zones)
- [Tado zone state API endpoint](https://my.tado.com/api/v2/homes/$TADO_HOME_ID/zones/$ZONE_ID/state)
- [Tado zone overlay API endpoint](https://my.tado.com/api/v2/homes/$TADO_HOME_ID/zones/$ZONE_ID/overlay)
- [Tado energy usage API endpoint](https://my.tado.com/api/v2/homes/$TADO_HOME_ID/energyUsage)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with bash, JSON, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Tado OAuth tokens, refresh token, home ID, and zone ID values before API calls can run.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
