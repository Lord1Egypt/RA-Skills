## Description: <br>
Send photos via Telegram Bot API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suileyan](https://clawhub.ai/user/suileyan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users can use this skill to send local image files or screenshots to a configured Telegram chat through the Telegram Bot API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is preconfigured with a fixed Telegram bot token and chat ID. <br>
Mitigation: Rotate or remove the exposed bot token and replace the chat ID with a securely managed destination before use. <br>
Risk: The skill can automatically send the latest screenshot from a local folder. <br>
Mitigation: Require explicit user confirmation of the exact image path and destination chat before uploading any file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suileyan/telegram-send-photo) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python code examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Telegram Bot API requests that upload local image files with an optional caption.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
