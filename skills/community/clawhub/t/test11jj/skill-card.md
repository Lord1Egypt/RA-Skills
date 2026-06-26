## Description: <br>
Manage Trello boards, lists, and cards via the Trello REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjcloud](https://clawhub.ai/user/hjcloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to look up Trello boards, lists, and cards and to prepare Trello REST API commands for creating, moving, commenting on, or archiving cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trello API keys and tokens can grant account access if exposed or over-scoped. <br>
Mitigation: Treat the token like a password, keep it out of logs and shared prompts, and use the narrowest Trello access available. <br>
Risk: Create, move, comment, and archive commands can change real Trello boards. <br>
Mitigation: Review each mutating command before execution and confirm the target board, list, card, and text values. <br>
Risk: Repeated requests can hit Trello API rate limits. <br>
Mitigation: Throttle repeated operations and retry only after confirming the intended action still applies. <br>


## Reference(s): <br>
- [Trello REST API documentation](https://developer.atlassian.com/cloud/trello/rest/) <br>
- [Trello API key page](https://trello.com/app-key) <br>
- [ClawHub skill page](https://clawhub.ai/hjcloud/test11jj) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq plus TRELLO_API_KEY and TRELLO_TOKEN environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
