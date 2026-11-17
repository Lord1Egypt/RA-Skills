## Description:

Retrieves Steam inventory data for a user from steamcommunity.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluesyparty-src](https://clawhub.ai/user/bluesyparty-src)

### License/Terms of Use:


## Use Case:

Developers and Steam users use this skill to retrieve, inspect, summarize, and paginate Steam Community inventory JSON for a SteamID64 and game app ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using STEAM_COOKIES can expose an authenticated Steam web session if the cookie is pasted into shared terminals, logs, or shell history.

Mitigation: Prefer public unauthenticated inventory requests when possible; treat steamLoginSecure like a password, unset it after use, and revoke the session if exposure is suspected.

Risk: The skill's security verdict is suspicious because it asks users to export a live Steam session cookie without enough warning or scoping.

Mitigation: Review the commands before use and limit cookie use to inventory requests where authentication is necessary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bluesyparty-src/skills/steam-community-inventory)
- [Steam Community developer documentation](https://steamcommunity.com/dev)
- [steamid.io SteamID lookup](https://steamid.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl and jq command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses STEAM_ID and optional STEAM_COOKIES environment variables; inventory responses are JSON from Steam Community endpoints.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
