## Description: <br>
Store and retrieve website credentials as domain, username, password, and notes entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raunaksingwi](https://clawhub.ai/user/raunaksingwi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create, list, retrieve, update, delete, and generate website login credentials through the Ravi password manager. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plaintext passwords may appear in command output, shell history, logs, screenshots, or chat transcripts. <br>
Mitigation: Retrieve credentials only when needed, avoid pasting real passwords into command lines or shared contexts, and prefer generated passwords when creating entries. <br>
Risk: The skill stores and retrieves website credentials through Ravi, so misuse or misplaced trust could expose sensitive account access. <br>
Mitigation: Install and use the skill only when the user trusts Ravi with website credentials, and do not use it for API keys or other non-website secrets. <br>


## Reference(s): <br>
- [Passwords API Reference](https://ravi.id/docs/schema/passwords.json) <br>
- [ClawHub release page](https://clawhub.ai/raunaksingwi/ravi-passwords) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command outputs can include plaintext website credentials during normal use.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
