## Description: <br>
Create interactive Telegram messages with inline buttons through the OpenClaw CLI for selections, confirmation dialogs, workflow menus, quick actions, callback handling, and message editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NetanelRotem](https://clawhub.ai/user/NetanelRotem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to create Telegram inline-button interactions, including selection menus, confirmations, quick actions, callback acknowledgement, and message edits after a button is selected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Telegram bot token can authorize message sending and editing in chats where the bot is present. <br>
Mitigation: Keep the token out of git, prefer environment variables or secure OpenClaw configuration, rotate exposed tokens, and restrict the bot to chats you control. <br>
Risk: Helper scripts send or edit Telegram messages using the target chat ID and message content supplied by the user. <br>
Mitigation: Review scripts before running them and double-check chat IDs, message text, and example placeholders before using the skill in a live workspace. <br>


## Reference(s): <br>
- [Telegram Interactive Buttons Reference](references/REFERENCE.md) <br>
- [Setup Guide](SETUP.md) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [Telegram Bot API](https://core.telegram.org/bots/api) <br>
- [BotFather](https://t.me/BotFather) <br>
- [ClawHub Skill Page](https://clawhub.ai/NetanelRotem/telegram-interactive-buttons) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands, JSON snippets, and helper script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw, bash, and a Telegram bot token; python3 is optional for button JSON validation.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
