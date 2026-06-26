## Description: <br>
Resolve Telegram media placeholders into local files for vision, document, video, audio, or other follow-up analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurinzo](https://clawhub.ai/user/kurinzo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill when an agent sees a Telegram media placeholder and needs to retrieve the referenced file for analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Telegram bot token for chats where the bot is present. <br>
Mitigation: Use a limited-purpose bot, treat the token as a secret, and avoid pasting or logging it. <br>
Risk: The skill can forward private Telegram messages to another chat to retrieve media metadata. <br>
Mitigation: Set --forward-to only to a private chat you control and avoid sensitive group media. <br>
Risk: Downloaded or forwarded media copies may remain after use. <br>
Mitigation: Delete downloaded files after analysis and confirm forwarded-message cleanup succeeded. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kurinzo/tg-media-resolve) <br>
- [Publisher profile](https://clawhub.ai/user/kurinzo) <br>
- [Telegram Bot API endpoint](https://api.telegram.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns downloaded Telegram media files in a local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
