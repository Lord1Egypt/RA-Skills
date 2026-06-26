## Description: <br>
A slow-channel inbox for leaving an operator important messages when something notable, abnormal, or decision-requiring happens but is not urgent enough to interrupt, and for checking, marking read, or archiving those messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dvdegenz](https://clawhub.ai/user/dvdegenz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agent operators use this skill to keep a persistent local inbox for notable, abnormal, or decision-requiring events that should be reviewed later rather than interrupting the operator immediately. The agent can add, list, render, mark read, and archive inbox messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inbox messages are stored persistently on local disk and may include sensitive operational context if users or agents place secrets in messages. <br>
Mitigation: Avoid storing secrets in inbox entries and set OPENCLAW_WORKSPACE when storage should be confined to a specific workspace. <br>
Risk: Rendering all messages or running bulk actions can expose or change more inbox state than intended. <br>
Mitigation: Require clear user intent before rendering all messages or running read-all and archive-read. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dvdegenz/snailmail) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [CLI output as text, Markdown, HTML, or JSON depending on command and render mode.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a local inbox/messages.json file under OPENCLAW_WORKSPACE or the user's home directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
