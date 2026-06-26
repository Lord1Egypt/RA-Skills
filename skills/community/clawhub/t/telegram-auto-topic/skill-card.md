## Description: <br>
Add `/topic` to the start of any message in a Telegram forum group to auto-create a new topic from it, with a title generated automatically from the message content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itstauq](https://clawhub.ai/user/itstauq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Telegram group operators and bot maintainers use this skill to create new forum topics from `/topic` messages, quote or forward the original message into the new topic, and continue the conversation there. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create Telegram forum topics through a configured bot. <br>
Mitigation: Install it only for Telegram forum groups where members should be allowed to create topics through the bot. <br>
Risk: The Telegram bot token and Manage Topics permission grant topic-management capability. <br>
Mitigation: Keep the bot token protected and grant Manage Topics only in intended groups. <br>
Risk: Disabling mention-required behavior can make topic creation easier to trigger in a group. <br>
Mitigation: Leave mention-required behavior enabled unless the group is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/itstauq/telegram-auto-topic) <br>
- [Publisher profile](https://clawhub.ai/user/itstauq) <br>
- [GitHub project link from skill documentation](https://github.com/itstauq/telegram-auto-topic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command invocation and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Script returns topic_id, title, and link for the created Telegram forum topic.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
