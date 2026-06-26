## Description: <br>
Controls Discord through Clawdbot so agents can send and manage messages, reactions, stickers, emojis, polls, threads, pins, searches, server information, and moderation actions in DMs or channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fresh3](https://clawhub.ai/user/fresh3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to let an agent interact with Discord bot workflows: posting updates, reacting to messages, managing polls, threads, pins, and searches, checking server context, uploading media, and performing gated role or moderation actions when enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent act through a Discord bot with broad message, search, upload, and server-state actions. <br>
Mitigation: Limit the bot to intended servers and channels, disable unneeded discord.actions.* groups, and require explicit approval before public posts, edits, deletions, pins, searches, file uploads, or member-affecting actions. <br>
Risk: Role and moderation actions can affect Discord members if enabled. <br>
Mitigation: Keep roles and moderation disabled unless required, and grant only the minimum bot permissions needed for the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fresh3/taizi-discord) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON action payloads, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples for Discord action payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Discord action groups can be disabled; role and moderation actions are disabled by default.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
