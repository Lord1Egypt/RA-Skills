## Description: <br>
Manage Trello boards, lists, and cards via the Trello REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChaunceyLiu](https://clawhub.ai/user/ChaunceyLiu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Trello users use this skill to have an agent list boards, inspect lists and cards, and create, move, comment on, or archive Trello cards via the Trello REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trello API credentials can grant access to account data. <br>
Mitigation: Install only when an agent should use the user's Trello API key and token, keep credentials secret, and avoid logging or committing them. <br>
Risk: The provided commands can create, move, comment on, or archive Trello cards. <br>
Mitigation: Require explicit confirmation before mutating requests and verify board, list, and card IDs before execution. <br>
Risk: Bursting requests can hit Trello rate limits. <br>
Mitigation: Throttle command execution according to the documented Trello limits. <br>


## Reference(s): <br>
- [Trello REST API documentation](https://developer.atlassian.com/cloud/trello/rest/) <br>
- [Trello API key and token setup](https://trello.com/app-key) <br>
- [ClawHub skill page](https://clawhub.ai/ChaunceyLiu/test1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq plus TRELLO_API_KEY and TRELLO_TOKEN; commands may read or mutate Trello data depending on endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
