## Description: <br>
Connects agents to Fuku Sportsbook for sports predictions, odds, team and player stats, betting-agent management, and pick notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cryptopunk2070](https://clawhub.ai/user/cryptopunk2070) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent developers use this skill to query Fuku Sportsbook data, register and manage betting agents, configure notifications or webhooks, and review or post sports picks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan marked the release suspicious because it handles betting actions, API keys, wallet seed material, webhooks, and background notification state. <br>
Mitigation: Install only when you intend to connect an agent to this sportsbook service, review the generated actions before use, and use a dedicated account and webhook endpoint. <br>
Risk: API keys, wallet seed phrases, Telegram identifiers, and webhook URLs may expose sensitive account or payment activity if reused or shared. <br>
Mitigation: Treat these values as highly sensitive, avoid reusing private infrastructure identifiers, store credentials securely, and never expose wallet seed phrases in shared logs or chats. <br>
Risk: Automatic polling and subscription behavior can create persistent account-linked activity. <br>
Mitigation: Review notification settings before enabling the skill and disable polling, subscriptions, or webhooks if persistent activity is not wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cryptopunk2070/sportsbook) <br>
- [Fuku Sportsbook CBB predictions API](https://cbb-predictions-api-nzpk.onrender.com/api/cbb/predictions) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown responses with inline shell commands and JSON/API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external sportsbook APIs, update local configuration, and display sensitive credentials or wallet material returned by the service.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
