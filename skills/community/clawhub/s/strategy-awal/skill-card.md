## Description: <br>
OpenClaw MVP v8.1 - Email Classification & Google Workspace Execution for Awalcom. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[strategy-awal](https://clawhub.ai/user/strategy-awal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operators use this skill to monitor the strategy@awalcom.net mailbox, classify regional strategy emails, send Telegram summaries for approval, and create approved Google Docs, Sheets, or Slides assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive mailbox data and can create or share Google Workspace assets. <br>
Mitigation: Use only approved mailboxes and Google Workspace resources, restrict OAuth scopes and sharing destinations, and keep created assets private until reviewed. <br>
Risk: Automation could execute document creation, modification, or sharing from incomplete or sensitive email context. <br>
Mitigation: Require explicit human confirmation before any document creation, modification, or sharing action. <br>
Risk: Telegram summaries may expose sensitive email metadata or content. <br>
Mitigation: Use a private controlled Telegram channel and limit summaries to information needed for approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/strategy-awal/strategy-awal) <br>
- [README](README.md) <br>
- [Approval Workflow](docs/approval-workflow.md) <br>
- [Telegram Commands](docs/telegram-commands.md) <br>
- [Troubleshooting](docs/troubleshooting.md) <br>
- [Email Classification Keywords](context/email-classification-keywords.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Files, Guidance] <br>
**Output Format:** [Markdown instructions, Telegram response text, Google Workspace documents, and configuration JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authenticated gog CLI access, Google Workspace OAuth scopes, and a Telegram integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
