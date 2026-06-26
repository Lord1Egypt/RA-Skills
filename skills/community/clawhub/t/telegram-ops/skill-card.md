## Description: <br>
Telegram Bot API operations for forum management. Use for creating/editing/archiving forum topics, setting topic icons, managing Telegram groups via Bot API. Use when archiving channels/topics. Requires bot token from OpenClaw config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create, configure, archive, and clean up Telegram forum topics that are integrated with OpenClaw sessions and configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to manage Telegram forum topics and modify persistent OpenClaw Telegram configuration. <br>
Mitigation: Use a minimally privileged bot token and review every config.patch payload before applying it. <br>
Risk: New topic configuration can leave all skills available by default. <br>
Mitigation: Add an explicit skills allowlist for each topic when broad tool access is not required. <br>
Risk: Bot tokens can be exposed through logs, shell history, or chat transcripts. <br>
Mitigation: Keep tokens out of transcripts and logs, and pass credentials through a controlled configuration source. <br>


## Reference(s): <br>
- [Forum Topic Emoji IDs](references/emoji-ids.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Telegram Bot API and OpenClaw configuration instructions; commands may call external Telegram endpoints when executed by a user or agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
