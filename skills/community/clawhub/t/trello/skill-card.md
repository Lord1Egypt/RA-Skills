## Description: <br>
Manage Trello boards, lists, and cards via the Trello REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to list Trello boards, inspect lists and cards, and prepare curl commands that create, move, comment on, or archive cards through the Trello REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands run with a Trello token can read and change Trello cards. <br>
Mitigation: Use the skill only where Trello API access is acceptable, and review board, list, and card IDs before running POST or PUT commands. <br>
Risk: The Trello API key and token provide account access if exposed. <br>
Mitigation: Keep credentials in environment variables, avoid sharing them in logs or prompts, and revoke the token when it is no longer needed. <br>


## Reference(s): <br>
- [Trello REST API documentation](https://developer.atlassian.com/cloud/trello/rest/) <br>
- [Trello API key and token setup](https://trello.com/app-key) <br>
- [ClawHub Trello skill page](https://clawhub.ai/steipete/trello) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/steipete) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq plus TRELLO_API_KEY and TRELLO_TOKEN environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
