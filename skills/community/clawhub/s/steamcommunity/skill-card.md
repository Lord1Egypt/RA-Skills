## Description:

Retrieves Steam inventory data and manages trade offers on steamcommunity.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluesyparty-src](https://clawhub.ai/user/bluesyparty-src)

### License/Terms of Use:


## Use Case:

Agents assisting Steam users use this skill to retrieve inventory JSON, summarize item metadata, and prepare or manage Steam trade offers with user-provided Steam credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Steam session cookies and API keys can expose account access if copied into logs, chat history, shell history, or shared terminals.

Mitigation: Treat STEAM_COOKIES, STEAM_SESSION_ID, and STEAM_API_KEY like passwords; keep them out of logs and rotate them if exposed.

Risk: Trade-offer commands can send, accept, cancel, or decline real item transfers if partner IDs, trade tokens, or asset IDs are wrong.

Mitigation: Require an explicit preview and manually verify every partner ID, trade token, and asset ID before executing any trade action.

Risk: Steam Community inventory endpoints are rate-limited, and repeated requests can fail or trigger temporary access restrictions.

Mitigation: Throttle inventory requests, respect pagination, and avoid automated retry loops against Steam endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bluesyparty-src/skills/steamcommunity)
- [Steam Community Developer](https://steamcommunity.com/dev)
- [Steam Web API Key Registration](https://steamcommunity.com/dev/apikey)
- [SteamID Lookup](https://steamid.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, curl, and jq snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, STEAM_ID, STEAM_COOKIES, STEAM_API_KEY, and STEAM_SESSION_ID; generated commands can call live Steam inventory and trade-offer endpoints.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
