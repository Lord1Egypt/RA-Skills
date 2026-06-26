## Description: <br>
Use when you need to control Slack from OpenClaw via the message tool, including reacting to messages or pinning/unpinning items in Slack channels or DMs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ailven](https://clawhub.ai/user/ailven) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Slack through OpenClaw message actions, including sending, reading, editing, deleting, reacting to, pinning, and unpinning messages. It is intended for Slack channels and DMs configured through the required Slack channel integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send, edit, delete, pin, unpin, download files, and retrieve Slack member profile details through a configured bot token. <br>
Mitigation: Install it only with Slack bot scopes and channel access limited to the workspace areas and actions actually needed. <br>
Risk: Slack write and profile-reading actions can affect other users or expose sensitive information if executed without review. <br>
Mitigation: Require explicit approval before sending, editing, deleting, pinning, unpinning, downloading files, or retrieving member profile details. <br>
Risk: Open-ended channel monitoring may collect more Slack activity than intended. <br>
Mitigation: Avoid broad or continuous channel reads unless monitoring is an intended and approved use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ailven/slack-socket) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and message action examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured Slack channel access through channels.slack.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; package.json states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
