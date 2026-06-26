## Description: <br>
Agent Mail helps an agent send, receive, manage, and thread email through the AgentMail API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fhbillwer](https://clawhub.ai/user/fhbillwer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to manage email workflows through AgentMail, including sending messages, checking inboxes, handling attachments, and organizing message threads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured AgentMail account and API access may expose inbox contents or allow messages to be sent from the account. <br>
Mitigation: Verify ownership of fhbillwer@agentmail.to, confirm API key permissions, and require review before sending messages or making mailbox changes. <br>
Risk: Email contents and attachments may include confidential data and may be stored locally. <br>
Mitigation: Review retention and deletion procedures for /workspace/data/emails/ before using the skill with sensitive mail. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fhbillwer/ws-agent-mail) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown or plain text responses with email workflow instructions and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in mailbox actions, attachment handling, and local email data stored under /workspace/data/emails/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
