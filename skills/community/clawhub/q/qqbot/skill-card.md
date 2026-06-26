## Description: <br>
Configures and runs a QQ Official Bot with WebSocket messaging, OpenClaw AI handoff, daemon management, and troubleshooting guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byzgpc](https://clawhub.ai/user/byzgpc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to set up a QQ Official Bot, connect it to QQ messaging events, and route incoming chat messages through an OpenClaw workspace workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes a real-looking QQ credential in config.example.json. <br>
Mitigation: Replace and rotate any QQ credentials before use, and treat the example credential as exposed if it is real. <br>
Risk: Chat content and replies are written through files under ~/.openclaw/workspace. <br>
Mitigation: Use restrictive permissions on the OpenClaw workspace and avoid sensitive chats until log and queue retention are understood. <br>
Risk: The package includes ClawHub publishing helper scripts unrelated to running the bot. <br>
Mitigation: Remove or ignore the publishing scripts when installing only the QQ bot runtime. <br>


## Reference(s): <br>
- [QQ Bot Platform Documentation](https://bot.q.qq.com/wiki) <br>
- [QQ Bot API Documentation](https://bot.q.qq.com/wiki/develop/api/) <br>
- [QQ Bot Gateway Intents](https://bot.q.qq.com/wiki/develop/api/gateway/intents.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/byzgpc/qqbot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python, shell, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes daemon commands, QQ credential configuration, queue-file handoff behavior, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, _meta.json, package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
