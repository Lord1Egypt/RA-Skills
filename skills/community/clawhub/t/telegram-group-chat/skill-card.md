## Description: <br>
Manages Telegram group chat replies by responding to mentions, questions, name calls, technical topics, or priority users while preventing spam and bot loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zboxman](https://clawhub.ai/user/zboxman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Telegram group bots so they reply only when useful and stay silent for small talk, bot messages, emoji-only posts, repeated topics, or other low-value messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad reply triggers could cause unwanted Telegram group replies if the skill is applied outside the intended bot or group. <br>
Mitigation: Install it only for the intended Telegram bot and group, set the bot name and priority users carefully, and monitor early behavior. <br>
Risk: Silent NO_REPLY handling could suppress responses if the surrounding bot integration applies the policy too broadly. <br>
Mitigation: Test mention, question, bot-message, emoji-only, and cooldown scenarios before relying on the configuration. <br>


## Reference(s): <br>
- [Telegram Group Chat on ClawHub](https://clawhub.ai/zboxman/telegram-group-chat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with reply rules, configuration snippets, examples, and testing checklist items.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code; includes NO_REPLY guidance for silent handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
