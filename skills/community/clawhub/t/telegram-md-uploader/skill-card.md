## Description: <br>
Uploads and sends Markdown files from an OpenClaw workspace to a specific Telegram chat using the Telegram Bot API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[courtneejay](https://clawhub.ai/user/courtneejay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content authors use this skill to send selected Markdown workspace files to a Telegram recipient or group. It is suited to intentional file sharing after the user has configured a Telegram bot token and chat ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected Markdown files may contain secrets, private drafts, or other sensitive workspace content that will be shared externally through Telegram. <br>
Mitigation: Review each file before upload, confirm the intended chat ID, and send only content meant for the recipient. <br>
Risk: Telegram bot tokens and chat IDs are sensitive configuration values. <br>
Mitigation: Use a dedicated bot token, keep credentials in private environment variables, and avoid committing or sharing them. <br>


## Reference(s): <br>
- [Telegram BotFather](https://t.me/BotFather) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill sends user-selected .md files to Telegram when the uploader script is run with the required environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
