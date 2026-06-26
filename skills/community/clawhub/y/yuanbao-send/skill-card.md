## Description: <br>
主动向元宝派（Yuanbao Pai）群聊和私聊发送消息和文件，独立于 OpenClaw 插件通道，通过 WebSocket 协议直接推送，适用于 cron 定时任务、跨 session 通知等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luhuiwang](https://clawhub.ai/user/luhuiwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let agents or scheduled jobs send Yuanbao Pai group or direct messages and upload files through a configured bot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents or scheduled jobs can send messages and upload files as the configured Yuanbao bot. <br>
Mitigation: Restrict who can invoke the skill, confirm recipients and file paths before execution, and avoid sending secrets or private files. <br>
Risk: The skill depends on local Yuanbao credentials stored in ~/.openclaw/openclaw.json. <br>
Mitigation: Protect the configuration file and limit filesystem access for users or processes that can run the skill. <br>
Risk: Using the direct WebSocket connection can disrupt the normal OpenClaw Yuanbao plugin connection. <br>
Mitigation: Run the skill only when proactive messaging is intentional and avoid using it while the normal Yuanbao plugin must remain online. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luhuiwang/yuanbao-send) <br>
- [Publisher profile](https://clawhub.ai/user/luhuiwang) <br>
- [Release provenance](unavailable: No server-resolved GitHub import provenance is stored for this version.) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, websocket-client, cos-python-sdk-v5, and Yuanbao app credentials in ~/.openclaw/openclaw.json.] <br>

## Skill Version(s): <br>
2.1.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
