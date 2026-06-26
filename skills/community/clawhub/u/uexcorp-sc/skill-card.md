## Description: <br>
Advanced Star Citizen trade advisor. Query live commodity prices, optimize trade routes, contribute market data, and create trade listings using the UEXCorp API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rikyz90](https://clawhub.ai/user/rikyz90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Star Citizen players and trading agents use this skill to query UEXCorp market data, compare trade routes, calculate profits, submit price observations, and create marketplace or trade listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit market data and create, delete, or recreate remote UEXCorp marketplace records. <br>
Mitigation: Require the agent to show the exact listing, payload, or database change and obtain explicit user approval before any create, update, or delete action. <br>
Risk: The skill requires a UEXCorp bearer token and may require a separate secret key for marketplace listing workflows. <br>
Mitigation: Keep tokens and secret keys out of chat logs, screenshots, and version control, and provide them only through the configured secret mechanism. <br>
Risk: UEXCorp market data is community-sourced and may differ from live in-game prices. <br>
Mitigation: Present trade recommendations as estimates and remind users to verify important prices in game before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rikyz90/uexcorp-sc) <br>
- [UEXCorp API documentation](https://uexcorp.space/api/documentation/) <br>
- [UEXCorp API apps](https://uexcorp.space/api/apps) <br>
- [UEXCorp](https://uexcorp.space) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown responses with tables, API request guidance, and concise trade recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uexcorp.apiToken configuration and may require a separate UEXCorp secret key for marketplace listing workflows.] <br>

## Skill Version(s): <br>
1.1.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
