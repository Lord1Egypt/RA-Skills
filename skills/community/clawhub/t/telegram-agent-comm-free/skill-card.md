## Description: <br>
A lightweight Telegram messaging specification for a single agent to send basic notifications and task updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, independent creators, and personal automation users use this skill to guide an agent in sending Telegram text notifications, task status updates, and concise work summaries through a configured Telegram channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens and target IDs can expose or misdirect notifications if stored or entered carelessly. <br>
Mitigation: Store the bot token securely, keep the Telegram target ID fixed and verified, and avoid embedding credentials in shared logs or prompts. <br>
Risk: Outbound Telegram messages may disclose secrets, private logs, or sensitive work details to an external chat service. <br>
Mitigation: Send only concise status information and review message content before allowing the agent to transmit notifications. <br>
Risk: The free version is text-only and does not provide audit logging, batch scheduling, media delivery, or multi-account routing. <br>
Mitigation: Use it for single-recipient text notifications and keep a separate local log when delivery history is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/telegram-agent-comm-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline JSON, JavaScript, shell, and text examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for text-only Telegram notifications; media sending, multi-account routing, batch scheduling, and audit logging are out of scope for the free version.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
