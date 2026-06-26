## Description: <br>
Helps an agent post text, photos, videos, and image albums to configured Telegram groups through OpenClaw CLI or Telegram API commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larthe](https://clawhub.ai/user/larthe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks to publish a Telegram group post or lesson report, including optional media, to known Telegram group IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a reusable Telegram bot credential. <br>
Mitigation: Rotate the bot token, remove credentials from the skill, and store secrets in a dedicated secret mechanism before use. <br>
Risk: The documented bot setup has broad group access and can post to configured target groups. <br>
Mitigation: Limit bot permissions, enable Privacy Mode unless full-message access is required, and confirm the target group, message, and media before posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/larthe/telegram-post) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Telegram chat IDs, message text, media file paths, and API calls for media albums.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
