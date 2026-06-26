## Description: <br>
Telethon Master helps an agent operate a Telegram user account through a Telethon bridge for messaging, chat history, media transfer, channel actions, statistics, and ElevenLabs voice notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[producedbysavant](https://clawhub.ai/user/producedbysavant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they intentionally want an agent to read from and act through a real Telegram user account, including messages, files, reactions, channel management, and voice-note generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private Telegram messages and downloaded media. <br>
Mitigation: Require explicit user confirmation for reads and downloads, and avoid enabling it for private chats unless necessary. <br>
Risk: The skill can perform write and destructive Telegram actions such as sends, edits, deletes, forwards, joins, button clicks, and channel changes. <br>
Mitigation: Configure TG_ALLOWED_CHAT_IDS before use and require confirmation before write, join, click, forward, delete, and channel-management actions. <br>
Risk: The skill depends on sensitive local services, sessions, credentials, and a network tunnel. <br>
Mitigation: Verify that the local bridge, session, VPS tunnel, and .env credentials are owned by the operator and are properly secured before installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/producedbysavant/telethon-master) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tool-call examples, configuration snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to perform Telegram reads, writes, media downloads, channel changes, and local bridge maintenance through configured MCP tools.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
