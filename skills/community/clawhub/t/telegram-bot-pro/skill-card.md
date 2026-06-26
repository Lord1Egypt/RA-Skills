## Description: <br>
Create and manage Telegram bots for notifications, automation, customer support, group management, and interactive commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to scaffold and run Telegram bots for notifications, automation, customer support, group administration, and interactive command flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bot script can install an unpinned python-telegram-bot package at runtime. <br>
Mitigation: Review the script before use and install a pinned dependency yourself in a virtual environment. <br>
Risk: Custom handler files are loaded as local Python code and can process bot updates. <br>
Mitigation: Only pass handler files that you wrote or fully trust, and keep the Telegram bot token private. <br>
Risk: Bots with broad group-admin permissions can affect group members or settings if commands are wrong. <br>
Mitigation: Test commands with limited permissions before granting group-admin access. <br>


## Reference(s): <br>
- [Telegram Bot Examples](references/examples.md) <br>
- [Telegram Bot API](https://core.telegram.org/bots/api) <br>
- [python-telegram-bot](https://python-telegram-bot.org) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a user-supplied Telegram bot token and optional local Python handler file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
