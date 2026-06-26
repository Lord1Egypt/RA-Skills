## Description: <br>
Provides Python scripts for an agent to send email through AgentMail and download unread inbox messages as local JSON files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lausser](https://clawhub.ai/user/lausser) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure an AgentMail inbox, check for unread messages, save them as JSON, and send or reply to email from Python scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts require access to an AgentMail inbox through an API key. <br>
Mitigation: Use a dedicated or revocable API key and keep the .env file out of shared folders and source control. <br>
Risk: Downloaded email contents are stored locally as MAIL.* JSON files. <br>
Mitigation: Delete MAIL.* files when they are no longer needed and avoid storing sensitive mail in shared workspaces. <br>
Risk: Checking mail marks unread messages as read after saving them. <br>
Mitigation: Run the checker only when this state change is expected, and review saved files before deleting or processing them. <br>
Risk: The send script contains placeholder recipient and inbox values. <br>
Mitigation: Verify placeholders and message content before sending email. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/lausser/python-agentmail-send-receive) <br>
- [ClawHub skill page](https://clawhub.ai/lausser/python-agentmail-send-receive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python code examples and shell commands; runtime scripts write JSON mail files and console status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AgentMail API key and configured inbox identity before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
