## Description: <br>
Complete guide to connecting OpenClaw with Telegram, including bot setup, channel configuration, groups and topics, voice messages, inline buttons, media, and common troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mosoonpi-ai](https://clawhub.ai/user/mosoonpi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up or troubleshoot an OpenClaw Telegram bot, including BotFather setup, OpenClaw channel configuration, group and topic routing, voice-message transcription, media handling, and production readiness checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens or allowed chat IDs may be mishandled during setup. <br>
Mitigation: Review configuration before use, keep bot tokens out of source control and chats, and restrict access with allowedChatIds and rejectUnknown. <br>
Risk: Incorrect Telegram group privacy, routing, or OpenClaw gateway settings can expose the bot to unintended users or prevent expected responses. <br>
Mitigation: Follow the production checklist, review commands before execution, and verify gateway status and logs in a trusted maintenance context. <br>
Risk: Voice transcription setup installs and runs third-party Python dependencies. <br>
Mitigation: Install dependencies in an isolated environment and review package choices before enabling voice transcription. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mosoonpi-ai/telegram-agent-setup) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell, JSON, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps, configuration examples, troubleshooting checks, and a production checklist.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
