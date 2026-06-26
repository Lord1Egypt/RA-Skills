## Description: <br>
Xiayu helps users bind a local Xiayu account, build a dating or social profile, monitor matched conversations, and handle automated replies through the Xiayu service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiwenbing](https://clawhub.ai/user/jiwenbing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Xiayu users use this skill to set up and operate an AI social screening agent, including account binding, profile collection, match polling, and reply handling. It is intended for users who trust the local Xiayu service with account access and dating or profile details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for account access and dating or profile details. <br>
Mitigation: Install only if the user trusts the Xiayu local service, and review what information is shared before binding an account or completing a profile. <br>
Risk: The skill can keep polling and sending messages for the user. <br>
Mitigation: Confirm how to stop polling, review or disable automated replies, and pause or unpublish the agent when unattended operation is not desired. <br>
Risk: The skill stores a local session file with an access token. <br>
Mitigation: Delete the local session file and revoke or refresh the stored access token when access should end. <br>


## Reference(s): <br>
- [Xiayu ClawHub release](https://clawhub.ai/jiwenbing/xiayu) <br>
- [Xiayu local API base](http://127.0.0.1:3000/api/v1) <br>
- [Xiayu local notifications](http://127.0.0.1:3000/notifications) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, API calls, Files, Guidance] <br>
**Output Format:** [Markdown conversation text with JSON request bodies, HTTP API calls, and a local session JSON file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May poll for pending messages every 60 seconds and may store a local session file containing account and access-token details.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
