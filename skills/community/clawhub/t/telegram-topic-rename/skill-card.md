## Description:

Renames Telegram forum topics and optionally changes their icons through the Telegram Bot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwjjhh1995](https://clawhub.ai/user/wwjjhh1995)

### License/Terms of Use:


## Use Case:

External users and Telegram group administrators use this skill to rename forum topics and choose matching topic icons from a documented icon set.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Telegram bot with admin rights can rename forum topics in groups where it is authorized.

Mitigation: Use a least-privilege bot token and grant only the Telegram permissions needed for the intended group.

Risk: Incorrect chat, thread, topic name, or icon parameters can change the wrong Telegram forum topic.

Mitigation: Confirm the chat ID, thread ID, new name, and icon before running the script.

Risk: The bot token can be exposed to local process observers or command-line logging while the curl command runs.

Mitigation: Run the skill only in trusted local environments and avoid recording shell commands or process arguments that include credentials.

## Reference(s):

- [Telegram Topic Icons Reference](references/icons.md)
- [ClawHub skill page](https://clawhub.ai/wwjjhh1995/skills/telegram-topic-rename)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Telegram bot token and Telegram chat/thread identifiers before executing topic changes.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
