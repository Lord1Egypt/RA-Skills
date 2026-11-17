## Description:

Advanced Star Citizen trade advisor. Query live commodity prices, optimize trade routes, contribute market data, and create trade listings using the UEXCorp API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rikyz90](https://clawhub.ai/user/rikyz90)

### License/Terms of Use:

MIT-0

## Use Case:

External Star Citizen players and agent users use this skill to query UEXcorp market data, optimize trade routes, calculate trade outcomes, contribute price observations, and create marketplace listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, post, and delete live UEXcorp marketplace records using a user token.

Mitigation: Require explicit user approval before any write, post, or delete action, including the exact payload, target listing, and sandbox or production mode.

Risk: Updating an existing marketplace listing may require deleting the live listing before recreating it.

Mitigation: Confirm the listing ID, preserve the current listing details, test payloads in sandbox mode, and delete production listings only after the user approves the replacement.

Risk: The skill may send uploaded images, listing details, and market observations to UEXcorp.

Mitigation: Tell the user what data will be transmitted to UEXcorp and proceed only after consent.

Risk: Community-sourced market data may differ from current in-game values.

Mitigation: Present UEXcorp market data as advisory and include the skill's community-sourced data disclaimer in price and route guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rikyz90/skills/uexcorp-sc)
- [Publisher profile](https://clawhub.ai/user/rikyz90)
- [UEXcorp API documentation](https://uexcorp.space/api/documentation/)
- [UEXcorp API apps](https://uexcorp.space/api/apps)
- [UEXcorp API 2.0 base URL](https://api.uexcorp.space/2.0/)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown responses with tables, calculations, JSON payload previews, and API request guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uexcorp.apiToken; skill guidance states UEXcorp data is community-sourced and may differ from live in-game values.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
