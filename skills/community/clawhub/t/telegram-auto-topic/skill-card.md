## Description:

Adds /topic handling for Telegram forum groups so an agent can create a new forum topic from a message and generate a concise title from the message content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itstauq](https://clawhub.ai/user/itstauq)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an OpenClaw Telegram bot turn /topic messages in forum-enabled groups into dedicated discussion topics, quote the original message, and continue the conversation in the new thread.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Telegram bot token is powerful and may be exposed locally during execution.

Mitigation: Use a dedicated bot token, grant access only to required groups and topic-management permissions, protect the OpenClaw config file, avoid multi-user or heavily monitored hosts, and fix curl token handling before broad deployment.

Risk: The skill can create topics only in Telegram groups that have forums enabled and where the bot has Manage Topics permission.

Mitigation: Confirm the target group is forum-enabled and verify the bot's administrator permissions before enabling the /topic workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itstauq/skills/telegram-auto-topic)
- [Publisher profile](https://clawhub.ai/user/itstauq)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with a shell script invocation and JSON script output containing topic_id, title, and link.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, an OpenClaw Telegram configuration file, and Telegram forum group permissions.]

## Skill Version(s):

0.1.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
