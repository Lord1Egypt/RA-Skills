## Description: <br>
Manage Trello boards, lists, and cards via the Trello REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjcloud](https://clawhub.ai/user/hjcloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent prepare Trello REST API commands for listing boards, lists, and cards and for creating, moving, commenting on, or archiving cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Trello API credentials that can access the user's Trello account. <br>
Mitigation: Install only when the agent should use those credentials, keep the token secret, and revoke or rotate it if exposed. <br>
Risk: Create, move, comment, and archive commands can make live changes to Trello cards. <br>
Mitigation: Review commands before execution and verify board, list, and card IDs before running write operations. <br>
Risk: Trello API calls are subject to documented rate limits. <br>
Mitigation: Throttle repeated commands and retry later when Trello rate limits are reached. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hjcloud/testjeff) <br>
- [Trello REST API documentation](https://developer.atlassian.com/cloud/trello/rest/) <br>
- [Trello API key setup](https://trello.com/app-key) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq plus TRELLO_API_KEY and TRELLO_TOKEN environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
