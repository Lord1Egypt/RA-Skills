## Description: <br>
Send files quickly via Telegram using the tsend CLI tool with optional captions, profiles, and simple token/chat ID configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shingwha](https://clawhub.ai/user/Shingwha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to install and run a Telegram file-sending CLI, configure bot credentials and chat IDs, and send one or more local files or short text messages to a configured Telegram chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected files are uploaded from the local device to the configured Telegram chat. <br>
Mitigation: Use --dry-run before broad globs or sensitive folders, and send only files intended to leave the device. <br>
Risk: Bot credentials may be saved in ~/.tsend/config.json. <br>
Mitigation: Treat the token as a secret, restrict access to the config file, or use environment variables when saved credentials are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Shingwha/tsend) <br>
- [Telegram Bot API endpoint used by the skill](https://api.telegram.org/bot{token}) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI can send files or text through Telegram and prints status, dry-run previews, and error messages.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
